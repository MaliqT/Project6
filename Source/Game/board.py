import pygame as py
import copy

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
        self.board = [[0, 1, 0, 0, 0, 1, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0],
[0, 1, 0, 1, 0, 0, 0, 1],
[0, 0, 0, 0, 1, 0, 1, 0],
[0, 2, 0, 2, 0, 2, 0, 0],
[2, 0, 0, 0, 0, 0, 2, 0],
[0, 0, 0, 2, 0, 2, 0, 2],
[2, 0, 2, 0, 2, 0, 2, 0]]

        # [
        #     [0, 1, 0, 1, 0, 1, 0, 1],
        #     [1, 0, 1, 0, 1, 0, 1, 0],
        #     [0, 1, 0, 1, 0, 1, 0, 1],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [2, 0, 2, 0, 2, 0, 2, 0],
        #     [0, 2, 0, 2, 0, 2, 0, 2],
        #     [2, 0, 2, 0, 2, 0, 2, 0]
        #
        # ]
        self.black_turn = True
        self.vs_ai = False
        self.players_turn = self.is_first = False
        self.more_jumps = False
        self.last_piece = None
        self.hint_board = set()
        self.ideal_piece = self.ideal_move = None
        self.turn_log = []

    def draw_board(self, screen, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = py.Color('white') if (row + col) % 2 == 0 else py.Color('black')
                py.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != 0:
                    screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, board, sq1, sq2, maximizing_player, real_move):
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
                self.more_jumps = self.can_jump(board, sq2)
                self.last_piece = (sq2_row, sq2_col)
                if board[sq2_row][sq2_col] <= 2 and ((maximizing_player and sq2_row == 0) or (not maximizing_player and sq2_row == 7)):
                    board[sq2_row][sq2_col] += 2
                if not self.more_jumps and real_move:
                    self.black_turn = not self.black_turn

        else:
            if board[sq2_row][sq2_col] <= 2 and ((maximizing_player and sq2_row == 0) or (not maximizing_player and sq2_row == 7)):
                board[sq2_row][sq2_col] += 2

            if not self.more_jumps and real_move:
                self.black_turn = not self.black_turn
        # else ???
        # print(move_or_jump(Piece((sq1_row, sq1_col), 'king' if piece > 2 else 'pawn', 'black' if piece % 2 == 0 else 'white'), board))
        # print(move_or_jump(Piece((sq1_col, sq1_row), 'king' if piece > 2 else 'pawn', 'black' if piece % 2 == 0 else 'white'), board))

    def can_jump(self, board, sq1):
        piece = board[sq1[0]][sq1[1]]
        row = sq1[0]
        col = sq1[1]
        up = row - 2
        down = row + 2
        right = col + 2
        left = col - 2

        if self.black_turn:
            if self.within_bounds(up, right) and self.is_white(board[row - 1][col + 1]):  # moving up on board
                if board[up][right] == 0:
                    return True
            if self.within_bounds(up, left) and self.is_white(board[row - 1][col - 1]):
                if board[up][left] == 0:
                    return True
            if piece == 4:  # black king
                if self.within_bounds(down, right) and self.is_white(board[row + 1][col + 1]):  # moving down on board
                    if board[down][right] == 0:
                        return True
                if self.within_bounds(down, left) and self.is_white(board[row + 1][col - 1]):
                    if board[down][left] == 0:
                        return True

        else:
            if self.within_bounds(down, right) and self.is_black(board[row + 1][col + 1]):
                if board[down][right] == 0:
                    return True
            if self.within_bounds(down, left) and self.is_black(board[row + 1][col - 1]):
                if board[down][left] == 0:
                    return True

            if piece == 3:  # white king
                if self.within_bounds(up, right) and self.is_black(board[row - 1][col + 1]):
                    if board[up][right] == 0:
                        return True
                if self.within_bounds(up, left) and self.is_black(board[row - 1][col - 1]):
                    if board[up][left] == 0:
                        return True
        return False

    def possible_jumps(self, board, sq1, extra, maximizing_player):

        piece = board[sq1[0]][sq1[1]]
        row = sq1[0]
        col = sq1[1]
        up = row - 2
        down = row + 2
        right = col + 2
        left = col - 2
        possible_places = []


        if maximizing_player:
            if self.within_bounds(up, right) and self.is_white(board[row - 1][col + 1]):  # moving up on board
                if board[up][right] == 0:
                    jumps = self.possible_jumps(board, (up, right), True, maximizing_player)
                    if jumps:
                        for jump in jumps:
                            possible_places.append([(up, right)])
                            possible_places[-1].extend(jump)
                    else:
                        possible_places.append([(up, right)])
            if self.within_bounds(up, left) and self.is_white(board[row - 1][col - 1]):
                if board[up][left] == 0:
                    jumps = self.possible_jumps(board, (up, left), True, maximizing_player)
                    if jumps:
                        for jump in jumps:
                            possible_places.append([(up, left)])
                            possible_places[-1].extend(jump)
                    else:
                        possible_places.append([(up, left)])

            if piece == 4:  # black king
                if self.within_bounds(down, right) and self.is_white(board[row + 1][col + 1]):  # moving down on board
                    if board[down][right] == 0:
                        jumps = self.possible_jumps(board, (down, right), True, maximizing_player)
                        if jumps:
                            for jump in jumps:
                                possible_places.append([(down, right)])
                                possible_places[-1].extend(jump)
                        else:
                            possible_places.append([(down, right)])
                if self.within_bounds(down, left) and self.is_white(board[row + 1][col - 1]):
                    if board[down][left] == 0:
                        jumps = self.possible_jumps(board, (down, left), True, maximizing_player)
                        if jumps:
                            for jump in jumps:
                                possible_places.append([(down, left)])
                                possible_places[-1].extend(jump)
                        else:
                            possible_places.append([(down, left)])
        else:
            if self.within_bounds(down, right) and self.is_black(board[row + 1][col + 1]):
                if board[down][right] == 0:
                    jumps = self.possible_jumps(board, (down, right), True, maximizing_player)
                    if jumps:
                        for jump in jumps:
                            possible_places.append([(down, right)])
                            possible_places[-1].extend(jump)
                    else:
                        possible_places.append([(down, right)])
            if self.within_bounds(down, left) and self.is_black(board[row + 1][col - 1]):
                if board[down][left] == 0:
                    jumps = self.possible_jumps(board, (down, left), True, maximizing_player)
                    if jumps:
                        for jump in jumps:
                            possible_places.append([(down, left)])
                            possible_places[-1].extend(jump)
                    else:
                        possible_places.append([(down, left)])

            if piece == 3:  # white king
                if self.within_bounds(up, right) and self.is_black(board[row - 1][col + 1]):
                    if board[up][right] == 0:
                        jumps = self.possible_jumps(board, (up, right), True, maximizing_player)
                        if jumps:
                            for jump in jumps:
                                possible_places.append([(up, right)])
                                possible_places[-1].extend(jump)
                        else:
                            possible_places.append([(up, right)])
                if self.within_bounds(up, left) and self.is_black(board[row - 1][col - 1]):
                    if board[up][left] == 0:
                        jumps = self.possible_jumps(board, (up, left), True, maximizing_player)
                        if jumps:
                            for jump in jumps:
                                possible_places.append([(up, left)])
                                possible_places[-1].extend(jump)
                        else:
                            possible_places.append([(up, left)])


        return possible_places

    def possible_moves(self, board, sq1, maximizing_player):

        piece = board[sq1[0]][sq1[1]]
        row = sq1[0]
        col = sq1[1]
        up = row - 1
        down = row + 1
        right = col + 1
        left = col - 1
        possible_places = []

        if maximizing_player:
            if self.within_bounds(up, right) and board[up][right] == 0:  # moving up on board
                possible_places.append([(up, right)])
            if self.within_bounds(up, left) and board[up][left] == 0:
                possible_places.append([(up, left)])
            if piece == 4:  # black king
                if self.within_bounds(down, right) and board[down][right] == 0:  # moving down on board
                    possible_places.append([(down, right)])
                if self.within_bounds(down, left) and board[down][left] == 0:
                    possible_places.append([(down, left)])

        else:
            if self.within_bounds(down, right) and board[down][right] == 0:
                possible_places.append([(down, right)])
            if self.within_bounds(down, left) and board[down][left] == 0:
                possible_places.append([(down, left)])
            if piece == 3:  # white king
                if self.within_bounds(up, right) and board[up][right] == 0:
                    possible_places.append([(up, right)])
                if self.within_bounds(up, left) and board[up][left] == 0:
                    possible_places.append([(up, left)])

        return possible_places

    def can_move(self, board, sq1):

        piece = board[sq1[0]][sq1[1]]
        row = sq1[0]
        col = sq1[1]
        up = row - 1
        down = row + 1
        right = col + 1
        left = col - 1

        if self.black_turn:
            if self.within_bounds(up, right) and board[up][right] == 0:  # moving up on board
                return True
            if self.within_bounds(up, left) and board[up][right] == 0:
                return True
            if piece == 4:  # black king
                if self.within_bounds(down, right) and board[up][right] == 0:  # moving down on board
                    return True
                if self.within_bounds(down, left) and board[up][right] == 0:
                    return True

        else:
            if self.within_bounds(down, right) and board[up][right] == 0:
                return True
            if self.within_bounds(down, left) and board[up][right] == 0:
                if board[down][left] == 0:
                    return True

            if piece == 3:  # white king
                if self.within_bounds(up, right) and board[up][right] == 0:
                    return True
                if self.within_bounds(up, left) and board[up][right] == 0:
                    return True

        return False

    def is_black(self, piece):
        return True if piece != 0 and (piece == 2 or piece == 4) else False

    def is_white(self, piece):
        return True if piece % 2 != 0 else False

    def is_black_king(self, row):
        return True if row == 0 else False

    def is_white_king(self, row):
        return True if row == 7 else False

    def within_bounds(self, row, col):
        return True if 0 <= row <= 7 and 0 <= col <= 7 else False

    def find_possible_moves(self, board, maximizing_player):
        possible_moves = {}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != 0:
                    if maximizing_player and self.is_black(board[row][col]):
                        jumps = self.possible_jumps(board, (row, col), False, maximizing_player)
                        print(jumps)
                        all_jumps = []
                        for jump in jumps:
                            if jump: all_jumps.append(jump)

                        moves = self.possible_moves(board, (row, col), maximizing_player)
                        if len(jumps + moves) != 0:
                            possible_moves[(row, col)] = all_jumps + moves

                    elif not maximizing_player and self.is_white(board[row][col]):
                        jumps = self.possible_jumps(board, (row, col), False, maximizing_player)
                        all_jumps = []
                        for jump in jumps:
                            if jump: all_jumps.append(jump)
                        moves = self.possible_moves(board, (row, col), maximizing_player)
                        if len(jumps + moves) != 0:
                            possible_moves[(row, col)] = all_jumps + moves

        return possible_moves

    def count_pieces(self, board):
        pieces = {1: 0, 2: 0, 3: 0, 4: 0}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != 0:
                    pieces[board[row][col]] += 1

        return pieces

    # def find_captured_pieces(self, board):
    #     possible_moves = self.find_possible_moves(board)
    #     ideal_piece = None
    #     ideal_move = []
    #     ideal_score = float('-inf')
    #
    #
    #     for movable_piece in possible_moves:  # piece
    #         for possible_move in possible_moves[movable_piece]:  # moves
    #             gs = Game_State()
    #             gs.board = copy.deepcopy(board)
    #             sq1 = movable_piece
    #             for possible_sq in possible_move: # single move
    #                 gs.move(gs.board, sq1, possible_sq)
    #                 sq1 = possible_sq
    #
    #             count = self.count_pieces(gs.board)
    #             black_score = count[2] + count[4]
    #             white_score = count[1] + count[3]
    #
    #             if self.black_turn:
    #                 score = black_score - white_score
    #             else:
    #                 score = white_score - black_score
    #
    #             if score > ideal_score:
    #                 ideal_score = score
    #                 ideal_piece = movable_piece
    #                 ideal_move = possible_move
    #     return ideal_score

    def possible_boards(self, board, maximizing_player):
        possible_moves = self.find_possible_moves(board, maximizing_player)
        all_possible_boards = []

        for movable_piece in possible_moves:  # piece
            for possible_move in possible_moves[movable_piece]:  # moves
                gs = Game_State()
                gs.board = copy.deepcopy(board)
                sq1 = movable_piece
                for possible_sq in possible_move: # single move
                    gs.move(gs.board, sq1, possible_sq, maximizing_player, False)
                    sq1 = possible_sq

                all_possible_boards.append((movable_piece, possible_move, gs.board))


        return all_possible_boards

    def get_score(self, board, maximizing_player):

        count = self.count_pieces(board)
        black_score = count[2] + (2 * count[4])
        white_score = count[1] + (2 * count[3])

        if maximizing_player:
            score = black_score - white_score
        else:
            score = white_score - black_score

        return score

    def heuristic_value(self, board, maximizing_player):

        value = self.get_score(board, maximizing_player)
        return value

    def alphabeta(self, node, depth, alpha, beta, maximizing_player):  # initial call: alphabeta(curr_state, depth, −inf, inf, True)

        if depth == 0 or not self.find_possible_moves(node, maximizing_player):
            return self.heuristic_value(node, maximizing_player), None, None  # the heuristic value of node

        ideal_move = None
        ideal_piece = None
        if maximizing_player:
            max_value = float('-inf')
            for piece, move, possible_board in self.possible_boards(node, maximizing_player):
                value, _, _ = self.alphabeta(possible_board, depth - 1, alpha, beta, False)
                if value > max_value:
                    max_value = value
                    ideal_move = move
                    ideal_piece = piece
                alpha = max(alpha, max_value)
                if max_value >= beta:
                    break
            return max_value, ideal_piece, ideal_move
        else:
            max_value = float('inf')
            for piece, move, possible_board in self.possible_boards(node, maximizing_player):
                value, _, _ = self.alphabeta(possible_board, depth - 1, alpha, beta, True)
                if value < max_value:
                    max_value = value
                    ideal_move = move
                    ideal_piece = piece

                beta = min(beta, max_value)
                if max_value <= alpha:
                    break
            return max_value, ideal_piece, ideal_move

    def create_hint(self, screen, board):

        max_value, self.ideal_piece, self.ideal_move = self.alphabeta(board, 5, float('-inf'), float('inf'), self.black_turn)

    def ai_move(self, board):

        max_value, ideal_piece, ideal_move = self.alphabeta(board, 5, float('-inf'), float('inf'), self.black_turn)
        print(ideal_move)
        sq1 = ideal_piece
        for possible_sq in ideal_move:  # single move
            self.move(board, sq1, possible_sq, self.black_turn, True)
            sq1 = possible_sq


    def pre_draw_hint(self, screen, board):
        sq1 = self.ideal_piece
        for sq2 in self.ideal_move:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if abs(sq1[0] - row) == abs(sq1[1] - col) and \
                            min(sq1[0], sq2[0]) <= row <= max(sq1[0], sq2[0]) and \
                            min(sq1[1], sq2[1]) <= col <= max(sq1[1], sq2[1]):
                        self.hint_board.add((row, col))
            sq1 = sq2


    def draw_hint(self, screen, board):  # assumption: sq1 and sq2 are diagonal
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row, col) in self.hint_board:
                    color = (255, 230, 0)
                elif (row + col) % 2 == 0:
                    color = py.Color('white')
                else:
                    color = py.Color('black')
                py.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != 0:
                    screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

