import numpy as np
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import generate_random_bits, generate_random_bases, apply_channel_error, sift_key, calculate_qber
import time

def simulate_error_only(qubit_count: int, error_rate: float = 0.1, **kwargs) -> Dict[str, Any]:
    """
    Simulate BB84 protocol with channel noise but no eavesdropping.
    """
    start_time = time.time()
    
    # Alice generates random bits and bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)
    
    # Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)
    
    # Channel noise affects qubits during transmission
    noisy_bits = apply_channel_error(alice_bits, error_rate)
    
    # Bob measures the noisy qubits
    bob_bits = noisy_bits.copy()
    
    # Sift the key
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    
    # Calculate QBER due to channel noise
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)
    
    execution_time = time.time() - start_time
    
    summary = {
        "total_qubits": qubit_count,
        "matching_bases": int(np.sum(matching_bases)),
        "sifted_key_length": len(sifted_key_str),
        "channel_error_rate": error_rate,
        "expected_qber": error_rate,
        "actual_qber": qber,
        "protocol_status": "Channel noise present" if qber > 0.05 else "Good quality channel",
        "security_level": "Secure (No eavesdropping)"
    }
    
    return {
        "scenario": "error-only",
        "qubit_count": qubit_count,
        "sifted_key": sifted_key_str[:100] + "..." if len(sifted_key_str) > 100 else sifted_key_str,
        "sifted_key_length": len(sifted_key_str),
        "qber": qber,
        "error_rate": error_rate,
        "eve_fraction": 0.0,
        "summary": summary,
        "execution_time": execution_time
    }
