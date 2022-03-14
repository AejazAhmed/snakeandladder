"""
main file which runs the simulation
"""
import argparse
import json
from snakeandladder.simulate import SimulateAndProcessResult
from time import time


def main():
    parser = argparse.ArgumentParser()
    options = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "--simulations", default=1, help="provide number of simulation to perform"
    )
    parser.add_argument(
        "--players", default=1, help="provide number of players for simulation"
    )
    options.add_argument(
        "--config", help="provide snakes and ladders configuration in json format"
    )
    options.add_argument(
        "--config-file",
        help="provide path of file for snakes and ladders configuration in json format",
    )
    args = parser.parse_args()
    SimulateAndProcessResult(args).simulate()


if __name__ == "__main__":
    main()
