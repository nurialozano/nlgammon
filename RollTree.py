import copy
from RuleBook import RuleBook
from Dice import Dice


class RollTree:
    def __init__(self, parent, move, rulebook, level, plays):
        self.parent = parent
        self.children = []
        self.move = move
        self.rulebook = rulebook
        self.level = level
        self.ply = []
        self.leaf = False
        self.plays = plays

        if self.rulebook.dice.is_double_dice():
            self.rulebook.dice.set_dice(self.rulebook.dice.die1, 0)

    def get_next_board(self):
        board_copy = copy.deepcopy(self.rulebook.board)
        board_copy.move(self.move)
        return board_copy

    def get_next_rulebook(self, board):
        dice_copy = Dice()
        dice_copy.set_dice(self.rulebook.dice.die1, self.rulebook.dice.die2)
        if self.plays == 2:
            dice_copy.mark_used_die(self.move)
        return RuleBook(board, self.rulebook.player, dice_copy)

    def activate(self):
        if self.level == self.plays:
            self.ply.extend(self.parent)
            self.ply.append(self.move)
            self.leaf = True

        else:
            new_rulebook = self.get_next_rulebook(self.get_next_board())
            children = new_rulebook.get_legal_moves()

            if not children:
                self.ply.extend(self.parent)
                self.ply.append(self.move)
                self.leaf = True

            else:
                for move in children:
                    parent = []
                    parent.extend(self.parent)
                    parent.append(self.move)
                    rolltree = RollTree(parent, move, new_rulebook, self.level + 1, self.plays)
                    self.children.append(rolltree)
                    rolltree.activate()

    def traverse_roll_tree(self, roll_tree, ply_list):
        if roll_tree.leaf:
            ply_list.append(roll_tree.ply)
        else:
            for subtree in roll_tree.children:
                self.traverse_roll_tree(subtree, ply_list)
        return ply_list
