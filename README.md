"snake and ladder assignment"

Requirements:
python version supported is 3.6+

use the simulate_game.sh script to run the simulation.

The simulate_game.sh script will take the following command line arguments

To run the script open the terminal and do the following.
./simulate_game.sh --config|--config-file value/filepath --players count --simulations count

You must provide one of the following argument.
--config-file file-path/file.json 
    The provided file must be a json file.
    ex: --config-file board-config.json
--config value
    The provided configuration mush be a string of json formatted data.
    ex: --config '{"snakes":{},"ladders":{}}'

The following are arguments can be provided if not provided it will be set by default with value 1
--players count 
    number of players to play the game for simulation
    value must be an integer value, if not provided the value will be set to 1 by default.
    ex: --player 5

--simulations count 
    Number of simulation to perform
    value must be integer, if not provided it will be set by default to 1.


Board Configuration or snakes and ladder customization:

snakes and ladders configurations can be provided using the json format integer value.

Snakes: The key will be represented as mouth of snake and value will be represented as tail. Note: key must be strictly greater than the value.
    ex: {"99":"24"}
ladders: The key will be represented as start of ladder and value will be represented end to be climbed. Note: key must be strictly less than the value.
    ex: {"3":"10"}

So the configuration will be looks like the following:

{
    "snakes":{"80":"50",...},
    "ladders":{"10":"30", ....}
}

The result will be given as a json file containing all the values which is asked.


Test script:

Test script uses the given sampleboardconfig ad run the script 
You can run the tests using test_run_simulation.sh directly from terminal
It will generate the result for 5 players and run simulation for 50 times.