import json
import os
from argparse import ArgumentParser

from baseline_models.visualisation_code.dict_to_state import dict_to_state
from baseline_models.visualisation_code.custom_renderer import CustomRenderer

def render_state(state, output_path, game_id='unspecified'):
    if not state:
        raise Exception("state is not found")
    
    name = state.get("name")
    if name == "COMPLETED": 
        return
    print(f"Current state: {name}")

    game, phase = dict_to_state(state)
    renderer = CustomRenderer(game, phase=phase)
    renderer.custom_render(output_path=os.path.join(output_path, f"output_{game_id}_{name}.svg"))

def generate_games_from(data_dir, output_path, max_generated: int = -1):
    data_path = os.path.join(data_dir, "dipnet-data-diplomacy-v1-27k-msgs", "standard_no_press.jsonl")
    with open(data_path, "r") as data:
        for i, line in enumerate(data):
            if i == max_generated:
                break
            game = json.loads(line)
            print(f"Currently game id: {i}")
            for phase in game["phases"]:
                state = phase["state"]
                render_state(state, output_path, game_id=i)

def main():
    parent_dir = os.path.dirname(os.getcwd())

    parser = ArgumentParser()
    parser.add_argument("-d", "--data_dir", type=str, default=os.path.join(parent_dir, "data"))
    parser.add_argument("-o", "--output_path", type=str, default=os.path.join(parent_dir, "output"))
    parser.add_argument("-n", "--max_games", type=int, default=-1)
    args = parser.parse_args()

    data_dir = args.data_dir
    output_path = args.output_path
    max_generated = args.max_games
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    generate_games_from(data_dir=data_dir, output_path=args.output_path, max_generated=max_generated)


if __name__ == "__main__":
    main()
