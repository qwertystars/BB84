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
    
    This scenario demonstrates how eavesdropping is detected in BB84 through QBER analysis.
    
    Eve's Intercept-Resend Attack:
    1. Eve intercepts a fraction of qubits from Alice
    2. Eve measures each intercepted qubit in a random basis
    3. Eve resends the measured state to Bob
    
    Physical Consequences:
    - If Eve guesses the correct basis: no disturbance
    - If Eve guesses wrong basis: 50% chance of bit flip
    - Average error introduced by Eve: 25% of intercepted qubits
    
    Expected QBER:
    - QBER_total = QBER_channel + QBER_eve
    - QBER_eve ≈ 0.25 × eve_fraction
    - Example: 50% interception → ~12.5% added QBER
    
    Detection:
    - Compare measured QBER vs expected channel noise
    - Significant excess indicates eavesdropping
    - QBER > 11% (Holevo bound) → abort key exchange
    
    Args:
        qubit_count: Number of qubits to transmit
        error_rate: Channel noise level (0.0-0.5)
        eve_fraction: Fraction of qubits Eve intercepts (0.0-1.0)
        
    Returns:
        Dictionary with simulation results including QBER and security status
    """
    start_time = time.time()
    
    # Step 1: Alice generates random bits and encodes them in random bases
    alice_bits = generate_random_bits(qubit_count)
    alice_bases = generate_random_bases(qubit_count)
    
    # Step 2: Eve's intercept-resend attack
    eve_bits = alice_bits.copy()
    eve_bases = generate_random_bases(qubit_count)
    
    # Eve intercepts a fraction of qubits
    eve_intercepts = np.random.random(qubit_count) < eve_fraction
    
    # When Eve intercepts, she may introduce errors due to basis mismatch
    # Physics: If Eve measures in wrong basis (50% probability),
    # she has 50% chance of getting wrong result → 25% total error rate
    for i in range(qubit_count):
        if eve_intercepts[i]:
            if alice_bases[i] != eve_bases[i]:
                # Wrong basis measurement causes 50% probability of error
                if np.random.random() < 0.5:
                    eve_bits[i] = 1 - alice_bits[i]
    
    # Step 3: Bob generates random bases for measurement
    bob_bases = generate_random_bases(qubit_count)
    
    # Step 4: Channel noise affects qubits after Eve's interference
    final_bits = apply_channel_error(eve_bits, error_rate)
    
    # Step 5: Bob measures the final qubits
    bob_bits = final_bits.copy()
    
    # Step 6: Basis sifting - Alice and Bob publicly compare bases
    sifted_key_str, matching_bases = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    
    # Step 7: Calculate QBER for security analysis
    qber = calculate_qber(alice_bits, bob_bits, matching_bases)
    
    # Calculate theoretical QBER contribution from Eve
    # Physics: Eve introduces 25% error rate on intercepted qubits
    eve_qber_contribution = 0.25 * eve_fraction
    expected_qber = error_rate + eve_qber_contribution
    
    execution_time = time.time() - start_time
    
    # Security analysis
    # If QBER significantly exceeds channel noise, eavesdropping is detected
    eve_detected = qber > error_rate + 0.1
    
    summary = {
        "total_qubits": qubit_count,
        "matching_bases": int(np.sum(matching_bases)),
        "sifted_key_length": len(sifted_key_str),
        "channel_error_rate": error_rate,
        "eve_fraction": eve_fraction,
        "expected_qber": expected_qber,
        "actual_qber": qber,
        "eve_detected": bool(eve_detected),
        "protocol_status": "Eavesdropping detected" if eve_detected else "Eavesdropping may be present",
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
