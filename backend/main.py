from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np
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
    n_qubits: int = 100
    noise_level: float = 0.0
    seed: Optional[int] = None

class BB84Results:
    def __init__(self):
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_measurements = []
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        self.qber = 0.0
        self.circuits = []

# Thread-safe storage for simulation results
# Note: For production use, consider using Redis or a database for scalability
latest_results = None
results_lock = threading.Lock()

def prepare_bb84_qubit(bit: int, basis: str) -> QuantumCircuit:
    """
    Prepare a qubit for BB84 protocol.
    
    Args:
        bit: The bit value (0 or 1) to encode
        basis: The basis to use ('Z' for computational, 'X' for Hadamard)
    
    Returns:
        QuantumCircuit with prepared qubit
    """
    qc = QuantumCircuit(1, 1)
    
    # Encode the bit
    if bit == 1:
        qc.x(0)
    
    # Apply basis
    if basis == 'X':
        qc.h(0)
    
    return qc

def measure_bb84_qubit(qc: QuantumCircuit, basis: str) -> QuantumCircuit:
    """
    Measure a qubit in the specified basis.
    
    Args:
        qc: The quantum circuit to measure
        basis: The basis to measure in ('Z' or 'X')
    
    Returns:
        QuantumCircuit with measurement added
    """
    if basis == 'X':
        qc.h(0)
    qc.measure(0, 0)
    return qc

def simulate_bb84(n_qubits: int, noise_level: float = 0.0, seed: Optional[int] = None) -> BB84Results:
    """
    Simulate the BB84 protocol.
    
    Args:
        n_qubits: Number of qubits to simulate
        noise_level: Noise level (0.0 to 1.0)
        seed: Random seed for reproducibility
    
    Returns:
        BB84Results object containing all simulation data
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = BB84Results()
    
    # Step 1: Alice generates random bits and bases
    results.alice_bits = np.random.randint(0, 2, n_qubits).tolist()
    results.alice_bases = ['Z' if b == 0 else 'X' for b in np.random.randint(0, 2, n_qubits)]
    
    # Step 2: Bob chooses random measurement bases
    results.bob_bases = ['Z' if b == 0 else 'X' for b in np.random.randint(0, 2, n_qubits)]
    
    # Step 3: Prepare simulator with optional noise
    simulator = AerSimulator()
    if noise_level > 0:
        noise_model = NoiseModel()
        error = depolarizing_error(noise_level, 1)
        noise_model.add_all_qubit_quantum_error(error, ['x', 'h'])
        simulator = AerSimulator(noise_model=noise_model)
    
    # Step 4: Simulate each qubit transmission
    for i in range(n_qubits):
        # Alice prepares qubit
        qc = prepare_bb84_qubit(results.alice_bits[i], results.alice_bases[i])
        
        # Bob measures qubit
        qc = measure_bb84_qubit(qc, results.bob_bases[i])
        
        # Store circuit for visualization
        results.circuits.append(qc)
        
        # Run simulation
        job = simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        
        # Get measurement result
        measured_bit = int(list(counts.keys())[0])
        results.bob_measurements.append(measured_bit)
    
    # Step 5: Key sifting - keep only bits where bases match
    for i in range(n_qubits):
        if results.alice_bases[i] == results.bob_bases[i]:
            results.sifted_key_alice.append(results.alice_bits[i])
            results.sifted_key_bob.append(results.bob_measurements[i])
    
    # Step 6: Calculate QBER (Quantum Bit Error Rate)
    if len(results.sifted_key_alice) > 0:
        errors = sum([1 for a, b in zip(results.sifted_key_alice, results.sifted_key_bob) if a != b])
        results.qber = errors / len(results.sifted_key_alice)
    else:
        results.qber = 0.0
    
    return results

@app.get("/")
async def root():
    return {
        "message": "BB84 Quantum Key Distribution Simulator API",
        "version": "1.0.0",
        "endpoints": {
            "/run_bb84": "POST - Run BB84 simulation",
            "/results": "GET - Get latest simulation results",
            "/stats": "GET - Get statistics from latest simulation",
            "/visualize_round": "GET - Get circuit visualization for specific round"
        }
    }

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
        # Validate input
        if request.n_qubits < 1 or request.n_qubits > 1000:
            raise HTTPException(status_code=400, detail="n_qubits must be between 1 and 1000")
        
        if request.noise_level < 0 or request.noise_level > 1:
            raise HTTPException(status_code=400, detail="noise_level must be between 0 and 1")
        
        # Run simulation
        results = simulate_bb84(request.n_qubits, request.noise_level, request.seed)
        
        # Thread-safe update of global results
        with results_lock:
            latest_results = results
        
        return {
            "status": "success",
            "message": "BB84 simulation completed",
            "n_qubits": request.n_qubits,
            "noise_level": request.noise_level,
            "sifted_key_length": len(results.sifted_key_alice),
            "qber": results.qber
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
            raise HTTPException(status_code=404, detail="No simulation results available. Run /run_bb84 first.")
        
        return {
            "alice_bits": latest_results.alice_bits,
            "alice_bases": latest_results.alice_bases,
            "bob_bases": latest_results.bob_bases,
            "bob_measurements": latest_results.bob_measurements,
            "sifted_key_alice": latest_results.sifted_key_alice,
            "sifted_key_bob": latest_results.sifted_key_bob,
            "matching_bases": [
                i for i in range(len(latest_results.alice_bases))
                if latest_results.alice_bases[i] == latest_results.bob_bases[i]
            ]
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
            raise HTTPException(status_code=404, detail="No simulation results available. Run /run_bb84 first.")
        
        total_qubits = len(latest_results.alice_bits)
        sifted_length = len(latest_results.sifted_key_alice)
        efficiency = sifted_length / total_qubits if total_qubits > 0 else 0
        
        return {
            "qber": latest_results.qber,
            "total_qubits": total_qubits,
            "sifted_key_length": sifted_length,
            "efficiency": efficiency,
            "matching_bases_count": sifted_length,
            "error_count": sum([1 for a, b in zip(latest_results.sifted_key_alice, latest_results.sifted_key_bob) if a != b])
        }

@app.get("/visualize_round/{round_index}")
async def visualize_round(round_index: int):
    """
    Get a visualization of a specific round's quantum circuit.
    
    Args:
        round_index: The index of the round to visualize (0-based)
    
    Returns:
        Base64-encoded PNG image of the circuit diagram
    """
    with results_lock:
        if latest_results is None:
            raise HTTPException(status_code=404, detail="No simulation results available. Run /run_bb84 first.")
        
        if round_index < 0 or round_index >= len(latest_results.circuits):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid round_index. Must be between 0 and {len(latest_results.circuits) - 1}"
            )
        
        try:
            # Get the circuit for this round
            circuit = latest_results.circuits[round_index]
            
            # Draw circuit
            fig, ax = plt.subplots(figsize=(8, 3))
            circuit.draw('mpl', ax=ax)
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close(fig)
            
            return {
                "round_index": round_index,
                "alice_bit": latest_results.alice_bits[round_index],
                "alice_basis": latest_results.alice_bases[round_index],
                "bob_basis": latest_results.bob_bases[round_index],
                "bob_measurement": latest_results.bob_measurements[round_index],
                "bases_match": latest_results.alice_bases[round_index] == latest_results.bob_bases[round_index],
                "circuit_image": f"data:image/png;base64,{image_base64}"
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Visualization failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
