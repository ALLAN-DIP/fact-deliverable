"""Python script to restore elasticsearch index from snapshot"""

from time import time
import argparse

from baseline_models.message_advisor_code.constants import SNAPSHOT_NAME, DEFAULT_HOST
from baseline_models.message_advisor_code.elastic.simple_client import SimpleClient
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


def main():
    # Keyword argument handling
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-e", "--elastic_host", type=str, default=DEFAULT_HOST)
    argparser.add_argument("-s", "--snapshot", type=str, default=SNAPSHOT_NAME)

    args = argparser.parse_args()
    host = args.elastic_host
    snapshot = args.snapshot

    es = SimpleClient(host, request_timeout = 3000)
    es.restore_snapshot(snapshot)

if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")