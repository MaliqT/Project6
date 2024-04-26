class Piece:
    def __init__(self, color):
        self.color = color # Black or Red
        self.king = False # piece is not king at first

    def make_king(self):
        self.king = True

    def is_king(self):
        return self.king

    def __str__(self):
        return "K" if self.king else self.color[0].upper()

    def __repr__(self):
        return f"Piece(color={self.color}, king={self.king})"


if __name__ == "__main__":

    # Test to see if class functions work
    black_piece = Piece("Black")
    print(black_piece)

    red_piece = Piece("Red")
    print(red_piece)

    black_piece.make_king()
    print(black_piece)

    print(black_piece.is_king())