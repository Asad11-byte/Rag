import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'force-close-on-end',
      apply: 'build',
      closeBundle() {
        setTimeout(() => process.exit(0), 1000);
      }
    }
  ],
  build: {
    watch: false
  },
  // Add this block to handle local development redirecting to your FastAPI server
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})