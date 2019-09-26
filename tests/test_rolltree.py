from RollTree import RollTree
from RuleBook import RuleBook
from Board import Board
from ComputerPlayer import ComputerPlayer
from Dice import Dice
from Move import Move


def test_rolltree():
    board = Board()
    board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0]]
    player = ComputerPlayer(1)
    dice = Dice()
    dice.set_dice(1, 1)
    rulebook = RuleBook(board, player, dice)
    rolltree = RollTree([], Move(1, 8, 7), rulebook, 1, 4)

    test_dice = Dice()
    test_dice.set_dice(1, 0)
    assert rolltree.rulebook.dice == test_dice

    rolltree.activate()
    assert len(rolltree.children) == 1
    assert rolltree.traverse_roll_tree(rolltree, []) == [[Move(1, 8, 7), Move(1, 7, 6), Move(1, 6, 5), Move(1, 5, 4)]]

    rulebook.board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0]]
    rolltree = RollTree([], Move(1, 2, 1), rulebook, 1, 4)
    rolltree.activate()
    assert rolltree.traverse_roll_tree(rolltree, []) == [[Move(1, 2, 1), Move(1, 1, 0)]]

    rulebook.board.board = [[9, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [3, 7, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    rulebook.dice.set_dice(1, 6)

    assert rulebook.generate_legal_ply_list() == [[Move(1, 1, 0), Move(1, 5, 0)], [Move(1, 5, 4), Move(1, 4, 0)],
                                                  [Move(1, 4, 3), Move(1, 5, 0)], [Move(1, 3, 2), Move(1, 5, 0)],
                                                  [Move(1, 2, 1), Move(1, 5, 0)]]
