import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { getScenarios, runSimulation } from '../api'
import LoadingSpinner from '../components/LoadingSpinner'
import SimulationForm from '../components/SimulationForm'
import ResultsDisplay from '../components/ResultsDisplay'

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
        setError('Failed to load scenarios')
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
      setError('Simulation failed. Please check your parameters and try again.')
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
      setError('Batch simulation failed. Please check your parameters and try again.')
      console.error('Error in batch simulation:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loadingScenarios) {
    return <LoadingSpinner />
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2">BB84 Simulation</h1>
        <p className="text-gray-300">Run quantum key distribution simulations with different scenarios</p>
      </div>

      {error && (
        <div className="card p-4 bg-red-500/20 border-red-500/50">
          <p className="text-red-200">{error}</p>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
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

        {currentResult && (
          <ResultsDisplay
            result={currentResult}
            results={results}
          />
        )}
      </div>
    </div>
  )
}

export default Simulation
