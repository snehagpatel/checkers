import pygame
import os
import copy
from random import randrange
from PIL import Image
from piece import Piece


class Board:
    def __init__(self):
        self.board = None
        self.num_user_pieces = 12
        self.num_cpu_pieces = 12
        self.winner = None
        self.max_jumps_called = False


    #draws the board
    def draw(self, surface):
        for i in range(8):
            for j in range(8):
                if self.get_board_val(i, j):
                    if self.get_board_val(i, j) == Piece('CPU', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), (j * 100 + 5, i * 100 + 5))
                    elif self.get_board_val(i, j) == Piece('USER', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), (j * 100 + 5, i * 100 + 5))
                    elif self.get_board_val(i, j) == Piece('CPU_KING', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), (j * 100 + 5, i * 100 + 5))
                    elif self.get_board_val(i, j) == Piece('USER_KING', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), (j * 100 + 5, i * 100 + 5))

        # black and red squares for checker board
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 0:
                    surface.fill((255, 0, 0), rect=(j, 100 * i, 100, 100))
                else:
                    surface.fill((255, 0, 0), rect=(j + 100, 100 * i, 100, 100))

        # yellow outline and divider lines
        for i in range(100, 800, 100):
            pygame.draw.line(surface, (255, 233, 0), (0, i), (800, i), 2)
            pygame.draw.line(surface, (255, 233, 0), (i, 0), (i, 800), 2)
        pygame.draw.line(surface, (255, 233, 0), (0, 0), (0, 800), 5)
        pygame.draw.line(surface, (255, 233, 0), (0, 800), (800, 800), 5)
        pygame.draw.line(surface, (255, 233, 0), (800, 800), (800, 0), 5)
        pygame.draw.line(surface, (255, 233, 0), (800, 0), (0, 0), 5)

        surface.fill((0, 65, 0), rect=(800, 0, 400, 800))

    def draw_squares(self, surface):
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 0:
                    surface.fill((255, 0, 0), rect=(j, 100 * i, 100, 100))
                else:
                    surface.fill((255, 0, 0), rect=(j + 100, 100 * i, 100, 100))

    def reset_squares(self, surface):
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 1:
                    surface.fill((0, 0, 0), rect=(j, 100 * i, 100, 100))
                else:
                    surface.fill((0, 0, 0), rect=(j + 100, 100 * i, 100, 100))

    #sets up the board array with the pieces
    def initialize_game(self):
        board_arr = [[None for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(0, 8, 2):
                if i < 3:
                    if i % 2 == 0:
                        board_arr[i][j + 1] = Piece('CPU', i, j + 1)
                    else:
                        board_arr[i][j] = Piece('CPU', i, j)
                elif i > 4:
                    if i % 2 == 0:
                        board_arr[i][j + 1] = Piece('USER', i, j + 1)
                    else:
                        board_arr[i][j] = Piece('USER', i, j)
        self.board = board_arr

    def get_board_val(self, row, col):
        return self.board[row][col]

    def in_bounds(self, i, j):
        return i < 8 and j < 8 and i > -1 and j > -1

    def valid_pos(self, i, j):
        return self.in_bounds(i, j) and self.board[i][j] is None

    # returns -> after clicking on piece, finds spaces in board that are valid for piece to move to
    def space_available(self, piece):
        available_positions = []
        row = piece.get_row()
        col = piece.get_col()
        piece_type = piece.get_type()
        if piece_type == 'CPU':
            # no jump
            # left
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            # right
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            # jump left
            if self.in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] is not None:
                if (self.board[row + 1][col - 1].get_type() == 'USER' or self.board[row + 1][col - 1].get_type() == 'USER_KING') and self.valid_pos(row + 2, col - 2):
                    available_positions.append(((row + 2, col - 2), True))
            # jump right
            if self.in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] is not None:
                if (self.board[row + 1][col + 1].get_type() == 'USER' or self.board[row + 1][col + 1].get_type() == 'USER_KING') and self.valid_pos(row + 2, col + 2):
                    available_positions.append(((row + 2, col + 2), True))
        elif piece_type == 'USER':
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            if self.in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] is not None:
                if (self.board[row - 1][col - 1].get_type() == 'CPU' or self.board[row - 1][col - 1].get_type() == 'CPU_KING') and self.valid_pos(row - 2, col - 2):
                    available_positions.append(((row - 2, col - 2), True))
            if self.in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] is not None:
                if (self.board[row - 1][col + 1].get_type() == 'CPU' or self.board[row - 1][col + 1].get_type() == 'CPU_KING') and self.valid_pos(row - 2, col + 2):
                    available_positions.append(((row - 2, col + 2), True))
        elif piece_type == 'CPU_KING':
            # no jump
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            # jump
            if self.in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] is not None:
                if (self.board[row + 1][col - 1].get_type() == 'USER' or self.board[row + 1][col - 1].get_type() == 'USER_KING') and self.valid_pos(row + 2, col - 2):
                    available_positions.append(((row + 2, col - 2), True))
            if self.in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] is not None:
                if (self.board[row + 1][col + 1].get_type() == 'USER' or self.board[row + 1][col + 1].get_type() == 'USER_KING') and self.valid_pos(row + 2, col + 2):
                    available_positions.append(((row + 2, col + 2), True))
            if self.in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] is not None:
                if (self.board[row - 1][col - 1].get_type() == 'USER' or self.board[row - 1][col - 1].get_type() == 'USER_KING') and self.valid_pos(row - 2, col - 2):
                    available_positions.append(((row - 2, col - 2), True))
            if self.in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] is not None:
                if (self.board[row - 1][col + 1].get_type() == 'USER' or self.board[row - 1][col + 1].get_type() == 'USER_KING') and self.valid_pos(row - 2, col + 2):
                    available_positions.append(((row - 2, col + 2), True))
        elif piece_type == 'USER_KING':
            # no jump
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            # jump
            if self.in_bounds(row + 1, col - 1) and self.board[row + 1][col - 1] is not None:
                if (self.board[row + 1][col - 1].get_type() == 'CPU' or self.board[row + 1][col - 1].get_type() == 'CPU_KING') and self.valid_pos(row + 2, col - 2):
                    available_positions.append(((row + 2, col - 2), True))
            if self.in_bounds(row + 1, col + 1) and self.board[row + 1][col + 1] is not None:
                if (self.board[row + 1][col + 1].get_type() == 'CPU' or self.board[row + 1][col + 1].get_type() == 'CPU_KING') and self.valid_pos(row + 2, col + 2):
                    available_positions.append(((row + 2, col + 2), True))
            if self.in_bounds(row - 1, col - 1) and self.board[row - 1][col - 1] is not None:
                if (self.board[row - 1][col - 1].get_type() == 'CPU' or self.board[row - 1][col - 1].get_type() == 'CPU_KING') and self.valid_pos(row - 2, col - 2):
                    available_positions.append(((row - 2, col - 2), True))
            if self.in_bounds(row - 1, col + 1) and self.board[row - 1][col + 1] is not None:
                if (self.board[row - 1][col + 1].get_type() == 'CPU' or self.board[row - 1][col + 1].get_type() == 'CPU_KING') and self.valid_pos(row - 2, col + 2):
                    available_positions.append(((row - 2, col + 2), True))
        return available_positions

    '''__CPU MOVE RATING__
    1. if piece can become king, make king
    2. piece can make n jumps
    3. if move made, can player make king
    4. number of jumps player can make after move
    5. random between these highest rated moves
    '''

    def get_move_score(self, piece, move):
        old_row = piece.get_row()
        old_col = piece.get_col()
        new_row = move[0]
        new_col = move[1]
        score = 0
        if piece.get_type() == 'CPU' and new_row == 7:
            score += 2
        delta_x = new_row - old_row
        delta_y = new_col - old_col
        if delta_x % 2 == 0 and delta_y % 2 == 0:
            score += 1
        return score

    def cpu_next_move(self):
        d = {}
        l = []
        for i in range(8):
            for j in range(8):
                if self.get_board_val(i, j) is not None and (self.get_board_val(i, j).get_type() == 'CPU' or self.get_board_val(i, j).get_type() == 'CPU_KING'):
                    p = self.get_board_val(i, j)
                    pos = (i, j)
                    if len(self.space_available(p)) != 0:
                        spaces = self.space_available(p)
                        for space in spaces:
                            l.append(self.get_move_score(p, space[0]))
                            d.update({pos: {space: self.get_move_score(p, space[0])}})
        max_score = max(l)
        max_score_moves = []
        for i in list(d.keys()):
            for j in list(d.get(i).keys()):
                if d.get(i).get(j) == max_score:
                    max_score_moves.append((i, j[0]))

        n = len(max_score_moves)
        random_index = randrange(n)
        move = max_score_moves[random_index]
        old_row = move[0][0]
        old_col = move[0][1]
        new_row = move[1][0]
        new_col = move[1][1]
        return old_row, old_col, new_row, new_col



    # returns a new board with the piece at (old_row, old_col) moved to (new_row, new_col)
    def update_board(self, old_row, old_col, new_row, new_col):
        board = self.board
        piece = board[old_row][old_col]
        delta_x = new_row - old_row
        delta_y = new_col - old_col
        all_moves = self.space_available(piece)
        # ensures move is possible
        if (new_row, new_col) in [move[0] for move in all_moves]:
            # see if a piece is jumped, if so remove the piece between
            if (delta_x % 2 == 0):
                jumped_x = delta_x // 2
                jumped_y = delta_y // 2
                if (jumped_y == -1 and jumped_x == 1) or (jumped_y == 1 and jumped_x == -1):
                    board[old_row - jumped_y][old_col - jumped_x] = None
                else:
                    board[old_row + jumped_y][old_col + jumped_x] = None
                if piece.get_type() == 'USER' or piece.get_type() == 'USER_KING' and not self.max_jumps_called:
                    self.num_cpu_pieces -= 1
                else:
                    self.num_user_pieces -= 1
            board[old_row][old_col] = None
            piece.set_location(new_row, new_col)

            if piece.get_type() == 'USER' and new_row == 0:
                piece = Piece('USER_KING', new_row, new_col)
            elif piece.get_type() == 'CPU' and new_row == 7:
                piece = Piece('CPU_KING', new_row, new_col)
            board[new_row][new_col] = piece
        return board

    # for CPU: checks to see if a number of jumps is possible
    def max_jumps(self, piece):
        max = -1
        all_moves = self.space_available(piece)
        if len(all_moves) != 0:
            max = 0
        for move in all_moves:
            if move[1]:
                curr_row = piece.get_row()
                curr_col = piece.get_col()
                (next_row, next_col) = move[0]
                new_board = self.update_board(curr_row, curr_col, next_row, next_col)
                max = 1 + new_board.max_jumps(piece)
        return max

    def check_game_over(self):
        if self.num_user_pieces == 0:
            self.winner = 'CPU won!'
        elif self.num_cpu_pieces == 0:
            self.winner = 'User won!'
        return self.winner
