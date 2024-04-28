import pygame as py
from piece import Piece
from Source.AI.ai import move_or_jump

BOARD_SIZE = 8
SQUARE_SIZE = 75
IMAGES = {1: py.transform.scale(py.image.load('../Constants/Images/wt.png'), (SQUARE_SIZE, SQUARE_SIZE)),
          2: py.transform.scale(py.image.load('../Constants/Images/bk.png'), (SQUARE_SIZE, SQUARE_SIZE)),
          3: py.transform.scale(py.image.load('../Constants/Images/wt.png'), (SQUARE_SIZE, SQUARE_SIZE)),
          4: py.transform.scale(py.image.load('../Constants/Images/bk.png'), (SQUARE_SIZE, SQUARE_SIZE))}

class Game_State():
    def __init__(self, ):
        self.board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]

        ]
        self.black_turn = True
        self.more_jumps = False
        self.last_piece = None
        self.turn_log = []

    def draw_hint(self, screen, board, sq1, sq2):  # assumption: sq1 and sq2 are diagonal
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if abs(sq1[0] - row) == abs(sq1[1] - col) and min(sq1[0], sq2[0]) <= row <= max(sq1[0], sq2[0]) and min(sq1[1], sq2[1]) <= col <= max(sq1[1], sq2[1]):
                    color = py.Color('lightgoldenrod1') if (row + col) % 2 == 0 else (255, 230, 0)
                elif (row + col) % 2 == 0:
                    color = py.Color('white')
                else:
                    color = py.Color('black')
                py.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != 0:
                    screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def draw_board(self, screen, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = py.Color('white') if (row + col) % 2 == 0 else py.Color('black')
                py.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != 0:
                    screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, board, sq1, sq2):
        sq1_row = sq1[0]
        sq1_col = sq1[1]
        sq2_row = sq2[0]
        sq2_col = sq2[1]

        piece = board[sq1_row][sq1_col]
        board[sq1_row][sq1_col] = 0
        piece_taken = board[sq2_row][sq2_col]
        board[sq2_row][sq2_col] = piece

        row = (sq1_row + sq2_row) // 2
        col = (sq1_col + sq2_col) // 2
        between_piece = board[row][col]

        if abs(sq1_row - sq2_row) == 2:  # jump move -- assume last piece is sq1
            if between_piece != 0:  # jump was made
                board[row][col] = 0
                self.more_jumps = self.possible_jumps(board, sq2)
                self.last_piece = (sq2_row, sq2_col)
                if not self.more_jumps:
                    self.black_turn = not self.black_turn

        else:
            if not self.more_jumps:
                self.black_turn = not self.black_turn
        # else ???
        # print(move_or_jump(Piece((sq1_row, sq1_col), 'king' if piece > 2 else 'pawn', 'black' if piece % 2 == 0 else 'white'), board))
        # print(move_or_jump(Piece((sq1_col, sq1_row), 'king' if piece > 2 else 'pawn', 'black' if piece % 2 == 0 else 'white'), board))


    def possible_jumps(self, board, sq1):
        piece = board[sq1[0]][sq1[1]]
        row = sq1[0]
        col = sq1[1]
        up = row - 2
        down = row + 2
        right = col + 2
        left = col - 2

        if self.black_turn:
            if self.is_white(board[row - 1][col + 1]) and self.within_bounds(up, right): # moving up on board
                if board[row - 2][col + 2] == 0:
                    return True
            if self.is_white(board[row - 1][col - 1]) and self.within_bounds(up, left):
                if board[row - 2][col - 2] == 0:
                    return True
            if piece == 4:  # black king
                if self.is_white(board[row + 1][col + 1]) and self.within_bounds(down, right): # moving down on board
                    if board[row + 2][col + 2] == 0:
                        return True
                if self.is_white(board[row + 1][col - 1]) and self.within_bounds(down, left):
                    if board[row + 2][col - 2] == 0:
                        return True

        else:
            if self.is_black(board[row + 1][col + 1]) and self.within_bounds(down, right):
                if board[row + 2][col + 2] == 0:
                    return True
            if self.is_black(board[row + 1][col - 1]) and self.within_bounds(down, left):
                if board[row + 2][col - 2] == 0:
                    return True

            if piece == 3:  # white king
                if self.is_black(board[row - 1][col + 1]) and self.within_bounds(up, right):
                    if board[row - 2][col + 2] == 0:
                        return True
                if self.is_black(board[row - 1][col - 1]) and self.within_bounds(up, left):
                    if board[row - 2][col - 2] == 0:
                        return True
        return False

    def is_black(self, piece):
        return True if piece != 0 and (piece == 2 or piece == 4) else False

    def is_white(self, piece):
        return True if piece % 2 != 0 else False

    def within_bounds(self, row, col):
        return True if 0 <= row <= 7 and 0 <= col <= 7 else False

    def count_pieces(self, board):
        pieces = {1: 0, 2: 0, 3: 0, 4: 0}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != 0:
                    pieces[board[row][col]] += 1

        return pieces


    def create_hint(self, screen, board):
        sq1 = ()
        sq2 = ()

        
        self.draw_hint(screen, board, sq1, sq2)