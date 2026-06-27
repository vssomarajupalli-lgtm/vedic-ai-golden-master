import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useChartStore } from '../store/useChartStore';
import { apiService } from '../api/backend';
import { Download, FileJson, FileCode2, FileText, Loader2 } from 'lucide-react';

export default function ExportReport() {
  const { canonicalContent, machineIndex, report } = useChartStore();
  const [downloading, setDownloading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Guard clause
  if (!canonicalContent || !machineIndex) {
    return <Navigate to="/upload" replace />;
  }

  const handleDownloadJSON = () => {
    try {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2));
      const downloadAnchorNode = document.createElement('a');
      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", "vedic_ai_report.json");
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    } catch (err) {
      setError("Failed to generate JSON locally.");
    }
  };

  const handleDownload = async (format: 'html' | 'pdf') => {
    setDownloading(format);
    setError(null);
    try {
      await apiService.downloadReport(canonicalContent, machineIndex, format);
    } catch (err: any) {
      setError(`Failed to download ${format.toUpperCase()}: ${err.response?.data?.detail || err.message}`);
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 text-center">
        <Download className="w-12 h-12 text-indigo-600 mx-auto mb-6" />
        <h2 className="text-3xl font-bold text-slate-900 mb-4">Export Analysis</h2>
        <p className="text-slate-600 mb-10 max-w-lg mx-auto">
          Download your fully calculated deterministic report in your preferred format. The data is immutable and securely generated from the mathematical engine.
        </p>

        {error && (
          <div className="mb-8 bg-red-50 text-red-700 px-4 py-3 rounded-lg text-sm font-medium">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-6">
          {/* JSON Export */}
          <button
            onClick={handleDownloadJSON}
            className="flex flex-col items-center justify-center p-6 bg-slate-50 border border-slate-200 rounded-xl hover:bg-indigo-50 hover:border-indigo-200 transition-colors group"
          >
            <FileJson className="w-10 h-10 text-slate-400 group-hover:text-indigo-600 mb-4 transition-colors" />
            <span className="font-semibold text-slate-800">Raw JSON</span>
            <span className="text-xs text-slate-500 mt-2 text-center">Best for developers & API integration</span>
          </button>

          {/* HTML Export */}
          <button
            onClick={() => handleDownload('html')}
            disabled={downloading !== null}
            className="flex flex-col items-center justify-center p-6 bg-slate-50 border border-slate-200 rounded-xl hover:bg-blue-50 hover:border-blue-200 transition-colors group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {downloading === 'html' ? (
              <Loader2 className="w-10 h-10 text-blue-600 mb-4 animate-spin" />
            ) : (
              <FileCode2 className="w-10 h-10 text-slate-400 group-hover:text-blue-600 mb-4 transition-colors" />
            )}
            <span className="font-semibold text-slate-800">Standalone HTML</span>
            <span className="text-xs text-slate-500 mt-2 text-center">Best for offline viewing & emails</span>
          </button>

          {/* PDF Export */}
          <button
            onClick={() => handleDownload('pdf')}
            disabled={downloading !== null}
            className="flex flex-col items-center justify-center p-6 bg-slate-50 border border-slate-200 rounded-xl hover:bg-rose-50 hover:border-rose-200 transition-colors group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {downloading === 'pdf' ? (
              <Loader2 className="w-10 h-10 text-rose-600 mb-4 animate-spin" />
            ) : (
              <FileText className="w-10 h-10 text-slate-400 group-hover:text-rose-600 mb-4 transition-colors" />
            )}
            <span className="font-semibold text-slate-800">Printable PDF</span>
            <span className="text-xs text-slate-500 mt-2 text-center">Best for printing & sharing</span>
          </button>
        </div>
      </div>
    </div>
  );
}
