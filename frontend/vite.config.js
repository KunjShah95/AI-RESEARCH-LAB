import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/auth': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/papers': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/debate': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/synthesize': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/write': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/projects': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/collections': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/clipboard': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/compare': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/search': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
})
