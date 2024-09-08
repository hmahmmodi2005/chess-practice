import pygame
import sys

from const import *
from game import Game
from square import Square

# initializes game and checks for events
class Main:

    # __init__(self) is like a constructor for the Main class
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Skibidi chekers")
        self.game = Game()

    def mainloop(self):
        # self.value => value
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            # updates dragged piece because when the mouse is still the show_background goes over the piece
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.mouse_tracker(event.pos)

                    # turns cords to section of the board from 745px,712px => 7,7 by dividing by total SQR_SIZE and rounding to INT
                    clicked_row = dragger.y // SQR_SIZE
                    clicked_col = dragger.x // SQR_SIZE

                    # Check if the place/square has a piece on it
                    square = board.squares[clicked_row][clicked_col]
                    if square.has_piece():
                        piece = square.piece  # saves piece object
                        # Check if the piece color matches the current turn
                        if (game.whites_turn and piece.color == "white") or (
                            not game.whites_turn and piece.color == "black"
                        ):
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(clicked_row, clicked_col)
                            dragger.drag_piece(piece)

                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # drag
                elif event.type == pygame.MOUSEMOTION:
                    if Square.in_range(event.pos[1] // SQR_SIZE, event.pos[0] // SQR_SIZE):
                        game.set_hover(event.pos[1] // SQR_SIZE, event.pos[0] // SQR_SIZE)

                    if dragger.dragging:
                        dragger.mouse_tracker(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.move_piece(board, game)
                        if game.check_winner(dragger.piece.color, self.screen) == False:
                            game.show_winner(dragger.piece.color, self.screen)

                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                        else:
                            dragger.undrag_piece()

                # reset
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

            pygame.display.update()


main = Main()
main.mainloop()