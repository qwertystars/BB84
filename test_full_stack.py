#!/usr/bin/env python3
"""
Comprehensive test script for BB84 QKD Simulator
Tests all backend endpoints and functionality
"""

import requests
import json
import sys

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("  ✓ Health check passed")

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{API_BASE}/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    print("  ✓ Root endpoint passed")

def test_simulation():
    """Test BB84 simulation"""
    print("🔍 Testing BB84 simulation...")

    # Test with various parameters
    test_cases = [
        {"n_qubits": 10, "noise_level": 0.0, "seed": 42},
        {"n_qubits": 50, "noise_level": 0.05, "seed": 123},
        {"n_qubits": 100, "noise_level": 0.1, "seed": None},
    ]

    for i, params in enumerate(test_cases, 1):
        print(f"  Test case {i}: {params}")
        response = requests.post(f"{API_BASE}/run_bb84", json=params)
        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert data["status"] == "success"
        assert "summary" in data
        assert data["summary"]["total_qubits"] == params["n_qubits"]
        assert 0 <= data["summary"]["efficiency"] <= 1
        assert 0 <= data["summary"]["qber"] <= 1

        # For zero noise, QBER should be 0
        if params["noise_level"] == 0.0:
            assert data["summary"]["qber"] == 0.0, f"Expected QBER 0 but got {data['summary']['qber']}"

        print(f"    ✓ Simulation successful - QBER: {data['summary']['qber']*100:.2f}%, Efficiency: {data['summary']['efficiency']*100:.1f}%")

def test_results():
    """Test results endpoint"""
    print("🔍 Testing results endpoint...")

    # First run a simulation
    requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 20, "noise_level": 0.0, "seed": 42})

    # Get results
    response = requests.get(f"{API_BASE}/results")
    assert response.status_code == 200
    data = response.json()

    # Check all required fields
    required_fields = ["alice_bits", "alice_bases", "bob_bases", "bob_measurements",
                      "sifted_key_alice", "sifted_key_bob", "matching_bases"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    # Check data consistency
    assert len(data["alice_bits"]) == 20
    assert len(data["alice_bases"]) == 20
    assert len(data["bob_bases"]) == 20
    assert len(data["bob_measurements"]) == 20

    # Check sifted keys have same length
    assert len(data["sifted_key_alice"]) == len(data["sifted_key_bob"])

    print(f"  ✓ Results retrieved - {len(data['alice_bits'])} qubits, {len(data['sifted_key_alice'])} sifted bits")

def test_stats():
    """Test stats endpoint"""
    print("🔍 Testing stats endpoint...")

    response = requests.get(f"{API_BASE}/stats")
    assert response.status_code == 200
    data = response.json()

    required_fields = ["qber", "total_qubits", "sifted_key_length", "efficiency",
                      "matching_bases_count", "error_count", "secure"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    # Check value ranges
    assert 0 <= data["qber"] <= 1
    assert 0 <= data["efficiency"] <= 1
    assert data["total_qubits"] > 0
    assert data["sifted_key_length"] <= data["total_qubits"]

    print(f"  ✓ Stats retrieved - QBER: {data['qber']*100:.3f}%, Efficiency: {data['efficiency']*100:.1f}%")

def test_visualization():
    """Test circuit visualization endpoint"""
    print("🔍 Testing circuit visualization...")

    # Run simulation first
    requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 5, "noise_level": 0.0, "seed": 42})

    # Test visualization for first circuit
    response = requests.get(f"{API_BASE}/visualize_round/0")
    assert response.status_code == 200
    data = response.json()

    # Check required fields
    required_fields = ["round_index", "alice_bit", "alice_basis", "bob_basis",
                      "bob_measurement", "bases_match", "circuit_image"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    # Check circuit image is base64
    assert data["circuit_image"].startswith("data:image/png;base64,")
    assert len(data["circuit_image"]) > 1000  # Should be a reasonable size image

    print(f"  ✓ Visualization retrieved - Round {data['round_index']}, Image size: {len(data['circuit_image'])} chars")

def test_error_handling():
    """Test error handling"""
    print("🔍 Testing error handling...")

    # Test invalid parameters
    response = requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 0, "noise_level": 0.0})
    assert response.status_code == 422  # Validation error

    response = requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 2000, "noise_level": 0.0})
    assert response.status_code == 422  # Validation error

    response = requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 10, "noise_level": 2.0})
    assert response.status_code == 422  # Validation error

    # Test invalid visualization round
    requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 5, "noise_level": 0.0})
    response = requests.get(f"{API_BASE}/visualize_round/100")
    assert response.status_code == 400

    print("  ✓ Error handling working correctly")

def test_bb84_correctness():
    """Test BB84 protocol correctness"""
    print("🔍 Testing BB84 protocol correctness...")

    # With zero noise and same seed, results should be deterministic
    requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 100, "noise_level": 0.0, "seed": 12345})
    results1 = requests.get(f"{API_BASE}/results").json()

    requests.post(f"{API_BASE}/run_bb84", json={"n_qubits": 100, "noise_level": 0.0, "seed": 12345})
    results2 = requests.get(f"{API_BASE}/results").json()

    # Results should be identical
    assert results1["alice_bits"] == results2["alice_bits"]
    assert results1["alice_bases"] == results2["alice_bases"]
    assert results1["bob_bases"] == results2["bob_bases"]

    # With zero noise, sifted keys should match perfectly
    assert results1["sifted_key_alice"] == results1["sifted_key_bob"]

    # Check that only matching bases are in sifted key
    matching_count = sum(1 for i in range(len(results1["alice_bases"]))
                        if results1["alice_bases"][i] == results1["bob_bases"][i])
    assert len(results1["sifted_key_alice"]) == matching_count

    print(f"  ✓ BB84 protocol logic verified - {matching_count}/{len(results1['alice_bits'])} bases matched")

def main():
    """Run all tests"""
    print("=" * 60)
    print("BB84 QKD Simulator - Full Stack Test Suite")
    print("=" * 60)
    print()

    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("BB84 Simulation", test_simulation),
        ("Results Retrieval", test_results),
        ("Statistics", test_stats),
        ("Circuit Visualization", test_visualization),
        ("Error Handling", test_error_handling),
        ("BB84 Protocol Correctness", test_bb84_correctness),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
            print()
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
            print()

    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("🎉 All tests passed! The BB84 simulator is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
