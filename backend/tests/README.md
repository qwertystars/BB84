# BB84 Quantum Key Distribution Simulator - Unit Tests

This directory contains comprehensive unit tests for the BB84 QKD Simulator backend.

## Test Coverage

### Test Files

1. **test_main.py** - Main test suite covering:
   - `BB84Results` class initialization and thread safety
   - `prepare_bb84_qubit()` function - all 4 quantum state preparations
   - `measure_bb84_qubit()` function - Z and X basis measurements
   - `simulate_bb84()` function - complete BB84 protocol simulation
   - FastAPI endpoints (/, /health, /run_bb84, /results, /stats, /visualize_round)
   - Request validation (BB84Request model)
   - Edge cases and error handling

2. **test_requirements.py** - Dependency validation:
   - Requirements file existence and readability
   - Core dependencies presence
   - Version constraint validation

### Test Categories

#### Pure Function Tests
- **prepare_bb84_qubit**: Tests all 4 state preparations (|0⟩, |1⟩, |+⟩, |−⟩)
- **measure_bb84_qubit**: Tests Z and X basis measurements
- Validates quantum circuit structure and gate sequences

#### Simulation Logic Tests
- Deterministic behavior with seeds
- Non-deterministic behavior without seeds
- Key sifting correctness
- QBER calculation accuracy
- Zero noise produces zero QBER
- Noise increases QBER appropriately
- Statistical properties (50% efficiency, even bit/basis distribution)

#### API Endpoint Tests
- Root endpoint (/) information
- Health check (/health)
- Simulation execution (/run_bb84)
- Results retrieval (/results)
- Statistics (/stats)
- Circuit visualization (/visualize_round/{index})
- Input validation and error handling

#### Edge Cases
- Single qubit simulation
- Maximum qubits (1000)
- Zero and maximum noise levels
- Invalid parameter validation
- Boundary value testing

## Running the Tests

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or install test dependencies separately:

```bash
pip install -r test-requirements.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_main.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_main.py::TestPrepareBB84Qubit -v
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestPrepareBB84Qubit::test_prepare_bit_0_basis_z -v
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Run Only Fast Tests (exclude slow tests)

```bash
pytest tests/ -v -m "not slow"
```

## Test Structure

Each test class follows this pattern:

```python
class TestFeatureName:
    """Test cases for feature"""
    
    def test_happy_path(self):
        """Test normal/expected behavior"""
        # Arrange
        # Act
        # Assert
    
    def test_edge_case(self):
        """Test boundary conditions"""
        # Test edge cases
    
    def test_error_handling(self):
        """Test error conditions"""
        # Test exceptions
```

## Key Testing Principles

1. **Determinism**: Tests using seeds are deterministic and repeatable
2. **Isolation**: Each test is independent and doesn't affect others
3. **Clarity**: Test names clearly describe what is being tested
4. **Coverage**: Tests cover happy paths, edge cases, and error conditions
5. **Fast Execution**: Most tests run quickly; slow tests are marked

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Exit code 0 indicates all tests passed.

## Adding New Tests

When adding new features to the BB84 simulator:

1. Add corresponding test class to `test_main.py`
2. Test all public interfaces
3. Include edge cases and error conditions
4. Ensure tests are independent and repeatable
5. Use descriptive test names
6. Add docstrings explaining what is tested

## Test Metrics

Expected test execution time: < 30 seconds for full suite

Current test count: 50+ tests covering:
- Pure functions
- Simulation logic
- API endpoints
- Validation
- Edge cases
- Error handling