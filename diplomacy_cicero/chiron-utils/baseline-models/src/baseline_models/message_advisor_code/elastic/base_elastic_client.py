"""Abstract base class for elastic search client to store and search messages sent in diplomacy games as vector database."""

import re
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from elasticsearch import Elasticsearch
from baseline_models.model_code.constants import POWERS
from baseline_models.message_advisor_code.constants import REPOSITORY_NAME
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


@dataclass
class BaseElasticClient(ABC):
    """Abstract base class for elastic search client to store and search messages sent in diplomacy games as vector database."""
    vector_element_type: str
    debug: bool = False


    def __init__(self, host: str, username: str, password: str, cert_path: str, **kwargs):
        if username:
            self.client = Elasticsearch(
                host,
                ca_certs = cert_path,
                http_auth = (username, password),
                **kwargs)
        else:
            self.client = Elasticsearch(
                host,
                **kwargs)


    def create_index(self, index):
        """
        Create index.
        """
        self.client.indices.delete(index=index, ignore_unavailable=True)
        self.client.indices.create(index=index, mappings={
            "properties": {
                "raw_game_state": {
                    "type": "dense_vector",
                    "element_type": self.vector_element_type,
                },
                "embedding": {
                    "type": "dense_vector",
                    "element_type": self.vector_element_type,
                },
                "messages": {
                    "type": "text",
                },
                "tags": {
                    "type": "keyword",
                }
            }
        })


    def populate_index(self, index, data_path, batch_size=500):
        """
        Populate index.
        """
        with open(data_path, "r") as src:
            batch = []
            
            for i, line in enumerate(src):
                batch.append(line.strip())

                if len(batch) == batch_size:
                    game_state_list, attribute_list, message_list = self.preprocess_data(batch)
                    self.insert(index, game_state_list, attribute_list, message_list)
                    batch = []
            
            if batch:
                game_state_list, attribute_list, message_list = self.preprocess_data(batch)
                self.insert(index, game_state_list, attribute_list, message_list)
    
    
    def insert(self, index, game_state_list, attribute_list, message_list):
        for game_state, atrb, msg in zip(game_state_list, attribute_list, message_list):
            if not msg:
                # Skip pairs with no messages
                continue

            tags = set()
            for message in msg:
                tags.add(message["sender"] + "-" + message["recipient"])

            self.client.index(index = index, document = {
                "raw_game_state": game_state.astype(int),
                "embedding": atrb.astype(float),
                "messages": json.dumps(msg),
                "tags": list(tags),
            })


    def get_docs(self, index: str, state: dict, num_candidates: int, k: int):
        """
        Retrieve k nearest documents from index.
        """
        attribute = self.get_embedding(state)

        results = self.client.search(
            index = index,
            knn = {
                "field": "embedding",
                "query_vector": attribute,
                "num_candidates": num_candidates,
                "k": k,
            },
            size = k
        )

        docs = results["hits"]["hits"]
        return docs


    def get_docs_by_tag(self, index: str, state: dict, num_candidates: int, k: int, tag: str):
        """
        Retrieve k nearest documents from index, filtered by tag
        """
        attribute = self.get_embedding(state)

        filters = []
        filters.append({
            "term": {
                "tags": {
                    "value": tag
                }
            },
        })
        
        results = self.client.search(
            index = index,
            knn = {
                "field": "embedding",
                "query_vector": attribute,
                "num_candidates": num_candidates,
                "k": k,
                "filter": filters,
            },
            size = k,
        )

        docs = results["hits"]["hits"]
        return docs


    def get_messages_from_sender(self, index: str, state: dict, sender: str, num_candidates: int = 50, k: int = 10):
        """
        Retrieves message recommendations for a power to send to other powers given game state.
        """
        result = dict()
        for power in POWERS:
            if power == sender:
                continue
            docs = self.get_docs_by_tag(index, state, num_candidates, k, sender + "-" + power)
            for doc in docs:
                messages = json.loads(doc["_source"]["messages"])
                for message in messages:
                    if message["sender"] == sender and message["recipient"] == power:
                            
                        if not validate_message(message["message"]):
                            # skip invalid messages
                            continue

                        cleaned_message = clean_message(message["message"])
                        if self.debug:
                            cleaned_message = cleaned_message + f" [{doc['_score']:.{3}f}]"

                        if message["recipient"] not in result.keys():
                            result[message["recipient"]] = list()
                        result[message["recipient"]].append(cleaned_message)

        return result
    
    
    def register_repository(self):
        """
        Register elasticsearch repository
        """
        snapshot_body = {
            "type": "fs",
            "settings": {
                    "location": "/mount/backups/fs"
                }
        }
        self.client.snapshot.create_repository(name=REPOSITORY_NAME, body=snapshot_body)
    

    def create_snapshot(self, name: str):
        """
        Create snapshot of elasticsearch index
        """
        self.register_repository()
        self.client.snapshot.create(repository=REPOSITORY_NAME, snapshot=name)
    

    def restore_snapshot(self, name: str):
        """
        Restore elasticsearch index from snapshot
        """
        self.register_repository()
        self.client.snapshot.restore(repository=REPOSITORY_NAME, snapshot=name, wait_for_completion=True, master_timeout=-1)
        logger.info("Restoring elastic data from snapshot")
    

    @abstractmethod
    def preprocess_data(self, batch, **kwargs):
        """Generate embedding-message pairs from dataset.

        Returns:
            list of embeddings and list of messages
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_embedding(self, state, **kwargs):
        """Generate embedding from game state.

        Returns:
            embedding
        """
        raise NotImplementedError


def validate_message(msg_txt: str) -> bool:
    # filter short messages
    if len(msg_txt) <= 10:
        return False
    
    # filter long messages
    if len(msg_txt) >= 1000:
        return False
    
    # filter user ids
    if re.search(r"\[\d+\]", msg_txt):
        return False
    return True


def clean_message(msg_txt: str) -> str:
    # remove corrupt newlines
    msg_txt = uncorrupt_newlines(msg_txt)
    # remove trailing carriage return
    if msg_txt.endswith('\r'):
        return msg_txt[:-1]

    return msg_txt


def uncorrupt_newlines(msg_txt: str) -> str:
    """
    Replace corrupted newlines (~N~) with newline characters.
    """
    corrupted_newline_cnt = msg_txt.count("~N~")
    if corrupted_newline_cnt > 0:
        for i in reversed(range(1, corrupted_newline_cnt + 1)):
            # replace `i` corrupted newlines in a row
            corrupted_newlines = " " + " ".join(["~N~" for _ in range(i)]) + " "
            fixed_newlines = '\n' * i
            msg_txt = msg_txt.replace(corrupted_newlines, fixed_newlines)

    return msg_txt