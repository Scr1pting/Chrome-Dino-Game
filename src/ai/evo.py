from copy import deepcopy
import numpy as np
import random
import math

import ai.chromedino as chromedino


INPUT_SIZE = 3
OUTPUT_SIZE = 3
HIDDEN_LAYERS = 2
LAYER_SIZE = 16

GENOMES_SIZE = 100
EPOCHS = 20
MUTATION_RATE = 0.2
ELITISM = 0.1


# MARK: Genome
class Genome:
    def __init__(
            self,
            all_weights: list, # 3D array
            all_biases: list # 2D array
        ):
        self.id = id(self)
        self.all_weights = all_weights
        self.all_biases = all_biases
        self.score = 0

    def __lt__(self, other):
        return self.score < other.score

def create_genome() -> Genome:
    # Three arrays of weights
    # 2x16, 16x16, 16x3
    # Weights are initialized with a normal distribution
    all_weights = [
        np.random.normal(size=(INPUT_SIZE, LAYER_SIZE)),
        *np.random.normal(size=(
            HIDDEN_LAYERS - 1,
            LAYER_SIZE,
            LAYER_SIZE)
        ),
        np.random.normal(size=(LAYER_SIZE, OUTPUT_SIZE))
    ]
    # Three arrays of biases
    # 1x16, 1x16, 1x3 
    # Biases are initialized with a normal distribution
    all_biases = [
        *np.random.normal(size=(HIDDEN_LAYERS, LAYER_SIZE)),
        np.random.normal(size=(OUTPUT_SIZE))
    ]
    return Genome(all_weights, all_biases)


# MARK: Evolution
def get_fitness(genomes: list, epoch) -> list:
    return chromedino.start_game(genomes, epoch)

def select_elite(fitnesses: list[Genome]) -> list[Genome]:
    return sorted(fitnesses, reverse=True)[:math.ceil(ELITISM * len(fitnesses))]

def select_parents(fitnesses: list[Genome]) -> list[Genome]:
    # Tournament selection
    parents = []
    for _ in range(GENOMES_SIZE):
        tournament = random.sample(fitnesses, 2)
        parents.append(max(tournament))
    return parents
    
def mutate(genome: Genome) -> Genome:
    for i, weights in enumerate(genome.all_weights):
        for row in range(len(weights)):
            for col in range(len(weights[row])):
                if np.random.rand() < MUTATION_RATE:
                    genome.all_weights[i][row, col] += np.random.normal()
    
    for i, biases in enumerate(genome.all_biases):
        for j in range(len(biases)):
            if np.random.rand() < MUTATION_RATE:
                genome.all_biases[i][j] += np.random.normal()
    
    return genome
    
def breed():
    genomes = [create_genome() for _ in range(GENOMES_SIZE)]

    for epoch in range(EPOCHS):
        genomes_with_fitness = get_fitness(genomes, epoch)
        
        parents = select_parents(genomes_with_fitness)
        new_genomes = select_elite(genomes_with_fitness)

        for _ in range(GENOMES_SIZE - len(new_genomes)):
            # Without deepcopy, the same same genome would be mutated
            # multiple times, including the genome selected through
            # elitism.
            new_genome = mutate(deepcopy(random.choice(parents)))
            new_genome.score = 0
            new_genomes.append(new_genome)

        genomes = new_genomes

    best_genome = max(genomes)
    print(f"Best score {best_genome.score}")


if __name__ == "__main__":
    breed()
