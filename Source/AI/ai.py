
from Source.Game.piece import *


board = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]

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
        if board[x][y] == 2:
            piece = Piece((y, x), "pawn", "black")
        elif board[x][y] == 1:
            piece = Piece((y, x), "pawn", "white")
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
    if piece.type == "pawn":
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

# given a piece finds returns the list of valid moves of the piece
def move_or_jump(piece, board):
    moves = find_possible_moves(piece)
    valid_moves = []
    for move in (moves):

        if valid_move(move, board):
            if piece.color == 2 or piece.color == 4:  # if piece.color == "black":
                # print(board[move[1]][move[0]])
                if board[move[1]][move[0]] == 1 or board[move[1]][move[0]] == 3:  # if board[move[1]][move[0]] == "wt":
                    x, y = move[0] - piece.pos[0], move[1] - piece.pos[1]
                    if valid_move((move[0] + x, move[1] + y), board) and board[move[1] + y][move[0] + x] == "-":
                        m = Move((move[0] + x, move[1] + y))
                        m.is_jump()
                        valid_moves = [m]
                        break
            if piece.color == 1 or piece.color == 3:  # if piece.color == "white":
                if board[move[1]][move[0]] == 2 or board[move[1]][move[0]] == 4:  # if board[move[1]][move[0]] == "bk":
                    x, y = move[0] - piece.pos[0], move[1] - piece.pos[1]
                    if valid_move((move[0] + x, move[1] + y), board) and board[move[1] + y][move[0] + x] == 0:
                        m = Move((move[0] + x, move[1] + y))
                        m.is_jump()
                        valid_moves = [m]
                        break
            # print(board[move[1]][move[0]])
            if board[move[1]][move[0]] == 0:
                valid_moves.append(Move(move))
    return valid_moves

# given a player finds all pieces that can move, if jump avaliable finds only the pieces that can jump
def avaliable_pieces(board, player):
    # valid_pieces = []
    valid_moves = []
    jumps = []
    for piece in player.pieces:
        moves = move_or_jump(piece, board)
        if len(moves) >= 1:
            if moves[0].jump:
                jumps.append(piece)
            else:
                valid_moves.append(piece)
    if len(jumps) >= 1:
        return jumps
    return valid_moves

p1 = Player("black")
p2 = Player("white")

a = avaliable_pieces(board, p1)
a2 = avaliable_pieces(board, p2)

for piece in a:
    print(piece.pos)







