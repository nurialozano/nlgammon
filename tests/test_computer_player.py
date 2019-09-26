import pytest
from ComputerPlayer import ComputerPlayer
from Board import Board
from Dice import Dice
from Move import Move


@pytest.fixture
def test_computerplayer():
    return ComputerPlayer(1)


def test_next_move(test_computerplayer):
    board = Board()
    board.board = [[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                   [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 2]]
    dice = Dice()
    dice.set_dice(1, 5)
    test_computerplayer.next_move(board, dice)
    assert test_computerplayer.next_move(board, dice) == [Move(1, 26, 20)]
