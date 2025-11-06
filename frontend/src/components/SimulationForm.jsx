const SimulationForm = ({
  scenarios,
  selectedScenario,
  parameters,
  onScenarioChange,
  onParameterChange,
  onRunSimulation,
  onRunBatchSimulation,
  loading
}) => {
  const currentScenario = scenarios.find(s => s.id === selectedScenario)

  const scenarioIcons = {
    'ideal': '🔒',
    'error-only': '📡',
    'error-eve': '👁️',
    'decoherence-free': '✨'
  }

  return (
    <div className="card p-6 space-y-6">
      <div className="flex items-center gap-3">
        <span className="text-3xl">⚙️</span>
        <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Simulation Parameters
        </h2>
      </div>

      <div className="space-y-5">
        {/* Scenario Selection */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
            <span>🎭</span> Scenario Type
          </label>
          <select
            value={selectedScenario}
            onChange={(e) => onScenarioChange(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:border-white/40 transition-all"
          >
            {scenarios.map(scenario => (
              <option key={scenario.id} value={scenario.id} className="bg-gray-900">
                {scenarioIcons[scenario.id]} {scenario.name}
              </option>
            ))}
          </select>
        </div>

        {/* Qubit Count Slider */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <span>⚛️</span> Qubit Count
            </span>
            <span className="text-lg font-bold text-blue-400">{parameters.qubit_count}</span>
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.qubit_count.min || 10}
            max={currentScenario?.parameters.qubit_count.max || 1000}
            value={parameters.qubit_count}
            onChange={(e) => onParameterChange('qubit_count', parseInt(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider-thumb"
          />
          <div className="flex justify-between text-xs text-gray-400">
            <span>{currentScenario?.parameters.qubit_count.min || 10} qubits</span>
            <span>{currentScenario?.parameters.qubit_count.max || 1000} qubits</span>
          </div>
          <p className="text-xs text-gray-500">Higher qubit count increases key length but takes longer to simulate</p>
        </div>

        {/* Error Rate Slider */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <span>📊</span> Channel Error Rate
            </span>
            <span className="text-lg font-bold text-purple-400">{(parameters.error_rate * 100).toFixed(1)}%</span>
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.error_rate.min || 0}
            max={currentScenario?.parameters.error_rate.max || 0.5}
            step={0.01}
            value={parameters.error_rate}
            onChange={(e) => onParameterChange('error_rate', parseFloat(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider-thumb"
            disabled={currentScenario?.parameters.error_rate.min === currentScenario?.parameters.error_rate.max}
          />
          <div className="flex justify-between text-xs text-gray-400">
            <span>{(currentScenario?.parameters.error_rate.min || 0) * 100}%</span>
            <span>{(currentScenario?.parameters.error_rate.max || 0.5) * 100}%</span>
          </div>
          <p className="text-xs text-gray-500">Simulates noise in the quantum channel during transmission</p>
        </div>

        {/* Eve Fraction Slider */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <span>👤</span> Eavesdropper Fraction (Eve)
            </span>
            <span className="text-lg font-bold text-pink-400">{(parameters.eve_fraction * 100).toFixed(1)}%</span>
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.eve_fraction.min || 0}
            max={currentScenario?.parameters.eve_fraction.max || 1}
            step={0.01}
            value={parameters.eve_fraction}
            onChange={(e) => onParameterChange('eve_fraction', parseFloat(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider-thumb"
            disabled={currentScenario?.parameters.eve_fraction.min === currentScenario?.parameters.eve_fraction.max}
          />
          <div className="flex justify-between text-xs text-gray-400">
            <span>{(currentScenario?.parameters.eve_fraction.min || 0) * 100}%</span>
            <span>{(currentScenario?.parameters.eve_fraction.max || 1) * 100}%</span>
          </div>
          <p className="text-xs text-gray-500">Percentage of qubits intercepted by an eavesdropper (intercept-resend attack)</p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="space-y-3 pt-2">
        <button
          onClick={onRunSimulation}
          disabled={loading}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Running Simulation...</span>
            </>
          ) : (
            <>
              <span>▶️</span>
              <span>Run Single Simulation</span>
            </>
          )}
        </button>
        <button
          onClick={onRunBatchSimulation}
          disabled={loading}
          className="w-full btn-secondary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Running Batch...</span>
            </>
          ) : (
            <>
              <span>📊</span>
              <span>Run 10 Simulations (Batch)</span>
            </>
          )}
        </button>
      </div>

      {/* Scenario Description */}
      {currentScenario && (
        <div className="text-sm pt-4 border-t border-white/10 space-y-2">
          <h3 className="font-medium text-gray-300 flex items-center gap-2">
            <span>{scenarioIcons[currentScenario.id]}</span>
            <span>About This Scenario:</span>
          </h3>
          <p className="text-gray-400 leading-relaxed">{currentScenario.description}</p>
        </div>
      )}
    </div>
  )
}

export default SimulationForm
