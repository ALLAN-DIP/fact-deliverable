from diplomacy.engine.game import Game


def clean_input(input_list: list) -> list:
    """
    Removes backslashes from a list of strings
    """
    return list(map(lambda x: x.replace('\\', ''), input_list))

def converting(state_attr: str, state_dict: dict, game: Game):
    unannotated_powers = set([power.name for power in game.powers.values()])

    for power_name, power_attr in state_dict[state_attr].items():
        unannotated_powers.remove(power_name)
        power = game.powers.get(power_name)
        if power is None:
            print(f"Inaccurate power '{power_name}' found in state dict")
            return
        if state_attr == "retreats":
            setattr(power, state_attr, power_attr)
        else:
            setattr(power, state_attr, clean_input(power_attr)) 

    for power_name in unannotated_powers:
        power = game.powers.get(power_name)
        if state_attr == "retreats":
            setattr(power, state_attr, {})
        else:
            setattr(power, state_attr, [])
    return game

def dict_to_state(state_dict: dict) -> tuple[Game, dict]:
    """
    Loads a game state into a Game object from a dictionary
    """
    game = Game()

    for state_attr in ["units", "centers", "influence", "homes", "retreats"]:
        converting(state_attr, state_dict, game)
    
    phase = state_dict["name"]

    return game, phase
