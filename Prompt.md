You are an expert full-stack AI developer and quantum computing engineer.

Build a complete full-stack web application that simulates the BB84 Quantum Key Distribution (QKD) protocol, using the following specifications and workflow.


---

🧠 Overall Goal

Create an interactive web app that:

1. Simulates the BB84 protocol end-to-end using Qiskit (Python backend with FastAPI).


2. Lets users visualize quantum states, bases, and measurement outcomes.


3. Displays key sifting and QBER (Quantum Bit Error Rate).


4. Runs locally or deploys easily to cloud (e.g., Render, Vercel + Railway).




---

⚙️ Backend (FastAPI + Qiskit)

Use FastAPI for backend API endpoints.

Include endpoints to:

/run_bb84 → runs full simulation with parameters: number of qubits (N), noise level, random seed.

/visualize_round → returns per-round circuit diagram (in SVG or base64 image).

/results → returns JSON of Alice’s bits, bases, Bob’s bases, and measured bits.

/stats → computes and returns final shared key and QBER.


Use Qiskit AerSimulator for simulation and noise injection.

Backend flow should follow these steps:

1. Setup environment

pip install fastapi uvicorn qiskit qiskit-aer numpy matplotlib


2. Import essentials

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
import numpy as np


3. Define BB84 preparation function

def prepare_bb84_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if basis == 'X':
        qc.h(0)
    if bit == 1:
        qc.x(0)
    return qc


4. Random bits and bases

N = params['N']
alice_bits = np.random.randint(0, 2, N)
alice_bases = np.random.randint(0, 2, N)
bob_bases = np.random.randint(0, 2, N)


5. Build and run circuits

circuits = []
for bit, a_basis, b_basis in zip(alice_bits, alice_bases, bob_bases):
    qc = prepare_bb84_qubit(bit, 'X' if a_basis else 'Z')
    if b_basis == 1:
        qc.h(0)
    qc.measure(0, 0)
    circuits.append(qc)
simulator = AerSimulator()
results = simulator.run(circuits, shots=1).result()


6. Return results as JSON




---

🎨 Frontend (React + Tailwind + Chart.js)

Frontend should be a modern single-page interface (React preferred).

Main components:

1. Control Panel

Inputs: Number of qubits, Noise level, Seed

Button: “Run Simulation”



2. Visualization Section

Quantum Circuits Viewer: display per-round circuit SVGs (from backend)

Bit Basis Comparison Table

Key Sifting Animation (Alice vs Bob)

QBER Gauge Chart



3. Results Dashboard

Display: Alice’s bits/bases, Bob’s bits/bases, sifted key, QBER.

Download results as CSV.




Use TailwindCSS for styling, React Query or Axios for API calls, and Recharts/Chart.js for QBER plots.


---

🌐 Data Flow

graph LR
A[Frontend (React)] -->|POST /run_bb84| B[FastAPI Backend]
B -->|Run Simulation with Qiskit| C[AerSimulator]
C -->|Results (bits, bases, outcomes)| B
B -->|JSON Response| A
A -->|Render Results| D[Visualization Dashboard]


---

🧩 Optional Enhancements

Add noise models (e.g., depolarizing, bit-flip) to show QBER impact.

Animate photon polarization using Three.js.

Include educational tooltips explaining bases, qubits, and measurement.

Allow seed input to reproduce same results.

Add downloadable report of simulation data and charts.



---

🧱 Deliverables

The AI should output:

1. backend/main.py — FastAPI code with BB84 logic and endpoints.


2. frontend/ — React app with TailwindCSS, Axios, and visualization components.


3. README.md — setup + architecture diagram (use Mermaid for flow).


4. Optional: Dockerfile for full-stack deployment.
