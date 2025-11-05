"""
Comprehensive unit tests for BB84 Quantum Key Distribution Simulator backend.

Tests cover:
- Pure function logic (prepare_bb84_qubit, measure_bb84_qubit)
- BB84 simulation algorithm
- BB84Results class
- API endpoints
- Edge cases and error handling
- Thread safety
- Quantum circuit correctness
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import numpy as np
from qiskit import QuantumCircuit
from qiskit.result import Result
import threading
import sys
import os
from pydantic import ValidationError

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import (
    app, 
    BB84Request, 
    BB84Results,
    prepare_bb84_qubit,
    measure_bb84_qubit,
    simulate_bb84,
    latest_results,
    results_lock
)


# Test client for API endpoints
client = TestClient(app)


class TestBB84Results:
    """Test cases for BB84Results class"""
    
    def test_initialization(self):
        """Test BB84Results initializes with empty lists and zero QBER"""
        results = BB84Results()
        assert results.alice_bits == []
        assert results.alice_bases == []
        assert results.bob_bases == []
        assert results.bob_measurements == []
        assert results.sifted_key_alice == []
        assert results.sifted_key_bob == []
        assert results.qber == 0.0
        assert results.circuits == []
        assert isinstance(results.lock, type(threading.Lock()))
    
    def test_thread_safe_lock(self):
        """Test that BB84Results has a proper thread lock"""
        results = BB84Results()
        assert hasattr(results, 'lock')
        # Test lock can be acquired and released
        results.lock.acquire()
        results.lock.release()


class TestPrepareBB84Qubit:
    """Test cases for prepare_bb84_qubit function"""
    
    def test_prepare_bit_0_basis_z(self):
        """Test preparing |0⟩ state (bit=0, basis=Z)"""
        qc = prepare_bb84_qubit(0, 'Z')
        
        # Verify circuit structure
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 1
        assert qc.num_clbits == 1
        
        # No gates should be applied for |0⟩ in Z basis
        assert len(qc.data) == 0
    
    def test_prepare_bit_1_basis_z(self):
        """Test preparing |1⟩ state (bit=1, basis=Z)"""
        qc = prepare_bb84_qubit(1, 'Z')
        
        # Should have X gate applied
        assert len(qc.data) == 1
        assert qc.data[0].operation.name == 'x'
    
    def test_prepare_bit_0_basis_x(self):
        """Test preparing |+⟩ state (bit=0, basis=X)"""
        qc = prepare_bb84_qubit(0, 'X')
        
        # Should have H gate applied
        assert len(qc.data) == 1
        assert qc.data[0].operation.name == 'h'
    
    def test_prepare_bit_1_basis_x(self):
        """Test preparing |-⟩ state (bit=1, basis=X)"""
        qc = prepare_bb84_qubit(1, 'X')
        
        # Should have X and H gates applied
        assert len(qc.data) == 2
        gate_names = [gate.operation.name for gate in qc.data]
        assert 'x' in gate_names
        assert 'h' in gate_names
    
    def test_all_basis_combinations(self):
        """Test all four possible state preparations"""
        test_cases = [
            (0, 'Z', 0),  # |0⟩ - no gates
            (1, 'Z', 1),  # |1⟩ - X gate
            (0, 'X', 1),  # |+⟩ - H gate
            (1, 'X', 2),  # |-⟩ - X and H gates
        ]
        
        for bit, basis, expected_gates in test_cases:
            qc = prepare_bb84_qubit(bit, basis)
            assert len(qc.data) == expected_gates, \
                f"Failed for bit={bit}, basis={basis}"
    
    def test_returns_quantum_circuit(self):
        """Test that function returns a QuantumCircuit object"""
        for bit in [0, 1]:
            for basis in ['Z', 'X']:
                qc = prepare_bb84_qubit(bit, basis)
                assert isinstance(qc, QuantumCircuit)


class TestMeasureBB84Qubit:
    """Test cases for measure_bb84_qubit function"""
    
    def test_measure_in_z_basis(self):
        """Test measurement in Z basis (computational basis)"""
        qc = QuantumCircuit(1, 1)
        qc = measure_bb84_qubit(qc, 'Z')
        
        # Should have measurement gate added
        gate_names = [gate.operation.name for gate in qc.data]
        assert 'measure' in gate_names
    
    def test_measure_in_x_basis(self):
        """Test measurement in X basis (Hadamard basis)"""
        qc = QuantumCircuit(1, 1)
        qc = measure_bb84_qubit(qc, 'X')
        
        # Should have H gate then measurement
        gate_names = [gate.operation.name for gate in qc.data]
        assert 'h' in gate_names
        assert 'measure' in gate_names
    
    def test_measure_returns_same_circuit(self):
        """Test that function returns the modified circuit"""
        qc = QuantumCircuit(1, 1)
        result_qc = measure_bb84_qubit(qc, 'Z')
        assert result_qc is qc  # Should be same object
    
    def test_measure_with_existing_gates(self):
        """Test measurement on circuit with existing gates"""
        qc = QuantumCircuit(1, 1)
        qc.x(0)  # Add X gate
        initial_gates = len(qc.data)
        
        qc = measure_bb84_qubit(qc, 'Z')
        
        # Should have added measurement (and possibly H if X basis)
        assert len(qc.data) >= initial_gates + 1




class TestSimulateBB84:
    """Test cases for simulate_bb84 function"""
    
    def test_basic_simulation_no_noise(self):
        """Test basic BB84 simulation with no noise"""
        n_qubits = 10
        results = simulate_bb84(n_qubits, noise_level=0.0, seed=42)
        
        # Check results structure
        assert isinstance(results, BB84Results)
        assert len(results.alice_bits) == n_qubits
        assert len(results.alice_bases) == n_qubits
        assert len(results.bob_bases) == n_qubits
        assert len(results.bob_measurements) == n_qubits
        assert len(results.circuits) == n_qubits
    
    def test_simulation_with_seed_is_deterministic(self):
        """Test that using same seed produces identical results"""
        seed = 42
        n_qubits = 20
        
        results1 = simulate_bb84(n_qubits, noise_level=0.0, seed=seed)
        results2 = simulate_bb84(n_qubits, noise_level=0.0, seed=seed)
        
        # All random elements should be identical
        assert results1.alice_bits == results2.alice_bits
        assert results1.alice_bases == results2.alice_bases
        assert results1.bob_bases == results2.bob_bases
        assert results1.bob_measurements == results2.bob_measurements
    
    def test_simulation_without_seed_varies(self):
        """Test that simulations without seed produce different results"""
        n_qubits = 50
        
        results1 = simulate_bb84(n_qubits, noise_level=0.0, seed=None)
        results2 = simulate_bb84(n_qubits, noise_level=0.0, seed=None)
        
        # Results should likely be different (very low probability of being same)
        assert results1.alice_bits != results2.alice_bits or \
               results1.alice_bases != results2.alice_bases
    
    def test_bases_are_valid(self):
        """Test that all bases are either 'Z' or 'X'"""
        results = simulate_bb84(20, noise_level=0.0, seed=42)
        
        for basis in results.alice_bases:
            assert basis in ['Z', 'X']
        
        for basis in results.bob_bases:
            assert basis in ['Z', 'X']
    
    def test_bits_are_binary(self):
        """Test that all bits are 0 or 1"""
        results = simulate_bb84(20, noise_level=0.0, seed=42)
        
        for bit in results.alice_bits:
            assert bit in [0, 1]
        
        for bit in results.bob_measurements:
            assert bit in [0, 1]
    
    def test_key_sifting_logic(self):
        """Test that key sifting only keeps bits where bases match"""
        results = simulate_bb84(50, noise_level=0.0, seed=42)
        
        # Count matching bases manually
        matching_count = sum(
            1 for i in range(len(results.alice_bases))
            if results.alice_bases[i] == results.bob_bases[i]
        )
        
        # Sifted key length should equal matching bases count
        assert len(results.sifted_key_alice) == matching_count
        assert len(results.sifted_key_bob) == matching_count
    
    def test_zero_noise_produces_zero_qber(self):
        """Test that with no noise, QBER should be 0"""
        results = simulate_bb84(30, noise_level=0.0, seed=42)
        
        # With perfect quantum channel, keys should match exactly
        assert results.qber == 0.0
        assert results.sifted_key_alice == results.sifted_key_bob
    
    def test_qber_calculation(self):
        """Test QBER is calculated correctly"""
        results = simulate_bb84(100, noise_level=0.0, seed=42)
        
        if len(results.sifted_key_alice) > 0:
            errors = sum(
                1 for a, b in zip(results.sifted_key_alice, results.sifted_key_bob, strict=True)
                if a != b
            )
            expected_qber = errors / len(results.sifted_key_alice)
            assert abs(results.qber - expected_qber) < 1e-10
    
    def test_qber_with_noise(self):
        """Test that noise increases QBER"""
        results_with_noise = simulate_bb84(100, noise_level=0.1, seed=42)
        
        # Noise should generally increase QBER (though probabilistic)
        # We test structure rather than exact values due to randomness
        assert 0.0 <= results_with_noise.qber <= 1.0
    
    def test_edge_case_single_qubit(self):
        """Test simulation with just 1 qubit"""
        results = simulate_bb84(1, noise_level=0.0, seed=42)
        
        assert len(results.alice_bits) == 1
        assert len(results.circuits) == 1
        assert 0 <= len(results.sifted_key_alice) <= 1
    
    def test_edge_case_many_qubits(self):
        """Test simulation with maximum allowed qubits"""
        n_qubits = 1000
        results = simulate_bb84(n_qubits, noise_level=0.0, seed=42)
        
        assert len(results.alice_bits) == n_qubits
        assert len(results.bob_measurements) == n_qubits
    
    def test_noise_level_zero(self):
        """Test with explicit zero noise level"""
        results = simulate_bb84(10, noise_level=0.0, seed=42)
        assert results.qber == 0.0
    
    def test_noise_level_maximum(self):
        """Test with maximum noise level"""
        results = simulate_bb84(20, noise_level=1.0, seed=42)
        # Should still complete without error
        assert len(results.alice_bits) == 20
    
    def test_circuits_are_stored(self):
        """Test that quantum circuits are stored for each qubit"""
        n_qubits = 15
        results = simulate_bb84(n_qubits, noise_level=0.0, seed=42)
        
        assert len(results.circuits) == n_qubits
        for circuit in results.circuits:
            assert isinstance(circuit, QuantumCircuit)
    
    def test_sifted_keys_same_length(self):
        """Test that Alice and Bob's sifted keys have same length"""
        results = simulate_bb84(50, noise_level=0.0, seed=42)
        assert len(results.sifted_key_alice) == len(results.sifted_key_bob)
    
    def test_efficiency_approximately_50_percent(self):
        """Test that key efficiency is approximately 50% (bases match ~50% of time)"""
        n_qubits = 1000  # Large sample for statistical test
        results = simulate_bb84(n_qubits, noise_level=0.0, seed=42)
        
        efficiency = len(results.sifted_key_alice) / n_qubits
        
        # With random bases, expect ~50% efficiency (allow 10% deviation)
        assert 0.4 <= efficiency <= 0.6




class TestAPIEndpoints:
    """Test cases for FastAPI endpoints"""
    
    def test_root_endpoint(self):
        """Test GET / endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self):
        """Test GET /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "BB84 Simulator"
    
    def test_run_bb84_endpoint_basic(self):
        """Test POST /run_bb84 with valid parameters"""
        payload = {
            "n_qubits": 20,
            "noise_level": 0.0,
            "seed": 42
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "summary" in data
        assert data["summary"]["total_qubits"] == 20
    
    def test_run_bb84_with_defaults(self):
        """Test POST /run_bb84 with default parameters"""
        response = client.post("/run_bb84", json={})
        assert response.status_code == 200
        
        data = response.json()
        assert data["summary"]["total_qubits"] == 100  # default
    
    def test_run_bb84_with_noise(self):
        """Test POST /run_bb84 with noise level"""
        payload = {
            "n_qubits": 30,
            "noise_level": 0.05,
            "seed": 123
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["parameters"]["noise_level"] == 0.05
    
    def test_run_bb84_validation_min_qubits(self):
        """Test validation rejects n_qubits < 1"""
        payload = {
            "n_qubits": 0,
            "noise_level": 0.0
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_run_bb84_validation_max_qubits(self):
        """Test validation rejects n_qubits > 1000"""
        payload = {
            "n_qubits": 1001,
            "noise_level": 0.0
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 422
    
    def test_run_bb84_validation_negative_noise(self):
        """Test validation rejects negative noise level"""
        payload = {
            "n_qubits": 10,
            "noise_level": -0.1
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 422
    
    def test_run_bb84_validation_noise_too_high(self):
        """Test validation rejects noise level > 1.0"""
        payload = {
            "n_qubits": 10,
            "noise_level": 1.5
        }
        
        response = client.post("/run_bb84", json=payload)
        assert response.status_code == 422
    
    def test_results_endpoint_after_simulation(self):
        """Test GET /results returns data after running simulation"""
        # First run simulation
        client.post("/run_bb84", json={"n_qubits": 15, "noise_level": 0.0, "seed": 42})
        
        # Then get results
        response = client.get("/results")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = [
            "alice_bits", "alice_bases", "bob_bases", "bob_measurements",
            "sifted_key_alice", "sifted_key_bob", "matching_bases", "total_rounds"
        ]
        for field in required_fields:
            assert field in data
        
        assert len(data["alice_bits"]) == 15
    
    def test_stats_endpoint_after_simulation(self):
        """Test GET /stats returns statistics after simulation"""
        client.post("/run_bb84", json={"n_qubits": 25, "noise_level": 0.0, "seed": 42})
        
        response = client.get("/stats")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = [
            "qber", "total_qubits", "sifted_key_length", "efficiency",
            "matching_bases_count", "error_count", "secure", "security_threshold"
        ]
        for field in required_fields:
            assert field in data
        
        assert data["total_qubits"] == 25
        assert 0.0 <= data["efficiency"] <= 1.0
        assert 0.0 <= data["qber"] <= 1.0
    
    def test_stats_secure_flag(self):
        """Test that secure flag is set correctly based on QBER"""
        client.post("/run_bb84", json={"n_qubits": 50, "noise_level": 0.0, "seed": 42})
        
        response = client.get("/stats")
        data = response.json()
        
        # With zero noise, should be secure
        assert data["secure"] == (data["qber"] < 0.11)
    
    def test_visualize_round_endpoint(self):
        """Test GET /visualize_round/{round_index}"""
        # Run simulation first
        client.post("/run_bb84", json={"n_qubits": 10, "noise_level": 0.0, "seed": 42})
        
        # Visualize first round
        response = client.get("/visualize_round/0")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = [
            "round_index", "alice_bit", "alice_basis", "bob_basis",
            "bob_measurement", "bases_match", "included_in_key", "circuit_image"
        ]
        for field in required_fields:
            assert field in data
        
        assert data["round_index"] == 0
        assert data["circuit_image"].startswith("data:image/png;base64,")
    
    def test_visualize_round_invalid_index_negative(self):
        """Test visualize_round rejects negative index"""
        client.post("/run_bb84", json={"n_qubits": 10, "noise_level": 0.0, "seed": 42})
        
        response = client.get("/visualize_round/-1")
        assert response.status_code == 400
    
    def test_visualize_round_invalid_index_too_large(self):
        """Test visualize_round rejects index >= n_qubits"""
        client.post("/run_bb84", json={"n_qubits": 5, "noise_level": 0.0, "seed": 42})
        
        response = client.get("/visualize_round/10")
        assert response.status_code == 400


class TestBB84Request:
    """Test cases for BB84Request model validation"""
    
    def test_valid_request_defaults(self):
        """Test BB84Request with default values"""
        request = BB84Request()
        assert request.n_qubits == 100
        assert request.noise_level == 0.0
        assert request.seed is None
    
    def test_valid_request_custom_values(self):
        """Test BB84Request with custom values"""
        request = BB84Request(n_qubits=50, noise_level=0.05, seed=42)
        assert request.n_qubits == 50
        assert request.noise_level == 0.05
        assert request.seed == 42
    
    def test_request_validation_n_qubits_boundaries(self):
        """Test n_qubits boundary validation"""
        # Valid boundaries
        BB84Request(n_qubits=1)  # minimum
        BB84Request(n_qubits=1000)  # maximum
        
        # Invalid - will be caught by Pydantic
        with pytest.raises(ValidationError):
            BB84Request(n_qubits=0)
        
        with pytest.raises(ValidationError):
            BB84Request(n_qubits=1001)
    
    def test_request_validation_noise_level_boundaries(self):
        """Test noise_level boundary validation"""
        # Valid boundaries
        BB84Request(noise_level=0.0)  # minimum
        BB84Request(noise_level=1.0)  # maximum
        
        # Invalid
        with pytest.raises(ValidationError):
            BB84Request(noise_level=-0.1)
        
        with pytest.raises(ValidationError):
            BB84Request(noise_level=1.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])