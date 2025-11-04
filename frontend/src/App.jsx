import { useState } from 'react';
import axios from 'axios';
import ControlPanel from './components/ControlPanel';
import VisualizationSection from './components/VisualizationSection';
import ResultsDashboard from './components/ResultsDashboard';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runSimulation = async (params) => {
    setLoading(true);
    setError(null);
    setSimulationData(null);

    try {
      // Run the simulation
      const runResponse = await axios.post(`${API_BASE_URL}/run_bb84`, {
        n_qubits: params.nQubits,
        noise_level: params.noiseLevel,
        seed: params.seed || null
      });

      // Get the detailed results
      const resultsResponse = await axios.get(`${API_BASE_URL}/results`);
      const statsResponse = await axios.get(`${API_BASE_URL}/stats`);

      setSimulationData({
        summary: runResponse.data,
        results: resultsResponse.data,
        stats: statsResponse.data
      });
    } catch (err) {
      console.error('Simulation error:', err);
      setError(err.response?.data?.detail || err.message || 'Simulation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-5xl font-bold text-indigo-900 mb-2">
            BB84 Quantum Key Distribution
          </h1>
          <p className="text-lg text-gray-700">
            Interactive Quantum Cryptography Simulator
          </p>
        </header>

        <ControlPanel onRunSimulation={runSimulation} loading={loading} />

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <strong className="font-bold">Error: </strong>
            <span>{error}</span>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-700"></div>
          </div>
        )}

        {simulationData && !loading && (
          <>
            <VisualizationSection 
              data={simulationData} 
              apiBaseUrl={API_BASE_URL}
            />
            <ResultsDashboard data={simulationData} />
          </>
        )}

        {!simulationData && !loading && !error && (
          <div className="text-center py-12 text-gray-500">
            <p className="text-xl">
              Configure parameters above and click "Run Simulation" to begin
            </p>
          </div>
        )}
      </div>

      <footer className="bg-indigo-900 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">
            BB84 Protocol Simulator | Built with FastAPI, Qiskit, and React
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
