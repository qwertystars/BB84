from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class ScenarioType(str, Enum):
    IDEAL = "ideal"
    ERROR_ONLY = "error-only"
    ERROR_EVE = "error-eve"
    DECOHERENCE_FREE = "decoherence-free"

class SimulationRequest(BaseModel):
    qubit_count: int = Field(default=100, ge=10, le=1000, description="Number of qubits to simulate")
    error_rate: Optional[float] = Field(default=0.0, ge=0.0, le=0.5, description="Channel error rate")
    eve_fraction: Optional[float] = Field(default=0.5, ge=0.0, le=1.0, description="Fraction of qubits intercepted by Eve")

class SimulationResult(BaseModel):
    scenario: str
    qubit_count: int
    sifted_key: str
    sifted_key_length: int
    qber: float
    error_rate: Optional[float]
    eve_fraction: Optional[float]
    summary: Dict[str, Any]
    execution_time: float

class ScenarioInfo(BaseModel):
    id: str
    name: str
    description: str
    parameters: Dict[str, Any]

class ScenariosResponse(BaseModel):
    scenarios: List[ScenarioInfo]
