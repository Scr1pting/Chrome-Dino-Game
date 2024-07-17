import numpy as np


def activation(input_values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-input_values))

def layer_prediction(
        input_values: np.ndarray,
        weights: np.ndarray,
        biases: np.ndarray
    ) -> np.ndarray:
    weights.shape
    # 1D arrays like input_values are treated as column vectors by np.
    # Therefore, we need to transpose the weights.
    return activation(weights.T @ input_values + biases)

def predict(genome, input_values: np.ndarray) -> np.ndarray:
    """Format input values:
    [speed, player height, distance next object, object height]
    """
    for i in range(len(genome.all_weights)):
        input_values = layer_prediction(
            input_values,
            genome.all_weights[i],
            genome.all_biases[i]
        )
    return input_values

def next_step(genome, input_values: np.ndarray) -> int:
    """
    0: Duck
    1: Run
    2: Jump
    """
    return int(np.argmax(predict(genome, input_values)))
