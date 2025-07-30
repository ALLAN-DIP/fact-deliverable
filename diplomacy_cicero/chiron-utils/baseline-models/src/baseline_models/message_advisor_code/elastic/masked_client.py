"""Elastic search client to store and search messages sent in diplomacy games as vector database."""

from abc import ABC
from dataclasses import dataclass
from baseline_models.message_advisor_code.elastic.base_elastic_client import BaseElasticClient
from baseline_models.model_code.preprocess import generate_attribute, generate_attribute_message_pair, get_scaled_masked_attribute
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


@dataclass
class MaskedClient(BaseElasticClient, ABC):
    """Abstract base class for Elasticsearch client."""
    vector_element_type = "float"

    def __init__(self, host: str, username: str = None, password: str = None, cert_path: str = None):
        super(MaskedClient, self).__init__(host, username, password, cert_path)

        
    def preprocess_data(self, batch):
        """Generate embedding-message pairs from dataset."""
        masked_attribute_list = list()
        attribute_list = list()
        message_list = list()
        attribute_list, message_list = generate_attribute_message_pair(batch)

        for attribute in attribute_list:
            masked_attribute_list.append(get_scaled_masked_attribute(attribute, mask_phase=True, mask_home=True, mask_influence=True, scale_center=100))
        assert len(masked_attribute_list) == len(message_list)

        return attribute_list, masked_attribute_list, message_list
    

    def get_embedding(self, state):
        """
        Preprocess attribute to doc embedding.
        """
        attribute = generate_attribute(state)
        attribute = get_scaled_masked_attribute(attribute, mask_phase=True, mask_home=True, mask_influence=True, scale_center=100)

        return attribute.astype(int)