# Overview
The repository is modularised into three main components:
- model_code: Contains the base model code such as KNN and LR for training models
- visualisation_code: Contains code for visualising suggestions
- web_code: Contains starter code for a interactive web implementation (development has been paused)
- message_advisor_code: Contains client code for Elastic Search vector database for querying message advice given game state

## Setup
Perform the following setup to run the code.
- All setup steps should be completed from the topmost directory
- Using a venv is recommended

Install packages in requirements.txt to build the model with the correct version:
- pip install -r requirements.txt

To make code imports cleaner across multiple directories, packages were used in conjunction with setuptools. To create the package:
- pip install -e .

# Usage
## model_code/predict.py
Renders predictions from the model on a test set
Keyword arguments:
- -t:   The path to the jsonl files containing the test states of the model
- -m:   The path to the model folder containing the model binaries
- -o:   The path to the output folder for the rendered suggestions overlayed on the map
- -g:   The max number of games to render from the test file (-1 for full file)
- -p:   The max number of phases to render for any game (-1 for full game)
- -u:   The max number of units to render suggestions for any phase (-1 for all units)
- -s:   The max number of order suggestions to render for any unit (-1 for all suggestions)

## visualisation_code/render_examples.py
Renders example suggestions on states defined in "examples.py"
Keyword arguments:
- -o:   The path to the output folder for the rendered suggestions overlayed on the map

## `message_advisor_code/restore_snapshot.py`

Restore Elasticsearch index from snapshot for querying message advice

Keyword arguments:

- `-e`/`--elastic_host`: The URL of the Elasticsearch database API
- `-s`/`--snapshot`: The name of the snapshot being used

The script requires a running Elasticsearch instance. To start a local Elasticsearch single-node cluster using Docker, run the following commands:

```bash
cd src/baseline_models/message_advisor_code
docker compose up
```

This will spin-up an Elasticsearch instance accessible at <http://localhost:9200>.

To restore the Elasticsearch index:

- Download the snapshot from GitHub at <https://github.com/ALLAN-DIP/large-file-storage/tree/main/elasticsearch_dump>:

    ```bash
    wget https://github.com/ALLAN-DIP/large-file-storage/raw/refs/heads/main/elasticsearch_dump/fs{1..3}.zip
    ```

- Extract the contents of `fs.zip`:

    ```bash
    unzip fs1.zip
    unzip fs2.zip
    unzip fs3.zip
    ```

- Put the resulting `fs` folder into the `src/baseline_models/message_advisor_code/.snapshots` folder, creating the folder if it does not exist:

    ```bash
    mkdir -p .snapshots
    mv fs/ .snapshots/
    ```

- Run the script:

    ```bash
    python restore_snapshot.py
    ```

This will prompt Elasticsearch to restore data from the snapshot in the background, which will take several minutes.
