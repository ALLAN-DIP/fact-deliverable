"""Restore Elasticsearch index from snapshot for querying message advice."""

from time import time
import argparse

from baseline_models.message_advisor_code.constants import SNAPSHOT_NAME, DEFAULT_HOST
from baseline_models.message_advisor_code.elastic.simple_client import SimpleClient
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


def main():
    # Keyword argument handling
    argparser = argparse.ArgumentParser(__doc__)
    argparser.add_argument("-e", "--elastic_host", type=str, default=DEFAULT_HOST, help="URL of the Elasticsearch database API")
    argparser.add_argument("-s", "--snapshot", type=str, default=SNAPSHOT_NAME, help="Name of the snapshot being used")

    args = argparser.parse_args()
    host = args.elastic_host
    snapshot = args.snapshot

    es = SimpleClient(host, request_timeout = 3000)
    es.restore_snapshot(snapshot)

if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")