import numpy as np
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import generate_random_bits, generate_random_bases, sift_key, calculate_qber
import time

def simulate_decoherence_free(qubit_count: int, error_rate: float = 0.0, eve_fraction: float = 0.5, **kwargs) -> Dict[str, Any]:
    """
    Simulate BB84 protocol in decoherence-free space.
    Quantum information is preserved from environmental noise, but Eve's measurements still disturb the system.
    """
    start_time = time.time()
    
    # Alice generates random bits and bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)
    
    # Eve's attack: intercept-resend on a fraction of qubits
    # In decoherence-free space, Eve's measurement choices are the only source of disturbance
    eve_bits = alice_bits.copy()
    eve_bases = generate_random_bases(qubit_count)
    
    # Eve only intercepts a fraction of the qubits
    eve_intercepts = np.random.random(qubit_count) < eve_fraction
    
    # When Eve intercepts, she may introduce errors due to basis mismatch
    # 50% chance of wrong basis × 50% chance of wrong measurement = 25% error rate
    for i in range(qubit_count):
        if eve_intercepts[i]:
            if alice_bases[i] != eve_bases[i]:
                # Wrong basis measurement causes 50% probability of error
                if np.random.random() < 0.5:
                    eve_bits[i] = 1 - alice_bits[i]
    
    # Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)
    
    # In decoherence-free space, only Eve's interference affects qubits
    # No environmental channel noise
    final_bits = eve_bits.copy()
    
    # Bob measures the final qubits
    bob_bits = final_bits.copy()
    
    # Sift the key
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    
    # Calculate QBER (combination of Eve's interference only)
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)
    
    # Calculate theoretical QBER contribution from Eve
    # Physics: Eve intercepts × wrong basis (50%) × wrong measurement (50%) = 25% of intercepted qubits
    # QBER calculation already filters by matching bases, so: eve_fraction × 0.25
    eve_qber_contribution = 0.25 * eve_fraction  
    expected_qber = eve_qber_contribution  # No channel noise in decoherence-free space
    
    execution_time = time.time() - start_time
    
    summary = {
        "total_qubits": qubit_count,
        "matching_bases": int(np.sum(matching_bases)),
        "sifted_key_length": len(sifted_key_str),
        "decoherence_factor": 0.0,  # Perfect coherence from environment
        "eve_fraction": eve_fraction,
        "expected_qber": expected_qber,
        "actual_qber": qber,
        "eve_detected": bool(qber > 0.1),  # Eve detected if QBER exceeds threshold
        "quantum_coherence": "Preserved from environmental noise",
        "protocol_status": "Environmental decoherence eliminated, but Eve detection possible",
        "security_level": "Protected from noise, vulnerable to eavesdropping" if eve_fraction > 0 else "Maximum security (no eavesdropping)"
    }
    
    return {
        "scenario": "decoherence-free",
        "qubit_count": qubit_count,
        "sifted_key": sifted_key_str[:100] + "..." if len(sifted_key_str) > 100 else sifted_key_str,
        "sifted_key_length": len(sifted_key_str),
        "qber": qber,
        "error_rate": error_rate,
        "eve_fraction": eve_fraction,
        "summary": summary,
        "execution_time": execution_time
    }
