import numpy as np
from typing import Tuple, List
import time

def generate_random_bits(length: int) -> np.ndarray:
    """Generate random classical bits (0 or 1).
    
    In BB84, Alice uses these random bits to encode her quantum states.
    Each bit represents the state she wants to send to Bob.
    """
    return np.random.randint(0, 2, length)

def generate_random_bases(length: int) -> np.ndarray:
    """Generate random measurement bases (0 for Z-basis, 1 for X-basis).
    
    In BB84:
    - Z-basis (computational basis): measures |0⟩ and |1⟩ states
    - X-basis (Hadamard basis): measures |+⟩ and |-⟩ states
    
    Both Alice and Bob randomly choose bases. Security comes from the fact 
    that measuring in the wrong basis gives random results.
    """
    return np.random.randint(0, 2, length)

def compare_arrays(arr1: np.ndarray, arr2: np.ndarray) -> float:
    """Calculate the error rate between two binary arrays.
    
    Used to compute QBER (Quantum Bit Error Rate).
    """
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must have the same length")
    errors = np.sum(arr1 != arr2)
    return errors / len(arr1)

def apply_channel_error(qubits: np.ndarray, error_rate: float) -> np.ndarray:
    """Apply random bit flip errors to simulate noisy quantum channel.
    
    Simulates effects like photon loss, detector inefficiency, 
    environmental decoherence, and transmission errors.
    """
    noisy_qubits = qubits.copy()
    error_positions = np.random.random(len(qubits)) < error_rate
    noisy_qubits[error_positions] = 1 - noisy_qubits[error_positions]
    return noisy_qubits

def sift_key(alice_bits: np.ndarray, bob_bits: np.ndarray, 
             alice_bases: np.ndarray, bob_bases: np.ndarray) -> Tuple[str, np.ndarray]:
    """Perform basis sifting - keep only bits where bases matched.
    
    Crucial BB84 step:
    1. Alice and Bob publicly announce their bases (not results!)
    2. Keep only bits where bases matched
    3. These form the sifted key
    
    On average, bases match 50% of the time.
    """
    matching_bases = alice_bases == bob_bases
    sifted_bits = alice_bits[matching_bases]
    return ''.join(map(str, sifted_bits)), matching_bases

def calculate_qber(alice_bits: np.ndarray, bob_bits: np.ndarray, 
                   matching_bases: np.ndarray) -> float:
    """Calculate Quantum Bit Error Rate (QBER) - key security metric.
    
    QBER interpretation:
    - 0-5%: Excellent channel quality
    - 5-11%: Acceptable (below Holevo bound)
    - >11%: Potentially insecure
    - >25%: Definitely compromised
    """
    if np.sum(matching_bases) == 0:
        return 0.0
    alice_matched = alice_bits[matching_bases]
    bob_matched = bob_bits[matching_bases]
    return compare_arrays(alice_matched, bob_matched)
