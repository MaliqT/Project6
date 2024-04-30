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
    gs = Game_State()
    board = gs.board
    display_surface = py.Surface((600, 600))
    start_screen = run = True
    turn_screen = rules_screen = game_screen = hint = False

    selected_sq = ()  # clicked square
    user_clicks = []  # both clicked squares

    player_button = py.Rect(320, 160, 170, 35)
    ai_button = py.Rect(310, 220, 190, 35)
    rules_button = py.Rect(340, 360, 130, 35)
    back_button = py.Rect(650, 40, 100, 35)
    exit_button = py.Rect(353, 400, 100, 35)
    quit_button = py.Rect(650, 40, 100, 35)
    hint_button = py.Rect(650, 80, 100, 35)
    first_button = py.Rect(340, 320, 130, 35)
    second_button = py.Rect(340, 360, 130, 35)

    player_text = font.render('player vs. player', True, py.Color('white'))
    ai_text = font.render('player vs. computer', True, py.Color('white'))
    rules_text = font.render('show rules', True, py.Color('white'))
    back_text = font.render('back', True, py.Color('white'))
    exit_text = font.render('exit', True, py.Color('white'))
    quit_text = font.render('quit', True, py.Color('white'))
    hint_text = font.render('hint', True, py.Color('white'))
    first_text = font.render('go first?', True, py.Color('white'))
    second_text = font.render('go second?', True, py.Color('white'))

    player_text_center = player_text.get_rect(center=player_button.center)
    ai_text_center = ai_text.get_rect(center=ai_button.center)
    rules_text_center = rules_text.get_rect(center=rules_button.center)
    back_text_center = back_text.get_rect(center=back_button.center)
    exit_text_center = exit_text.get_rect(center=exit_button.center)
    quit_text_center = quit_text.get_rect(center=quit_button.center)
    hint_text_center = hint_text.get_rect(center=hint_button.center)
    first_text_center = first_text.get_rect(center=first_button.center)
    second_text_center = second_text.get_rect(center=second_button.center)

    for i in board:
        print(i)

    while run:

        for event in py.event.get():
            #  if chose_turn: #  AI MAKES MOVE HERE
            #  pass if game-state is first
            if event.type == py.QUIT:
                run = False
            elif event.type == py.MOUSEBUTTONDOWN:  # board click caught
                local = py.mouse.get_pos()

                # change to different screen names: screen 1 has basic buttons
                # screen 1 - start screen
                # screen 2 - first or second
                # screen 3 - rules
                # screen 4 - game
                if start_screen:
                    if player_button.collidepoint(local):
                        game_screen = True
                        start_screen = gs.vs_ai = False
                    if ai_button.collidepoint(local):
                        turn_screen = gs.vs_ai = True
                        start_screen = False
                    if rules_button.collidepoint(local):
                        rules_screen = True
                        start_screen = False
                    if exit_button.collidepoint(local):
                        run = False
                elif turn_screen:
                    if first_button.collidepoint(local):
                        gs.players_turn = game_screen = True
                        turn_screen = False
                    elif second_button.collidepoint(local):
                        gs.players_turn = turn_screen = False
                        game_screen = True
                elif rules_screen:
                    if back_button.collidepoint(local):
                        rules_screen = False
                        start_screen = True
                elif game_screen and local[0] > 600:
                    if quit_button.collidepoint(local):
                        game_screen = False
                        start_screen = True
                        selected_sq = ()
                        user_clicks = []
                        gs = Game_State()
                        board = gs.board

                    if hint_button.collidepoint(local):  # show hint
                        hint = not hint
                elif game_screen:
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
                        if sq1 == 0:  # sq is empty
                            selected_sq = ()
                            user_clicks = []

                        # clicked on wrong piece OR not your turn
                        elif (sq1 % 2 != 0 and gs.black_turn) or (sq1 % 2 == 0 and not gs.black_turn):
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

                        if (gs.black_turn and (row > sq1_row)) or (
                                not gs.black_turn and (sq1_row > row)):
                            print("Invalid move! A regular piece cannot move backwards.")
                        elif abs(sq1_row - row) != abs(sq1_col - col):
                            print("Invalid move! A piece can only move diagonally.")
                        elif gs.more_jumps and user_clicks[0] != gs.last_piece:
                            print("Invalid move! Must complete another jump.")
                        else:

                            if sq2 == 0 and (1 <= abs(sq1_row - row) <= 2) and (
                                    1 <= abs(sq1_col - col) <= 2):  # second sq is empty - moving piece to empty tile
                                # First check if we're capturing a piece or not

                                if abs(sq1_row - row) == 2:
                                    # Attempting to capture a piece. Check for piece
                                    if (((row + 1) and (col - 1)) != 0) or (((row + 1) and (col + 1)) != 0) or (
                                            ((row - 1) and (col - 1)) != 0) or (((row - 1) and (col + 1)) != 0):
                                        print("There is a piece here. Captured it.")
                                        hint = False
                                        move = gs.move(gs.board, user_clicks[0], user_clicks[1])
                                        if gs.vs_ai:  # game + vs ai + not first make players_turn = false when turn is done
                                            gs.players_turn = not gs.players_turn
                                else:
                                    hint = False
                                    move = gs.move(gs.board, user_clicks[0], user_clicks[1])
                                    if gs.vs_ai:  # game + vs ai + not first make players_turn = false when turn is done
                                        gs.players_turn = not gs.players_turn

                            else:  # A piece is there and space is not empty
                                print("Invalid space. A piece is there.")
                                # The player would need to capture the piece if possible

                        selected_sq = ()
                        user_clicks = []
                        for i in board:
                            print(i)
                        if gs.black_turn:
                            print("Black's Turn")
                        else:
                            print("White's Turn")


        # screen 1 - start screen
        # screen 2 - first or second
        # screen 3 - rules
        # screen 5 - game

        if not gs.players_turn:  # ai makes move here
            pass
        if start_screen:
            screen.fill('bisque2')
            py.draw.rect(screen, py.Color('gray45'), player_button)
            screen.blit(player_text, player_text_center)

            py.draw.rect(screen, py.Color('gray45'), ai_button)
            screen.blit(ai_text, ai_text_center)

            py.draw.rect(screen, py.Color('gray45'), rules_button)
            screen.blit(rules_text, rules_text_center)

            py.draw.rect(screen, py.Color('gray45'), exit_button)
            screen.blit(exit_text, exit_text_center)
        elif turn_screen:
            screen.fill('bisque2')
            py.draw.rect(screen, py.Color('gray45'), first_button)
            screen.blit(first_text, first_text_center)

            py.draw.rect(screen, py.Color('gray45'), second_button)
            screen.blit(second_text, second_text_center)
        if rules_screen:  # rules screen
            screen.fill('bisque2')
            py.draw.rect(screen, py.Color('gray45'), back_button)
            screen.blit(back_text, back_text_center)

            print_rules(screen)
        elif game_screen:
            gs.create_hint(display_surface, board) if hint else gs.draw_board(display_surface, board)
            screen.blit(display_surface, (0, 0))

            py.draw.rect(screen, py.Color('gray45'), quit_button)
            screen.blit(quit_text, quit_text_center)

            py.draw.rect(screen, py.Color('gray45'), hint_button)
            screen.blit(hint_text, hint_text_center)

        py.display.update()  # updates screen
    py.quit()
    exit()


# cant take ur own piece.
if __name__ == '__main__':
    main()
