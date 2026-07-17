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
        // Force the Node process to shut down 1 second after compilation ends
        setTimeout(() => process.exit(0), 1000);
      }
    }
  ],
  build: {
    // Explicitly shut off all file watchers during a production build
    watch: false
  }
})