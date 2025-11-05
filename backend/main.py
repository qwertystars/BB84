from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Optional
import threading

app = FastAPI(title="BB84 Quantum Key Distribution Simulator")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BB84Request(BaseModel):
    n_qubits: int = Field(default=100, ge=1, le=1000, description="Number of qubits (1-1000)")
    noise_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Noise level (0.0-1.0)")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")

class BB84Results:
    """Thread-safe storage for BB84 simulation results"""
    def __init__(self):
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_measurements = []
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        self.qber = 0.0
        self.circuits = []
        self.lock = threading.Lock()

# Global storage for simulation results
latest_results = None
results_lock = threading.Lock()

def prepare_bb84_qubit(bit: int, basis: str) -> QuantumCircuit:
    """
    Prepare a qubit for BB84 protocol (Alice's side).

    Args:
        bit: The bit value (0 or 1) to encode
        basis: The basis to use ('Z' for computational, 'X' for Hadamard)

    Returns:
        QuantumCircuit with prepared qubit

    BB84 Encoding:
        - Basis Z, Bit 0: |0⟩ state
        - Basis Z, Bit 1: |1⟩ state (apply X gate)
        - Basis X, Bit 0: |+⟩ state (apply H gate)
        - Basis X, Bit 1: |−⟩ state (apply X then H gate)
    """
    qc = QuantumCircuit(1, 1)

    # Encode the bit: if bit is 1, apply X gate to flip |0⟩ to |1⟩
    if bit == 1:
        qc.x(0)

    # Apply basis transformation: if X basis, apply Hadamard
    if basis == 'X':
        qc.h(0)

    return qc

def measure_bb84_qubit(qc: QuantumCircuit, basis: str) -> QuantumCircuit:
    """
    Add measurement to quantum circuit in the specified basis (Bob's side).

    Args:
        qc: The quantum circuit to measure
        basis: The basis to measure in ('Z' or 'X')

    Returns:
        QuantumCircuit with measurement added

    Measurement:
        - Z basis: Direct measurement in computational basis
        - X basis: Apply H gate before measurement (converts X basis to Z basis)
    """
    # If measuring in X basis, apply Hadamard to convert to Z basis
    if basis == 'X':
        qc.h(0)

    # Measure the qubit
    qc.measure(0, 0)
    return qc

def simulate_bb84(n_qubits: int, noise_level: float = 0.0, seed: Optional[int] = None) -> BB84Results:
    """
    Simulate the complete BB84 quantum key distribution protocol.

    Args:
        n_qubits: Number of qubits to simulate
        noise_level: Depolarizing noise level (0.0 to 1.0)
        seed: Random seed for reproducibility

    Returns:
        BB84Results object containing all simulation data

    BB84 Protocol Steps:
        1. Alice generates random bits and bases
        2. Alice prepares qubits based on her bits and bases
        3. Bob chooses random measurement bases
        4. Bob measures qubits in his chosen bases
        5. Alice and Bob compare bases (classical communication)
        6. Keep only bits where bases match (key sifting)
        7. Calculate QBER to detect eavesdropping/noise
    """
    # Set random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    results = BB84Results()

    # Step 1: Alice generates random bits and bases
    results.alice_bits = np.random.randint(0, 2, n_qubits).tolist()
    alice_bases_int = np.random.randint(0, 2, n_qubits)
    results.alice_bases = ['Z' if b == 0 else 'X' for b in alice_bases_int]

    # Step 2: Bob chooses random measurement bases
    bob_bases_int = np.random.randint(0, 2, n_qubits)
    results.bob_bases = ['Z' if b == 0 else 'X' for b in bob_bases_int]

    # Step 3: Setup simulator with optional noise model
    simulator = AerSimulator()

    if noise_level > 0:
        # Create noise model with depolarizing error
        noise_model = NoiseModel()
        # Apply depolarizing error to single-qubit gates
        error = depolarizing_error(noise_level, 1)
        # Add error to all single-qubit gates
        noise_model.add_all_qubit_quantum_error(error, ['x', 'h', 'id'])
        simulator = AerSimulator(noise_model=noise_model)

    # Step 4: Simulate each qubit transmission
    for i in range(n_qubits):
        # Alice prepares the qubit
        qc = prepare_bb84_qubit(results.alice_bits[i], results.alice_bases[i])

        # Bob measures the qubit
        qc = measure_bb84_qubit(qc, results.bob_bases[i])

        # Store circuit for visualization
        results.circuits.append(qc.copy())

        # Run simulation with a single shot
        try:
            job = simulator.run(qc, shots=1, seed_simulator=seed if seed else None)
            result = job.result()
            counts = result.get_counts(qc)

            # Get measurement result (extract the measured bit)
            measured_bit = int(list(counts.keys())[0])
            results.bob_measurements.append(measured_bit)
        except Exception as e:
            raise RuntimeError(f"Simulation failed at qubit {i}: {str(e)}")

    # Step 5: Key sifting - keep only bits where bases match
    for i in range(n_qubits):
        if results.alice_bases[i] == results.bob_bases[i]:
            results.sifted_key_alice.append(results.alice_bits[i])
            results.sifted_key_bob.append(results.bob_measurements[i])

    # Step 6: Calculate QBER (Quantum Bit Error Rate)
    if len(results.sifted_key_alice) > 0:
        errors = sum(1 for a, b in zip(results.sifted_key_alice, results.sifted_key_bob) if a != b)
        results.qber = errors / len(results.sifted_key_alice)
    else:
        results.qber = 0.0

    return results

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "BB84 Quantum Key Distribution Simulator API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "/run_bb84": "POST - Run BB84 simulation with parameters",
            "/results": "GET - Get detailed results from latest simulation",
            "/stats": "GET - Get statistics from latest simulation",
            "/visualize_round/{round_index}": "GET - Get circuit visualization for specific round",
            "/docs": "GET - Interactive API documentation",
            "/health": "GET - Health check endpoint"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "BB84 Simulator"}

@app.post("/run_bb84")
async def run_bb84(request: BB84Request):
    """
    Run a complete BB84 simulation.

    Args:
        request: BB84Request containing n_qubits, noise_level, and optional seed

    Returns:
        Summary of the simulation results
    """
    global latest_results

    try:
        # Run simulation
        results = simulate_bb84(request.n_qubits, request.noise_level, request.seed)

        # Thread-safe update of global results
        with results_lock:
            latest_results = results

        return {
            "status": "success",
            "message": "BB84 simulation completed successfully",
            "parameters": {
                "n_qubits": request.n_qubits,
                "noise_level": request.noise_level,
                "seed": request.seed
            },
            "summary": {
                "total_qubits": request.n_qubits,
                "sifted_key_length": len(results.sifted_key_alice),
                "efficiency": len(results.sifted_key_alice) / request.n_qubits if request.n_qubits > 0 else 0,
                "qber": results.qber,
                "secure": results.qber < 0.11
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/results")
async def get_results():
    """
    Get the full results of the latest BB84 simulation.

    Returns:
        Complete simulation data including bits, bases, and measurements
    """
    with results_lock:
        if latest_results is None:
            raise HTTPException(
                status_code=404,
                detail="No simulation results available. Please run /run_bb84 first."
            )

        # Find indices where bases match
        matching_indices = [
            i for i in range(len(latest_results.alice_bases))
            if latest_results.alice_bases[i] == latest_results.bob_bases[i]
        ]

        return {
            "alice_bits": latest_results.alice_bits,
            "alice_bases": latest_results.alice_bases,
            "bob_bases": latest_results.bob_bases,
            "bob_measurements": latest_results.bob_measurements,
            "sifted_key_alice": latest_results.sifted_key_alice,
            "sifted_key_bob": latest_results.sifted_key_bob,
            "matching_bases": matching_indices,
            "total_rounds": len(latest_results.alice_bits)
        }

@app.get("/stats")
async def get_stats():
    """
    Get statistics from the latest BB84 simulation.

    Returns:
        Statistics including QBER, key lengths, and efficiency
    """
    with results_lock:
        if latest_results is None:
            raise HTTPException(
                status_code=404,
                detail="No simulation results available. Please run /run_bb84 first."
            )

        total_qubits = len(latest_results.alice_bits)
        sifted_length = len(latest_results.sifted_key_alice)
        efficiency = sifted_length / total_qubits if total_qubits > 0 else 0
        error_count = sum(
            1 for a, b in zip(latest_results.sifted_key_alice, latest_results.sifted_key_bob)
            if a != b
        )

        return {
            "qber": latest_results.qber,
            "total_qubits": total_qubits,
            "sifted_key_length": sifted_length,
            "efficiency": efficiency,
            "matching_bases_count": sifted_length,
            "error_count": error_count,
            "secure": latest_results.qber < 0.11,
            "security_threshold": 0.11
        }

@app.get("/visualize_round/{round_index}")
async def visualize_round(round_index: int):
    """
    Get a visualization of a specific round's quantum circuit.

    Args:
        round_index: The index of the round to visualize (0-based)

    Returns:
        Base64-encoded PNG image of the circuit diagram with round details
    """
    with results_lock:
        if latest_results is None:
            raise HTTPException(
                status_code=404,
                detail="No simulation results available. Please run /run_bb84 first."
            )

        if round_index < 0 or round_index >= len(latest_results.circuits):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid round_index. Must be between 0 and {len(latest_results.circuits) - 1}"
            )

        try:
            # Get the circuit for this round
            circuit = latest_results.circuits[round_index]

            # Draw circuit as text (doesn't require pylatexenc)
            circuit_text = circuit.draw(output='text')

            # Create an image from the text representation
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.text(0.05, 0.5, str(circuit_text),
                   ha='left', va='center', fontsize=12, family='monospace',
                   transform=ax.transAxes, wrap=True)
            ax.axis('off')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=120, facecolor='white')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close(fig)

            # Get round details
            bases_match = latest_results.alice_bases[round_index] == latest_results.bob_bases[round_index]

            return {
                "round_index": round_index,
                "alice_bit": latest_results.alice_bits[round_index],
                "alice_basis": latest_results.alice_bases[round_index],
                "bob_basis": latest_results.bob_bases[round_index],
                "bob_measurement": latest_results.bob_measurements[round_index],
                "bases_match": bases_match,
                "included_in_key": bases_match,
                "circuit_image": f"data:image/png;base64,{image_base64}"
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Visualization failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting BB84 Quantum Key Distribution Simulator API...")
    print("API will be available at http://localhost:8000")
    print("API documentation at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
