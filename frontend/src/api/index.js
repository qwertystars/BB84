import axios from 'axios'

const getBackendUrls = () => {
  // Use explicit URL if provided via environment variable
  if (import.meta.env.VITE_API_URL) {
    return [import.meta.env.VITE_API_URL]
  }

  // In production (when served from the same domain), use relative URLs
  // This allows the frontend and backend to be deployed as a single service
  if (import.meta.env.PROD) {
    return [window.location.origin]
  }

  // In development, use localhost backend
  return ['http://localhost:8000']
}

const createApiWithFallback = async () => {
  const urls = getBackendUrls()
  
  for (const url of urls) {
    try {
      // Test if the endpoint is responsive
      await axios.get(`${url}/`, { timeout: 5000 })
      
      // If health check passes, create and return the API instance
      const api = axios.create({
        baseURL: url,
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      // Add request interceptor to handle errors gracefully
      api.interceptors.response.use(
        response => response,
        error => {
          // Don't log errors for individual requests that might fail
          return Promise.reject(error)
        }
      )
      
      return api
    } catch (error) {
      // Silently try the next URL
      continue
    }
  }
  
  // If all URLs fail, throw an error
  throw new Error('Unable to connect to any API endpoint')
}

let apiInstance = null
let apiPromise = null

const getApi = async () => {
  if (!apiInstance) {
    if (!apiPromise) {
      apiPromise = createApiWithFallback()
        .then(api => {
          apiInstance = api
          return api
        })
        .catch(error => {
          console.error('Failed to connect to any API endpoint:', error.message)
          throw error
        })
    }
    return apiPromise
  }
  return apiInstance
}

export const getScenarios = async () => {
  try {
    const api = await getApi()
    const response = await api.get('/scenarios')
    return response.data
  } catch (error) {
    throw error
  }
}

export const runSimulation = async (scenario, params) => {
  try {
    const api = await getApi()
    const response = await api.post(`/simulate/${scenario}`, params)
    return response.data
  } catch (error) {
    throw error
  }
}

export const runDetailedSimulation = async (params) => {
  try {
    const api = await getApi()
    const response = await api.post('/simulate/detailed', params)
    return response.data
  } catch (error) {
    throw error
  }
}

export default {
  get: async (...args) => {
    const api = await getApi()
    return api.get(...args)
  },
  post: async (...args) => {
    const api = await getApi()
    return api.post(...args)
  },
  put: async (...args) => {
    const api = await getApi()
    return api.put(...args)
  },
  delete: async (...args) => {
    const api = await getApi()
    return api.delete(...args)
  }
}
