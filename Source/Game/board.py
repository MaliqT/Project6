# Creates the board as text. Could be used to implement a board in UI instead.

class Board:
    def __init__(self):
        self.board_size = 8
        self.board = [[0] * self.board_size for _ in range(self.board_size)]

    def print_board(self):
        for row in self.board:
            print(row)

    def initialize_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = 'B'
                    elif row > 4:
                        self.board[row][col] = 'R'


    def display_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:
                    # spaces not available to move to
                    print("# ", end="")
                else:
                    if self.board[row][col] == 'B':
                        print("B ", end="")
                    elif self.board[row][col] == 'R':
                        print("R ", end="")
                    else:
                        # empty square spaces available to move to
                        print(". ", end="")
            print()

if __name__ == "__main__":
    board = Board()
    board.initialize_pieces()
    board.print_board()
    print()
    board.display_board()