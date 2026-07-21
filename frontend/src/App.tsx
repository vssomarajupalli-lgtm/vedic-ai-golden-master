import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';

import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Results from './pages/Results';
import QuestionEngine from './pages/QuestionEngine';
import QuestionBrowser from './pages/QuestionBrowser';
import ExportReport from './pages/ExportReport';
import VerificationConsole from './pages/VerificationConsole';
import ConsultationWorkspace from './components/consultation/ConsultationWorkspace';
import ConsultationLibrary from './pages/ConsultationLibrary';
import KnowledgeGraphViewer from './components/knowledge/KnowledgeGraphViewer';
import KnowledgeExplorer from './components/knowledge/KnowledgeExplorer';
import Clients from './pages/Clients';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="upload" element={<Upload />} />
          <Route path="results" element={<Results />} />
          <Route path="browse" element={<QuestionBrowser />} />
          <Route path="engine" element={<QuestionEngine />} />
          <Route path="ask" element={<Navigate to="/browse" replace />} />
          <Route path="export" element={<ExportReport />} />
          <Route path="verify" element={<VerificationConsole />} />
          <Route path="consultation" element={<ConsultationWorkspace />} />
          <Route path="consultation/:id" element={<ConsultationWorkspace />} />
          <Route path="consultation/library" element={<ConsultationLibrary />} />
          <Route path="clients" element={<Clients />} />
          <Route path="knowledge" element={<KnowledgeGraphViewer />} />
          <Route path="knowledge/explorer" element={<KnowledgeExplorer />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;