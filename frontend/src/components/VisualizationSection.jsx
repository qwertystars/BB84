import { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

function VisualizationSection({ data, apiBaseUrl }) {
  const [selectedRound, setSelectedRound] = useState(0);
  const [circuitImage, setCircuitImage] = useState(null);
  const [loadingCircuit, setLoadingCircuit] = useState(false);

  const { results, stats } = data;

  useEffect(() => {
    if (selectedRound !== null) {
      loadCircuitImage(selectedRound);
    }
  }, [selectedRound]);

  const loadCircuitImage = async (roundIndex) => {
    setLoadingCircuit(true);
    try {
      const response = await axios.get(`${apiBaseUrl}/visualize_round/${roundIndex}`);
      setCircuitImage(response.data);
    } catch (error) {
      console.error('Error loading circuit:', error);
    } finally {
      setLoadingCircuit(false);
    }
  };

  // Prepare chart data showing basis matching
  const basisMatchData = {
    labels: results.alice_bits.slice(0, 20).map((_, i) => `Q${i}`),
    datasets: [
      {
        label: 'Alice Basis (Z=0, X=1)',
        data: results.alice_bases.slice(0, 20).map(b => b === 'Z' ? 0 : 1),
        borderColor: 'rgb(99, 102, 241)',
        backgroundColor: 'rgba(99, 102, 241, 0.5)',
      },
      {
        label: 'Bob Basis (Z=0, X=1)',
        data: results.bob_bases.slice(0, 20).map(b => b === 'Z' ? 0 : 1),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Basis Comparison (First 20 Qubits)',
      },
    },
    scales: {
      y: {
        ticks: {
          callback: function(value) {
            return value === 0 ? 'Z' : 'X';
          }
        }
      }
    }
  };

  return (
    <div className="space-y-6 mb-8">
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Total Qubits</h3>
          <p className="text-3xl font-bold text-indigo-600">{stats.total_qubits}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Sifted Key Length</h3>
          <p className="text-3xl font-bold text-green-600">{stats.sifted_key_length}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Efficiency</h3>
          <p className="text-3xl font-bold text-blue-600">{(stats.efficiency * 100).toFixed(1)}%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-2">QBER</h3>
          <p className={`text-3xl font-bold ${stats.qber < 0.11 ? 'text-green-600' : 'text-red-600'}`}>
            {(stats.qber * 100).toFixed(2)}%
          </p>
        </div>
      </div>

      {/* Basis Comparison Chart */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Basis Comparison</h2>
        <Line options={chartOptions} data={basisMatchData} />
      </div>

      {/* Circuit Visualization */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Quantum Circuit Visualization</h2>
        <div className="mb-4">
          <label htmlFor="roundSelect" className="block text-sm font-medium text-gray-700 mb-2">
            Select Round (0 to {results.alice_bits.length - 1})
          </label>
          <input
            type="number"
            id="roundSelect"
            value={selectedRound}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              if (!isNaN(value) && value >= 0 && value < results.alice_bits.length) {
                setSelectedRound(value);
              }
            }}
            min="0"
            max={results.alice_bits.length - 1}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {loadingCircuit && (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-indigo-700"></div>
          </div>
        )}

        {circuitImage && !loadingCircuit && (
          <div>
            <div className="mb-4 p-4 bg-gray-50 rounded">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="font-medium">Alice's Bit:</span> {circuitImage.alice_bit}
                </div>
                <div>
                  <span className="font-medium">Alice's Basis:</span> {circuitImage.alice_basis}
                </div>
                <div>
                  <span className="font-medium">Bob's Basis:</span> {circuitImage.bob_basis}
                </div>
                <div>
                  <span className="font-medium">Bob's Measurement:</span> {circuitImage.bob_measurement}
                </div>
                <div className="col-span-2 md:col-span-4">
                  <span className="font-medium">Bases Match:</span>{' '}
                  <span className={circuitImage.bases_match ? 'text-green-600 font-bold' : 'text-red-600 font-bold'}>
                    {circuitImage.bases_match ? 'Yes ✓' : 'No ✗'}
                  </span>
                </div>
              </div>
            </div>
            <img
              src={circuitImage.circuit_image}
              alt="Quantum Circuit"
              className="w-full border border-gray-200 rounded"
            />
          </div>
        )}
      </div>

      {/* Bit-Basis Comparison Table */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Bit-Basis Comparison Table</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Round</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Alice Bit</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Alice Basis</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bob Basis</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bob Measured</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Match</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {results.alice_bits.slice(0, 20).map((bit, i) => {
                const basesMatch = results.alice_bases[i] === results.bob_bases[i];
                return (
                  <tr key={i} className={basesMatch ? 'bg-green-50' : ''}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm">{i}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-mono">{bit}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-mono">{results.alice_bases[i]}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-mono">{results.bob_bases[i]}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-mono">{results.bob_measurements[i]}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm">
                      {basesMatch ? (
                        <span className="text-green-600 font-bold">✓</span>
                      ) : (
                        <span className="text-red-600 font-bold">✗</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {results.alice_bits.length > 20 && (
            <p className="text-sm text-gray-500 mt-4 text-center">
              Showing first 20 of {results.alice_bits.length} rounds
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default VisualizationSection;
