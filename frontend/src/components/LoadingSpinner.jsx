const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center min-h-64">
      <div className="flex flex-col items-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        <p className="text-gray-300">Loading...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner
