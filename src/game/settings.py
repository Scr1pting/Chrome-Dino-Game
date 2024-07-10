import pygame
import os


# MARK: General
FRAME_RATE = 60

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT),
    flags=pygame.SCALED,
    vsync=1
)

pygame.display.set_caption("Chrome Dino Runner")

current_script_dir = os.path.dirname(os.path.abspath(__file__))

APP_ICON = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/other",
    "AppIcon.png"
))
pygame.display.set_icon(APP_ICON)


# MARK: Dino
RUNNING = [
    pygame.image.load(os.path.join(
        current_script_dir, 
        "../../assets/dino", 
        "DinoRun1.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/dino",
        "DinoRun2.png"
    )),
]
JUMPING = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/dino", 
    "DinoJump.png"
))
DUCKING = [
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/dino",
        "DinoDuck1.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/dino", 
        "DinoDuck2.png"
    )),
]
DEAD = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/dino",
    "DinoDead.png"
))

# MARK: Obstacles
SMALL_CACTUS = [
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/cactus",
        "SmallCactus1.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/cactus",
        "SmallCactus2.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/cactus",
        "SmallCactus3.png"
    )),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join(
        current_script_dir, 
        "../../assets/cactus",
        "LargeCactus1.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/cactus", 
        "LargeCactus2.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/cactus", 
        "LargeCactus3.png"
    )),
]
BIRD = [
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/bird",
        "Bird1.png"
    )),
    pygame.image.load(os.path.join(
        current_script_dir,
        "../../assets/bird",
        "Bird2.png"
    )),
]


# MARK: Background
CLOUD = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/other",
    "Cloud.png"
))
TRACK = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/other",
    "Track.png"
))


# MARK: Menu
RESET = pygame.image.load(os.path.join(
    current_script_dir,
    "../../assets/other",
    "Reset.png"
))


# MARK: Display
BACKGROUND_COLOR = (247, 247, 247)

FONT_COLOR = (83, 83, 83)
FONT_COLOR_LIGHT = (117, 117, 117)
FONT_FAMILY = os.path.join(
    current_script_dir,
    "../../assets/font",
    "PressStart2P.ttf"
)
