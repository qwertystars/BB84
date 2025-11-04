import { useState } from 'react';

function ControlPanel({ onRunSimulation, loading }) {
  const [nQubits, setNQubits] = useState(50);
  const [noiseLevel, setNoiseLevel] = useState(0.0);
  const [seed, setSeed] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onRunSimulation({
      nQubits: parseInt(nQubits),
      noiseLevel: parseFloat(noiseLevel),
      seed: seed ? parseInt(seed) : null
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Control Panel</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="nQubits" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Qubits
            </label>
            <input
              type="number"
              id="nQubits"
              value={nQubits}
              onChange={(e) => setNQubits(e.target.value)}
              min="1"
              max="1000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">Range: 1-1000</p>
          </div>

          <div>
            <label htmlFor="noiseLevel" className="block text-sm font-medium text-gray-700 mb-2">
              Noise Level
            </label>
            <input
              type="number"
              id="noiseLevel"
              value={noiseLevel}
              onChange={(e) => setNoiseLevel(e.target.value)}
              min="0"
              max="1"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">Range: 0.0-1.0</p>
          </div>

          <div>
            <label htmlFor="seed" className="block text-sm font-medium text-gray-700 mb-2">
              Random Seed (Optional)
            </label>
            <input
              type="number"
              id="seed"
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              placeholder="Leave empty for random"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">For reproducibility</p>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Running Simulation...' : 'Run Simulation'}
        </button>
      </form>
    </div>
  );
}

export default ControlPanel;
