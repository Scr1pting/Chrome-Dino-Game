import pygame

from game.settings import *


def draw_stats(epoch, individuals, max_distance, current_distance):
    font = pygame.font.Font(FONT_FAMILY, 17)

    text_run = font.render(f"Iteration: {epoch + 1}", False, FONT_COLOR)
    text_indivuals = font.render(f"Individuals: {individuals}", False, FONT_COLOR)
    text_points = font.render(f"Points: {current_distance // 80}", False, FONT_COLOR)
    text_highscore = font.render(f"Best Score: {max(max_distance, current_distance) // 80} ", False, FONT_COLOR)

    x_pos, y_pos = (750, 40)

    pygame.draw.rect(
        SCREEN,
        BACKGROUND_COLOR,
        (x_pos - 20, y_pos, SCREEN_WIDTH - x_pos + 20, 120)
    )

    # Blit both parts onto the screen
    SCREEN.blit(text_run, (x_pos, y_pos))
    SCREEN.blit(text_indivuals, (x_pos, y_pos + 30))
    SCREEN.blit(text_points, (x_pos, y_pos + 60))
    SCREEN.blit(text_highscore, (x_pos, y_pos + 90))
