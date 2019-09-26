import pytest
from ComputerGame import ComputerGame


@pytest.fixture
def test_computer_game():
    return ComputerGame('COMPUTER', 'COMPUTER')


def test_start(test_computer_game):
    test_computer_game.start()
    assert len(test_computer_game.game_boards) > 0
    assert test_computer_game.starting_player is not None


