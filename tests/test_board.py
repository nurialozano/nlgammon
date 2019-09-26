import pytest
from Board import Board
from Move import Move
from ComputerPlayer import ComputerPlayer


@pytest.fixture
def test_board():
    return Board()


@pytest.fixture
def test_board_bar():
    board = Board()
    board.board = [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
                   [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
    return board


@pytest.fixture
def test_board_blot():
    board = Board()
    board.board = [[0, 0, 0, 3, 1, 5, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 1, 1, 1, 1, 0, 3, 1, 0, 2, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
    return board


def test_create_board(test_board):
    assert test_board.board == [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]


def test_get_opponent_board(test_board_blot):
    assert test_board_blot.get_opponent_board(0) == [0, 0, 1, 1, 1, 1, 0, 3, 1, 0, 2, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    assert test_board_blot.get_opponent_board(1) == [0, 0, 0, 3, 1, 5, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0]


def test_get_point_value(test_board, test_board_blot):
    assert test_board.get_point_value(0, 24) == 2
    assert test_board.get_point_value(1, 6) == 5
    assert test_board_blot.get_point_value(0, 4) == 3
    assert test_board_blot.get_point_value(1, 3) == 1


def test_at(test_board):
    assert test_board.at(0, 1) == (0, 2)
    assert test_board.at(0, 6) == (5, 0)
    assert test_board.at(1, 1) == (2, 0)
    assert test_board.at(1, 6) == (0, 5)


def test_is_empty(test_board):
    assert not test_board.is_empty(0, 1)
    assert test_board.is_empty(0, 2)
    assert test_board.is_empty(1, 2)
    assert not test_board.is_empty(0, 6)


def test_bar_is_empty(test_board, test_board_bar):
    assert test_board.bar_is_empty(0)
    assert test_board.bar_is_empty(1)
    assert not test_board_bar.bar_is_empty(0)
    assert not test_board_bar.bar_is_empty(1)


def test_contains_own_checkers(test_board):
    assert test_board.contains_own_checkers(0, 6)
    assert not test_board.contains_own_checkers(0, 17)
    assert test_board.contains_own_checkers(1, 13)
    assert not test_board.contains_own_checkers(1, 12)


def test_one_opponent_checker(test_board):
    test_board.remove_checker(0, 24)
    assert test_board.one_opponent_checker(1, 1)
    assert not test_board.one_opponent_checker(1, 2)


def test_add_checker(test_board):
    test_board.add_checker(0, 4)
    assert test_board.board == [[0, 0, 0, 1, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]


def test_remove_checker(test_board):
    test_board.remove_checker(0, 6)
    assert test_board.board == [[0, 0, 0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
    test_board.remove_checker(1, 8)
    assert test_board.board == [[0, 0, 0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]

    with pytest.raises(ValueError):
        test_board.remove_checker(0, 1)

    with pytest.raises(ValueError):
        test_board.remove_checker(1, 2)


def test_move(test_board):
    move = Move(0, 24, 23)
    test_board.move(move)
    assert test_board.board == [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]


def test_apply_hit(test_board_blot):
    move = Move(0, 23, 22)
    hit_board = [[0, 0, 0, 3, 1, 5, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 0, 3, 1, 0, 2, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]]
    test_board_blot.apply_hit(move)
    assert test_board_blot.board == hit_board


def test_hit_to_string(test_board_blot):
    move = Move(0, 23, 22)
    test_board_blot.apply_hit(move)
    player = ComputerPlayer(1)
    assert test_board_blot.hit_to_string(player) == "WHITE checker is hit"


def test_board_to_vector(test_board):
    board_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                    0, 0, 0, 0, 1, 0]
    assert len(board_vector) == 198
    assert test_board.board_to_vector(0).tolist() == board_vector
