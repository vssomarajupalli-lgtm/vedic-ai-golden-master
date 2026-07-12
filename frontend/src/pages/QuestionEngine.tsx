import { useState, useEffect, useRef } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, Loader2, Database } from 'lucide-react';
import { useChartStore } from '../store/useChartStore';
import { apiService } from '../api/backend';
import { QuestionResultCard, type StructuredQuestionResult } from '../components/Questionnaire/QuestionResultCard';

export default function QuestionEngine() {
  const { rawOutputs, setQuestionResults } = useChartStore();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [results, setResults] = useState<StructuredQuestionResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchedQuestionRef = useRef<string | null>(null);

  useEffect(() => {
    if (location.state) {
      const { initialQuestionId } = location.state;
      if (initialQuestionId) {
        // Only fetch if we haven't already fetched this question synchronously via ref
        if (fetchedQuestionRef.current !== initialQuestionId) {
          fetchedQuestionRef.current = initialQuestionId;
          fetchStructuredQuestion(initialQuestionId);
        }
      }
      
      // Clear location state so refresh doesn't refetch - use React Router navigation to properly clear state
      navigate('.', { replace: true });
    }
  }, [location.state, navigate]);

  // Guard clause
  if (!rawOutputs) {
    return <Navigate to="/upload" replace />;
  }

  const fetchStructuredQuestion = async (id: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.askStructuredQuestion(id, rawOutputs);
      if (response.results && response.results.length > 0) {
        setResults(prev => {
          const next = [...prev, ...response.results];
          setQuestionResults(next);
          return next;
        });
      }
    } catch (err: any) {
      setError(`Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToBrowser = () => {
    navigate('/browse');
  };

  return (
    <div className="max-w-4xl mx-auto min-h-[80vh] flex flex-col bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      
      {/* Header */}
      <div className="bg-indigo-600 text-white p-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold flex items-center">
            <Database className="w-5 h-5 mr-2" />
            Vedic-AI Structured Engine
          </h2>
          <p className="text-indigo-100 text-sm">Deterministic astrological assessment</p>
        </div>
        <button 
          onClick={handleBackToBrowser}
          className="flex items-center text-sm font-medium bg-indigo-700 hover:bg-indigo-800 px-4 py-2 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Questions
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-50 space-y-6">
        {results.length === 0 && !loading && !error && (
          <div className="text-center text-slate-500 mt-10">
            <p>No results yet. Select a question from the Question Browser.</p>
          </div>
        )}
        
        {results.map((result, idx) => (
          <QuestionResultCard key={idx} result={result} />
        ))}
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
            {error}
          </div>
        )}

        {loading && (
          <div className="flex justify-center my-8">
            <div className="bg-white border border-slate-200 px-6 py-4 rounded-xl shadow-sm flex items-center text-indigo-600 font-medium">
              <Loader2 className="w-6 h-6 mr-3 animate-spin" />
              Calculating deterministic evaluation...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
