from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn

from models import SimulationRequest, SimulationResult, ScenariosResponse, ScenarioInfo, ScenarioType
from simulations.ideal import simulate_ideal
from simulations.error_only import simulate_error_only
from simulations.error_with_eve import simulate_error_with_eve
from simulations.decoherence_free import simulate_decoherence_free

app = FastAPI(
    title="BB84 Quantum Key Distribution Simulator",
    description="A simulator for BB84 quantum key distribution protocol with various scenarios",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bb84.srijan.dpdns.org", "https://bb84-api.srijan.dpdns.org", "http://localhost:5173", "http://localhost:3000"],  # Production domains and development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulation functions mapping
SIMULATION_FUNCTIONS = {
    ScenarioType.IDEAL: simulate_ideal,
    ScenarioType.ERROR_ONLY: simulate_error_only,
    ScenarioType.ERROR_EVE: simulate_error_with_eve,
    ScenarioType.DECOHERENCE_FREE: simulate_decoherence_free,
}

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "BB84 Quantum Key Distribution Simulator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/scenarios", response_model=ScenariosResponse)
async def get_scenarios():
    """Get list of available simulation scenarios."""
    scenarios = [
        ScenarioInfo(
            id=ScenarioType.IDEAL,
            name="Ideal Conditions",
            description="Perfect BB84 protocol with no errors or eavesdropping",
            parameters={
                "qubit_count": {"default": 100, "min": 10, "max": 1000},
                "error_rate": {"default": 0.0, "min": 0.0, "max": 0.0},
                "eve_fraction": {"default": 0.0, "min": 0.0, "max": 0.0}
            }
        ),
        ScenarioInfo(
            id=ScenarioType.ERROR_ONLY,
            name="Channel with Random Error",
            description="BB84 protocol with channel noise but no eavesdropping",
            parameters={
                "qubit_count": {"default": 100, "min": 10, "max": 1000},
                "error_rate": {"default": 0.1, "min": 0.0, "max": 0.5},
                "eve_fraction": {"default": 0.0, "min": 0.0, "max": 0.0}
            }
        ),
        ScenarioInfo(
            id=ScenarioType.ERROR_EVE,
            name="Error with Eavesdropping",
            description="BB84 protocol with channel noise and Eve's intercept-resend attack",
            parameters={
                "qubit_count": {"default": 100, "min": 10, "max": 1000},
                "error_rate": {"default": 0.05, "min": 0.0, "max": 0.5},
                "eve_fraction": {"default": 0.5, "min": 0.0, "max": 1.0}
            }
        ),
        ScenarioInfo(
            id=ScenarioType.DECOHERENCE_FREE,
            name="Decoherence-Free Space",
            description="Theoretical scenario where quantum coherence is preserved even with eavesdropping",
            parameters={
                "qubit_count": {"default": 100, "min": 10, "max": 1000},
                "error_rate": {"default": 0.0, "min": 0.0, "max": 0.0},
                "eve_fraction": {"default": 0.5, "min": 0.0, "max": 1.0}
            }
        ),
    ]
    return ScenariosResponse(scenarios=scenarios)

@app.post("/simulate/{scenario}", response_model=SimulationResult)
async def run_simulation(scenario: ScenarioType, request: SimulationRequest):
    """Run a BB84 simulation for the specified scenario."""
    try:
        if scenario not in SIMULATION_FUNCTIONS:
            raise HTTPException(status_code=400, detail="Invalid scenario type")
        
        simulation_func = SIMULATION_FUNCTIONS[scenario]
        
        # Prepare parameters for the simulation
        params = request.model_dump()
        
        # Run the simulation
        result = simulation_func(**params)
        
        return SimulationResult(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/simulate/{scenario}", response_model=SimulationResult)
async def run_simulation_get(scenario: ScenarioType, qubit_count: int = 100, error_rate: float = 0.0, eve_fraction: float = 0.0):
    """Run a BB84 simulation using GET request with query parameters."""
    try:
        if scenario not in SIMULATION_FUNCTIONS:
            raise HTTPException(status_code=400, detail="Invalid scenario type")
        
        simulation_func = SIMULATION_FUNCTIONS[scenario]
        
        # Prepare parameters for the simulation
        params = {
            "qubit_count": qubit_count,
            "error_rate": error_rate,
            "eve_fraction": eve_fraction
        }
        
        # Run the simulation
        result = simulation_func(**params)
        
        return SimulationResult(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
