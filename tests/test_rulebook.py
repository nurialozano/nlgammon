import pytest
from RuleBook import RuleBook
from Board import Board
from Move import Move
from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer
from Dice import Dice
from HumanGame import HumanGame


@pytest.fixture
def test_rulebook():
    board = Board()
    player = HumanPlayer(0)
    dice = Dice()
    return RuleBook(board, player, dice)


@pytest.fixture
def test_bar():
    board = Board()
    board.board = [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                   [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
    player = HumanPlayer(0)
    dice = Dice()
    return RuleBook(board, player, dice)


@pytest.fixture
def test_bearoff():
    board = Board()
    board.board = [[0, 2, 2, 3, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
    player = HumanPlayer(0)
    dice = Dice()
    return RuleBook(board, player, dice)


@pytest.fixture
def test_highest():
    game = HumanGame('HUMAN', 'COMPUTER')
    highest_board = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0]]
    game.board.board = highest_board
    game.dice.set_dice(1, 5)
    return RuleBook(game.board, game.player1, game.dice)


@pytest.fixture
def test_alternative():
    game = HumanGame('HUMAN', 'COMPUTER')
    game.board.board = [[2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                        [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0]]
    game.dice.set_dice(6, 5)
    return RuleBook(game.board, game.player1, game.dice)


def test_is_valid_from_point(test_rulebook):
    assert test_rulebook.is_valid_from_point(test_rulebook.player.colour, 24)
    assert test_rulebook.is_valid_from_point(1, 13)
    assert not test_rulebook.is_valid_from_point(1, 22)


def test_is_valid_to_point(test_rulebook, test_bearoff):
    assert test_rulebook.is_valid_to_point(1, 18)
    assert test_rulebook.is_valid_to_point(1, 8)

    test_bearoff.move = Move(0, 1, 0)
    assert test_bearoff.is_valid_to_point(0, 0)

    test_bearoff.player.colour = 1
    assert not test_bearoff.is_valid_to_point(1, 0)


def test_is_valid_number_of_positions(test_rulebook):
    dice = Dice()
    dice.set_dice(1, 2)
    move = Move(0, 24, 23)
    assert test_rulebook.is_valid_number_of_positions(move, dice)


def test_is_valid_move(test_rulebook):
    move1 = Move(0, 6, 4)
    move2 = Move(0, 13, 14)
    move3 = Move(0, 12, 13)

    test_rulebook.dice.set_dice(1, 2)

    test_rulebook.move = move1
    assert test_rulebook.is_valid_move(move1)

    test_rulebook.move = move2
    assert not test_rulebook.is_valid_move(move2)

    test_rulebook.move = move3
    assert not test_rulebook.is_valid_move(move3)


def test_get_board_moves(test_rulebook):
    test_rulebook.board.board = [[2, 6, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                                 [3, 3, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]]
    test_rulebook.dice.set_dice(5, 1)
    assert test_rulebook.get_board_moves() == [Move(0, 7, 2), Move(0, 7, 6), Move(0, 2, 1)]


def test_checker_in_bar(test_bar, test_rulebook):
    assert test_bar.checker_in_bar()
    assert not test_rulebook.checker_in_bar()


def test_can_move_bar_checker(test_bar):
    test_bar.dice.set_dice(1, 2)
    assert test_bar.can_move_bar_checker()

    test_bar.dice.set_dice(6, 6)
    assert not test_bar.can_move_bar_checker()


def test_get_bar_moves(test_bar):
    moves = [Move(0, 26, 24), Move(0, 26, 23)]
    test_bar.dice.set_dice(1, 2)
    assert test_bar.get_bar_moves() == moves

    test_bar.dice.set_dice(6, 6)
    assert test_bar.get_bar_moves() == []


def test_all_checkers_in_home_board(test_bearoff, test_bar, test_rulebook):
    assert test_bearoff.all_checkers_in_home_board()
    assert not test_bar.all_checkers_in_home_board()
    assert not test_rulebook.all_checkers_in_home_board()


def test_checkers_on_higher_numbered_points(test_bearoff):
    test_bearoff.dice.set_dice(1, 3)
    test_bearoff.board.board = [[0, 2, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.checkers_on_higher_numbered_points()

    test_bearoff.board.board = [[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.checkers_on_higher_numbered_points()

    test_bearoff.board.board = [[0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.checkers_on_higher_numbered_points()

    test_bearoff.dice.set_dice(5, 3)
    test_bearoff.board.board = [[2, 6, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                                [3, 3, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]]
    assert test_bearoff.checkers_on_higher_numbered_points()


def test_can_bear_off(test_bearoff, test_bar, test_rulebook):

    assert test_bearoff.can_bear_off()
    # can bear off from points indicated by the dice

    test_bearoff.board.board = [[0, 2, 2, 3, 2, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]
    assert not test_bearoff.can_bear_off()
    # one checker is not in home board

    test_bearoff.dice.set_dice(5, 6)
    test_bearoff.board.board = [[3, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.can_bear_off()
    # no checkers in points 5 and 6 but can still bear off from highest point where there are checkers

    test_bearoff.dice.set_dice(1, 3)
    test_bearoff.board.board = [[0, 2, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert not test_bearoff.can_bear_off()
    # there are checkers in higher numbered points which must be moved before bearing-off

    test_bearoff.player = HumanPlayer(1)
    assert not test_bearoff.can_bear_off()


def test_get_bear_off_moves(test_bearoff, test_rulebook):

    test_bearoff.dice.set_dice(4, 2)
    assert test_bearoff.get_bear_off_moves() == [Move(0, 4, 0), Move(0, 2, 0)]

    test_bearoff.dice.set_dice(3, 1)
    test_bearoff.board.board = [[0, 2, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == []

    test_bearoff.dice.set_dice(6, 4)
    test_bearoff.board.board = [[3, 2, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == []

    test_bearoff.dice.set_dice(4, 6)
    test_bearoff.board.board = [[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [5, 5, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == [Move(0, 1, 0)]

    test_bearoff.dice.set_dice(3, 4)
    test_bearoff.board.board = [[9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [5, 5, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == [Move(0, 2, 0)]

    test_bearoff.dice.set_dice(3, 4)
    test_bearoff.board.board = [[8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [5, 5, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == [Move(0, 2, 0)]

    test_bearoff.dice.set_dice(3, 3)
    test_bearoff.board.board = [[8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                                [5, 5, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == [Move(0, 2, 0)]

    test_bearoff.player = ComputerPlayer(1)
    test_bearoff.dice.set_dice(0, 6)
    test_bearoff.board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                [3, 7, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_bearoff.get_bear_off_moves() == [Move(1, 4, 0)]


def test_get_legal_moves_per_die(test_rulebook):
    test_rulebook.dice.set_dice(3, 2)
    legal_moves = test_rulebook.get_legal_moves()
    assert test_rulebook.get_legal_moves_per_die(legal_moves, test_rulebook.dice.die1) == [Move(0, 24, 21),
                                                                                           Move(0, 13, 10),
                                                                                           Move(0, 8, 5),
                                                                                           Move(0, 6, 3)]


def test_generate_legal_ply_list(test_rulebook):
    test_rulebook.player = ComputerPlayer(1)
    test_rulebook.dice.set_dice(1, 6)
    test_rulebook.board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                 [3, 7, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert test_rulebook.generate_legal_ply_list() == [[Move(1, 1, 0), Move(1, 5, 0)], [Move(1, 5, 4), Move(1, 4, 0)],
                                                       [Move(1, 4, 3), Move(1, 5, 0)], [Move(1, 3, 2), Move(1, 5, 0)],
                                                       [Move(1, 2, 1), Move(1, 5, 0)]]

    test_rulebook.board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0]]
    test_rulebook.dice.set_dice(1, 1)
    assert test_rulebook.generate_legal_ply_list() == [[Move(1, 9, 8), Move(1, 8, 7), Move(1, 7, 6), Move(1, 6, 5)]]

