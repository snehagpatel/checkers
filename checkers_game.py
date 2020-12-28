import pygame
import os
import time
from PIL import Image
from checker_board import Board

'''
1. kings
2. turns
3. users restricted to red pieces
4. game over screen
5. info to right of game board
'''

os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Checkers')

board = Board()
board.initialize_game()


game_in_progress = True
turn = 'USER'
selected_piece = False
click = 0
saved_pos = {}

mouse_clicked = True
while game_in_progress:

    if board.num_user_pieces == 0 or board.num_cpu_pieces == 0:
        # GAME OVER
        print(board.check_game_over())
        break
    if turn == 'USER':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_in_progress = False

            if event.type == pygame.MOUSEBUTTONUP:
                # if click == 2, then a move has been made the last turn, and so this "resets"
                # to let another move happen
                if click == 2:
                    click = 0


                # if click == 1, it means a piece has been selected and the available spaces are shown
                if click == 1:
                    x1, y1 = event.pos
                    new_row = y1 // 100
                    new_col = x1 // 100
                    new_piece = board.get_board_val(new_row, new_col)
                    #if a new piece is selected
                    if new_piece is not None and (new_piece.get_type() == 'USER' or piece.get_type() == 'USER_KING'):
                        click = 0
                    # if the next click is an available space
                    if ((new_row, new_col), False) in positions or ((new_row, new_col), True) in positions:
                        board.board = board.update_board(saved_pos.get('original_row'), saved_pos.get('original_col'), new_row, new_col)
                        print("User went, it is now the CPU's turn")
                        board.reset_squares(surface)
                        board.draw(surface)
                        saved_pos = {}
                        click = 2
                        turn = 'CPU'


                # if click == 0, it means a piece has not been selected
                if click == 0:
                    x, y = event.pos
                    row = y // 100
                    col = x // 100
                    saved_pos.update({'original_row': row})
                    saved_pos.update({'original_col': col})
                    piece = board.get_board_val(row, col)
                    if piece is not None and (piece.get_type() == 'USER' or piece.get_type() == 'USER_KING'):
                        board.reset_squares(surface)
                        click = 1
                        positions = board.space_available(piece)
                        for position in positions:
                            row = position[0][0]
                            col = position[0][1]
                            surface.fill((0, 186, 255), rect=(col * 100, row * 100, 100, 100))

    elif turn == 'CPU':
        print("CPU went, it is now the User's turn")
        time.sleep(0.1)
        move = board.cpu_next_move()
        board.update_board(move[0], move[1], move[2], move[3])
        board.reset_squares(surface)
        board.draw(surface)
        turn = 'USER'

    surface.fill((0, 65, 0), rect=(800, 0, 400, 800))
    board.draw(surface)
    pygame.display.flip()
