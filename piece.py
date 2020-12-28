import pygame
from PIL import Image

cp = Image.open('cpu_piece.PNG')
cpu_piece_pic = pygame.image.fromstring(cp.tobytes(), cp.size, cp.mode)
ck = Image.open('cpu_king.PNG')
cpu_king_piece_pic = pygame.image.fromstring(ck.tobytes(), ck.size, ck.mode)
up = Image.open('user_piece.PNG')
user_piece_pic = pygame.image.fromstring(up.tobytes(), up.size, up.mode)
uk = Image.open('user_king.PNG')
user_king_piece_pic = pygame.image.fromstring(uk.tobytes(), uk.size, uk.mode)

icon_dict = {'CPU' : cpu_piece_pic, 'CPU_KING' : cpu_king_piece_pic,
             'USER' : user_piece_pic, 'USER_KING' : user_king_piece_pic}

# initializes the Piece object

class Piece:
    def __init__(self, type, row, col):
        self.is_king = False
        self.type = type
        self.row = row
        self.col = col
        self.icon = icon_dict.get(type)



    def __eq__(self, other_piece):
        return self.__dict__ == other_piece.__dict__

    def get_icon(self):
        return self.icon

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_type(self):
        return self.type

    def set_location(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
