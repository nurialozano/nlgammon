from Colour import Colour
from Game import Game, GameType
from Player import PlayerType
from Testable import Testable
from Move import Move

import pygame
from GUI.Colours import Colours
from GUI.Measures import Measures
from GUI.GUIBoard import GUIBoard
from GUI.GUIDice import GUIDice
from GUI.GUIBottom import GUIBottom


class GraphicGame(Game, Testable):

    def __init__(self, player_type_1, player_type_2, player1_brain=None, player2_brain=None):
        super(GraphicGame, self).__init__(player_type_1, player_type_2, player1_brain, player2_brain)
        self.type = GameType.GRAPHIC
        self.graphic_board = GUIBoard()
        self.graphic_dice = GUIDice()
        self.graphic_bottom = GUIBottom()
        self.points = []
        self.DISPLAYSURF = None
        self.boardSurf = None
        self.diceSurf = None
        self.bottomSurf = None
        self.blot_hit = False

    def draw_interface(self):
        """Generates initial interface and surfaces with 30 checkers in initial positions"""
        self.boardSurf = self.graphic_board.generate_board_surface()
        self.graphic_board.draw_point_numbers(self.boardSurf)
        self.points = self.graphic_board.create_points()
        self.graphic_board.create_checkers(self.points)
        self.bottomSurf = self.graphic_bottom.generate_bottom_surface()
        self.graphic_bottom.draw_title(self.bottomSurf)
        self.diceSurf = self.graphic_dice.generate_dice_surface()

    def draw_board_status(self, display_surface):
        """Displays point checkers on the board surface"""
        for point in self.points:
            point.draw_checkers()
            display_surface.blit(point, point.point_position)

    def start(self):
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP])

        self.DISPLAYSURF = pygame.display.set_mode((Measures.WINDOWWIDTH.value, Measures.WINDOWHEIGHT.value))
        pygame.display.set_caption("PyGammon")
        self.DISPLAYSURF.fill(Colours.WHITE.value)

        self.draw_interface()
        self.DISPLAYSURF.blit(self.boardSurf, (0, 0))
        self.DISPLAYSURF.blit(self.bottomSurf, (0, Measures.BOARDHEIGHT.value))
        self.DISPLAYSURF.blit(self.diceSurf, (Measures.BOARDWIDTH.value, 0))
        self.draw_board_status(self.DISPLAYSURF)

        self.initiate()

        while True:
            self.play()
            pygame.display.update()  # update the screen for GAME OVER message

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def initiate(self):
        self.roll_start_roll()
        self.graphic_dice.draw_dice(self.dice.die1, self.dice.die2, self.diceSurf, self.DISPLAYSURF)
        self.graphic_bottom.display_text(self.bottomSurf, self.is_turn_of, 'START', self.DISPLAYSURF)
        self.get_player_moves()
        self.change_player()

    def play(self):
        while not self.is_game_over():
            self.dice.roll()
            self.graphic_dice.draw_dice(self.dice.die1, self.dice.die2, self.diceSurf, self.DISPLAYSURF)

            if self.has_some_legal_move(self.is_turn_of):
                if self.is_turn_of.type == PlayerType.ML:
                    self.graphic_bottom.empty_text_box(self.bottomSurf, self.DISPLAYSURF)  # clears the text box

                self.get_player_moves()

            else:
                self.graphic_bottom.display_text(self.bottomSurf, self.is_turn_of, 'MOVE', self.DISPLAYSURF)

            self.change_player()

        self.graphic_bottom.display_text(self.bottomSurf, self.is_turn_of, 'OVER', self.DISPLAYSURF)
        self.draw_board_status(self.DISPLAYSURF)

    def get_player_moves(self):

        self.draw_board_status(self.DISPLAYSURF)

        if self.is_turn_of.type == PlayerType.ML:
            moves = self.is_turn_of.next_move(self.board, self.dice)
            self.execute_ply(moves)
            self.make_graphic_moves(moves)

        if self.is_turn_of.type == PlayerType.GRAPHIC:
            available_moves = self.player_move_quantity()
            while available_moves > 0 and self.has_some_legal_move(self.is_turn_of):
                move = self.get_graphic_move()
                possible_moves = self.is_turn_of.next_move(self.board, self.dice)

                if move in possible_moves:
                    self.blot_hit = False
                    self.execute_move(move)
                    available_moves -= 1

                else:
                    self.undo_graphic_move(move)

    def get_graphic_move(self):
        """Returns the Move specified by the user on GUI"""
        to_point, from_point = None, None
        from_point_value = None
        from_point_event = None
        selected_checker = None
        need_move = True

        while need_move:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONUP and from_point is None:
                    movex, movey = event.pos
                    from_point_value = self.click_to_point(movex, movey)
                    from_point_event = event

                    try:
                        from_point = self.points[from_point_value]

                        for checker in from_point.checkers:
                            if checker.get_rect(topleft=(from_point.point_position[0] + checker.x,
                                                         from_point.point_position[1] + checker.y)).collidepoint(movex, movey):
                                selected_checker = checker

                                if selected_checker is None:
                                    selected_checker = from_point.checkers[-1]

                        if selected_checker is None:
                            from_point = None

                    except TypeError:
                        from_point = None

                if event.type == pygame.MOUSEBUTTONUP and from_point is not None and event.pos != from_point_event.pos \
                        and to_point is None:
                        movex, movey = event.pos
                        to_point_value = self.click_to_point(movex, movey)

                        try:
                            to_point = self.points[to_point_value]

                            from_point.remove_point_checker(self.boardSurf)
                            self.DISPLAYSURF.blit(from_point, from_point.point_position)

                            if len(to_point.checkers) == 1 and to_point.checkers[0].colour == Colours.WHITE.value:  # handles blot hit
                                to_remove_checker = to_point.checkers[0]
                                to_point.remove_point_checker(self.boardSurf)
                                self.points[25].checkers.append(to_remove_checker)
                                self.points[25].draw_checkers()
                                self.DISPLAYSURF.blit(self.points[25], self.points[25].point_position)
                                self.blot_hit = True

                            to_point.checkers.append(selected_checker)
                            to_point.draw_checkers()
                            self.DISPLAYSURF.blit(to_point, to_point.point_position)

                            to_point, from_point = None, None
                            need_move = False

                            if from_point_value == 25:
                                from_point_value = 26  # bar is point 26 in the original game version

                            move = Move(self.checker_colour_to_colour(selected_checker.colour), from_point_value,
                                        to_point_value)

                        except TypeError:
                            to_point = None

                pygame.display.update()

        return move

    @staticmethod
    def checker_colour_to_colour(checker_colour):
        if checker_colour == (0, 0, 0):
            return 0
        else:
            return 1

    def undo_graphic_move(self, move):
        to_point = self.points[move.to_point]
        from_point = self.points[move.from_point]
        checker = to_point.checkers[-1]

        if move.to_point == 0:
            to_point.remove_point_checker(self.bottomSurf)
        else:
            to_point.remove_point_checker(self.boardSurf)

        from_point.checkers.append(checker)

        if self.blot_hit:
            to_undo_bar_checker = self.points[25].checkers[-1]
            self.points[25].remove_point_checker(self.boardSurf)
            to_point.checkers.append(to_undo_bar_checker)
            self.blot_hit = False

        self.draw_board_status(self.DISPLAYSURF)

    def make_graphic_moves(self, ply):
        """Displays computer moves on GUI"""
        for move in ply:
            from_point = self.points[25 - move.from_point]
            to_point = self.points[25 - move.to_point]

            if move.to_point == 0:
                to_point = self.points[0]

            checker = from_point.checkers[-1]
            from_point.remove_point_checker(self.boardSurf)
            self.draw_board_status(self.DISPLAYSURF)

            if len(to_point.checkers) == 1 and to_point.checkers[-1].colour == Colours.BLACK.value:
                to_remove_checker = to_point.checkers[-1]
                to_point.remove_point_checker(self.boardSurf)
                self.points[25].checkers.append(to_remove_checker)
                self.points[25].draw_checkers()
                self.draw_board_status(self.DISPLAYSURF)

            to_point.checkers.append(checker)
            to_point.draw_checkers()
            self.draw_board_status(self.DISPLAYSURF)

        for move in ply:
            self.display_move(move, ply.index(move))

    def display_move(self, move, step):
        """Displays move descriptions in bottom pane"""
        if move.from_point == 26:
            text = Colour(move.colour).name + " moved from BAR" + " to " + str(move.to_point)
        elif move.to_point == 0:
            text = Colour(move.colour).name + " bore-off from " + str(move.from_point)
        else:
            text = Colour(move.colour).name + " moved from " + str(move.from_point) + " to " + str(move.to_point)

        self.graphic_bottom.display_move_string(self.bottomSurf, text, step, self.DISPLAYSURF)

    def click_to_point(self, mousex, mousey):
        for point in self.points:
            if point.get_rect(topleft=point.point_position).collidepoint(mousex, mousey) != 0:
                return self.points.index(point)
