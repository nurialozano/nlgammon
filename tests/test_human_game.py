import pytest
from HumanGame import HumanGame
from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer


@pytest.fixture
def test_human_game():
    return HumanGame('HUMAN', 'COMPUTER')


@pytest.fixture
def test_bar():
    human_game = HumanGame('HUMAN', 'COMPUTER')
    bar_board = [[0, 0, 0, 3, 1, 5, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3],
                 [0, 2, 0, 1, 1, 1, 0, 3, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
    human_game.board.board = bar_board
    return human_game


def test_request_user_colour(test_human_game, monkeypatch):
    human_player = HumanPlayer(0)
    computer_player = ComputerPlayer(1)

    monkeypatch.setattr('builtins.input', lambda x: 'b')
    test_human_game.request_user_colour()

    assert test_human_game.player1 == human_player and test_human_game.player2 == computer_player

    human_player = HumanPlayer(1)
    computer_player = ComputerPlayer(0)

    monkeypatch.setattr('builtins.input', lambda x: 'w')
    test_human_game.request_user_colour()

    assert test_human_game.player1 == human_player and test_human_game.player2 == computer_player


def test_roll_to_string(test_human_game):
    test_human_game.dice.set_dice(1, 2)
    human_player = HumanPlayer(0)
    test_human_game.is_turn_of = human_player
    assert test_human_game.roll_to_string() == "BLACK rolls 1 and 2"


def test_load_saved_game(monkeypatch):
    game = HumanGame('HUMAN', 'COMPUTER')
    monkeypatch.setattr('builtins.input', lambda x: "test")
    game.save_game()
    saved_game = game.load_saved_game("test")
    assert saved_game == game


def test_user_colour_to_string(test_human_game):
    test_human_game.user_colour = 0
    assert test_human_game.user_colour_to_string() == "You are playing BLACK"

