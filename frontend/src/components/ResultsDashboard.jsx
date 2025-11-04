function ResultsDashboard({ data }) {
  const { results, stats } = data;

  const downloadCSV = () => {
    const headers = ['Round', 'Alice Bit', 'Alice Basis', 'Bob Basis', 'Bob Measurement', 'Bases Match'];
    const rows = results.alice_bits.map((bit, i) => [
      i,
      bit,
      results.alice_bases[i],
      results.bob_bases[i],
      results.bob_measurements[i],
      results.alice_bases[i] === results.bob_bases[i] ? 'Yes' : 'No'
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'bb84_simulation_results.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Results Dashboard</h2>
        <button
          onClick={downloadCSV}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition duration-200"
        >
          Download CSV
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Summary Statistics */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Summary Statistics</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Qubits Transmitted:</span>
              <span className="font-bold">{stats.total_qubits}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Matching Bases Count:</span>
              <span className="font-bold">{stats.matching_bases_count}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Sifted Key Length:</span>
              <span className="font-bold text-green-600">{stats.sifted_key_length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Key Efficiency:</span>
              <span className="font-bold">{(stats.efficiency * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Error Count:</span>
              <span className="font-bold text-red-600">{stats.error_count}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">QBER:</span>
              <span className={`font-bold ${stats.qber < 0.11 ? 'text-green-600' : 'text-red-600'}`}>
                {(stats.qber * 100).toFixed(3)}%
              </span>
            </div>
          </div>
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded">
            <p className="text-xs text-blue-800">
              <strong>Note:</strong> A QBER below 11% is considered secure for BB84 protocol. 
              Above this threshold, the key should not be used as it may be compromised.
            </p>
          </div>
        </div>

        {/* Sifted Key Display */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Sifted Key</h3>
          <div className="space-y-3">
            <div>
              <h4 className="text-sm font-medium text-gray-600 mb-1">Alice's Key:</h4>
              <div className="p-2 bg-gray-100 rounded font-mono text-xs break-all">
                {results.sifted_key_alice.join('')}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-600 mb-1">Bob's Key:</h4>
              <div className="p-2 bg-gray-100 rounded font-mono text-xs break-all">
                {results.sifted_key_bob.join('')}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-600 mb-1">Key Match:</h4>
              <div className={`p-2 rounded text-sm font-bold ${
                JSON.stringify(results.sifted_key_alice) === JSON.stringify(results.sifted_key_bob)
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {JSON.stringify(results.sifted_key_alice) === JSON.stringify(results.sifted_key_bob)
                  ? '✓ Keys match perfectly!'
                  : `✗ Keys differ in ${stats.error_count} positions`}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Educational Information */}
      <div className="mt-6 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
        <h3 className="text-lg font-semibold text-indigo-900 mb-2">About BB84 Protocol</h3>
        <div className="text-sm text-indigo-800 space-y-2">
          <p>
            <strong>BB84</strong> is a quantum key distribution protocol developed by Charles Bennett and 
            Gilles Brassard in 1984. It uses quantum mechanics to securely distribute cryptographic keys.
          </p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li><strong>Alice</strong> encodes random bits in random bases (Z or X)</li>
            <li><strong>Bob</strong> measures received qubits in randomly chosen bases</li>
            <li><strong>Key Sifting:</strong> Only bits where bases matched are kept</li>
            <li><strong>QBER:</strong> Quantum Bit Error Rate indicates eavesdropping or noise</li>
            <li><strong>Security:</strong> Any eavesdropping attempt disturbs the quantum states, 
                increasing QBER</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
