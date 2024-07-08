import pygame # type: ignore
import os


FRAME_RATE = 60

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT),
    flags=pygame.SCALED,
    vsync=1
)

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("../assets/dino/DinoJump.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("../assets/dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("../assets/dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("../assets/dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("../assets/dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("../assets/dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("../assets/cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("../assets/cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("../assets/cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("../assets/cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("../assets/cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("../assets/cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("../assets/bird", "Bird1.png")),
    pygame.image.load(os.path.join("../assets/bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("../assets/other", "Cloud.png"))

BG = pygame.image.load(os.path.join("../assets/other", "Track.png"))

FONT_COLOR = (83, 83, 83)
FONT_FAMILY = "../assets/font/PressStart2p.ttf"
