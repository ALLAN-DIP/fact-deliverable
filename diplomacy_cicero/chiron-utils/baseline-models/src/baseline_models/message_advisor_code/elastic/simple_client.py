"""Elastic search client to store and search messages sent in diplomacy games as vector database."""

from abc import ABC
from dataclasses import dataclass
from baseline_models.message_advisor_code.elastic.base_elastic_client import BaseElasticClient
from baseline_models.model_code.preprocess import generate_attribute, generate_attribute_message_pair
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


@dataclass
class SimpleClient(BaseElasticClient, ABC):
    """Elasticsearch client using raw game attributes."""
    vector_element_type = "bit"


    def __init__(self, host: str, username: str = None, password: str = None, cert_path: str = None, **kwargs):
        super(SimpleClient, self).__init__(host, username, password, cert_path, **kwargs)

        
    def preprocess_data(self, batch):
        """Generate embedding-message pairs from dataset."""
        attribute_list = list()
        message_list = list()
        attribute_list, message_list = generate_attribute_message_pair(batch)
        assert len(attribute_list) == len(message_list)
        return attribute_list, attribute_list, message_list
    

    def get_embedding(self, state):
        """
        Preprocess attribute to doc embedding.
        """
        attribute = generate_attribute(state)
        attribute = attribute.astype(int)
        return attribute