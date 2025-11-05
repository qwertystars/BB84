import numpy as np
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import generate_random_bits, generate_random_bases, apply_channel_error, sift_key, calculate_qber
import time

def simulate_error_with_eve(qubit_count: int, error_rate: float = 0.05, eve_fraction: float = 0.5, **kwargs) -> Dict[str, Any]:
    """
    Simulate BB84 protocol with channel noise and Eve's intercept-resend attack.
    """
    start_time = time.time()
    
    # Alice generates random bits and bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)
    
    # Eve's attack: intercept-resend on a fraction of qubits
    eve_bits = alice_bits.copy()
    eve_bases = generate_random_bases(qubit_count)
    
    # Eve only intercepts a fraction of the qubits
    eve_intercepts = np.random.random(qubit_count) < eve_fraction
    
    # When Eve intercepts, she may introduce errors if she chooses wrong basis
    for i in range(qubit_count):
        if eve_intercepts[i]:
            if alice_bases[i] != eve_bases[i]:
                # Wrong basis measurement causes error probability of 0.5
                if np.random.random() < 0.5:
                    eve_bits[i] = 1 - alice_bits[i]
    
    # Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)
    
    # Channel noise affects qubits after Eve's interference
    final_bits = apply_channel_error(eve_bits, error_rate)
    
    # Bob measures the final qubits
    bob_bits = final_bits.copy()
    
    # Sift the key
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    
    # Calculate QBER (combination of channel noise and Eve's interference)
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)
    
    # Calculate theoretical QBER contribution from Eve
    eve_qber_contribution = 0.25 * eve_fraction  # Eve introduces 25% error rate on intercepted qubits
    expected_qber = error_rate + eve_qber_contribution
    
    execution_time = time.time() - start_time
    
    summary = {
        "total_qubits": qubit_count,
        "matching_bases": int(np.sum(matching_bases)),
        "sifted_key_length": len(sifted_key_str),
        "channel_error_rate": error_rate,
        "eve_fraction": eve_fraction,
        "expected_qber": expected_qber,
        "actual_qber": qber,
        "eve_detected": bool(qber > error_rate + 0.1),  # Eve detected if QBER significantly exceeds channel noise
        "protocol_status": "Eavesdropping detected" if qber > error_rate + 0.1 else "Eavesdropping may be present",
        "security_level": "Compromised" if qber > 0.15 else "Potentially secure"
    }
    
    return {
        "scenario": "error-eve",
        "qubit_count": qubit_count,
        "sifted_key": sifted_key_str[:100] + "..." if len(sifted_key_str) > 100 else sifted_key_str,
        "sifted_key_length": len(sifted_key_str),
        "qber": qber,
        "error_rate": error_rate,
        "eve_fraction": eve_fraction,
        "summary": summary,
        "execution_time": execution_time
    }
