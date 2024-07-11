import numpy as np
from tqdm import tqdm

import ai.chromedino as chromedino


INPUT_SIZE = 4
OUTPUT_SIZE = 3
HIDDEN_LAYERS = 2
LAYER_SIZE = 16

MUTATION_RATE = 0.1
POPULATION_SIZE = 1000
EPOCHS = 1000


# MARK: Genome
class Genome:
    def __init__(
            self,
            all_weights: list, # 3D array
            all_biases: list # 2D array
        ):
        self.all_weights = all_weights
        self.all_biases = all_biases

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
def get_fitness(genome: Genome) -> int:
    return chromedino.start_game(genome)

def select(population: list[Genome], fitnesses: list[int]) -> list[Genome]:
    probabilities = [fitness / sum(fitnesses) for fitness in fitnesses]

    parents = []

    for _ in range(len(population)):
        # Roulette wheel selection
        new_index = np.random.choice(
                range(len(population)),
                p=probabilities
            )
        parents.append(population[new_index])
    
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
    population = [create_genome() for _ in range(POPULATION_SIZE)]

    for i in range(EPOCHS):
        fitnesses = []

        print(f"Iteration {i}: ", end="")
        for genome in tqdm(population):
            fitness = get_fitness(genome)
            fitnesses.append(fitness)
        
        parents = select(population, fitnesses)
        new_population = []

        for i in range(POPULATION_SIZE):
            if i == 0:
                # Always keep the best genome
                # Elitism
                new_population += [population[np.argmax(fitnesses)]]
            else:
                genome1, genome2 = np.random.choice(np.array(parents), 2)
                new_population += [crossover(genome1, genome2)]
                new_population[i] = mutate(new_population[i])

        print(f"Max fitness: {max(fitnesses)}")

        population = new_population      


if __name__ == "__main__":
    breed()
