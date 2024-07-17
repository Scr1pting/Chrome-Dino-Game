import pygame
import os

from game.settings import *


def load_highscore() -> int:
    current_script_dir = os.path.dirname(__file__)

    # Highscore file for memory
    with open(
        os.path.join(current_script_dir, "../../highscore.txt"),
        "r"
    ) as f:
        try:
            return int(f.read().strip())
        except:
            return 0


def draw_score(highscore, distance):
    font = pygame.font.Font(FONT_FAMILY, 20)
    points = distance // 80
    
    if points > highscore:
        with open("../highscore.txt", "w") as f:
            f.write(str(points))
    
    text_highscore = font.render(f"HI: {str(highscore).zfill(5)} ", False, FONT_COLOR_LIGHT)
    text_points = font.render(str(points).zfill(5), False, FONT_COLOR)

    x_pos, y_pos = (760, 40)

    # Get the width of the first text part to calculate
    # the starting position of the second part.
    text_width, _ = text_highscore.get_size()
    x_pos_part2 = x_pos + text_width

    # Blit both parts onto the screen
    SCREEN.blit(text_highscore, (x_pos, y_pos))
    SCREEN.blit(text_points, (x_pos_part2, y_pos))
