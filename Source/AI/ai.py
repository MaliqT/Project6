import copy
# from queue import PriorityQueue

from Source.Game.piece import *


board = [
    #0  1  2  3  4  5  6  7
    [0, 1, 0, 1, 0, 1, 0, 1], # 0
    [1, 0, 1, 0, 0, 0, 1, 0], # 1
    [0, 0, 0, 2, 0, 2, 0, 1], # 2
    [0, 0, 0, 0, 0, 0, 0, 0], # 3
    [0, 0, 0, 2, 0, 2, 0, 0], # 4
    [2, 0, 0, 0, 0, 0, 0, 0], # 5
    [0, 2, 0, 2, 0, 0, 0, 2], # 6
    [2, 0, 1, 0, 2, 0, 2, 0]  # 7

]

# class Piece:
#     def __init__(self, pos, type, color):
#         self.pos = pos
#         self.type = type
#         self.color = color
#
#     def make_king(self):
#         self.type = "king"

class Move:
    def __init__(self,pos):
        self.pos = pos
        self.jump = False

    def is_jump(self):
        self.jump = True

# each location is the key of the board and the values are either a piece object or none
pieces = {}
for x in range(8):
    for y in range(8):
        piece = None
        if board[x][y] == 1:
            piece = Piece((y, x), "black")
        elif board[x][y] == 2:
            piece = Piece((y, x), "white")
        pieces[(x,y)] = piece
class Move:
    def __init__(self, pos):
        self.pos = pos
        self.jump = False

    def is_jump(self):
        self.jump = True

class Player:
    def __init__(self, color):
        self.color = color
        self.total_pieces = 12
        self.moves = 7
        self.moving_pieces = 4
        self.pieces = []
        self.init_pieces()

    # stores all pieces in the list piece
    def init_pieces(self):
        for v in pieces.values():
            if v:
                if v.color == self.color:
                    self.pieces.append(v)
        return pieces

    # update after turn
    def update(self, total_pieces, moves, moving_pieces):
        self.total_pieces = total_pieces
        self.moves = moves
        self.moving_pieces = moving_pieces


# given a piece finds all possible moves
def find_possible_moves(piece):
    # moves = []
    if piece.king == False:
        if piece.color == "black":
            return ((piece.pos[0] - 1, piece.pos[1] + 1), (piece.pos[0] + 1, piece.pos[1] + 1))
        else:
            return ((piece.pos[0] - 1, piece.pos[1] - 1), (piece.pos[0] + 1, piece.pos[1] - 1))
    else:
        return ((piece.pos[0] - 1, piece.pos[1] - 1), (piece.pos[0] + 1, piece.pos[1] - 1), (piece.pos[0] - 1, piece.pos[1] + 1), (piece.pos[0] + 1, piece.pos[1] + 1))

# givem a possible move possition checks if its valid or not
def valid_move(pos, board):
    if pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8:
        return True
    return False


def jumps(move, piece, board):
    new_move = None
    x, y = move[0] - piece.pos[0], move[1] - piece.pos[1]
    if valid_move((move[0] + x, move[1] + y), board) and board[move[1] + y][move[0] + x] == 0:
        m = Move((move[0] + x, move[1] + y))
        m.is_jump()
        new_move = m
    return new_move

#  return the position of possible jumps if any
def is_jump(piece, board):
    valid_jumps = []
    j = []
    # new_board = board
    moves = find_possible_moves(piece)
    for move in moves:
        if valid_move(move, board):
            if piece.color == "black":
                if board[move[1]][move[0]] == 2:
                    jump = jumps(move, piece, board)
                    # while jump:
                    if jump:
                        valid_jumps.append(jump)
                        # jump = jumps(jump.pos, piece, board)
                        # print(jump)
    # for valid_jumps
    return valid_jumps

def make_move(selected_piece, next_pos, board):
    if selected_piece.jump:
        x, y = next_pos[0] - selected_piece.pos[0], next_pos[1] - selected_piece.pos[1]
        x, y = int(selected_piece.pos[0] + (x / 2)), int(selected_piece.pos[1] + (y / 2))
        board[y][x] = 0
    board[selected_piece.pos[1]][selected_piece.pos[0]] = 0
    selected_piece.pos = next_pos
    selected_piece.move = False
    color = 1 if selected_piece.color == "black" else 2
    board[next_pos[1]][next_pos[0]] = color


    return board

# given a piece finds returns the list of valid moves of the piece
def move_or_jump(piece, board):
    moves = find_possible_moves(piece)
    valid_moves = []
    valid_jumps = []
    jump = is_jump(piece, board)
    if jump:
        piece.jump = True
        jumps_list = []
        for j in jump:
            jumps_list = [j]
            board = make_move(piece, j.pos, board)
            new_jump = is_jump(piece, board)
            if new_jump:
                jumps_list.extend(new_jump)
            valid_jumps.extend(jumps_list)
        return valid_jumps

    for move in moves:
        if valid_move(move, board):
            if board[move[1]][move[0]] == 0:
                valid_moves.append(Move(move))

    return valid_moves
# given a player finds all pieces that can move, if jump avaliable finds only the pieces that can jump
def avaliable_pieces(board, player):
    valid_pieces = []
    valid_moves = []
    jumps = []
    for piece in player.pieces:
        b = copy.deepcopy(board)
        p = copy.deepcopy(piece)
        moves = move_or_jump(p, b)
        # print(piece.pos)
        if len(moves) >= 1:
            if moves[0].jump:
                jumps.append(piece)
                player.jump = True
            else:
                valid_moves.append(piece)
    if len(jumps) >= 1:
        return jumps
    return valid_moves

def next_move(board, player):
    pass

# finds all moves given a player
# note: player class contains a list of all class pieces
def all_posible_moves(board, player):
    all_moves = []
    jumps = []
    b1 = copy.deepcopy(board)
    units = avaliable_pieces(b1, player)

    for unit in units:
        # jumps = []
        moves = []
        u = copy.deepcopy(unit)
        b1 = copy.deepcopy(board)
        unit_moves = move_or_jump(u, b1)
        if len(unit_moves) >= 1:
            if unit_moves[0].jump:
                j = []
                unit.jump = True
                for m in unit_moves:
                    # if unit.king == False:
                    if m.pos not in j:
                        j.append(m.pos)
                    # else:
                    #     j.append(m.pos)
                jumps.append(j)
            else:
                for m in unit_moves:
                    moves.append(m.pos)
        all_moves.append(moves)
    if jumps:
        return jumps
    return all_moves

# given a piece finds returns a list of tuples (jump position, board after jump)
def find_jumps(piece, board):
    jump = is_jump(piece, board)
    if not jump:
        return []
    path = []
    # paths = []
    for next_pos in jump:
        board2 = copy.deepcopy(board)
        piece.jump = True
        if len(jump) >= 2 and jump[-2] == next_pos:
            if jump[-1].pos[0] == jump[-1].pos[0] or jump[-1].pos[1] == jump[-1].pos[1]:
                p1 = copy.deepcopy(piece)
                board2 = make_move(p1, next_pos.pos, board2)
                path.append((next_pos.pos, board2))
                path.extend(find_jumps(p1, board2))
                board2 = copy.deepcopy(board)

        else:
            board2 = make_move(piece, next_pos.pos, board2)
            path.append((next_pos.pos, board2))
            path.extend(find_jumps(piece, board2))
    return path

# returns the list of all moves or jumps board each move is a list of tuples (move or jump position, board after move or jump)
def moves_and_results(board, player):

    result = []
    player_pieces = avaliable_pieces(copy.deepcopy(board), player)

    for piece in player_pieces:
        if piece.jump == True:
            result.append(find_jumps(piece, board))
        else:
            moves = move_or_jump(piece, board)
            piece_moves = []
            for move in moves:
                new_board = make_move(copy.deepcopy(piece), move.pos, copy.deepcopy(board))
                piece_moves.append((move.pos, new_board))
            result.append(piece_moves)

    return result


p1 = Player("black")
p2 = Player("white")
p1.pieces[8].make_king()
# p1.pieces[8].jump = True

a = moves_and_results(board, p2)


# a = moves_and_results(board, p1)
# a = all_posible_moves(board, p1)
# m = move_or_jump(p1.pieces[8], board)

# c
a



