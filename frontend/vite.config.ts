import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API calls to the backend to avoid CORS in development/Codespaces
      '/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        ws: false,
      }
    }
  }
})
