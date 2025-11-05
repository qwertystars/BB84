const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="flex flex-col items-center space-y-6">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500"></div>
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-500 absolute top-0 left-0" style={{ animationDirection: 'reverse', animationDuration: '1s' }}></div>
        </div>
        <div className="text-center space-y-2">
          <p className="text-gray-300 text-xl font-semibold">Loading Quantum Simulation...</p>
          <p className="text-gray-500 text-sm">Preparing quantum states</p>
        </div>
        <div className="flex gap-2">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  )
}

export default LoadingSpinner
