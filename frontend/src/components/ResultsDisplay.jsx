import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const ResultsDisplay = ({ result, results }) => {
  if (!result) {
    return (
      <div className="card p-6 text-center">
        <p className="text-gray-400">Run a simulation to see results</p>
      </div>
    )
  }

  const chartData = results.map((res, index) => ({
    run: index + 1,
    qber: res.qber * 100,
    keyLength: res.sifted_key_length
  }))

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <h2 className="text-2xl font-bold mb-4">Current Results</h2>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-sm text-gray-400 mb-1">Scenario</h3>
            <p className="text-lg font-semibold capitalize">{result.scenario.replace('-', ' ')}</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-sm text-gray-400 mb-1">QBER</h3>
            <p className="text-lg font-semibold">{(result.qber * 100).toFixed(2)}%</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-sm text-gray-400 mb-1">Sifted Key Length</h3>
            <p className="text-lg font-semibold">{result.sifted_key_length}</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-sm text-gray-400 mb-1">Execution Time</h3>
            <p className="text-lg font-semibold">{result.execution_time.toFixed(3)}s</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Sifted Key</h3>
            <div className="bg-black/30 rounded-lg p-3 font-mono text-sm break-all">
              {result.sifted_key}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Summary</h3>
            <div className="space-y-2">
              {Object.entries(result.summary).map(([key, value]) => (
                <div key={key} className="flex justify-between text-sm">
                  <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}:</span>
                  <span>
                    {typeof value === 'boolean' ? (value ? 'Yes' : 'No') :
                     typeof value === 'number' ? 
                       (key.includes('rate') || key.includes('qber') || key.includes('fraction') ? 
                        `${(value * 100).toFixed(1)}%` : value) : value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {results.length > 1 && (
        <div className="card p-6">
          <h2 className="text-2xl font-bold mb-4">Batch Results Analysis</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Quantum Bit Error Rate (QBER)</h3>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="run" stroke="#fff" />
                  <YAxis stroke="#fff" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="qber" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="QBER (%)"
                    dot={{ fill: '#3b82f6' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Key Length</h3>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="run" stroke="#fff" />
                  <YAxis stroke="#fff" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.2)' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="keyLength" 
                    stroke="#0ea5e9" 
                    strokeWidth={2}
                    name="Key Length (bits)"
                    dot={{ fill: '#0ea5e9' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 rounded-lg p-4">
                <h3 className="text-sm text-gray-400 mb-1">Average QBER</h3>
                <p className="text-lg font-semibold">
                  {(results.reduce((sum, r) => sum + r.qber, 0) / results.length * 100).toFixed(2)}%
                </p>
              </div>
              <div className="bg-white/5 rounded-lg p-4">
                <h3 className="text-sm text-gray-400 mb-1">Average Key Length</h3>
                <p className="text-lg font-semibold">
                  {Math.round(results.reduce((sum, r) => sum + r.sifted_key_length, 0) / results.length)}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsDisplay
