from Move import Move


class RuleBook:

    def __init__(self, board, player, dice):
        self.board = board
        self.player = player
        self.dice = dice

    def is_valid_from_point(self, colour, from_point):
        """Returns whether the player has 1 checker or more in a certain point"""
        return self.board.get_point_value(colour, from_point) > 0

    def is_valid_to_point(self, colour, to_point):
        """Returns whether the to-point is empty, contains 1 opponent checker,
        or contains other checkers from the same player"""
        valid = False
        b, w = self.board.at(colour, to_point)
        if to_point == 0:
            if self.can_bear_off():
                valid = True
        else:
            if self.board.is_empty(colour, to_point):
                valid = True
            elif self.board.one_opponent_checker(colour, to_point):
                valid = True
            elif self.board.contains_own_checkers(colour, to_point):
                valid = True
        return valid

    @staticmethod
    def is_valid_number_of_positions(move, dice):
        positions = move.from_point - move.to_point
        return positions in (dice.die1, dice.die2)

    @staticmethod
    def is_valid_number_of_positions_from_bar(move, dice):
        positions = move.from_point - move.to_point - 1
        return positions in (dice.die1, dice.die2)

    def is_valid_direction_points(self, move):
        return move.from_point > move.to_point and \
               self.is_valid_from_point(move.colour, move.from_point) and \
               self.is_valid_to_point(move.colour, move.to_point)

    def is_valid_move(self, move):
        return self.is_valid_direction_points(move) and \
               self.is_valid_number_of_positions(move, self.dice)

    def is_valid_move_from_bar(self, move):
        return self.is_valid_direction_points(move) and \
               self.is_valid_number_of_positions_from_bar(move, self.dice) and \
               move.to_point != 25

    def get_legal_moves(self):
        """Returns a list of all legal moves for the player"""
        legal_moves = []
        if self.checker_in_bar():
            if self.can_move_bar_checker():
                legal_moves = self.get_bar_moves()
        else:
            if self.can_bear_off():
                legal_moves.extend(self.get_bear_off_moves())

            legal_moves.extend(self.get_board_moves())

        return legal_moves

    def get_board_moves(self):
        """Returns a list of all legal moves of the player's checkers in the board"""
        board_moves = []

        board_moves.extend(self.get_board_moves_for_die(self.dice.die1))

        if not self.dice.is_double_dice():
            board_moves.extend(self.get_board_moves_for_die(self.dice.die2))

        return board_moves

    def get_board_moves_for_die(self, die):
        """Returns a list of all legal moves of the player's checkers in the board for a particular die"""
        board_moves_die = []
        for i in range(23, -1, -1):
            if self.board.board[self.player.colour][i] > 0:  # checks if the move is within the board
                if i + 1 - die < 1:
                    continue
                else:
                    move = Move(self.player.colour, (i+1), (i+1 - die))
                    if self.is_valid_move(move):
                        board_moves_die.append(move)
        return board_moves_die

    def checker_in_bar(self):
        """Returns True if there is a checker or more on the player's bar"""
        player_board = self.board.board[self.player.colour]
        return player_board[25] > 0

    def can_move_bar_checker(self):
        """Returns True if a checker on the bar can be moved to the board"""
        opponent_board = self.board.get_opponent_board(self.player.colour)
        return opponent_board[self.dice.die1-1] <= 1 or opponent_board[self.dice.die2-1] <= 1

    def get_bar_moves(self):
        bar_moves = []
        move = Move(self.player.colour, 26, 25 - self.dice.die1)
        if self.is_valid_move_from_bar(move):
            bar_moves.append(move)
        move = Move(self.player.colour, 26, 25 - self.dice.die2)
        if self.is_valid_move_from_bar(move):
            bar_moves.append(move)
        return bar_moves

    def all_checkers_in_home_board(self):
        """Returns True if all checkers are in the home board"""
        player_board = self.board.board[self.player.colour]
        all_home = True
        for i in range(23, 5, -1):
            if player_board[i] > 0:
                all_home = False
        return all_home

    def can_bear_off_from_dice_points(self):
        """Returns True if there are checkers to bear off at the points given by the dice"""
        player_board = self.board.board[self.player.colour]
        return player_board[self.dice.die1 - 1] > 0 or player_board[self.dice.die2 - 1] > 0

    def checkers_on_higher_numbered_points(self):
        """Returns True if all checkers are in home board, and there are checkers in higher numbered points
        than the ones given by the dice"""
        player_board = self.board.board[self.player.colour]

        checkers_on_higher_numbered_points = False

        if self.dice.die1 > 0:
            for i in range(5, self.dice.die1-1, -1):
                if player_board[i] > 0:
                    checkers_on_higher_numbered_points = True

        if self.dice.die2 > 0:
            for i in range(5, self.dice.die2-1, -1):
                if player_board[i] > 0:
                    checkers_on_higher_numbered_points = True

        return checkers_on_higher_numbered_points

    def can_bear_off(self):
        """Returns True if there are checkers that can be borne off"""
        can_bear_off = False
        if self.all_checkers_in_home_board() and self.board.bar_is_empty(self.player.colour):
            if self.can_bear_off_from_dice_points():
                can_bear_off = True
            else:
                if not self.checkers_on_higher_numbered_points():
                    can_bear_off = True
        return can_bear_off

    def get_bear_off_moves(self):
        """Returns a list with all possible bear-off moves, first it checks if there are possible moves from dice
        points, and if not it adds the bear-off moves from the highest point where there are checkers"""
        bear_off_moves = []

        # First it checks whether there are possible moves from dice points
        if self.can_bear_off_from_dice_points():
            if self.board.board[self.player.colour][self.dice.die1 - 1] > 0:
                bear_off_moves.append(Move(self.player.colour, self.dice.die1, 0))
            if self.board.board[self.player.colour][self.dice.die2 - 1] > 0:
                bear_off_moves.append(Move(self.player.colour, self.dice.die2, 0))

        # If not it adds the bear-off moves from the highest point where there are checkers
        else:
            if not self.checkers_on_higher_numbered_points():
                for i in range(5, -1, -1):
                    if self.board.board[self.player.colour][i] > 0:
                        move = Move(self.player.colour, i + 1, 0)
                        bear_off_moves.append(move)
                        break
        return bear_off_moves

    @staticmethod
    def get_legal_moves_per_die(legal_moves, die):
        """Given a list of legal moves, it returns the list of moves for the given die"""
        die_moves = []
        for move in legal_moves:
            if move.get_number_of_positions() == die:
                die_moves.append(move)
        return die_moves

    def are_legal_moves_for_each_die(self, legal_moves):
        die1 = self.get_legal_moves_per_die(legal_moves, self.dice.die1)
        die2 = self.get_legal_moves_per_die(legal_moves, self.dice.die2)
        return len(die1) > 0 and len(die2) > 0

    @staticmethod
    def check_highest_die_rule(ply_list):
        """Applies the rule according to which if either die can be used but not both, the highest die must be used"""
        if len(ply_list) == 2:
            if len(ply_list[0]) == 1 and len(ply_list[1]) == 1:
                if ply_list[0][0].get_number_of_positions() != ply_list[1][0].get_number_of_positions():
                    if ply_list[0][0].get_number_of_positions() > ply_list[1][0].get_number_of_positions():
                        ply_list.pop(1)
                    else:
                        ply_list.pop(0)

    def generate_legal_ply_list(self):
        from RollTree import RollTree
        legal_ply_list = []
        roll_qty = self.dice.get_roll_move_quantity()
        moves = self.get_legal_moves()

        if roll_qty > 1:

            for move in moves:
                tree_structure = RollTree([], move, self, 1, roll_qty)
                tree_structure.activate()
                legal_ply_list.extend(tree_structure.traverse_roll_tree(tree_structure, []))

        else:
            legal_ply_list = [moves[x:x + 1] for x in range(0, len(moves), 1)]
            # if there is only one move possible, the list of plies contains one of the legal moves per ply

        self.check_highest_die_rule(legal_ply_list)

        return legal_ply_list
