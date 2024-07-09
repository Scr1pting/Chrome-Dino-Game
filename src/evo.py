import numpy as np
import random


def activation(input_values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-input_values))

def prediction(
        input_values: np.ndarray,
        weights: np.ndarray,
        biases: np.ndarray
    ) -> np.ndarray:
    return activation(weights @ input_values + biases)


def crossbreed(parent1, parent2):
    return [parent1[0]] + parent2[1:]

def mutate(genome):
    genome[random.randint(0, 2)] += np.random.randn()

# def breed():
