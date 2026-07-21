import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { registerSW } from 'virtual:pwa-register'
import './index.css'
import App from './App.tsx'
import { seedKnowledgeGraph } from './services/knowledge'
import ErrorBoundary from './components/ErrorBoundary'

seedKnowledgeGraph()

// Register service worker with update prompt
registerSW({
  immediate: true,
  onNeedRefresh() {
    if (confirm('A new version is available. Refresh to update?')) {
      return true;
    }
  },
  onOfflineReady() {
    console.log('App ready to work offline');
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
