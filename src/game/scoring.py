import pygame
import os

from settings import *


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

def render_score(highscore, points):
    font = pygame.font.Font(FONT_FAMILY, 20)
    
    if points >= highscore:
        highscore = points

        with open("../highscore.txt", "w") as f:
            f.write(str(highscore))
        
    text1 = font.render(f"HI: {str(highscore).zfill(5)} ", False, FONT_COLOR_LIGHT)
    text2 = font.render(str(points).zfill(5), False, FONT_COLOR)

    x_pos, y_pos = (760, 40)

    # Get the width of the first text part to calculate
    # the starting position of the second part.
    text_width, _ = text1.get_size()
    x_pos_part2 = x_pos + text_width

    # Blit both parts onto the screen
    SCREEN.blit(text1, (x_pos, y_pos))
    SCREEN.blit(text2, (x_pos_part2, y_pos))
