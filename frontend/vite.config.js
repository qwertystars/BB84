import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Allow external connections for reverse proxy
    cors: true,   // Enable CORS for development
    allowedHosts: ['bb84.srijan.dpdns.org', 'bb84-api.srijan.dpdns.org', 'localhost'] // Allow production domains
  },
  // API proxy for development only
  define: {
    // Use production API URL for all environments
    __APP__: JSON.stringify({
      API_URL: 'https://bb84-api.srijan.dpdns.org'
    })
  }
})
