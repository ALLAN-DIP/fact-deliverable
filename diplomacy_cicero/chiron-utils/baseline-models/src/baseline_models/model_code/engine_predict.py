from baseline_models.model_code.predict import predict_order
from baseline_models.model_code.preprocess import generate_attribute, get_units, get_retreats, get_season_phase

class PHASES:
    MOVEMENT="M"
    BUILD="WA"
    RETREAT="R"

class BaselineAdvice:
    """
    Class for generating baseline model predictions to display move suggestions on game engine
    """
    def __init__(self, model_path: str, state: dict, province: str):
        """
        Class constructor

        Params:
            model_path (str) -- file path to model
            state (dict) -- dictionary storing current state information
            province (str) -- province selected
        """
        self.model_path = model_path
        self.state = state
        self.province = province
        self.power = None # power associated with province selected
        self.season_phase = None
        self.attribute = None
    
     # UTIL FUNCTIONS
    def set_season_phase(self):
        """
        Setter for season_phase using state dict
        """
        season_phase = get_season_phase(self.state["name"])
        if season_phase is not None:
            self.season_phase = season_phase
        return self.season_phase
    
    def set_attribute(self):
        """
        Setter for attribute using state dict
        """
        attr = generate_attribute(self.state)
        if attr is not None:
            self.attribute = attr
        return self.attribute
    
    def set_power(self, power):
        """
        Setter for associated power
        """
        if power != None:
            self.power = power
        return self.power
    

    def get_unit_from_province(self):
        """
        returns active unit and associated power in the provided province

        Returns:
            (tuple) -- tuple containing active unit and associated power. 
                        Else, returns None if active unit not found.
        """
        units = self.state["units"]
        for power, units_ls in units.items():
            if units_ls is None:
                continue

            for unit in units_ls:
                if unit.split(" ")[1] == self.province:
                    return (unit, power)
        
        return None
    
    def get_retreat_from_province(self):
        """
        returns retreating unit and associated power in the provided province

        Returns:
            (tuple) -- tuple containing retreating unit and associated power. 
                        Else, returns None if retreating unit not found in provided province. 
        """
        retreats = self.state["retreats"]
        for power, units_dict in retreats.items():
            if units_dict is None:
                continue
            for unit in units_dict.keys():
                if unit.split(" ")[1] == self.province:
                    return (unit, power)
        return None
    
    def get_home_power_of_province(self):
        """
        Returns the power that has this province as one of its homes
        
        Returns:
            (string)  -- string representing the home power 
        """
        homes = self.state["homes"]
        if self.province.find('/') != -1: # need to clean up naming if have multiple names
            self.province = self.province.split('/')[0]
        for power, home_ls in homes.items():
            if home_ls is None:
                continue
            for home in home_ls:
                if home == self.province:
                    return power
        return None

    @staticmethod
    def sort_preds(preds: dict, phase: PHASES, top_k: int):
        """
        Sort the predicted orders by their predicted probabilities in decreasing order

        Params:
            preds (dict) -- dictionary where each key is a unit, corresponding value is a 
            list of tuples of the form (possible_order, predicted_probabiltity)
            phase (PHASES) -- constant specifying whether phase is retreat, movement, or build
            top_k (int) -- integer specifying the orders returned are the top k highest probability orders 

        Returns:
            (dict) -- dictionary where each key is an order and its corresponding value is a dictionary
            storing its rank, predicted probability and rendering opacity. Rank is determined by predicted probability 
            sorted in decreasing order.
            e.g., {'A GAL R WAR': {'rank': 0, 'pred_prob': 0.3635689010282275, 'opacity': 1}, ...}}
        """
        sorted_json = dict()
        sorted_orders = []
        
        for unit, orders in preds.items():
            sorted_orders = sorted(orders, key=lambda x: x[1], reverse=True)[:min(top_k, len(orders))]

        # convert to json for easier parsing to frontend
        for rank, (order, pred_prob) in enumerate(sorted_orders):
            sorted_json[order] = dict()
            sorted_json[order]["rank"] = rank
            sorted_json[order]["pred_prob"] = pred_prob
            sorted_json[order]["opacity"] = pred_prob/sorted_orders[0][1] # linearly scaled
        return sorted_json
    
    # PREDICT FUNCTIONS 
    def predict_build(self):
        """
        Predict build phase for power in selected province
        (PROVINCE DEPENDENT)
        
        Returns:
            (dict) -- dictionary where each key is a home/unit of the power
            and the corresponding value is a list of its possible orders and predicted probabilities.
        """
        preds = dict() # key=home, val=[(possible_order, pred_prob),...]

        # check invalid
        if self.state is None:
            return preds
        
        res = self.get_unit_from_province()
        # unit is present in province, predict if it is a disbandable unit
        if res is not None:
            unit, power = res
            builds = self.state["builds"].get(power)
            if builds is None:
                return preds
            if builds["count"] < 0:
                preds = predict_order([unit], self.season_phase, self.model_path, self.attribute)
                self.set_power(power)
            return preds
        
        # unit is not present in province, predict if it is a buildable province
        power = self.get_home_power_of_province()
        if power is None:
            # province is not a home
            return preds
        
        # check if power can build
        builds = self.state["builds"].get(power)
        if builds is None:
            return preds
        if builds["count"] > 0:
            power_homes = builds["homes"]
            if self.province in power_homes:
                preds = predict_order([self.province], self.season_phase, self.model_path, self.attribute)
                self.set_power(power)
        return preds

    def predict_retreat(self):
        """
        Predict retreat phase for power in selected province
        (PROVINCE DEPENDENT)

        Returns:
            (dict) -- dictionary with one key being the retreating unit
            and the corresponding value is a list of its possible orders and predicted probabilities.
        """
        preds = dict()
        res = self.get_retreat_from_province()
        if res is None:
            return preds
        retreat_unit, power = res
        if retreat_unit[0] == '*':
            retreat_unit = retreat_unit[1:]

        self.set_power(power)
        return predict_order([retreat_unit], self.season_phase, self.model_path, self.attribute)
    
    def predict_move(self):
        """
        Predict move phase for power in selected province
        (PROVINCE DEPENDENT)

        Returns:
            (dict) -- dictionary with one key being the moving unit
            and the corresponding value is a list of its possible orders and predicted probabilities.
        """
        preds = dict()
        res = self.get_unit_from_province()

        if res is None:
            return preds
        
        move_unit, power = res
        self.set_power(power)
        return predict_order([move_unit], self.season_phase, self.model_path, self.attribute)
    
    def predict(self, top_k: int = 5):
        """
        Predict orders for power in current phase. 

        Params:
            top_k (int) -- integer specifying the orders returned are the top k highest probability orders 

        Returns:
            (dict) -- dictionary storing top k orders predicted for power in current phase
            e.g., {'A GAL R WAR': {'rank': 0, 'pred_prob': 0.3635689010282275, "opacity": 1}, ...}
        """
        self.set_attribute()
        self.set_season_phase()
        phase = PHASES.MOVEMENT
        preds = dict()
                
        if self.model_path is None or self.model_path == "":
            return {"error": "Server unable to locate model"}

        if self.season_phase[-1] == PHASES.RETREAT:
            phase = PHASES.RETREAT
            preds = self.predict_retreat()
        
        elif self.season_phase == PHASES.BUILD:
            phase = PHASES.BUILD
            preds = self.predict_build()

        else:
            preds = self.predict_move()

        sorted_preds = BaselineAdvice.sort_preds(preds, phase, top_k)

        return {"power": self.power, "preds": sorted_preds}
