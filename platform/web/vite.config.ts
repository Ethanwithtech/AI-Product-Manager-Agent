import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Backend API server address — override via VITE_API_URL env var
// Local dev: http://localhost:8000 (default)
// Team deploy: http://10.x.x.x:8000 (your shared server IP)
const apiTarget = process.env.VITE_API_URL || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    allowedHosts: true,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
})
