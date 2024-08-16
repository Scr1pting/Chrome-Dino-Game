import math
import random

from game.settings import *


class Game:
    def __init__(self) -> None:
        self.speed = INITIAL_SPEED
        self.obstacles = []

        self.frame = 0
        self.distance = 0
        self.is_dead = False

        self.next_generate_distance = 0

    @property
    def points(self) -> int:
        return self.distance // 80


def get_game_speed(distance: int) -> int:
    """Returns the speed based on equation (square root) with clamping"""
    return min(MAX_SPEED, int(math.sqrt(distance // 700) + INITIAL_SPEED))


def next_object_distance(distance: int, game_speed: int) -> int:
    """Returns the distance for generation of new objects"""
    return distance + random.randint(300 + game_speed * 20, 1000)
