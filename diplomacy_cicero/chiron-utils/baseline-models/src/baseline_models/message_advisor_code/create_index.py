"""Python script to generate and populate message index from dataset"""

from time import time
import argparse
import os

from baseline_models.message_advisor_code.constants import DEFAULT_HOST, DEFAULT_INDEX
from baseline_models.message_advisor_code.elastic.autoencoder_client import AutoencoderClient
from baseline_models.message_advisor_code.elastic.simple_client import SimpleClient
from baseline_models.message_advisor_code.elastic.masked_client import MaskedClient
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


def main():
    parent_dir = os.path.dirname(os.getcwd())

    # Keyword argument handling
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-d", "--data_path", type=str, default=os.path.join(parent_dir, "data", "webdip_with_msgs.jsonl"))
    argparser.add_argument("-m", "--model_path", type=str, default=os.path.join(parent_dir, "models", "example"))
    argparser.add_argument("-u", "--elastic_username", type=str, default=None)
    argparser.add_argument("-p", "--elastic_password", type=str, default=None)
    argparser.add_argument("-e", "--elastic_host", type=str, default=DEFAULT_HOST)
    argparser.add_argument("-c", "--elastic_cert_path", type=str, default=None)
    argparser.add_argument("-i", "--index", type=str, default=DEFAULT_INDEX)
    argparser.add_argument("-t", "--client_type", type=str, default="simple")

    args = argparser.parse_args()
    data_path = args.data_path
    model_path = args.model_path
    username = args.elastic_username
    password = args.elastic_password
    host = args.elastic_host
    cert_path = args.elastic_cert_path
    index = args.index

    es = None
    if args.client_type == "simple":
        es = SimpleClient(host)
    elif args.client_type == "autoencoder":
        es = AutoencoderClient(host, model_path)
    elif args.client_type == "masked":
        es = MaskedClient(host)

    es.create_index(index)
    es.populate_index(index, data_path, 500)

if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")