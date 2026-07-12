import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig(() => {
  // Detect if this is a Tauri build
  const isTauriBuild = process.env.TAURI_BUILD === 'true';
  
  // For Tauri desktop builds, use the sidecar backend URL
  // For development/preview, use the local backend
  const apiBaseUrl = isTauriBuild 
    ? 'http://localhost:8000/api/v1'
    : 'http://localhost:8000/api/v1';
  
  return {
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(apiBaseUrl),
    },
    plugins: [
      react(),
      VitePWA({
        registerType: 'autoUpdate',
        includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
        manifest: {
          name: 'Vedic-AI',
          short_name: 'VedicAI',
          description: 'Deterministic Astrological Analysis',
          theme_color: '#ffffff',
          icons: [
            {
              src: 'pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png'
            },
            {
              src: 'pwa-512x512.png',
              sizes: '512x512',
              type: 'image/png'
            }
          ]
        }
      })
    ],
  };
});
