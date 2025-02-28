from sklearn.linear_model import LogisticRegression
from time import time
import os
import pickle
from baseline_models.model_code.preprocess import generate_x_y
from baseline_models.model_code.evaluation import evaluate_model
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


def run_lr(train_path, test_path, model_path):
    train_dict = dict()

    logger.info("Preprocessing training data")
    with open(train_path, 'r') as train:
        generate_x_y(train_dict, train)

    logger.info("Training models")
    for unit, data in train_dict.items():

        # skip if there is only 1 class
        if len(set(data[1])) <= 1:
            continue

        model = LogisticRegression(random_state=1, solver='lbfgs', C=0.01)
        model.fit(data[0], data[1])
        
        if model_path is not None:
            with open(os.path.join(model_path, unit), 'wb') as model_file:
                pickle.dump(model, model_file)

    logger.info("Preprocessing testing data")
    test_dict = dict()
    with open(test_path, 'r') as test:
        generate_x_y(test_dict, test)

    logger.info("Evaluating model")
    results = evaluate_model(test_dict, model_path)
    logger.info(results)


def main():
    data_path = os.path.join("D:", os.sep, "Downloads", "dipnet-data-diplomacy-v1-27k-msgs", "test")
    train_path = os.path.join(data_path, "train.jsonl")
    test_path = os.path.join(data_path, "test.jsonl")
    model_path = os.path.join(data_path, "lr_models")

    run_lr(train_path, test_path, model_path)


if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")
