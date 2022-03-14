import pytest
from unittest import mock
from snakeandladder.snakeandladder import SnakeLadderBoard, Player, start_game


def snake_fixture():
    return {10: 2, 50: 8, 99: 46, 87: 56}

def ladder_fixture():
    return {8: 20, 40: 56, 23: 60}

def player_fixture(idx):
    player = Player(idx)
    player.total_climbs = 1
    player.total_slides = 1
    player.lucky = 1
    player.unlucky = 1
    return player


def board_fixture():
    snake = snake_fixture()
    ladder = ladder_fixture()
    return SnakeLadderBoard(snake, ladder)


@pytest.mark.parametrize(
    "snakes,ladders",
    [
        ({10: 2, 50: 8, 99: 46, 87: 56}, {8: 20, 40: 56, 23: 60}),
        ({25: 4, 70: 28, 99: 62, 82: 56}, {4: 20, 30: 52, 21: 72}),
    ],
)
def test_snakeandladder_boardconfig(snakes, ladders):
    board = SnakeLadderBoard(snakes, ladders)
    assert board.snakes == snakes
    assert board.ladders == ladders


@pytest.mark.parametrize(
    "current_position,outcome,expected_position",
    [(41, 4, 45), (34, 6, 56), (97, 2, 46)],
)
def test_player_config(current_position, outcome, expected_position):
    player = player_fixture(0)
    assert player.current_position == 0
    player.current_position = current_position
    board_fixture().move(player, outcome)
    assert player.current_position == expected_position


@pytest.mark.parametrize(
    "current_position,outcome,expected_position,climbed",
    [(35, 5, 56, 2), (34, 6, 56, 2), (6, 2, 20, 2), (10, 2, 12, 1), (15, 6, 21, 1)],
)
def test_player_climb(current_position, outcome, expected_position, climbed):
    player = player_fixture(0)
    assert player.current_position == 0
    assert player.climbs != climbed
    player.current_position = current_position
    board_fixture().move(player, outcome)
    assert player.current_position == expected_position
    assert player.total_climbs == climbed


@pytest.mark.parametrize(
    "current_position,outcome,expected_position,slides",
    [(85, 2, 56, 2), (95, 4, 46, 2), (46, 4, 8, 2), (20, 4, 24, 1), (98, 2, 100, 1)],
)
def test_player_slide(current_position, outcome, expected_position, slides):
    player = player_fixture(0)
    assert player.current_position == 0
    assert player.climbs != slides
    player.current_position = current_position
    board_fixture().move(player, outcome)
    assert player.current_position == expected_position
    assert player.total_slides == slides


@pytest.mark.parametrize(
    "current_position,outcome,expected_position,luck_count",
    [(85, 3, 88, 2), (95, 5, 100, 2), (46, 4, 8, 1), (49, 3, 52, 2), (24, 4, 28, 1)],
)
def test_luck(current_position, outcome, expected_position, luck_count):
    player = player_fixture(0)
    assert player.current_position == 0
    player.current_position = current_position
    board_fixture().move(player, outcome)
    assert player.current_position == expected_position
    assert player.lucky == luck_count


@pytest.mark.parametrize(
    "current_position,outcome,expected_position,unlucky_count",
    [(85, 2, 56, 2), (95, 4, 46, 2), (46, 4, 8, 2), (49, 4, 53, 1), (24, 4, 28, 1)],
)
def test_unlucky(current_position, outcome, expected_position, unlucky_count):
    player = player_fixture(0)
    assert player.current_position == 0
    player.current_position = current_position
    board_fixture().move(player, outcome)
    assert player.current_position == expected_position
    assert player.unlucky == unlucky_count

@pytest.mark.parametrize("number_player,snakes,ladders",
                         [
                             (1,snake_fixture(),ladder_fixture()),
(6,snake_fixture(),ladder_fixture()),
(4,snake_fixture(),ladder_fixture()),
                         ])
def test_run_simulation(number_player,snakes, ladders):
    result = start_game(number_player,snakes, ladders, {})
    assert len(result) == number_player
    for p,r in result.items():
        assert r.get("turns")!=0
        assert len(r.get("longest_turn"))!=0
