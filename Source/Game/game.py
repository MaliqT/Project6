# game.py handles the game logic. How the pieces move and the rules of the game.

import pygame

Black = (0, 0, 0)
White = (255, 255, 255)

def print_rules(screen):
    font = pygame.font.SysFont('Arial', 16)

    rules = [
        "Checkers Rules:",
        "1. Checkers is played on an 8x8 board with alternating dark and light squares.",
        "2. Each player starts with 12 pieces, placed on the darker squares of the first three rows",
        "closest to them.",
        "3. Pieces can only move diagonally along the corresponding colored square, one square", ""
        "at a time.",
        "4. If a player's piece reaches the back row of the opponent, their piece becomes a king piece.",
        "5. A king piece gains the ability to move diagonally backwards. Essentially, it can move",
        "in any direction.",
        "6. A player must 'Capture' every piece of their opponent in order to win.",
        "7. In order to capture a piece, a player must move their piece over their opponents piece",
        "so long as there is an empty square space on the other side.",
        "8. A player may also capture multiple pieces in one turn, ONLY IF, the player has captured",
        "a single piece first AND an opponents piece is adjacent from the new position of the current",
        "piece AND if that opposing piece has an empty square space on the other side. If the piece",
        "is not a king piece, then the piece can only move forward. If the piece is a king piece, then",
        "it can move forward and back to capture multiple pieces."]

    # Initial position of text displayed on screen
    y_position = 50

    for line in rules:
        text_surface = font.render(line, True, Black)
        screen.blit(text_surface, (50, y_position))
        y_position += 30
