import pygame as py

BOARD_SIZE = 8
SQUARE_SIZE = 75
class Game_State():
    def __init__(self):
        self.board = [
            ['-', 'bk', '-', 'bk', '-', 'bk', '-', 'bk'],
            ['bk', '-', 'bk', '-', 'bk', '-', 'bk', '-'],
            ['-', 'bk', '-', 'bk', '-', 'bk', '-', 'bk'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wt', '-', 'wt', '-', 'wt', '-', 'wt', '-'],
            ['-', 'wt', '-', 'wt', '-', 'wt', '-', 'wt'],
            ['wt', '-', 'wt', '-', 'wt', '-', 'wt', '-']
        ]
        self.your_turn = True
        self.turn_log = []
    def draw_board(self, screen, board):
        IMAGES = {}
        IMAGES['wt'] = py.transform.scale(py.image.load('../Constants/Images/wt.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES['bk'] = py.transform.scale(py.image.load('../Constants/Images/bk.png'), (SQUARE_SIZE, SQUARE_SIZE))

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = py.Color('white') if (row + col) % 2 == 0 else py.Color('black')
                py.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != '-':
                    screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, board, sq1, sq2):
        sq1_row = sq1[0]
        sq1_col = sq1[1]
        sq2_row = sq2[0]
        sq2_col = sq2[1]

        piece = board[sq1_row][sq1_col]
        board[sq1_row][sq1_col] = '-'
        piece_taken = board[sq2_row][sq2_col]
        board[sq2_row][sq2_col] = piece

        self.your_turn = not self.your_turn
