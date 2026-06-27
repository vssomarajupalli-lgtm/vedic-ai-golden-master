import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Loader2, AlertCircle } from 'lucide-react';
import { useChartStore } from '../store/useChartStore';
import { apiService } from '../api/backend';

export default function Upload() {
  const navigate = useNavigate();
  const { setUploads, setResults } = useChartStore();
  
  const [canonical, setCanonical] = useState<any>(null);
  const [machine, setMachine] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'canonical' | 'machine') => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        if (type === 'canonical') setCanonical(json);
        if (type === 'machine') setMachine(json);
        setError(null);
      } catch (err) {
        setError(`Failed to parse ${file.name}. Must be valid JSON.`);
      }
    };
    reader.readAsText(file);
  };

  const handleProcess = async () => {
    if (!canonical || !machine) {
      setError("Both canonical_content.json and machine_index.json are required.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      // 1. Process chart to get raw math breakdown (for QuestionEngine)
      const outputs = await apiService.processChart(canonical, machine);
      
      // 2. Process report to get UI formatting Schema
      const report = await apiService.generateReport(canonical, machine);
      
      // 3. Save to Zustand memory
      setUploads(canonical, machine);
      setResults(outputs, report);
      
      // 4. Redirect
      navigate('/results');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      const errorMessage = typeof detail === 'string' 
        ? detail 
        : Array.isArray(detail) 
          ? detail.map((e: any) => `${e.loc?.join('.') || 'Error'}: ${e.msg}`).join(' | ') 
          : err.message || "An error occurred connecting to the backend.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center">
          <UploadCloud className="w-6 h-6 mr-2 text-indigo-600" />
          Upload Chart Data
        </h2>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}

        <div className="space-y-6">
          {/* Canonical Input */}
          <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:bg-slate-50 transition-colors">
            <label className="cursor-pointer block">
              <span className="text-sm font-medium text-slate-700 block mb-2">Upload canonical_content.json</span>
              <input 
                type="file" 
                accept=".json" 
                className="hidden" 
                onChange={(e) => handleFileUpload(e, 'canonical')}
              />
              <span className="inline-block px-4 py-2 bg-white border border-slate-300 rounded text-sm text-indigo-600 font-medium shadow-sm">
                Choose File
              </span>
            </label>
            {canonical && <p className="mt-2 text-sm text-green-600 font-medium">✓ Loaded canonical data</p>}
          </div>

          {/* Machine Index Input */}
          <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:bg-slate-50 transition-colors">
            <label className="cursor-pointer block">
              <span className="text-sm font-medium text-slate-700 block mb-2">Upload machine_index.json</span>
              <input 
                type="file" 
                accept=".json" 
                className="hidden" 
                onChange={(e) => handleFileUpload(e, 'machine')}
              />
              <span className="inline-block px-4 py-2 bg-white border border-slate-300 rounded text-sm text-indigo-600 font-medium shadow-sm">
                Choose File
              </span>
            </label>
            {machine && <p className="mt-2 text-sm text-green-600 font-medium">✓ Loaded machine index</p>}
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-slate-200 flex justify-end">
          <button
            onClick={handleProcess}
            disabled={loading || !canonical || !machine}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Processing...
              </>
            ) : (
              'Generate Analysis'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
