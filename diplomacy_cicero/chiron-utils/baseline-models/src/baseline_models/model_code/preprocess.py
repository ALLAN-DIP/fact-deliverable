import numpy as np
from baseline_models.model_code.constants import *
import json
import re
from typing import TextIO
from baseline_models.utils.utils import return_logger

logger = return_logger(__name__)



def get_power_of_unit(state: dict, unit: str) ->  str:
    """
    Gets the power of the unit

    Args:
        state (dict): Dictionary storing state information
        unit (str): string of the unit

    Returns:
        (str): the name of the power that the unit belongs to
        If not found, None is returned.
    """
    units = state["units"]
    for (power, unit_ls) in units.items():
        if unit in unit_ls:
            return power
        if f'*{unit}' in unit_ls:
            return power
    return None


def get_power_of_home(state: dict, home: str) -> str: 
    """
    Gets the power of a home province

    Args:
        state (dict): Dictionary storing state information
        home (str): string of the home (uppercase 3 letter code)

    Returns:
        (str): the name of the power that the home province belongs to 
        If not found, None is returned.
    """
    homes = state["homes"]
    for (power, homes_ls) in homes.items():
        if home in homes_ls:
            return power
    return None

def get_unit_from_order(order: str) -> str:
    order_terms = order.split(" ")
    return " ".join(order_terms[0:2])


def generate_key(unit: str, season_phase: str) -> str:
    """
    Converts the unit description and season phase to model filename

    Args:
        unit (str): String describing unit type and location
        season_phase (str): Season phase type (e.g. "FM", "SR", "WA")
    Returns:
        (str): Model key and filename
    """
    key = unit + " " + season_phase
    return re.sub(r"[\\/ \s]", "_", key)


def entry_to_vectors(phase: dict) -> tuple:
    """
    Encodes a phase into a one hot encoding comprising of three lists:

    Args:
        phase (dict): The dictionary describing the current state
    Returns:
        (tuple): A tuple containing:
            [0] attributes: list of np array of attributes/features
            [1] classes: list of orders
            [2] keys: list of model types
    """
    state = phase["state"]
    orders = phase["orders"]
    results = phase["results"]
    builds = state["builds"]
    units = state["units"]

    attributes = list()
    classes = list()
    keys = list()

    season_phase = get_season_phase(state["name"])
    attribute = generate_attribute(state)

    if season_phase == "WA":
        for power, build_dict in builds.items():
            if build_dict["count"] == 0:
                continue
            elif build_dict["count"] > 0:
                # build orders
                homes = build_dict["homes"]
                order_list = orders[power]
                for home in homes:
                    attributes.append(attribute)
                    if order_list is not None:
                        if "A " + home + " B" in order_list:
                            classes.append("A " + home + " B")
                        elif "F " + home + " B" in order_list:
                            classes.append("F " + home + " B")
                        elif "F " + home + "/NC B" in order_list:
                            classes.append("F " + home + "/NC B")
                        elif "F " + home + "/SC B" in order_list:
                            classes.append("F " + home + "/SC B")
                        else:
                            classes.append(CLASSNOORDER)
                    else:
                        classes.append(CLASSNOORDER)
                    key = generate_key(home, season_phase)
                    keys.append(key)
            else:
                # disband orders
                unit_list = units[power]
                order_list = orders[power]
                for unit in unit_list:
                    attributes.append(attribute)
                    if order_list is not None:
                        if unit + " D" in order_list:
                            classes.append(unit + " D")
                        else:
                            classes.append(CLASSNOORDER)
                    else:
                        classes.append(CLASSNOORDER)
                    key = generate_key(unit, season_phase)
                    keys.append(key)

    else:
        for _, order_list in orders.items():
            if order_list is not None:
                for order in order_list:
                    # parse unit from order
                    unit = get_unit_from_order(order)
                    if unit in results:
                        # skip illegal moves
                        if "void" in results[unit]:
                            continue
                    key = generate_key(unit, season_phase)

                    attributes.append(attribute)
                    classes.append(order)
                    keys.append(key)

    return attributes, classes, keys


def generate_attribute(state: dict, name_data=None, units_data=None, centers_data=None, homes_data=None, influences_data=None) -> np.ndarray:
    """
    Encodes the power, centers, homes and influence components of the states into a one-hot vector

    Args:
        state (dict): The current game state
    Returns:
        (np.ndarray): The one-hot vector encoding
    """

    # FIELDS = ["powers", "centers", "homes", "influence"]
    phases = {
        'SM': 0,
        'FM': 1,
        'WA': 2,
        'SR': 3,
        'FR': 4,
        'CD': 5
    }

    # If the entire phase is available in dipnet format, pass phase directly in.
    if state:
        name_data = state["name"]               # string of state name e.g. S1901M
        units_data = state["units"]             # dict of powers to their units e.g. "AUSTRIA": ["A SER","A TYR","F ADR"]
        centers_data = state["centers"]         # dict of powers to centers under their control e.g. "AUSTRIA": ["BUD","TRI","VIE", "SER"]
        homes_data = state["homes"]             # dict of powers to centers where they can build units
        influences_data = state["influence"]    # dict of powers to the territories under their influence (territories that are last occupied by them)
    n_powers = len(POWERS)

    # Setting encoding sizes for each field
    phase_atr = np.zeros([len(phases)], dtype=bool)
    units_atr = np.zeros([n_powers * 2 * len(INFLUENCES)], dtype=bool)
    centers_atr = np.zeros([n_powers * len(CENTERS)], dtype=bool)
    homes_atr = np.zeros([n_powers * len(HOMES)], dtype=bool)
    influences_atr = np.zeros([n_powers * len(TERRITORIES)], dtype=bool)

    if state:
        season_phase = get_season_phase(name_data)
    else:
        season_phase = get_season_phase(name_data, False)
    phase_atr[phases[season_phase]] = True

    for j, power in enumerate(POWERS):
        # Encoding units
        if power in units_data:
            if not units_data[power] is None:
                for i, region in enumerate(INFLUENCES):
                    if f"A {region}" in units_data[power] or f"*A {region}" in units_data[power]:
                        units_atr[2 * i * n_powers + (j*2)] = 1
                    elif f"F {region}" in units_data[power] or f"*F {region}" in units_data[power]:
                        units_atr[2 * i * n_powers + (j*2) + 1] = 1
        # Encoding centers
        if power in centers_data:
            if not centers_data[power] is None:
                for i, center in enumerate(CENTERS):
                    if center in centers_data[power]:
                        centers_atr[i * n_powers + j] = power
        # Encoding homes
        if power in homes_data:
            if not homes_data[power] is None:
                for i, home in enumerate(HOMES):
                    if home in homes_data[power]:
                        homes_atr[i * n_powers + j] = power
        # Encoding influences
        if power in influences_data:
            if not influences_data[power] is None:
                for i, inf in enumerate(TERRITORIES):
                    if inf in influences_data[power]:
                        influences_atr[i * n_powers + j] = power

    # Combining encodings into one vector
    attribute = np.concatenate((phase_atr, units_atr, centers_atr, homes_atr, influences_atr))

    return attribute


def get_scaled_masked_attribute(attribute, masked_powers:list=None, mask_phase=False, mask_unit=False, mask_center=False, mask_home=False, mask_influence=False, scaled_powers:dict = None, scale_phase=1, scale_unit=1, scale_center=1, scale_home=1, scale_influence=1):

    if not scaled_powers:
        scaled_powers = {
            'AUSTRIA': 1, 
            'ENGLAND': 1, 
            'FRANCE': 1, 
            'GERMANY': 1, 
            'ITALY': 1, 
            'RUSSIA': 1, 
            'TURKEY': 1
        }

    phase_len = 6
    masked_attribute = []
    n_powers = len(POWERS)

    phase_atr = np.zeros([phase_len], dtype=bool)
    units_atr = np.zeros([n_powers * 2 * len(INFLUENCES)], dtype=bool)
    centers_atr = np.zeros([n_powers * len(CENTERS)], dtype=bool)
    homes_atr = np.zeros([n_powers * len(HOMES)], dtype=bool)
    influences_atr = np.zeros([n_powers * len(TERRITORIES)], dtype=bool)

    k = 0
    phase_atr = attribute[k:phase_len]
    k += phase_len
    units_atr = attribute[k:k + (n_powers * 2 * len(INFLUENCES))]
    k += n_powers * 2 * len(INFLUENCES)
    centers_atr = attribute[k:k + (n_powers * len(CENTERS))]
    k += n_powers * len(CENTERS)
    homes_atr = attribute[k:k + (n_powers * len(HOMES))]
    k += n_powers * len(HOMES)
    influences_atr = attribute[k:k + (n_powers * len(TERRITORIES))]

    if not mask_phase:
        for val in phase_atr:
            masked_attribute.append(val*scale_phase)


    for j, power in enumerate(POWERS):
        if masked_powers and power in masked_powers:
            continue

        if not mask_unit:
            for i, region in enumerate(INFLUENCES):
                unit_index = 2 * i * n_powers + (2*j)
                masked_attribute.append(units_atr[unit_index]*scale_unit*scaled_powers[power])
                masked_attribute.append(units_atr[unit_index+1]*scale_unit*scaled_powers[power])

        # Encoding centers
        if not mask_center:
            for i, center in enumerate(CENTERS):
                masked_attribute.append(centers_atr[i * n_powers + j]*scale_center*scaled_powers[power])

        # Encoding homes
        if not mask_home:
            for i, home in enumerate(HOMES):
                masked_attribute.append(homes_atr[i * n_powers + j]*scale_home*scaled_powers[power])
        
        # Encoding influences
        if not mask_influence:
            for i, inf in enumerate(TERRITORIES):
                masked_attribute.append(influences_atr[i * n_powers + j]*scale_influence*scaled_powers[power])
    
    return np.array(masked_attribute)


def get_season_phase(name_data: str, abbr=True) -> str:
    """
    Gets the current season phase type (for example "FM" is fall movement)
    """
    
    if abbr:
        return name_data[0] + name_data[-1]
    split = name_data.split()
    return split[0][0] + split[2][0]


def get_units(state: dict, power: str = None) -> list:
    """
    Gets the list of active units from the current state
    """
    units = []
    units_data = state["units"]

    if power != None:
        if power in units_data:
            return units_data[power]
        else:
            logger.info(f"Power not found: {power}")
            return units

    for _, unit_list in units_data.items():
        if unit_list is not None:
            for unit in unit_list:
                units.append(unit)
    return units


def get_retreats(state: dict, power: str = None) -> list:
    """
    Gets the list of retreating units from the current state
    """
    units = []
    retreats_data = state["retreats"]

    if power != None:
        if power in retreats_data:
            for unit in retreats_data[power].keys():
                units.append(unit)
            return units
        else:
            logger.info(f"Power not found: {power}")
            return units

    for _, unit_dict in retreats_data.items():
        if unit_dict is not None:
            for unit in unit_dict.keys():
                units.append(unit)
    return units


def generate_x_y(groups: dict, src: TextIO) -> None:
    """
    Generates (state, order) pairs from a file input stream
    """
    for line in src:
        game = json.loads(line)
        for phase in game["phases"]:
            vectors = entry_to_vectors(phase)

            for attribute, order, key in zip(vectors[0], vectors[1], vectors[2]):
                if key not in groups.keys():
                    groups[key] = (list(), list())
                groups[key][0].append(attribute)
                groups[key][1].append(order)


def generate_attribute_message_pair(src):
    attribute_list = list()
    message_list = list()
    for line in src:
        game = json.loads(line)
        for phase in game["phases"]:
            state = phase["state"]
            attribute = generate_attribute(state)
            messages = phase["messages"]
            attribute_list.append(attribute)
            message_list.append(messages)
    return attribute_list, message_list


def generate_attribute_list(src: TextIO, no_dup: bool = False):
    result = list()
    result_set = set()
    
    for line in src:
        game = json.loads(line)
        for phase in game["phases"]:
            state = phase["state"]
            attribute = generate_attribute(state)
            if no_dup:
                atrb_string = attribute.tostring()
                if atrb_string not in result_set:
                    result_set.add(atrb_string)
                    result.append(attribute)
            else:
                result.append(attribute)
    
    return result
