import pytest
from Dice import Dice
from Move import Move


@pytest.fixture
def test_dice():
    return Dice()


def test_create_dice(test_dice):
    assert test_dice.die1 in range(1, 7)
    assert test_dice.die2 in range(1, 7)


def test_get_lowest_die(test_dice):
    test_dice.set_dice(4, 1)
    assert test_dice.get_lowest_die() == 1
    test_dice.set_dice(2, 5)
    assert test_dice.get_lowest_die() == 2


def test_get_roll_move_quantity(test_dice):
    test_dice.set_dice(1, 2)
    assert test_dice.get_roll_move_quantity() == 2
    test_dice.set_dice(6, 6)
    assert test_dice.get_roll_move_quantity() == 4
    test_dice.set_dice(4, 0)
    assert test_dice.get_roll_move_quantity() == 1


def test_is_double_dice(test_dice):
    test_dice.set_dice(2, 2)
    assert test_dice.is_double_dice()
    test_dice.set_dice(1, 2)
    assert not test_dice.is_double_dice()


def test_roll(test_dice):
    test_dice.roll()
    x, y = test_dice.die1, test_dice.die2
    assert x in range(1, 7) and y in range(1, 7)


def test_start_roll(test_dice):
    test_dice.start_roll()
    x, y = test_dice.die1, test_dice.die2
    assert x != y


def test_dice_status_to_string(test_dice):
    test_dice.set_dice(1, 2)
    assert test_dice.dice_status_to_string() == "Dice to play: 1 and 2"
    test_dice.set_dice(0, 4)
    assert test_dice.dice_status_to_string() == "Dice to play: 4"
    test_dice.set_dice(6, 0)
    assert test_dice.dice_status_to_string() == "Dice to play: 6"


def test_mark_used_die(test_dice):
    test_dice.set_dice(1, 2)
    move = Move(0, 24, 22)
    test_dice.mark_used_die(move)
    assert test_dice.die2 == 0

    test_dice.set_dice(4, 2)
    move = Move(0, 24, 20)
    test_dice.mark_used_die(move)
    assert test_dice.die1 == 0

    test_dice.set_dice(2, 3)
    move = Move(0, 26, 23)
    test_dice.mark_used_die(move)
    assert test_dice.die1 == 0
