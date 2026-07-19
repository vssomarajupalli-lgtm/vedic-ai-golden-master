import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { UploadCloud, Loader2, AlertCircle, Plus } from 'lucide-react';
import { useChartStore } from '../store/useChartStore';
import { useConsultationStore } from '../store/useConsultationStore';
import { apiService } from '../api/backend';

export default function Upload() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setUploads, setResults } = useChartStore();
  const { createConsultation, updateConsultation } = useConsultationStore();
  
  // Check if we're editing an existing consultation
  const consultationId = (location.state as any)?.consultationId;
  const existingConsultation = consultationId ? useConsultationStore.getState().consultations.find(c => c.id === consultationId) : null;
  
  const [canonical, setCanonical] = useState<any>(existingConsultation?.canonicalContent || null);
  const [machine, setMachine] = useState<any>(existingConsultation?.machineIndex || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [consultationName, setConsultationName] = useState(existingConsultation?.name || '');

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
      // 1. Process chart to get raw math breakdown
      const outputs = await apiService.processChart(canonical, machine);
      
      // 2. Process report to get UI formatting Schema
      const report = await apiService.generateReport(canonical, machine);
      
      // 3. Save to Zustand memory
      setUploads(canonical, machine);
      setResults(outputs, report);
      
      // 4. Create or update consultation
      const client = existingConsultation?.client ? {
        name: existingConsultation.client.name,
        email: existingConsultation.client.email,
        phone: existingConsultation.client.phone,
        birthData: existingConsultation.client.birthData,
      } : undefined;
      
      if (consultationId && existingConsultation) {
        // Update existing consultation
        await updateConsultation(consultationId, {
          name: consultationName || existingConsultation.name,
          canonicalContent: canonical,
          machineIndex: machine,
          rawOutputs: outputs,
          report: report,
          status: 'active',
          client,
          updatedAt: new Date().toISOString(),
        });
        navigate(`/consultation/${consultationId}`);
      } else {
        // Create new consultation
        const newConsultation = await createConsultation({
          clientId: existingConsultation?.clientId || 'new',
          client: existingConsultation?.client || { name: '' },
          name: consultationName || `Consultation ${new Date().toLocaleDateString()}`,
          canonicalContent: canonical,
          machineIndex: machine,
          rawOutputs: outputs,
          report: report,
          status: 'active',
        });
        navigate(`/consultation/${newConsultation.id}`);
      }
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
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-900 flex items-center">
            <UploadCloud className="w-6 h-6 mr-2 text-indigo-600" />
            {consultationId ? 'Update Consultation' : 'Create Consultation'}
          </h2>
          {!consultationId && (
            <span className="px-3 py-1 text-xs font-medium bg-indigo-100 text-indigo-700 rounded-full">
              New Consultation
            </span>
          )}
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}

        {!consultationId && (
          <div className="mb-6 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
            <p className="text-sm text-indigo-800 mb-3">
              <strong>Tip:</strong> You can also create a consultation from the Dashboard or Consultation Library.
            </p>
            <input
              type="text"
              value={consultationName}
              onChange={(e) => setConsultationName(e.target.value)}
              placeholder="Consultation name (optional)"
              className="w-full px-4 py-2 border border-indigo-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
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
                {consultationId ? 'Updating...' : 'Processing...'}
              </>
            ) : (
              <>
                {consultationId ? 'Update Consultation' : 'Generate Analysis'}
                <Plus className="ml-2 w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}