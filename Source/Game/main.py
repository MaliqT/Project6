import pygame as py
from sys import exit

from board import Game_State

BOARD_SIZE = 8
SQUARE_SIZE = 75


def main():
    py.init()
    screen = py.display.set_mode((600, 600))
    py.display.set_caption('Checkers ~AI')
    clock = py.time.Clock()
    game_state = Game_State()
    board = game_state.board
    display_surface = py.Surface((600, 600))
    screen.fill('bisque2')

    #  py.draw.rect(screen, py.Color('brown'), (40, 40, 500, 500), 10)  # creates board border

    selected_sq = ()  # clicked square
    user_clicks = []  # both clicked squares
    
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                local = py.mouse.get_pos()
                col = local[0] // SQUARE_SIZE
                row = local[1] // SQUARE_SIZE

                if selected_sq == (row, col):  # clicked square twice OR not own piece OR
                    selected_sq = ()
                    user_clicks = []
                else:
                    selected_sq = (row, col)
                    user_clicks.append(selected_sq)

                if len(user_clicks) == 2:
                    if board[user_clicks[0][0]][user_clicks[0][1]] == '-': # first clicked sq
                        selected_sq = ()
                        user_clicks = []


                    else:
                        move = game_state.move(game_state.board, user_clicks[0], user_clicks[1])
                        selected_sq = ()
                        user_clicks = []



        game_state.draw_board(display_surface, board)
        screen.blit(display_surface, (0, 0))
        py.display.update()  # updates screen
        clock.tick(60)


if __name__ == '__main__':
    main()
