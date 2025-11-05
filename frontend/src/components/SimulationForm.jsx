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

  return (
    <div className="card p-6 space-y-6">
      <h2 className="text-2xl font-bold">Simulation Parameters</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Scenario</label>
          <select
            value={selectedScenario}
            onChange={(e) => onScenarioChange(e.target.value)}
            className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {scenarios.map(scenario => (
              <option key={scenario.id} value={scenario.id} className="bg-gray-800">
                {scenario.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Qubit Count: {parameters.qubit_count}
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.qubit_count.min || 10}
            max={currentScenario?.parameters.qubit_count.max || 1000}
            value={parameters.qubit_count}
            onChange={(e) => onParameterChange('qubit_count', parseInt(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>{currentScenario?.parameters.qubit_count.min || 10}</span>
            <span>{currentScenario?.parameters.qubit_count.max || 1000}</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Error Rate: {(parameters.error_rate * 100).toFixed(1)}%
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.error_rate.min || 0}
            max={currentScenario?.parameters.error_rate.max || 0.5}
            step={0.01}
            value={parameters.error_rate}
            onChange={(e) => onParameterChange('error_rate', parseFloat(e.target.value))}
            className="w-full"
            disabled={currentScenario?.parameters.error_rate.min === currentScenario?.parameters.error_rate.max}
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>{(currentScenario?.parameters.error_rate.min || 0) * 100}%</span>
            <span>{(currentScenario?.parameters.error_rate.max || 0.5) * 100}%</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Eve Fraction: {(parameters.eve_fraction * 100).toFixed(1)}%
          </label>
          <input
            type="range"
            min={currentScenario?.parameters.eve_fraction.min || 0}
            max={currentScenario?.parameters.eve_fraction.max || 1}
            step={0.01}
            value={parameters.eve_fraction}
            onChange={(e) => onParameterChange('eve_fraction', parseFloat(e.target.value))}
            className="w-full"
            disabled={currentScenario?.parameters.eve_fraction.min === currentScenario?.parameters.eve_fraction.max}
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>{(currentScenario?.parameters.eve_fraction.min || 0) * 100}%</span>
            <span>{(currentScenario?.parameters.eve_fraction.max || 1) * 100}%</span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <button
          onClick={onRunSimulation}
          disabled={loading}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Running...' : 'Run Simulation'}
        </button>
        <button
          onClick={onRunBatchSimulation}
          disabled={loading}
          className="w-full btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Running Batch...' : 'Run 10 Simulations'}
        </button>
      </div>

      {currentScenario && (
        <div className="text-sm text-gray-400 pt-4 border-t border-white/10">
          <h3 className="font-medium mb-2">Scenario Description:</h3>
          <p>{currentScenario.description}</p>
        </div>
      )}
    </div>
  )
}

export default SimulationForm
