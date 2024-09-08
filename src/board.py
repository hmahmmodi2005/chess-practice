from const import *
from square import Square
from move import Move
from piece import *


class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(BOARD_DIMENSIONS)] # way to write a 2D array
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    # calculates all legal moves of piece
    def calc_moves(self, piece, row, col):
        piece.moves.clear()  # restart possible moves every time piece is chosen

        if isinstance(piece, Pawn):
            self.pawn_moves(piece, row, col)

        elif isinstance(piece, Knight):
            self.knight_moves(piece, row, col)

        elif isinstance(piece, Bishop):
            self.straight_line_moves([
                (-1, -1), # up-left
                (-1, 1), # up-right
                (1, -1), # down-left
                (1, 1) # down-right
            ],
            piece, row, col)

        elif isinstance(piece, Rook):
            self.straight_line_moves([
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1) # right
            ],
            piece, row, col)

        elif isinstance(piece, Queen):
            self.straight_line_moves([
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1), # right
                (-1, -1), # up-left
                (-1, 1), # up-right
                (1, -1), # down-left
                (1, 1) # down-right
            ],
            piece, row, col)

        elif isinstance(piece, King):
            self.king_moves(piece, row, col)

    def pawn_moves(self, piece, row, col):
        steps = 1 if piece.moved else 2 # if pawn moved, moves 1 step, else 2 steps

        start = row + piece.dir
        end = row + (piece.dir * (1 + steps))

        for possible_move_row in range(start, end, piece.dir):
            if Square.in_range(possible_move_row):
                if self.squares[possible_move_row][col].isempty():
                    initial = Square(row, col)
                    final = Square(possible_move_row, col)

                    move = Move(initial, final)
                    piece.add_move(move)
                # blocked by piece
                else: break
            # not in range
            else: break

        possible_move_row = row + piece.dir
        possible_move_cols = [col - 1, col + 1]

        for possible_move_col in possible_move_cols:
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)

                    move = Move(initial, final)
                    piece.add_move(move)

    def knight_moves(self, piece, row, col):
        possible_moves = [
            (row - 2, col - 1),
            (row - 2, col + 1),
            (row + 2, col - 1),
            (row + 2, col + 1),
            (row - 1, col - 2),
            (row - 1, col + 2),
            (row + 1, col - 2),
            (row + 1, col + 2),
        ]

        for possible_move in possible_moves:
            if Square.in_range(possible_move[0], possible_move[1]):
                if self.squares[possible_move[0]][possible_move[1]].isempty_or_enemy(piece.color):
                    initial = Square(row, col)
                    final = Square(possible_move[0], possible_move[1])
                    move = Move(initial, final)

                    piece.add_move(move)

    def straight_line_moves(self, incrs, piece, row, col):
        for incr in incrs:
            row_incr, col_incr = incr[0], incr[1]
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr

            while True:
                if Square.in_range(possible_move_row, possible_move_col):

                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)
                    move = Move(initial, final)

                    # continue incrementing if no empty
                    if self.squares[possible_move_row][possible_move_col].isempty():
                        piece.add_move(move)

                    # stops incrementing when hitting enemy piece
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        piece.add_move(move)
                        break
                    
                    # same as enemy rule, but doesn't allow for team piece to get captured by its own team
                    if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        break

                # not in range of board
                else: break

                # continues incrementing if not broken by piece
                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr

    def king_moves(self, piece, row, col):
        for possible_moves in [
                (row-1, col+0), # up
                (row+1, col+0), # down
                (row+0, col-1), # left
                (row+0, col+1), # right
                (row-1, col-1), # up-left
                (row-1, col+1), # up-right
                (row+1, col-1), # down-left
                (row+1, col+1) # down-right
                ]:
            possible_move_row = possible_moves[0]
            possible_move_col = possible_moves[1]
            
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)
                    move = Move(initial, final)
                    piece.add_move(move)

    def _create(self):
        for row in range(BOARD_DIMENSIONS):
            for col in range(BOARD_DIMENSIONS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # 6 is the 2nd last row on the bottom of the board, where the pawns all line up horizontally, and behind the pawns on row 7, are the "other" pieces
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # for all pawns
        for col in range(BOARD_DIMENSIONS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # for all knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # for all bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # for all rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # for queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # for kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))
