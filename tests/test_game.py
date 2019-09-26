import pytest
from HumanGame import HumanGame
from Move import Move


@pytest.fixture
def test_game():
    return HumanGame('HUMAN', 'COMPUTER')


@pytest.fixture
def test_blot():
    blot_board = [[0, 0, 0, 3, 1, 5, 0, 0, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                  [0, 1, 1, 1, 1, 1, 0, 3, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
    human_game = HumanGame('HUMAN', 'COMPUTER')
    human_game.board.board = blot_board
    human_game.is_turn_of = human_game.player1
    return human_game


def test_start_to_string(test_game):
    test_game.dice.set_dice(1, 2)
    test_game.is_turn_of = test_game.player2
    assert test_game.start_to_string() == "BLACK rolled 1, WHITE rolled 2. WHITE starts."


def test_is_not_turn_of(test_game):
    test_game.is_turn_of = test_game.player1
    assert test_game.is_not_turn_of() == test_game.player2


def test_roll_to_string(test_game):
    test_game.is_turn_of = test_game.player2
    test_game.dice.set_dice(4, 5)
    assert test_game.roll_to_string() == "WHITE rolls 4 and 5"


def test_change_player(test_game):
    test_game.is_turn_of = test_game.player1
    test_game.change_player()
    assert test_game.is_turn_of == test_game.player2


def test_is_game_over(test_game):
    black_wins_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0],
                        [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]

    white_wins_board = [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0]]

    test_game.board.board = black_wins_board
    assert test_game.is_game_over()

    test_game.board.board = white_wins_board
    assert test_game.is_game_over()


def test_is_blot_hit(test_blot):
    test_blot.dice.set_dice(1, 2)
    move = Move(0, 23, 22)
    assert test_blot.is_blot_hit(move)


def test_has_some_legal_move(test_game):
    assert test_game.has_some_legal_move(test_game.player1)
    assert test_game.has_some_legal_move(test_game.player2)

    test_game.board.board = [[0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0],
                             [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
    test_game.dice.set_dice(6, 6)
    assert not test_game.has_some_legal_move(test_game.player1)

    test_game.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 13, 0],
                             [0, 5, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]]
    test_game.dice.set_dice(1, 1)
    assert not test_game.has_some_legal_move(test_game.player1)

