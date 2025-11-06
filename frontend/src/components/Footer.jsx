const Footer = () => {
  return (
    <footer className="bg-black/30 backdrop-blur-lg border-t border-white/20 mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8 text-center md:text-left">
          {/* About Section */}
          <div className="space-y-3">
            <h3 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              About BB84
            </h3>
            <p className="text-sm text-gray-400">
              Interactive quantum key distribution simulator implementing the groundbreaking BB84 protocol 
              developed by Charles Bennett and Gilles Brassard in 1984.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h3 className="text-lg font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Key Concepts
            </h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>🔬 Quantum Key Distribution</li>
              <li>⚛️ No-Cloning Theorem</li>
              <li>📊 QBER Analysis</li>
              <li>🛡️ Eavesdropping Detection</li>
            </ul>
          </div>

          {/* Tech Stack */}
          <div className="space-y-3">
            <h3 className="text-lg font-bold bg-gradient-to-r from-pink-400 to-red-400 bg-clip-text text-transparent">
              Technology
            </h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>⚡ FastAPI + Python</li>
              <li>⚛️ React + Vite</li>
              <li>🎨 TailwindCSS</li>
              <li>📊 Recharts Visualization</li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-6 border-t border-white/10 text-center text-sm text-gray-500">
          <p>© 2025 BB84 QKD Simulator | Built for Quantum Cryptography Education</p>
          <p className="mt-2">Made by Srijan Guchhait (25BCE5104)</p>
          <p className="mt-2">
            <span className="text-blue-400">◆</span> Powered by Quantum Mechanics <span className="text-purple-400">◆</span>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
