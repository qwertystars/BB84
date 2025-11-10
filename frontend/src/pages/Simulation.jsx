import { useState, useEffect } from 'react'
import { getScenarios, runSimulation, runDetailedSimulation } from '../api'
import LoadingSpinner from '../components/LoadingSpinner'
import SimulationForm from '../components/SimulationForm'
import ResultsDisplay from '../components/ResultsDisplay'
import DetailedSimulation from '../components/DetailedSimulation'

const Simulation = () => {
  const [scenarios, setScenarios] = useState([])
  const [selectedScenario, setSelectedScenario] = useState('')
  const [parameters, setParameters] = useState({
    qubit_count: 100,
    error_rate: 0.0,
    eve_fraction: 0.0
  })
  const [results, setResults] = useState([])
  const [currentResult, setCurrentResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingScenarios, setLoadingScenarios] = useState(true)
  const [error, setError] = useState('')
  const [detailedData, setDetailedData] = useState(null)
  const [loadingDetailed, setLoadingDetailed] = useState(false)
  const [showDetailed, setShowDetailed] = useState(false)

  useEffect(() => {
    const fetchScenarios = async () => {
      try {
        const data = await getScenarios()
        setScenarios(data.scenarios)
        if (data.scenarios.length > 0) {
          setSelectedScenario(data.scenarios[0].id)
          setParameters({
            qubit_count: data.scenarios[0].parameters.qubit_count.default,
            error_rate: data.scenarios[0].parameters.error_rate.default,
            eve_fraction: data.scenarios[0].parameters.eve_fraction.default
          })
        }
      } catch (error) {
        setError('Failed to load scenarios. Please check your connection.')
        console.error('Error fetching scenarios:', error)
      } finally {
        setLoadingScenarios(false)
      }
    }

    fetchScenarios()
  }, [])

  const handleScenarioChange = (scenarioId) => {
    setSelectedScenario(scenarioId)
    const scenario = scenarios.find(s => s.id === scenarioId)
    if (scenario) {
      setParameters({
        qubit_count: scenario.parameters.qubit_count.default,
        error_rate: scenario.parameters.error_rate.default,
        eve_fraction: scenario.parameters.eve_fraction.default
      })
    }
    setResults([])
    setCurrentResult(null)
    setError('')
  }

  const handleParameterChange = (param, value) => {
    setParameters(prev => ({
      ...prev,
      [param]: value
    }))
  }

  const runSingleSimulation = async () => {
    setLoading(true)
    setError('')
    try {
      const result = await runSimulation(selectedScenario, parameters)
      setCurrentResult(result)
      setResults(prev => [...prev.slice(-9), result]) // Keep last 10 results
    } catch (error) {
      setError('❌ Simulation failed. Please check your parameters and try again.')
      console.error('Error running simulation:', error)
    } finally {
      setLoading(false)
    }
  }

  const runBatchSimulation = async () => {
    setLoading(true)
    setError('')
    const batchResults = []

    try {
      for (let i = 0; i < 10; i++) {
        const result = await runSimulation(selectedScenario, parameters)
        batchResults.push(result)
      }
      setResults(batchResults)
      setCurrentResult(batchResults[batchResults.length - 1])
    } catch (error) {
      setError('❌ Batch simulation failed. Please check your parameters and try again.')
      console.error('Error in batch simulation:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleShowDetailed = async (params) => {
    setLoadingDetailed(true)
    try {
      const data = await runDetailedSimulation(params)
      setDetailedData(data)
      setShowDetailed(true)
    } catch (error) {
      setError('❌ Failed to run detailed simulation. Please try again.')
      console.error('Failed to run detailed simulation:', error)
    } finally {
      setLoadingDetailed(false)
    }
  }

  if (loadingScenarios) {
    return <LoadingSpinner />
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-block text-5xl mb-2">⚛️🔬</div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          BB84 Quantum Simulation Lab
        </h1>
        <p className="text-gray-300 text-lg max-w-2xl mx-auto">
          Configure quantum channel parameters and observe key distribution in real-time
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="card p-4 bg-red-500/20 border-red-500/50 max-w-4xl mx-auto animate-pulse">
          <p className="text-red-200 text-center font-medium">{error}</p>
        </div>
      )}

      {/* Info Banner */}
      <div className="card p-4 bg-blue-500/10 border-blue-500/30 max-w-4xl mx-auto">
        <div className="flex items-center gap-3">
          <span className="text-2xl">💡</span>
          <p className="text-sm text-blue-200">
            <strong>Tip:</strong> QBER (Quantum Bit Error Rate) above 11% indicates potential eavesdropping or excessive channel noise. 
            Secure communication requires QBER below this threshold.
          </p>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
        <SimulationForm
          scenarios={scenarios}
          selectedScenario={selectedScenario}
          parameters={parameters}
          onScenarioChange={handleScenarioChange}
          onParameterChange={handleParameterChange}
          onRunSimulation={runSingleSimulation}
          onRunBatchSimulation={runBatchSimulation}
          loading={loading}
        />

        <ResultsDisplay
          result={currentResult}
          results={results}
          onShowDetailed={handleShowDetailed}
          loadingDetailed={loadingDetailed}
        />
      </div>

      {/* Detailed Simulation - Full Width */}
      {showDetailed && detailedData && (
        <div className="max-w-7xl mx-auto">
          <DetailedSimulation detailedData={detailedData} />
        </div>
      )}
    </div>
  )
}

export default Simulation
