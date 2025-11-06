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

  const scenarioColors = {
    'ideal': 'from-green-500 to-emerald-600',
    'error-only': 'from-blue-500 to-cyan-600',
    'error-eve': 'from-red-500 to-pink-600',
    'decoherence-free': 'from-purple-500 to-violet-600'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500"></div>
          <p className="text-gray-300 text-lg">Loading quantum scenarios...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section */}
      <div className="text-center space-y-6 py-8 animate-float">
        <div className="inline-block text-6xl mb-4 animate-pulse-glow">🔐⚛️</div>
        <h1 className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight">
          BB84 Quantum Key Distribution
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
          Explore quantum cryptography through interactive simulations of the groundbreaking BB84 protocol
        </p>
        <div className="flex gap-4 justify-center pt-4">
          <Link to="/simulation" className="btn-primary text-lg">
            🚀 Launch Simulation
          </Link>
        </div>
      </div>

      {/* About BB84 Section */}
      <div className="card p-8 md:p-10 max-w-5xl mx-auto quantum-glow">
        <div className="flex items-start gap-6">
          <div className="text-5xl hidden md:block">⚡</div>
          <div className="flex-1 space-y-4">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              What is BB84?
            </h2>
            <div className="space-y-3 text-gray-300 text-lg leading-relaxed">
              <p>
                <strong className="text-white">BB84</strong> is a quantum key distribution protocol developed by <strong className="text-blue-300">Charles Bennett</strong> and <strong className="text-purple-300">Gilles Brassard</strong> in 1984.
                It revolutionized cryptography by using quantum mechanics to enable provably secure communication.
              </p>
              <p>
                The protocol leverages fundamental quantum principles like the <strong className="text-blue-300">no-cloning theorem</strong> and <strong className="text-purple-300">measurement disturbance</strong> to detect eavesdropping attempts, making it impossible for attackers to intercept keys without being detected.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-4 pt-4">
              <div className="stat-card text-center">
                <div className="text-3xl mb-2">🔬</div>
                <div className="text-sm text-gray-400">Quantum Mechanics</div>
                <div className="text-lg font-semibold">Foundation</div>
              </div>
              <div className="stat-card text-center">
                <div className="text-3xl mb-2">🛡️</div>
                <div className="text-sm text-gray-400">Eavesdrop Detection</div>
                <div className="text-lg font-semibold">11% QBER Limit</div>
              </div>
              <div className="stat-card text-center">
                <div className="text-3xl mb-2">🔑</div>
                <div className="text-sm text-gray-400">Secure Keys</div>
                <div className="text-lg font-semibold">Provably Safe</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="card p-8 max-w-5xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          How BB84 Works
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <span className="text-2xl">1️⃣</span>
              <div>
                <h3 className="font-semibold text-lg text-blue-300">Quantum Transmission</h3>
                <p className="text-gray-400">Alice sends qubits to Bob using random bases (Z or X)</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">2️⃣</span>
              <div>
                <h3 className="font-semibold text-lg text-purple-300">Random Measurement</h3>
                <p className="text-gray-400">Bob measures each qubit using his own random basis choice</p>
              </div>
            </div>
          </div>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <span className="text-2xl">3️⃣</span>
              <div>
                <h3 className="font-semibold text-lg text-pink-300">Basis Reconciliation</h3>
                <p className="text-gray-400">Alice and Bob publicly compare bases, keeping matching results</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl">4️⃣</span>
              <div>
                <h3 className="font-semibold text-lg text-green-300">Error Checking</h3>
                <p className="text-gray-400">QBER analysis detects eavesdropping through increased errors</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scenarios Section */}
      <div className="space-y-6">
        <div className="text-center">
          <h2 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Simulation Scenarios
          </h2>
          <p className="text-gray-400 text-lg">Explore different quantum channel conditions and security scenarios</p>
        </div>
        <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
          {scenarios.map((scenario, index) => (
            <div
              key={scenario.id}
              className="card p-6 space-y-4 hover:scale-105 transition-transform duration-300"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-4xl">{scenarioIcons[scenario.id]}</span>
                  <h3 className="text-xl font-bold">{scenario.name}</h3>
                </div>
                <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${scenarioColors[scenario.id]}`}></div>
              </div>
              <p className="text-gray-300 leading-relaxed">{scenario.description}</p>
              <div className="bg-black/30 rounded-lg p-4 space-y-2">
                <h4 className="font-medium text-sm text-gray-400 mb-2">Default Parameters</h4>
                <div className="grid grid-cols-3 gap-2 text-sm">
                  <div className="text-center">
                    <div className="text-blue-400 font-semibold">{scenario.parameters.qubit_count.default}</div>
                    <div className="text-gray-500 text-xs">Qubits</div>
                  </div>
                  <div className="text-center">
                    <div className="text-purple-400 font-semibold">{(scenario.parameters.error_rate.default * 100).toFixed(0)}%</div>
                    <div className="text-gray-500 text-xs">Error Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-pink-400 font-semibold">{(scenario.parameters.eve_fraction.default * 100).toFixed(0)}%</div>
                    <div className="text-gray-500 text-xs">Eve Fraction</div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="card p-8 max-w-3xl mx-auto text-center quantum-glow">
        <h2 className="text-3xl font-bold mb-4">Ready to Explore Quantum Cryptography?</h2>
        <p className="text-gray-300 mb-6 text-lg">
          Run simulations, adjust parameters, and visualize how quantum mechanics ensures secure communication
        </p>
        <Link to="/simulation" className="btn-primary text-lg inline-block">
          ⚛️ Start Simulating Now
        </Link>
      </div>
    </div>
  )
}

export default Home
