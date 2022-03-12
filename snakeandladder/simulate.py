import json
from time import time
from snakeladder.snakeandladder import start_game


class SimulateAndProcessResult:
    def __init__(self, args):
        self.players = int(args.players)
        self.simulation = int(args.simulations)
        self.config = self.verify_board_config(json.loads(args.config)) if args.config else self.verify_board_config(json.load(open(args.config_file)))
        self.result = {}

    def simulate(self):
        print("simulation in progress .....")
        try:
            for i in range(self.simulation):
                self.result = start_game(
                        self.players, self.config["snakes"], self.config["ladders"], self.result)
            self.generate_stats_result()
        except Exception as e:
            print(f"Exception occurred with exception message \n {e} ")

    def verify_board_config(self, config:dict):
        if config:
            new_config = {"snakes": {}, "ladders": {}}
            if type(config.get("snakes")) is dict and type(config.get("ladders")) is dict:
                for key, value in config.get("snakes").items():
                    key = int(key)
                    value = int(value)
                    if key < value:
                        raise ValueError(
                            f"wrong snake configuration is provided \n key must be greater than value {key},{value}"
                        )
                    new_config["snakes"][key] = value
                for key, value in config.get("ladders").items():
                    key = int(key)
                    value = int(value)
                    if key > value:
                        raise ValueError(
                            "wrong ladder configuration is provided \n key must be less than value"
                        )
                    new_config["ladders"][key] = value
                return new_config
        raise ValueError("unable to find snakes and ladders configuration ")

    def generate_stats_result(self):
        response = {}
        for player in self.result:
            if not response.get(player):
                response[player] = {}
            response[player]["longest_turn"] = self.result[player].pop("longest_turn", [])
            for key, value in self.result[player].items():
                if not response.get(player).get(key):
                    response[player][key] = {
                        "minimum": None,
                        "maximum": None,
                        "average": None,
                    }
                value.sort()

                response[player][key]["minimum"] = value[0]
                response[player][key]["maximum"] = value[-1]
                response[player][key]["average"] = value[(0 + len(value)) // 2]
        file_name = f"./simulation_result-{time()}.json"
        f = open(file_name, "w")
        json.dump(response, f)
        print(
            f"simulation is completed please check the generated result under {file_name} file"
        )

