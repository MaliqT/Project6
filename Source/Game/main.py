import pygame as py
from sys import exit

from board import Game_State
from game import print_rules
BOARD_SIZE = 8
SQUARE_SIZE = 75


def main():
    py.init()
    screen = py.display.set_mode((800, 600))
    py.display.set_caption('Checkers ~AI')
    font = py.font.SysFont('Arial', 20)
    clock = py.time.Clock()
    game_state = Game_State()
    board = game_state.board
    display_surface = py.Surface((600, 600))
    run = True
    vs_ai = vs_player = show_rules = hint = False
    #  py.draw.rect(screen, py.Color('brown'), (40, 40, 500, 500), 10)  # creates board border

    selected_sq = ()  # clicked square
    user_clicks = []  # both clicked squares

    player_button = py.Rect(320, 160, 170, 35)
    ai_button = py.Rect(310, 220, 190, 35)
    rules_button = py.Rect(340, 360, 130, 35)
    back_button = py.Rect(650, 40, 100, 35)
    exit_button = py.Rect(353, 400, 100, 35)
    quit_button = py.Rect(650, 40, 100, 35)
    hint_button = py.Rect(650, 80, 100, 35)

    player_text = font.render('player vs. player', True, py.Color('white'))
    ai_text = font.render('player vs. computer', True, py.Color('white'))
    rules_text = font.render('show rules', True, py.Color('white'))
    back_text = font.render('back', True, py.Color('white'))
    exit_text = font.render('exit', True, py.Color('white'))
    quit_text = font.render('quit', True, py.Color('white'))
    hint_text = font.render('hint', True, py.Color('white'))

    player_text_center = player_text.get_rect(center=player_button.center)
    ai_text_center = ai_text.get_rect(center=ai_button.center)
    rules_text_center = rules_text.get_rect(center=rules_button.center)
    back_text_center = back_text.get_rect(center=back_button.center)
    exit_text_center = exit_text.get_rect(center=exit_button.center)
    quit_text_center = quit_text.get_rect(center=quit_button.center)
    hint_text_center = hint_text.get_rect(center=hint_button.center)

    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.MOUSEBUTTONDOWN:  # board click caught
                local = py.mouse.get_pos()

                if not vs_player and not vs_ai:
                    if player_button.collidepoint(local):
                        vs_player = True
                    if ai_button.collidepoint(local):
                        vs_ai = True
                    if rules_button.collidepoint(local):
                        show_rules = True
                    if back_button.collidepoint(local):
                        show_rules = False
                    if exit_button.collidepoint(local):
                        run = False
                elif local[0] > 600:
                    if quit_button.collidepoint(local):
                        vs_player = vs_ai = False
                        game_state = Game_State()
                        board = game_state.board

                    if hint_button.collidepoint(local):  # show hint
                        hint = not hint

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
                            hint = False
                            move = game_state.move(game_state.board, user_clicks[0], user_clicks[1])

                        # checking if piece being captured is not your own
                        elif (sq2 == 'wt' and game_state.black_turn) or (sq2 == 'bk' and not game_state.black_turn):
                            hint = False
                            move = game_state.move(game_state.board, user_clicks[0], user_clicks[1])

                        selected_sq = ()
                        user_clicks = []

        if show_rules:  # rules screen
            screen.fill('bisque2')
            py.draw.rect(screen, py.Color('gray45'), back_button)
            screen.blit(back_text, back_text_center)

            print_rules(screen)
        elif vs_player or vs_ai:  # game screen
            game_state.create_hint(display_surface, board) if hint else game_state.draw_board(display_surface, board)
            screen.blit(display_surface, (0, 0))

            py.draw.rect(screen, py.Color('gray45'), quit_button)
            screen.blit(quit_text, quit_text_center)

            py.draw.rect(screen, py.Color('gray45'), hint_button)
            screen.blit(hint_text, hint_text_center)
        else:  # start screen
            screen.fill('bisque2')
            py.draw.rect(screen, py.Color('gray45'), player_button)
            screen.blit(player_text, player_text_center)

            py.draw.rect(screen, py.Color('gray45'), ai_button)
            screen.blit(ai_text, ai_text_center)

            py.draw.rect(screen, py.Color('gray45'), rules_button)
            screen.blit(rules_text, rules_text_center)

            py.draw.rect(screen, py.Color('gray45'), exit_button)
            screen.blit(exit_text, exit_text_center)

        py.display.update()  # updates screen
    py.quit()
    exit()


# cant take ur own piece.
if __name__ == '__main__':
    main()
