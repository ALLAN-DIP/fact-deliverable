# States taken directly from dipnet dataset
# See render_examples.py to see how you can use your own examples

EXAMPLE_RENDERS = [
    {
        "state": {"timestamp":1542990097232324,"zobrist_hash":"5744784867136166527","note":"","name":"F1907R","units":{"AUSTRIA":["A GAL"],"ENGLAND":["A HOL","A LVN","F BAL","F NTH","F KIE","A YOR","A STP","A WAR","A PRU","A SWE"],"FRANCE":["A RUH","A BEL","A BER","F MAO","F MAR","A BUD","A BOH","A MUN","F SPA/SC"],"GERMANY":[],"ITALY":["F GRE","F TUN","A TRI","A VEN","F ION","F AEG"],"RUSSIA":[],"TURKEY":["F BLA","A SEV","A ARM","A RUM","A SER","A MOS","A BUL","*A WAR"]},"centers":{"AUSTRIA":["BUD"],"ENGLAND":["EDI","LON","LVP","NWY","HOL","STP","DEN","MOS","SWE","KIE"],"FRANCE":["BRE","MAR","PAR","BEL","POR","SPA","MUN","BER","VIE"],"GERMANY":[],"ITALY":["NAP","ROM","VEN","TUN","TRI","GRE"],"RUSSIA":[],"TURKEY":["ANK","CON","SMY","BUL","RUM","SEV","SER","WAR"]},"homes":{"AUSTRIA":["BUD","TRI","VIE"],"ENGLAND":["EDI","LON","LVP"],"FRANCE":["BRE","MAR","PAR"],"GERMANY":["BER","KIE","MUN"],"ITALY":["NAP","ROM","VEN"],"RUSSIA":["MOS","SEV","STP","WAR"],"TURKEY":["ANK","CON","SMY"]},"influence":{"AUSTRIA":["ALB","GAL"],"ENGLAND":["LON","LVP","EDI","HOL","NAO","NWG","LVN","WAL","BAL","NTH","KIE","DEN","YOR","NWY","STP","WAR","PRU","SWE"],"FRANCE":["BRE","PAR","POR","MAR","GAS","LYO","RUH","BEL","PIC","BER","MAO","BUR","VIE","NAF","BUD","WES","BOH","MUN","SPA"],"GERMANY":[],"ITALY":["NAP","ROM","TYR","GRE","TYS","TUN","TRI","VEN","ION","AEG"],"RUSSIA":["FIN","SIL"],"TURKEY":["CON","SMY","BLA","ANK","SEV","UKR","ARM","RUM","SER","MOS","BUL"]},"civil_disorder":{"AUSTRIA":0,"ENGLAND":0,"FRANCE":0,"GERMANY":0,"ITALY":0,"RUSSIA":0,"TURKEY":0},"builds":{"AUSTRIA":{"count":0,"homes":[]},"ENGLAND":{"count":0,"homes":[]},"FRANCE":{"count":0,"homes":[]},"GERMANY":{"count":0,"homes":[]},"ITALY":{"count":0,"homes":[]},"RUSSIA":{"count":0,"homes":[]},"TURKEY":{"count":0,"homes":[]}},"game_id":"n4_TKUAjyrh_qqw-","map":"standard","rules":["NO_PRESS","POWER_CHOICE"],"retreats":{"AUSTRIA":{},"ENGLAND":{},"FRANCE":{},"GERMANY":{},"ITALY":{},"RUSSIA":{},"TURKEY":{"A WAR":["SIL","UKR"]}}}, # noqa
        "alterations": [
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
    },
    {
        "state": {"timestamp":1542990200864072,"zobrist_hash":"327483533751009024","note":"","name":"F1903M","units":{"AUSTRIA":["F VEN","A MUN","A STP","A KIE","A ARM","F ION","A SER","A TYR","F ALB"],"FRANCE":["A NAP","A SPA","F TYS","F NTH","A BUR","F LYO","F ENG","A HOL"]},"centers":{"AUSTRIA":["BUD","TRI","VIE","VEN","WAR","RUM","BER","MUN","MOS","SEV"],"FRANCE":["BRE","MAR","PAR","LON","BEL","EDI","KIE","NAP","SPA"]},"homes":{"AUSTRIA":["BUD","TRI","VIE"],"FRANCE":["BRE","MAR","PAR"]},"influence":{"AUSTRIA":["BUD","VIE","TRI","GAL","VEN","WAR","SIL","RUM","ADR","MOS","BER","SEV","MUN","APU","STP","KIE","ARM","ION","SER","TYR","ALB"],"FRANCE":["BRE","MAR","PAR","PIE","PIC","LON","TUS","BEL","YOR","ROM","GAS","EDI","NAP","SPA","TYS","NTH","BUR","LYO","ENG","HOL"]},"civil_disorder":{"AUSTRIA":0,"FRANCE":0},"builds":{"AUSTRIA":{"count":0,"homes":[]},"FRANCE":{"count":0,"homes":[]}},"game_id":"sLOt32gk2nRZpcZP","map":"standard_france_austria","rules":["NO_PRESS","POWER_CHOICE"],"retreats":{"AUSTRIA":{},"FRANCE":{}}}, # noqa
        "alterations": [
            [
                [],
                [],
                [],
                [],
                [("A VEN - TYR", 1), ("A VEN S A ROM", 0.75), ("A VEN S A ROM - TUS", 0.5), ("A VEN - TUS", 0.25)],
                [],
                []
            ]
        ]
    },
    {
        "state": {"timestamp":1542990228221287,"zobrist_hash":"4563916897585667058","note":"","name":"S1908R","units":{"AUSTRIA":["A BUD","A SER"],"ENGLAND":["A SWE","A WAR","F NWY","*A MOS"],"FRANCE":["A BUR","A EDI","F WES","F LYO","F NTH","A BEL","A MAR","F DEN","F HOL"],"GERMANY":["A MUN","A RUH","A KIE","*F DEN"],"ITALY":["A VIE","A TRI","A PIE","F ION","A GRE","F TUN","F TYS"],"RUSSIA":["F BLA","F BUL\/EC","A SEV","A MOS"],"TURKEY":["F CON","F AEG","A ANK"]},"centers":{"AUSTRIA":["BUD","SER"],"ENGLAND":["NWY","STP","SWE","MOS"],"FRANCE":["BRE","MAR","PAR","SPA","POR","BEL","LON","LVP","EDI"],"GERMANY":["KIE","MUN","BER","DEN","HOL"],"ITALY":["NAP","ROM","VEN","TUN","GRE","VIE","TRI"],"RUSSIA":["SEV","WAR","RUM","BUL"],"TURKEY":["ANK","CON","SMY"]},"homes":{"AUSTRIA":["BUD","TRI","VIE"],"ENGLAND":["EDI","LON","LVP"],"FRANCE":["BRE","MAR","PAR"],"GERMANY":["BER","KIE","MUN"],"ITALY":["NAP","ROM","VEN"],"RUSSIA":["MOS","SEV","STP","WAR"],"TURKEY":["ANK","CON","SMY"]},"influence":{"AUSTRIA":["BUD","GAL","SER"],"ENGLAND":["BAR","FIN","LVN","STP","NWG","SWE","WAR","NWY"],"FRANCE":["BRE","PAR","BUR","POR","SPA","GAS","MAO","WAL","LON","LVP","YOR","PIC","EDI","ENG","WES","SKA","LYO","NTH","BEL","HEL","MAR","DEN","HOL"],"GERMANY":["MUN","BER","BAL","RUH","KIE"],"ITALY":["NAP","ROM","TYR","VEN","APU","ADR","VIE","ALB","TRI","PIE","ION","GRE","TUN","TYS"],"RUSSIA":["UKR","BOT","BLA","PRU","RUM","BUL","ARM","SIL","SEV","MOS"],"TURKEY":["SMY","CON","AEG","ANK"]},"civil_disorder":{"AUSTRIA":0,"ENGLAND":0,"FRANCE":0,"GERMANY":0,"ITALY":0,"RUSSIA":0,"TURKEY":0},"builds":{"AUSTRIA":{"count":0,"homes":[]},"ENGLAND":{"count":0,"homes":[]},"FRANCE":{"count":0,"homes":[]},"GERMANY":{"count":0,"homes":[]},"ITALY":{"count":0,"homes":[]},"RUSSIA":{"count":0,"homes":[]},"TURKEY":{"count":0,"homes":[]}},"game_id":"BoCmD_4wE7c6WTNd","map":"standard","rules":["NO_PRESS","POWER_CHOICE"],"retreats":{"AUSTRIA":{},"ENGLAND":{"A MOS":["LVN","STP","UKR"]},"FRANCE":{},"GERMANY":{"F DEN":["BAL","HEL"]},"ITALY":{},"RUSSIA":{},"TURKEY":{}}}, # noqa
        "alterations": [
            [
                [("A BUD H", 1), ("A BUD S A SER", 0.75), ("A BUD - VIE", 0.5)],
                [],
                [],
                [],
                [],
                [],
                []
            ],
            [
                [],
                [],
                [],
                [],
                [],
                [("F NOR C A SWE - STP", 1), ("F NOR H", 0.75), ("F NOR S A SWE", 0.5)],
                []
            ]
        ]
    }
]
