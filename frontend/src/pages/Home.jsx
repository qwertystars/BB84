import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getScenarios } from '../api'

const Home = () => {
  const [scenarios, setScenarios] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchScenarios = async () => {
      try {
        const data = await getScenarios()
        setScenarios(data.scenarios)
      } catch (error) {
        console.error('Failed to fetch scenarios:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchScenarios()
  }, [])

  const scenarioIcons = {
    'ideal': '🔒',
    'error-only': '📡',
    'error-eve': '👁️',
    'decoherence-free': '✨'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-400 to-quantum-400 bg-clip-text text-transparent">
          BB84 Quantum Key Distribution Simulator
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Explore the BB84 quantum cryptography protocol through interactive simulations
        </p>
      </div>

      <div className="card p-8 max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold mb-4">What is BB84?</h2>
        <p className="text-gray-300 mb-6">
          BB84 is a quantum key distribution protocol developed by Charles Bennett and Gilles Brassard in 1984.
          It uses quantum mechanics to enable secure communication between two parties, Alice and Bob.
          The security of BB84 relies on the fundamental principles of quantum mechanics, such as the
          no-cloning theorem and measurement disturbance.
        </p>
        <Link to="/simulation" className="btn-primary inline-block">
          Start Simulation
        </Link>
      </div>

      <div className="space-y-6">
        <h2 className="text-3xl font-bold text-center">Available Scenarios</h2>
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {scenarios.map((scenario) => (
            <div key={scenario.id} className="card p-6 space-y-4">
              <div className="flex items-center space-x-3">
                <span className="text-3xl">{scenarioIcons[scenario.id]}</span>
                <h3 className="text-xl font-semibold">{scenario.name}</h3>
              </div>
              <p className="text-gray-300">{scenario.description}</p>
              <div className="space-y-2">
                <h4 className="font-medium">Default Parameters:</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>Qubits: {scenario.parameters.qubit_count.default}</li>
                  <li>Error Rate: {scenario.parameters.error_rate.default}</li>
                  <li>Eve Fraction: {scenario.parameters.eve_fraction.default}</li>
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Home
