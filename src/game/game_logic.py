import math

from game.settings import *


class Game:
    def __init__(self) -> None:
        self.speed = INITIAL_SPEED
        self.obstacles = []

        self.frame = 0
        self.distance = 0
        self.points = 0
        self.is_dead = False

        self.next_generate_distance = 0


def get_game_speed(distance: int) -> int:
    return min(MAX_SPEED, int(math.sqrt(distance // 700) + INITIAL_SPEED))
