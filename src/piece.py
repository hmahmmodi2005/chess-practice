import os


class Piece:
    def __init__(self, name, color, value, img=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if self.color == "white" else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.img = img
        self.set_texture(80)
        self.texture_rect = texture_rect

    def set_texture(self, size):
        self.img = os.path.join(
            f"assets/images/imgs-{size}px/{self.color}_{self.name}.png"
        )

    def add_move(self, move):
        self.moves.append(move)


# -Children of Piece-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Pawn(Piece):
    def __init__(self, color):
        self.dir = (-1 if color == "white" else 1)  # white moves up || black goes down. note: pawns are the only pieces to move in a single direction, hence the 1 & -1
        super().__init__("pawn", color, 1.0)

    def legal_move(self):
        pass


class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 4)


class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 8.0)


class King(Piece):
    def __init__(self, color):
        super().__init__("king", color, 10.0)
