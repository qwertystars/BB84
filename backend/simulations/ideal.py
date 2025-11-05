import numpy as np
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import generate_random_bits, generate_random_bases, sift_key, calculate_qber
import time

def simulate_ideal(qubit_count: int, **kwargs) -> Dict[str, Any]:
    """
    Simulate BB84 protocol under ideal conditions.
    No errors, no eavesdropping.
    """
    start_time = time.time()
    
    # Alice generates random bits and bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)
    
    # Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)
    
    # In ideal conditions, Bob measures correctly when bases match
    bob_bits = alice_bits.copy()
    
    # Sift the key
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    
    # Calculate QBER (should be 0 in ideal conditions)
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)
    
    execution_time = time.time() - start_time
    
    summary = {
        "total_qubits": qubit_count,
        "matching_bases": int(np.sum(matching_bases)),
        "sifted_key_length": len(sifted_key_str),
        "expected_qber": 0.0,
        "actual_qber": qber,
        "protocol_status": "Perfect - No errors detected",
        "security_level": "Maximum (No eavesdropping)"
    }
    
    return {
        "scenario": "ideal",
        "qubit_count": qubit_count,
        "sifted_key": sifted_key_str[:100] + "..." if len(sifted_key_str) > 100 else sifted_key_str,
        "sifted_key_length": len(sifted_key_str),
        "qber": qber,
        "error_rate": 0.0,
        "eve_fraction": 0.0,
        "summary": summary,
        "execution_time": execution_time
    }
