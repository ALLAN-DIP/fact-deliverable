from time import time
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import os
import pickle
import numpy as np
from baseline_models.model_code.preprocess import generate_attribute_list
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


def run_ae(train_path, test_path, model_path):
    X_train = list()

    logger.info("Preprocessing training data")

    with open(train_path, 'r') as train:
        X_train = generate_attribute_list(train, True)

    logger.info(f"Train data length: {len(X_train)}")

    logger.info("Training model")
    autoencoder = MLPRegressor(alpha=1e-15, 
                           hidden_layer_sizes=(2057, 1024, 512, 256, 512, 1024, 2057), 
                           random_state=1, max_iter=10, verbose=True)
    autoencoder.fit(X_train, X_train)

    #evaluate
    with open(test_path, 'r') as test:
        X_test = generate_attribute_list(test)

    pred = autoencoder.predict(X_test)
    loss = mean_squared_error(X_test, pred)
    logger.info(f"Loss: {loss}")

    if model_path is not None:
        with open(os.path.join(model_path, "ae"), 'wb') as model_file:
            pickle.dump(autoencoder, model_file)


def encoder(encoder_weights, encoder_biases, data):
    res_ae = data
    for index, (w, b) in enumerate(zip(encoder_weights, encoder_biases)):
        if index+1 == len(encoder_weights):
            res_ae = res_ae@w+b 
        else:
            res_ae = np.maximum(0, res_ae@w+b)
    return res_ae


def get_encoding(model_path, state):
    if os.path.exists(model_path):
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
            weights = model.coefs_
            biases = model.intercepts_
            encoder_weights = weights[0:4]
            encoder_biases = biases[0:4]
            return encoder(encoder_weights, encoder_biases, state)
        

def batch_get_encoding(model_path, state, batchsize):
    encoding = list()
    logger.info(f"Batch size: {len(state)}")
    for i in range(0, len(state), batchsize):
        batch = state[i:i+batchsize]
        batch_encoding = get_encoding(model_path, batch)
        encoding.extend(batch_encoding)
        logger.info(f"Batch done length: {len(encoding)}")
    return encoding
        


def main():
    data_path = os.path.join("D:", os.sep, "Downloads", "dipnet-data-diplomacy-v1-27k-msgs", "test")
    train_path = os.path.join(data_path, "train.jsonl")
    test_path = os.path.join(data_path, "test.jsonl")
    model_path = os.path.join(data_path, "ae_models")

    run_ae(train_path, test_path, model_path)


if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")
