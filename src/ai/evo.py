import numpy as np
import random
from tqdm import tqdm

import ai.chromedino as chromedino


INPUT_SIZE = 4
OUTPUT_SIZE = 2
HIDDEN_LAYERS = 2
LAYER_SIZE = 8

MUTATION_RATE = 0.1
GENOMES_SIZE = 1_000
EPOCHS = 1_000


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
        return self.score > other.score

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
def get_fitness(genomes: list) -> list:
    return chromedino.start_game(genomes)

def select(fitnesses: list[Genome]) -> list[Genome]:
    return sorted(fitnesses[-5:], reverse=True)


    probabilities = [fitness / sum(fitnesses) for fitness in fitnesses]

    parents = []

    for _ in range(len(genomes)):
        # Roulette wheel selection
        new_index = np.random.choice(
                range(len(genomes)),
                p=probabilities
            )
        parents.append(genomes[new_index])
    
    return parents

def crossover(parent1: Genome, parent2: Genome) -> Genome:
    all_weights = []
    all_biases = []

    for i in range(len(parent1.all_weights)):
        all_weights.append(
            (parent1.all_weights[i] + parent2.all_weights[i]) / 2
        )

    for i in range(len(parent1.all_biases)):
        all_biases.append(
            (parent1.all_biases[i] + parent2.all_biases[i]) / 2
        )

    return Genome(all_weights, all_biases)
    
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

    for i in range(EPOCHS):
        fitnesses = get_fitness(genomes)

        print(f"Iteration {i}: ", end="")
        
        parents = select(fitnesses)
        new_genomes = []

        new_genomes += parents

        for _ in range(GENOMES_SIZE - 5):
            new_genome = mutate(random.choice(parents))
            new_genome.score = 0
            new_genomes += [new_genome]

        # print(f"Max fitness: {max(fitnesses)}")

        genomes = new_genomes      


if __name__ == "__main__":
    breed()
