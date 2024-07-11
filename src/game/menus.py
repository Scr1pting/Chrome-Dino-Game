import pygame

from game.settings import *


def initial_screen(highscore) -> float:
    SCREEN.fill(BACKGROUND_COLOR)

    font = pygame.font.Font(FONT_FAMILY, 20)

    text = font.render("Press any Key to Start", False, FONT_COLOR)

    hs_score_text = font.render(
        f"High Score: {highscore}", False, FONT_COLOR
    )

    hs_score_rect = hs_score_text.get_rect()
    hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    SCREEN.blit(hs_score_text, hs_score_rect)

    textRect = text.get_rect() 
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, textRect)
    # Image
    SCREEN.blit(RUNNING[1], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return highscore


def restart_screen():
    font = pygame.font.Font(FONT_FAMILY, 25)

    text = font.render("G A M E  O V E R", False, FONT_COLOR)
    textRect = text.get_rect() 
    textRect.center = (SCREEN_WIDTH // 2, 210)
    SCREEN.blit(text, textRect)

    reset_img = RESET
    reset_rect = reset_img.get_rect()
    # Position it at the center of the screen
    reset_rect.center = (SCREEN_WIDTH // 2, 310)  
    SCREEN.blit(reset_img, reset_rect)

    pygame.display.update()
