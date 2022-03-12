"""
    Snakes and Ladders Simulator
"""
import random


class SnakeLadderBoard:
    """contains board and game logic for each player."""

    def __init__(self, snakes: dict, ladders: dict):
        self.snakes = snakes
        self.ladders = ladders
        self.max_position = 100

    def move(self, player, outcome):
        """ makes the move on rolling the dice """
        if player.current_position + outcome > self.max_position:
            return
        player.current_position += outcome
        if player.current_position >= 94:
            player.lucky_turns += 1
        if self.is_lucky(player):
            return
        elif self.is_unlucky(player):
            return

    def climb(self, player):
        climb = self.ladders.get(player.current_position) - player.current_position
        player.climbs += climb
        player.total_climbs += 1
        player.biggest_climb = player.biggest_climb or climb
        player.current_position += climb
        return True

    def is_lucky(self, player):
        """pass"""
        luck = False
        if player.current_position in self.ladders:
            luck = self.climb(player)
        elif (
            player.current_position - 2 in self.snakes
            or player.current_position + 2 in self.snakes
            or player.current_position - 1 in self.snakes
            or player.current_position + 1 in self.snakes
        ):
            luck = True
        elif player.lucky_turns < 2 and player.current_position == self.max_position:
            luck = True
        if luck:
            player.lucky += +1
            return True

    def is_unlucky(self, player):
        """pass"""
        if self.snakes.get(player.current_position):
            slide_to_position = player.current_position - self.snakes.get(
                player.current_position
            )
            player.current_position = self.snakes.get(player.current_position)
            player.unlucky += 1
            player.slides += slide_to_position
            player.total_slides += 1
            player.biggest_slide = player.biggest_slide or slide_to_position
            return True

    def roll_dice(self, player):
        """roll the dice to move and move the player position """
        moves = []
        if player.current_position == self.max_position:
            player.finished = True
            return
        while True:
            outcome = random.randrange(1, 7)
            moves.append(outcome)
            self.move(player, outcome)
            if outcome != 6 or player.current_position == 100:
                break
        player.turns += 1
        player.update_longest_turn(moves)


class Player:
    """
    separate class to represent players and track their records.
    """

    def __init__(self, idx):
        self.idx = idx
        self.lucky_turns = 0
        self.current_position = 0
        self.finished = False
        self.turns = 0
        self.lucky = 0
        self.unlucky = 0
        self.climbs = 0
        self.slides = 0
        self.biggest_climb = 0
        self.biggest_slide = 0
        self.total_climbs = 0
        self.total_slides = 0
        self.longest_turn = []

    def update_longest_turn(self, moves):
        """calculate and memoize the longest turn by player"""
        if (
            len(moves) > len(self.longest_turn)
            or len(moves) == len(self.longest_turn)
            and moves[-1] > self.longest_turn[-1]
        ):
            self.longest_turn = moves

    def get_stat(self, idx, result):
        stat = {
            "winning_position": idx,
            "turns": self.turns,
            "lucky": self.lucky,
            "unlucky": self.unlucky,
            "climbs": self.climbs,
            "slides": self.slides,
            "biggest_climb": self.biggest_climb,
            "biggest_slide": self.biggest_slide,
            "total_climbs": self.total_climbs,
            "total_slides": self.total_slides
        }
        for i in stat:
            if result.get(i):
                result[i].append(stat[i])
            else:
                result[i] = [stat[i]]
        if result.get("longest_turn"):
            if result.get("longest_turn") > len(self.longest_turn):
                result["longest_turn"] = self.longest_turn
            elif result.get("longest_turn") == len(self.longest_turn):
                result["longest_turn"] = (
                    result.get("longest_turn") if result.get("longest_turn")[-1] > self.longest_turn[-1] else self.longest_turn
                )
        else:
            result["longest_turn"] = self.longest_turn
        return result


def start_game(number_of_players: int, snakes: dict, ladders: dict, result: dict):
    """
    :param number_of_players: number of players for simulation
    :param snakes: snakes as dict format key represent head and value represent tail
    :param ladders: ladder to climb value as dict, key represent start and value represent climbed value.
    :return: player stats after complition
    """
    players = [Player(i) for i in range(number_of_players)]

    board = SnakeLadderBoard(snakes, ladders)
    position = 1
    while len(players) > 0:
        for idx, player in enumerate(players):
            if player.finished:
                result[f"player{player.idx}"] = player.get_stat(position, result.get(f"player{player.idx}",{}))
                position += 1
                players.pop(idx)
            board.roll_dice(player)
    return result


if __name__ == "__main__":
    print(start_game(5, {97: 78, 80: 40}, {5: 15, 18: 40}))
