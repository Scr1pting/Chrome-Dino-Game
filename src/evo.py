import numpy as np


INPUT_SIZE = 2
OUTPUT_SIZE = 3
HIDDEN_LAYERS = 2
LAYER_SIZE = 16

MUTATION_RATE = 0.01


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
        np.random.normal(size=(LAYER_SIZE)),
        *np.random.normal(size=(HIDDEN_LAYERS, LAYER_SIZE)),
        np.random.normal(size=(OUTPUT_SIZE))
    ]
    return Genome(all_weights, all_biases)


# MARK: NN
def activation(input_values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-input_values))

def prediction(
        input_values: np.ndarray,
        weights: np.ndarray,
        biases: np.ndarray
    ) -> np.ndarray:
    return activation(weights @ input_values + biases)


# MARK: Evolution
def fitness(genome: Genome) -> float:
    

def crossbreed(parent1: Genome, parent2: Genome) -> Genome:
    all_weights = []
    all_biases = []

    for i in range(len(parent1.all_weights)):
        all_weights.append(
            (parent1.all_weights[i] + parent2.all_weights[i]) / 2
        )

    for i in range(len(parent1.all_biases)):
        all_weights.append(
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



if __name__ == "__main__":
    genome1 = create_genome()
    print(genome1.all_weights)
