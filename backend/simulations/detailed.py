import numpy as np
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import generate_random_bits, generate_random_bases, sift_key, calculate_qber
import time

def simulate_detailed(qubit_count: int = 10, error_rate: float = 0.0, eve_fraction: float = 0.0, show_all: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Generate a detailed step-by-step simulation of the BB84 protocol.
    Shows how each qubit is processed through the protocol.

    Args:
        qubit_count: Number of qubits to simulate
        error_rate: Channel error rate
        eve_fraction: Fraction of qubits Eve intercepts
        show_all: If False, limit to 20 qubits for readability. If True, show all qubits.
    """
    start_time = time.time()

    # Limit to 20 qubits for detailed view unless show_all is True
    if not show_all:
        qubit_count = min(qubit_count, 20)

    # Step 1: Alice generates random bits and bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)

    # Step 2: Eve's interception (if applicable)
    eve_bits = alice_bits.copy()
    eve_bases = generate_random_bases(qubit_count)
    eve_intercepts = np.random.random(qubit_count) < eve_fraction

    # Track Eve's interference
    eve_caused_error = np.zeros(qubit_count, dtype=bool)

    for i in range(qubit_count):
        if eve_intercepts[i]:
            if alice_bases[i] != eve_bases[i]:
                # Wrong basis measurement causes 50% probability of error
                if np.random.random() < 0.5:
                    eve_bits[i] = 1 - alice_bits[i]
                    eve_caused_error[i] = True

    # Step 3: Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)

    # Step 4: Apply channel noise
    final_bits = eve_bits.copy()
    channel_errors = np.random.random(qubit_count) < error_rate
    final_bits[channel_errors] = 1 - final_bits[channel_errors]

    # Step 5: Bob measures
    # CRITICAL: When Bob uses the wrong basis, his measurement is RANDOM!
    bob_bits = np.zeros(qubit_count, dtype=int)
    bases_match = alice_bases == bob_bases

    for i in range(qubit_count):
        if bases_match[i]:
            # Correct basis: Bob gets the transmitted bit (with any channel/Eve errors)
            bob_bits[i] = final_bits[i]
        else:
            # Wrong basis: Bob gets a RANDOM bit (quantum mechanics!)
            bob_bits[i] = np.random.randint(0, 2)

    # Step 6: Determine correctness
    bits_match = alice_bits == bob_bits

    # Create detailed qubit information
    qubits_detail = []
    for i in range(qubit_count):
        qubit_info = {
            "index": i,
            "alice_bit": int(alice_bits[i]),
            "alice_basis": "Z" if alice_bases[i] == 0 else "X",
            "alice_state": get_quantum_state(alice_bits[i], alice_bases[i]),
            "eve_intercepted": bool(eve_intercepts[i]),
            "eve_basis": "Z" if eve_bases[i] == 0 else "X" if eve_fraction > 0 else None,
            "eve_measured": int(eve_bits[i]) if eve_intercepts[i] else None,
            "eve_caused_error": bool(eve_caused_error[i]),
            "bob_basis": "Z" if bob_bases[i] == 0 else "X",
            "bob_measured": int(bob_bits[i]),
            "bases_match": bool(bases_match[i]),
            "bits_match": bool(bits_match[i]),
            "channel_error": bool(channel_errors[i]),
            "kept_in_key": bool(bases_match[i])
        }
        qubits_detail.append(qubit_info)

    # Sift the key
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)

    # Calculate QBER
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)

    execution_time = time.time() - start_time

    # Count statistics
    matching_bases_count = int(np.sum(bases_match))
    correct_when_matched = int(np.sum(bits_match[bases_match]))

    # When bases don't match, the result should be random (50% correct)
    if np.sum(~bases_match) > 0:
        correct_when_not_matched = int(np.sum(bits_match[~bases_match]))
        not_matched_count = int(np.sum(~bases_match))
    else:
        correct_when_not_matched = 0
        not_matched_count = 0

    summary = {
        "total_qubits": qubit_count,
        "matching_bases": matching_bases_count,
        "non_matching_bases": not_matched_count,
        "correct_when_bases_match": correct_when_matched,
        "correct_when_bases_dont_match": correct_when_not_matched,
        "eve_interceptions": int(np.sum(eve_intercepts)),
        "eve_caused_errors": int(np.sum(eve_caused_error)),
        "channel_errors": int(np.sum(channel_errors)),
        "sifted_key_length": len(sifted_key_str),
        "qber": qber
    }

    return {
        "scenario": "detailed",
        "qubit_count": qubit_count,
        "qubits": qubits_detail,
        "sifted_key": sifted_key_str,
        "sifted_key_length": len(sifted_key_str),
        "qber": qber,
        "error_rate": error_rate,
        "eve_fraction": eve_fraction,
        "summary": summary,
        "execution_time": execution_time
    }

def get_quantum_state(bit: int, basis: int) -> str:
    """
    Get the quantum state representation based on bit value and basis.

    Z-basis (0): |0⟩ for bit 0, |1⟩ for bit 1
    X-basis (1): |+⟩ for bit 0, |-⟩ for bit 1
    """
    if basis == 0:  # Z-basis
        return "|0⟩" if bit == 0 else "|1⟩"
    else:  # X-basis
        return "|+⟩" if bit == 0 else "|-⟩"
