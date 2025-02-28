from baseline_models.visualisation_code.custom_renderer import CustomRenderer
from diplomacy import Game
from baseline_models.visualisation_code.dict_to_state import dict_to_state

import os

DATA_PATH = os.path.join("D:", os.sep, "Downloads", "dipnet-data-diplomacy-v1-27k-msgs", "medium")
DIR_PATH = os.path.join(os.getcwd(), "visualisation_code")
OUT_PATH = os.path.join(DIR_PATH, "output")

test = {"timestamp":1542990097232324,"zobrist_hash":"5744784867136166527","note":"","name":"F1907R","units":{"AUSTRIA":["A GAL"],"ENGLAND":["A HOL","A LVN","F BAL","F NTH","F KIE","A YOR","A STP","A WAR","A PRU","A SWE"],"FRANCE":["A RUH","A BEL","A BER","F MAO","F MAR","A BUD","A BOH","A MUN","F SPA/SC"],"GERMANY":[],"ITALY":["F GRE","F TUN","A TRI","A VEN","F ION","F AEG"],"RUSSIA":[],"TURKEY":["F BLA","A SEV","A ARM","A RUM","A SER","A MOS","A BUL","*A WAR"]},"centers":{"AUSTRIA":["BUD"],"ENGLAND":["EDI","LON","LVP","NWY","HOL","STP","DEN","MOS","SWE","KIE"],"FRANCE":["BRE","MAR","PAR","BEL","POR","SPA","MUN","BER","VIE"],"GERMANY":[],"ITALY":["NAP","ROM","VEN","TUN","TRI","GRE"],"RUSSIA":[],"TURKEY":["ANK","CON","SMY","BUL","RUM","SEV","SER","WAR"]},"homes":{"AUSTRIA":["BUD","TRI","VIE"],"ENGLAND":["EDI","LON","LVP"],"FRANCE":["BRE","MAR","PAR"],"GERMANY":["BER","KIE","MUN"],"ITALY":["NAP","ROM","VEN"],"RUSSIA":["MOS","SEV","STP","WAR"],"TURKEY":["ANK","CON","SMY"]},"influence":{"AUSTRIA":["ALB","GAL"],"ENGLAND":["LON","LVP","EDI","HOL","NAO","NWG","LVN","WAL","BAL","NTH","KIE","DEN","YOR","NWY","STP","WAR","PRU","SWE"],"FRANCE":["BRE","PAR","POR","MAR","GAS","LYO","RUH","BEL","PIC","BER","MAO","BUR","VIE","NAF","BUD","WES","BOH","MUN","SPA"],"GERMANY":[],"ITALY":["NAP","ROM","TYR","GRE","TYS","TUN","TRI","VEN","ION","AEG"],"RUSSIA":["FIN","SIL"],"TURKEY":["CON","SMY","BLA","ANK","SEV","UKR","ARM","RUM","SER","MOS","BUL"]},"civil_disorder":{"AUSTRIA":0,"ENGLAND":0,"FRANCE":0,"GERMANY":0,"ITALY":0,"RUSSIA":0,"TURKEY":0},"builds":{"AUSTRIA":{"count":0,"homes":[]},"ENGLAND":{"count":0,"homes":[]},"FRANCE":{"count":0,"homes":[]},"GERMANY":{"count":0,"homes":[]},"ITALY":{"count":0,"homes":[]},"RUSSIA":{"count":0,"homes":[]},"TURKEY":{"count":0,"homes":[]}},"game_id":"n4_TKUAjyrh_qqw-","map":"standard","rules":["NO_PRESS","POWER_CHOICE"],"retreats":{"AUSTRIA":{},"ENGLAND":{},"FRANCE":{},"GERMANY":{},"ITALY":{},"RUSSIA":{},"TURKEY":{"A WAR":["SIL","UKR"]}}} # noqa


def test_alterations():
    game = Game("test")
    renderer = CustomRenderer(game)

    print("\n".join(p.name for p in game.powers.values()))
    alterations = [
        [
            [("A BER - SIL", 1)],           # Austria
            [("F EDI C A LVP - NOR", 1)],   # England
            [("A PAR H", 1)],               # France
            [],                             # Germany
            [],                             # Italy
            [("A STP S MOS", 1)],           # Russia
            [("A SMY S F ANK - ARM", 1)]    # Turkey
        ],
        [
            [],
            [("F LON - NTH", 1), ("F LON - ENG", 0.75), ("F LON - YOR", 0.5)],
            [],
            [],
            [],
            [],
            []
        ]
    ]

    for i, alt in enumerate(alterations):
        renderer.custom_render(output_path=os.path.join(OUT_PATH, f"out_{i}.svg"), alterations=alt)


def test_map_loading():
    game, phase = dict_to_state(test)
    renderer = CustomRenderer(game, phase=phase)

    alterations = [
        [
            [],
            [("F LON - NTH", 1), ("F LON - ENG", 0.75), ("F LON - YOR", 0.5)],
            [("A BEL H", 1), ("F SPA H", 0.75), ("F MAO H", 0.5)],
            [("A GAL S WAR", 1), ("A GAL S BOH", 0.75), ("A GAL S BUD", 0.5)],
            [("A TRI S F BUD - SER", 1), ("A TRI S F SER - BUD", 0.75), ("A TRI S F BUD - VIE", 0.5)],
            [],
            [("F BLA L C A RUM - ANK", 1), ("F BLA C A SEV - CON", 0.75), ("F BLA C A BUL - ANK", 0.5)]
        ],
        [
            [],
            [("A LIV - WAR", 1), ("A LIV S A PRU - WAR", 0.75), ("A LIV H", 0.5)],
            [],
            [],
            [],
            [],
            [],
        ]
    ]

    for i, alt in enumerate(alterations):
        renderer.custom_render(output_path=os.path.join(OUT_PATH, f"out_custom_{i}.svg"), alterations=alt)


def main():
    test_alterations()
    test_map_loading()


if __name__ == "__main__":
    main()
