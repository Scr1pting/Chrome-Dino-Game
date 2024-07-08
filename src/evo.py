import numpy as np
import random


def activation(x: float) -> float:
    return 1 / (1 + np.exp(-x))

def prediction(
        x: float,
        y: float,
        weight_x: float,
        weight_y: float,
        b: float
    ) -> float:
    return activation(x * weight_x + y * weight_y + b)


def crossbreed(parent1, parent2):
    return [parent1[0]] + parent2[1:]

def mutate(chromosome):
    chromosome[random.randint(0, 2)] += np.random.randn()

# def breed():
    
