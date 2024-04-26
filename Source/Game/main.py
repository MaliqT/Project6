import pygame as py
from sys import exit

from board import Game_State

BOARD_SIZE = 8
SQUARE_SIZE = 75


def main():
    py.init()
    screen = py.display.set_mode((600, 600))
    py.display.set_caption('Checkers ~AI')
    font = py.font.SysFont('Arial', 20)
    clock = py.time.Clock()
    game_state = Game_State()
    board = game_state.board
    display_surface = py.Surface((600, 600))
    screen.fill('bisque2')
    run = True
    play = False
    #  py.draw.rect(screen, py.Color('brown'), (40, 40, 500, 500), 10)  # creates board border

    selected_sq = ()  # clicked square
    user_clicks = []  # both clicked squares

    player_button = py.Rect(220, 200, 170, 35)
    ai_button = py.Rect(210, 250, 190, 35)
    player_text = font.render('player vs. player', True, py.Color('white'))
    ai_text = font.render('player vs. computer', True, py.Color('white'))

    player_text_center = player_text.get_rect(center=player_button.center)
    ai_text_center = ai_text.get_rect(center=ai_button.center)

    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.MOUSEBUTTONDOWN:  # board click caught
                local = py.mouse.get_pos()

                if not play:
                    if player_button.collidepoint(local):
                        play = True
                else:
                    col = local[0] // SQUARE_SIZE
                    row = local[1] // SQUARE_SIZE

                    # GENERAL CLICK RULES
                    if selected_sq == (row, col):  # clicked same sq twice
                        selected_sq = ()
                        user_clicks = []

                    else:  # click is registered
                        selected_sq = (row, col)
                        user_clicks.append(selected_sq)

                    # 1st CLICK RULES (1 square clicked)
                    if len(user_clicks) == 1:
                        sq1 = board[row][col]
                        if sq1 == '-':  # sq is empty
                            selected_sq = ()
                            user_clicks = []

                        # clicked on wrong piece OR not your turn
                        elif (sq1 == 'wt' and game_state.black_turn) or (sq1 == 'bk' and not game_state.black_turn):
                            selected_sq = ()
                            user_clicks = []

                    # 2nd CLICK RULES (2 squares clicked) -- user_clicks = [(sq1), (sq2)] = [(row1, col1), (row2, col2)]
                    if len(user_clicks) == 2:
                        sq1_row = user_clicks[0][0]
                        sq1_col = user_clicks[0][1]
                        sq1 = board[sq1_row][sq1_col]
                        sq2 = board[row][col]
                        # current click is also second click, so sq2's row = row and sq2's col = col

                        # IMPLEMENT MOVE RULES HERE

                        if sq2 == '-':  # second sq is empty - moving piece to empty tile
                            move = game_state.move(game_state.board, user_clicks[0], user_clicks[1])

                        # checking if piece being captured is not your own
                        elif (sq2 == 'wt' and game_state.black_turn) or (sq2 == 'bk' and not game_state.black_turn):
                            move = game_state.move(game_state.board, user_clicks[0], user_clicks[1])

                        selected_sq = ()
                        user_clicks = []

        if play:
            game_state.draw_board(display_surface, board)
            screen.blit(display_surface, (0, 0))
        else:
            py.draw.rect(screen, py.Color('gray45'), player_button)
            screen.blit(player_text, player_text_center)

            py.draw.rect(screen, py.Color('gray45'), ai_button)
            screen.blit(ai_text, ai_text_center)

        py.display.update()  # updates screen
    py.quit()
    exit()


# cant take ur own piece.
if __name__ == '__main__':
    main()
