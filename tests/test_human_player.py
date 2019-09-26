import pytest

from Board import Board
from Dice import Dice
from HumanPlayer import HumanPlayer
from Move import Move


@pytest.fixture
def test_humanplayer():
    return HumanPlayer(0)


def test_next_move(monkeypatch, test_humanplayer):
    board = Board()
    dice = Dice()
    dice.set_dice(2, 1)
    monkeypatch.setattr('builtins.input', lambda x: '13 11')
    assert test_humanplayer.next_move(board, dice) == Move(0, 13, 11)

    monkeypatch.setattr('builtins.input', lambda x: '24 23')
    assert test_humanplayer.next_move(board, dice) == Move(0, 24, 23)

    monkeypatch.setattr('builtins.input', lambda x: '6 5')
    assert test_humanplayer.next_move(board, dice) == Move(0, 6, 5)



