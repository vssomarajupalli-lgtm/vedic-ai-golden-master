import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { registerSW } from 'virtual:pwa-register'
import './index.css'
import App from './App.tsx'
import ErrorBoundary from './components/ErrorBoundary'

// Register service worker with update prompt
registerSW({
  immediate: true,
  onNeedRefresh() {
    if (confirm('A new version is available. Refresh to update?')) {
      return true;
    }
  },
  onOfflineReady() {
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
