from baseline_models.visualisation_code.custom_renderer import CustomRenderer
from baseline_models.visualisation_code.dict_to_state import dict_to_state
from baseline_models.visualisation_code.examples import EXAMPLE_RENDERS
from baseline_models.utils.utils import return_logger

import os
from argparse import ArgumentParser

logger = return_logger(__name__)

PARENT_DIR = os.path.dirname(os.getcwd())
OUT_PATH = os.path.join(PARENT_DIR, "output")
# DATA_PATH = os.path.join(os.getcwd(), "visualisation_code", "examples.jsonl")


def render_maps(data_dict=EXAMPLE_RENDERS, output_path=OUT_PATH):
    """
    Renders example states with alterations as .xml maps

    Args:
        data_dict (dict): The dictionary of states and alterations (see examples.py for dictionary format)
        output_path (str): The absolute file path for the output folder
    """

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # Iterate over each state provided
    for i, render_info in enumerate(data_dict):
        try:
            state = render_info["state"]
            alterations = render_info["alterations"]
        except KeyError:
            logger.info(f"Entry of index {i} is missing the state or alterations item and will not be rendered")
            continue

        game, phase = dict_to_state(state)
        renderer = CustomRenderer(game, phase=phase)

        # Render each set of alterations separately to allow many renderings for one state
        for j, alt in enumerate(alterations):
            renderer.custom_render(output_path=os.path.join(output_path, f"out_{i}.{j}.svg"), alterations=alt)

    logger.info("Rendering complete")


def main():
    parser = ArgumentParser()
    parser.add_argument("-o", "--output_path", type=str, default=OUT_PATH)
    args = parser.parse_args()

    render_maps(output_path=args.output_path)


if __name__ == "__main__":
    main()
