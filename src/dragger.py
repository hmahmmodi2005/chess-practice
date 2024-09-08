import pygame
from const import *
from square import Square


class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.x = 0
        self.y = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_blit(self, surface):
        self.piece.set_texture(size=128)
        texture = self.piece.img

        img = pygame.image.load(texture)
        img_center = (self.x, self.y)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)

    def mouse_tracker(self, pos):
        self.x, self.y = pos

    def save_initial(self, row, col):
        self.initial_row = row
        self.initial_col = col

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def move_piece(self, board, game):
        placed_row = self.y // SQR_SIZE
        placed_col = self.x // SQR_SIZE

        if Square.in_range(placed_row, placed_col):
            for valid_move in self.piece.moves:
                if (placed_row, placed_col) == (valid_move.final.row, valid_move.final.col):
                    sound = pygame.mixer.Sound("assets/sounds/capture.wav") if board.squares[valid_move.final.row][valid_move.final.col].has_enemy_piece(self.piece.color) else pygame.mixer.Sound("assets/sounds/move.wav")
                    sound.set_volume(0.5)
                    sound.play()

                    self.piece.moved = True
                    board.last_move = valid_move
                    game.check_swap_turns()

                    board.squares[placed_row][placed_col].piece = self.piece # place piece on new square
                    board.squares[self.initial_row][self.initial_col].piece = None # remove piece from old square