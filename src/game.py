import pygame
from const import *
from board import Board
from dragger import Dragger
from square import Square
import time


class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.font = pygame.font.SysFont("monospace", 18)
        self.whites_turn = True
        self.hovered_sqr = None

    def show_background(self, surface):
        for row in range(BOARD_DIMENSIONS):
            for col in range(BOARD_DIMENSIONS):
                if (row + col) % 2 == 0:
                    color = (255, 200, 200)  # light sqr
                else:
                    color = (100, 0, 100)  # dark sqr

                rect = (row * SQR_SIZE, col * SQR_SIZE, SQR_SIZE, SQR_SIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = (100, 0, 100) if row % 2 == 0 else (255, 200, 200)
                    text = self.font.render(str(8-row), 1, color)
                    text_pos = (5, 5 + row * SQR_SIZE)
                    surface.blit(text, text_pos)

                if row == 7:
                    color = (100, 0, 100) if (row + col) % 2 == 0 else (255, 200, 200)
                    text = self.font.render(Square.get_aplah_col(col), 1, color)
                    text_pos = (col * SQR_SIZE + SQR_SIZE - 20, SCREEN_HEIGHT - 20)
                    surface.blit(text, text_pos)

    def show_pieces(self, surface):
        for row in range(BOARD_DIMENSIONS):
            for col in range(BOARD_DIMENSIONS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces excepted dragged piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.img)
                        img_center = (
                            col * SQR_SIZE + SQR_SIZE // 2,
                            row * SQR_SIZE + SQR_SIZE // 2
                        )
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def check_swap_turns(self):
        initial_pos = (self.dragger.initial_row, self.dragger.initial_col)  # position where piece was taken
        curr_pos = (self.dragger.y // SQR_SIZE, self.dragger.x // SQR_SIZE)  # newest mouse position

        if initial_pos != curr_pos:
            self.whites_turn = not self.whites_turn

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = (130, 90, 255) if piece.color == "white" else (255, 90, 50)
                circle = (
                    (move.final.col * SQR_SIZE) + (SQR_SIZE * 0.5),
                    (move.final.row * SQR_SIZE) + (SQR_SIZE * 0.5),
                )
                pygame.draw.circle(surface, color, circle, (SQR_SIZE / 2) * 0.4)
    
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (100, 100, 0) if pos == initial else (155, 155, 0)
                rect = (pos.col * SQR_SIZE, pos.row * SQR_SIZE, SQR_SIZE, SQR_SIZE)
                pygame.draw.rect(surface, color, rect)
    
    def check_winner(self, color, surface):
        found = False
        for row in range(BOARD_DIMENSIONS):
            for col in range(BOARD_DIMENSIONS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.name == "king" and piece.color != color:
                        found = True
                        break
        if not found:
            sound = pygame.mixer.Sound("assets/sounds/win.wav")
            sound.set_volume(0.5)
            sound.play()
            self.show_winner(color, surface)
            print()
    
    def show_winner(self, color, surface):
        winner_text = None
        if color == "white":
            winner_text = self.font.render("White wins!", 1, (0, 0, 0), (255, 255, 255))
        else:
            winner_text = self.font.render("Black wins!", 1, (255, 255, 255), (0, 0, 0))

        winner_text = pygame.transform.scale(winner_text, (winner_text.get_width() * 4, winner_text.get_height() * 4)) # increase font size of winner 3x
        text_pos = (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2)
        surface.blit(winner_text, text_pos)

        pygame.display.flip()  # Update the display
        time.sleep(3)  # Wait for 3 seconds
        self.reset()  # Restart the game

    
    def show_hover(self, surface):
        if self.hovered_sqr:
            rect = (self.hovered_sqr.col * SQR_SIZE, self.hovered_sqr.row * SQR_SIZE, SQR_SIZE, SQR_SIZE)
            pygame.draw.rect(surface, (255, 0, 0), rect, 3)

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def reset(self):
        self.__init__()
