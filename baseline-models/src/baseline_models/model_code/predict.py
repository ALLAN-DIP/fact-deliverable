import os
import pickle
from time import time
import json
import numpy as np
import argparse

from baseline_models.model_code.preprocess import generate_key
from baseline_models.model_code.preprocess import generate_attribute
from baseline_models.model_code.preprocess import get_season_phase
from baseline_models.model_code.preprocess import get_units, get_retreats
from baseline_models.model_code.constants import CLASSNOORDER

from baseline_models.visualisation_code.custom_renderer import render_from_prediction
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)


RENDER_RESULT = True

def predict(model_path: str, state: dict, power: str = None) -> list:
    """
    Returns the model's predicted orders from the current state

    Args:
        model_path (str): The absolute file path to the model
        state (dict): The dictionary encoding of the current game state
        power (str): (Optional) Specify power to predict orders for
    Returns:
        (list): List of orders predicted by the model
    """

    orders = list()
    pred_orders = predict_probabilities(model_path, state, power)
    season_phase = get_season_phase(state["name"])

    if season_phase == "WA":
        builds = state["builds"]
        for builds_power, builds_data in builds.items():
            if power != None and builds_power != power:
                continue
            pred_order_list = list()
            if builds_data["count"] > 0:
                homes = builds_data["homes"]
                for home, order_probs in dict((k, pred_orders[k]) for k in homes).items():
                    best_order_prob = max(order_probs, key=lambda x: x[1])
                    if best_order_prob[0] != CLASSNOORDER:
                        pred_order_list.append(best_order_prob)

                sorted_orders = sorted(pred_order_list, key=lambda x: x[1], reverse=True)
                for i in range(builds_data["count"]):
                    if i < len(sorted_orders):
                        orders.append(sorted_orders[i][0])

            elif builds_data["count"] < 0:
                units = get_units(state, builds_power)
                for unit, order_probs in dict((k, pred_orders[k]) for k in units).items():
                    for order_prob in order_probs:
                        if order_prob[0] != CLASSNOORDER:
                            pred_order_list.append(order_prob)

                sorted_orders = sorted(pred_order_list, key=lambda x: x[1], reverse=True)
                for i in range(builds_data["count"]*-1):
                    if i < len(sorted_orders):
                        orders.append(sorted_orders[i][0])
    else:
            for unit, order_probs in pred_orders.items():
                orders.append(max(order_probs, key=lambda x: x[1])[0])
    
    return orders

def predict_probabilities(model_path: str, state: dict, power: str = None) -> dict:
    """
    Returns the model's predicted probabilities for all possible orders from the current state

    Args:
        model_path (str): The absolute file path to the model
        state (dict): The dictionary encoding of the current game state
        power (str): (Optional) Specify power to predict orders for
    Returns:
        (dict): A dictionary mapping units or centers to a list of tuples for possible orders
        and their corresponding probabilities
    """

    # Encode state as model input
    pred_orders = dict()
    attribute = generate_attribute(state)
    season_phase = get_season_phase(state["name"])

    if season_phase[-1] == 'R':
        units = get_retreats(state, power)
        pred_orders = predict_order(units, season_phase, model_path, attribute)

    elif season_phase == 'WA':
        builds = state["builds"]
        for builds_power, builds_data in builds.items():
            if power != None and builds_power != power:
                continue
            if builds_data["count"] > 0:
                homes = builds_data["homes"]
                pred_orders.update(predict_order(homes, season_phase, model_path, attribute))

            elif builds_data["count"] < 0:
                units = get_units(state, builds_power)
                pred_orders.update(predict_order(units, season_phase, model_path, attribute))

    else:
        units = get_units(state, power)
        pred_orders = predict_order(units, season_phase, model_path, attribute)

    return pred_orders

def predict_order(units, season_phase, model_path, attribute):
    pred_orders = dict()
    for unit in units:
        # Don't consider non-displaced units in a retreat phase
        # if season_phase[-1] == 'R' and unit[0] != '*':
        #     continue

        # Current model implementation combines retreats and regular orders into one model
        # unit = unit.replace("*", "")
        key = generate_key(unit, season_phase)
        file_path = os.path.join(model_path, key)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as model_file:
                model = pickle.load(model_file)
                attribute = np.reshape(attribute, (1, -1))
                pred_proba = model.predict_proba(attribute)

                pred_order_proba = []
                for order, prob in zip(model.classes_, pred_proba[0]):
                    pred_order_proba.append((order, prob))

                pred_orders[unit] = pred_order_proba
        else:
            # Currently does not assign order for a unit if corresponding model doesn't exist
            logger.info(f"Model not found | key: {key}")
    return pred_orders


def render_outputs(model_path: str, test_path: str, output_path: str, max_games=-1, max_phases=-1, max_units=-1, max_orders=100) -> None:
    """
    Creates a catalogue of .svg images for a series of games

    Args:
        model_path (str): The absolute path to the model folder
        test_path (str): The absolute path to the jsonl file containing the game states to render
        output_path (str): The absolute path to the output folder for the renderings
        max_games (int): The maximum number of games to render (-1 is until the end of the file)
        max_phases (int): The maximum number of phases to render for any game (-1 is until the end of the game)
        max_units (int): The maximum number of units to render orders for any game (-1 is all units)
        max_orders (int): The maximum number of orders to render on the map (-1 is until the end of the game)
    """

    with open(test_path, 'r') as test:

        # Each line in the test file is a json for a game
        for i, line in enumerate(test):
            game = json.loads(line)
            logger.info(f"Currently game id: {i}")

            # Iterate through each phase
            for j, phase in enumerate(game["phases"]):
                state = phase["state"]
                name = state["name"]

                if name == "COMPLETED":
                    continue
                logger.info(f"Current state: {name}")

                # Predict orders from the current state
                pred_probs = predict_probabilities(model_path, state)
                sorted_probs = dict()

                # Taking the top number of orders for each army
                for k, (unit, orders) in enumerate(pred_probs.items()):
                    sorted_probs[unit] = sorted(orders, key=lambda x: x[1], reverse=True)[:min(max_orders, len(orders))]

                    # Linearly scaling the probabilities
                    scalar = sorted_probs[unit][0][1]
                    if scalar > 0:
                        for m in range(len(sorted_probs[unit])):
                            sorted_probs[unit][m] = (sorted_probs[unit][m][0], sorted_probs[unit][m][1] / scalar)

                    # Rendering the order suggestions and saving as a file.
                    file_name = f"output_{i}_{state['name']}_{unit.replace('/', '_')}.svg".replace(" ", "_")
                    render_from_prediction(state, sorted_probs, os.path.join(output_path, file_name))
                    sorted_probs.clear()

                    if k == max_units - 1:
                        break

                if j == max_phases - 1:
                    break

            if i == max_games - 1:
                break


def main():
    parent_dir = os.path.dirname(os.getcwd())

    # Keyword argument handling
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-t", "--test_path", type=str, default=os.path.join(parent_dir, "data", "test.jsonl"))
    argparser.add_argument("-m", "--model_path", type=str, default=os.path.join(parent_dir, "models", "example"))
    argparser.add_argument("-o", "--output_path", type=str, default=os.path.join(parent_dir, "output"))
    argparser.add_argument("-g", "--max_games", type=int, default=-1)
    argparser.add_argument("-p", "--max_phases", type=int, default=-1)
    argparser.add_argument("-u", "--max_units", type=int, default=-1)
    argparser.add_argument("-s", "--max_suggestions", type=int, default=6)

    args = argparser.parse_args()
    test_path = args.test_path
    model_path = args.model_path
    output_path = args.output_path
    max_games = args.max_games
    max_phases = args.max_phases
    max_units = args.max_units
    max_orders = args.max_suggestions

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    """
    Deprecated with argparse addition, but still useful as a reference

    data_path = os.path.join("D:", os.sep, "Downloads", "dipnet-data-diplomacy-v1-27k-msgs", "medium")
    test_path = os.path.join(data_path, "test.jsonl")
    model_path = os.path.join(data_path, "knn_models")
    model_path = os.path.join("D:", os.sep, "Downloads", "lr_24102024", "lr_24102024")
    output_path = os.path.join(os.getcwd(), "output")
    """

    # Performing the rendering
    render_outputs(
        model_path,
        test_path,
        output_path,
        max_games=max_games,
        max_phases=max_phases,
        max_units=max_units,
        max_orders=max_orders
    )


if __name__ == "__main__":
    start_time = time()
    main()
    logger.info(f"Total runtime: {(time() - start_time):.2f} seconds")
