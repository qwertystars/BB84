import numpy as np
from typing import Tuple, List
import time

def generate_random_bits(length: int) -> np.ndarray:
    """Generate random classical bits (0 or 1)."""
    return np.random.randint(0, 2, length)

def generate_random_bases(length: int) -> np.ndarray:
    """Generate random bases (0 for Z, 1 for X)."""
    return np.random.randint(0, 2, length)

def compare_arrays(arr1: np.ndarray, arr2: np.ndarray) -> float:
    """Calculate the error rate between two arrays."""
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must have the same length")
    errors = np.sum(arr1 != arr2)
    return errors / len(arr1)

def apply_channel_error(qubits: np.ndarray, error_rate: float) -> np.ndarray:
    """Apply random bit flip errors to qubits."""
    noisy_qubits = qubits.copy()
    error_positions = np.random.random(len(qubits)) < error_rate
    noisy_qubits[error_positions] = 1 - noisy_qubits[error_positions]
    return noisy_qubits

def sift_key(alice_bits: np.ndarray, bob_bits: np.ndarray, alice_bases: np.ndarray, bob_bases: np.ndarray) -> Tuple[str, np.ndarray]:
    """Sift the key by keeping only bits where bases match."""
    matching_bases = alice_bases == bob_bases
    sifted_bits = alice_bits[matching_bases]
    return ''.join(map(str, sifted_bits)), matching_bases

def calculate_qber(alice_bits: np.ndarray, bob_bits: np.ndarray, matching_bases: np.ndarray) -> float:
    """Calculate Quantum Bit Error Rate."""
    if np.sum(matching_bases) == 0:
        return 0.0
    alice_matched = alice_bits[matching_bases]
    bob_matched = bob_bits[matching_bases]
    return compare_arrays(alice_matched, bob_matched)
