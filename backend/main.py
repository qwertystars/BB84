from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict, Any
import uvicorn
import os
from pathlib import Path

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
    allow_origins=["*"],  # Allow all origins for single service deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

# Simulation functions mapping
SIMULATION_FUNCTIONS = {
    ScenarioType.IDEAL: simulate_ideal,
    ScenarioType.ERROR_ONLY: simulate_error_only,
    ScenarioType.ERROR_EVE: simulate_error_with_eve,
    ScenarioType.DECOHERENCE_FREE: simulate_decoherence_free,
}

@app.get("/api", response_model=Dict[str, str])
@app.get("/api/", response_model=Dict[str, str])
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

# Mount static files if frontend dist exists
if FRONTEND_DIST.exists():
    # Mount static assets (JS, CSS, images, etc.)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    # Serve index.html for all other routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for all non-API routes."""
        # If it's an API route, let FastAPI handle it normally
        if full_path.startswith("api/") or full_path in ["scenarios", "docs", "redoc", "openapi.json"]:
            raise HTTPException(status_code=404, detail="Not found")

        # Check if the requested file exists in the dist directory
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(file_path)

        # Otherwise, serve index.html for client-side routing
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")
else:
    @app.get("/")
    async def frontend_not_built():
        return {
            "warning": "Frontend not built",
            "message": "Please build the frontend first by running: cd frontend && npm install && npm run build"
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
