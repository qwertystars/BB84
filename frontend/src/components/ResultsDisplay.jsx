import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'

const ResultsDisplay = ({ result, results, onShowDetailed, loadingDetailed, showAllQubits, setShowAllQubits }) => {
  if (!result) {
    return (
      <div className="card p-8 text-center space-y-4">
        <div className="text-6xl">⚛️</div>
        <p className="text-gray-400 text-lg">Run a simulation to see quantum key distribution results</p>
        <p className="text-sm text-gray-500">Adjust parameters and click "Run Simulation" to begin</p>
      </div>
    )
  }

  const chartData = results.map((res, index) => ({
    run: index + 1,
    qber: res.qber * 100,
    keyLength: res.sifted_key_length
  }))

  // Determine security level color
  const getSecurityColor = (qber) => {
    if (qber <= 0.05) return 'from-green-500 to-emerald-600'
    if (qber <= 0.11) return 'from-yellow-500 to-orange-600'
    return 'from-red-500 to-pink-600'
  }

  const getSecurityStatus = (qber) => {
    if (qber <= 0.05) return { text: 'Excellent Security', icon: '🛡️', color: 'text-green-400' }
    if (qber <= 0.11) return { text: 'Acceptable (Near Limit)', icon: '⚠️', color: 'text-yellow-400' }
    return { text: 'Compromised', icon: '🚨', color: 'text-red-400' }
  }

  const security = getSecurityStatus(result.qber)

  const handleShowDetailed = () => {
    const params = {
      qubit_count: result.qubit_count,
      error_rate: result.error_rate,
      eve_fraction: result.eve_fraction
    }
    onShowDetailed(params, showAllQubits)
  }

  return (
    <div className="space-y-6">
      {/* Current Results Card */}
      <div className="card p-6 space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Simulation Results
          </h2>
          <span className="text-3xl">{security.icon}</span>
        </div>

        {/* Security Status Banner */}
        <div className={`stat-card bg-gradient-to-r ${getSecurityColor(result.qber)} p-4 text-center`}>
          <h3 className="text-lg font-bold text-white mb-1">{security.text}</h3>
          <p className="text-sm text-white/90">QBER: {(result.qber * 100).toFixed(2)}% {result.qber <= 0.11 ? '(Below 11% threshold)' : '(Above secure threshold)'}</p>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="stat-card">
            <h3 className="text-xs text-gray-400 mb-1">Scenario</h3>
            <p className="text-base font-semibold capitalize">{result.scenario.replace('-', ' ')}</p>
          </div>
          <div className="stat-card">
            <h3 className="text-xs text-gray-400 mb-1">QBER</h3>
            <p className={`text-base font-semibold ${security.color}`}>{(result.qber * 100).toFixed(2)}%</p>
          </div>
          <div className="stat-card">
            <h3 className="text-xs text-gray-400 mb-1">Sifted Key Length</h3>
            <p className="text-base font-semibold text-blue-400">{result.sifted_key_length} bits</p>
          </div>
          <div className="stat-card">
            <h3 className="text-xs text-gray-400 mb-1">Execution Time</h3>
            <p className="text-base font-semibold text-purple-400">{result.execution_time.toFixed(3)}s</p>
          </div>
        </div>

        {/* Sifted Key Display */}
        <div className="space-y-2">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            🔑 Sifted Quantum Key
          </h3>
          <div className="bg-black/40 rounded-lg p-4 font-mono text-sm break-all border border-blue-500/30 hover:border-blue-500/50 transition-colors">
            {result.sifted_key}
          </div>
        </div>

        {/* Detailed Simulation Button */}
        <div className="pt-2 space-y-3">
          {/* Show All Qubits Checkbox */}
          <div className="flex items-center justify-center gap-2 text-sm">
            <input
              type="checkbox"
              id="showAllQubits"
              checked={showAllQubits}
              onChange={(e) => setShowAllQubits(e.target.checked)}
              className="w-4 h-4 rounded border-white/20 bg-white/10 text-blue-500 focus:ring-2 focus:ring-blue-500 cursor-pointer"
            />
            <label htmlFor="showAllQubits" className="text-gray-300 cursor-pointer select-none">
              Show all {result.qubit_count} qubits {!showAllQubits && `(default: first 20)`}
            </label>
          </div>

          <button
            onClick={handleShowDetailed}
            disabled={loadingDetailed}
            className="w-full btn-secondary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loadingDetailed ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Loading Detailed View...</span>
              </>
            ) : (
              <>
                <span>🔬</span>
                <span>Show Step-by-Step Detailed Simulation</span>
              </>
            )}
          </button>
          <p className="text-xs text-gray-500 text-center">
            See how each qubit is processed through the BB84 protocol
          </p>
        </div>

        {/* Summary Details */}
        <div className="space-y-2">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            📊 Technical Summary
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {Object.entries(result.summary).map(([key, value]) => (
              <div key={key} className="flex justify-between text-sm bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors">
                <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="font-semibold">
                  {typeof value === 'boolean' ? (
                    <span className={value ? 'text-red-400' : 'text-green-400'}>
                      {value ? '✓ Yes' : '✗ No'}
                    </span>
                  ) : typeof value === 'number' ? (
                    key.includes('rate') || key.includes('qber') || key.includes('fraction') ? 
                      `${(value * 100).toFixed(1)}%` : value
                  ) : value}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Batch Results Analysis */}
      {results.length > 1 && (
        <div className="card p-6 space-y-6">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            📈 Batch Analysis ({results.length} Simulations)
          </h2>

          {/* Statistical Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="stat-card text-center">
              <h3 className="text-xs text-gray-400 mb-1">Average QBER</h3>
              <p className="text-lg font-semibold text-blue-400">
                {(results.reduce((sum, r) => sum + r.qber, 0) / results.length * 100).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card text-center">
              <h3 className="text-xs text-gray-400 mb-1">Min QBER</h3>
              <p className="text-lg font-semibold text-green-400">
                {(Math.min(...results.map(r => r.qber)) * 100).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card text-center">
              <h3 className="text-xs text-gray-400 mb-1">Max QBER</h3>
              <p className="text-lg font-semibold text-red-400">
                {(Math.max(...results.map(r => r.qber)) * 100).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card text-center">
              <h3 className="text-xs text-gray-400 mb-1">Avg Key Length</h3>
              <p className="text-lg font-semibold text-purple-400">
                {Math.round(results.reduce((sum, r) => sum + r.sifted_key_length, 0) / results.length)} bits
              </p>
            </div>
          </div>

          {/* QBER Chart */}
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">Quantum Bit Error Rate (QBER) Trend</h3>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="run" stroke="#fff" label={{ value: 'Simulation Run', position: 'insideBottom', offset: -5 }} />
                <YAxis stroke="#fff" label={{ value: 'QBER (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(0,0,0,0.9)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="qber" 
                  stroke="#3b82f6" 
                  strokeWidth={3}
                  name="QBER (%)"
                  dot={{ fill: '#3b82f6', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Key Length Chart */}
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">Sifted Key Length Analysis</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="run" stroke="#fff" />
                <YAxis stroke="#fff" label={{ value: 'Key Length (bits)', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(0,0,0,0.9)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend />
                <Bar 
                  dataKey="keyLength" 
                  fill="#8b5cf6" 
                  name="Key Length (bits)"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsDisplay
