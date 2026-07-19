import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, AlertCircle } from 'lucide-react';
import { useConsultationStore } from '../../store/useConsultationStore';
import type { Consultation } from '../../types/consultation';

export default function ConsultationWorkspace() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { openConsultation } = useConsultationStore();
  
  const [consultation, setConsultation] = useState<Consultation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError('No consultation ID provided');
      setLoading(false);
      return;
    }

    const loadConsultation = () => {
      setLoading(true);
      setError(null);

      try {
        const consultation = useConsultationStore.getState().getConsultation(id);
        
        if (!consultation) {
          setError('Consultation not found');
          setLoading(false);
          return;
        }

        setConsultation(consultation);
        openConsultation(id);
      } catch (err) {
        setError('Failed to load consultation');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadConsultation();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-600">Loading consultation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 max-w-md w-full mx-4 text-center">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-slate-900 mb-2">Unable to Load Consultation</h2>
          <p className="text-slate-600 mb-6">{error}</p>
          <button 
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (!consultation) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 max-w-md w-full mx-4 text-center">
          <FileText className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-slate-900 mb-2">Consultation Not Found</h2>
          <p className="text-slate-600 mb-6">This consultation may have been deleted or the ID is invalid.</p>
          <button 
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatDateTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusBadge = (status: Consultation['status']) => {
    switch (status) {
      case 'active':
        return <span className="px-2 py-0.5 text-xs font-medium bg-emerald-100 text-emerald-800 rounded-full">Active</span>;
      case 'completed':
        return <span className="px-2 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-800 rounded-full">Completed</span>;
      case 'archived':
        return <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 text-slate-800 rounded-full">Archived</span>;
      case 'draft':
        return <span className="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-800 rounded-full">Draft</span>;
      default:
        return <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 text-slate-800 rounded-full">{status}</span>;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              
              <div>
                <h1 className="text-lg font-bold text-slate-900">{consultation.name}</h1>
                <p className="text-sm text-slate-500">
                  {consultation.client?.name ? `Client: ${consultation.client.name}` : 'No client assigned'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {getStatusBadge(consultation.status)}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
              <h2 className="text-lg font-bold text-slate-900 mb-4">Consultation Details</h2>
              <dl className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <dt className="text-sm text-slate-500">Status</dt>
                    <dd className="mt-1 flex items-center gap-2">
                      {getStatusBadge(consultation.status)}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm text-slate-500">Created</dt>
                    <dd className="font-medium mt-1">{formatDate(consultation.createdAt)}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-slate-500">Last Modified</dt>
                    <dd className="font-medium mt-1">{formatDateTime(consultation.updatedAt)}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-slate-500">Last Opened</dt>
                    <dd className="font-medium mt-1">
                      {consultation.lastOpenedAt ? formatDateTime(consultation.lastOpenedAt) : 'Never'}
                    </dd>
                  </div>
                </div>
                {consultation.horoscopeSource && (
                  <div>
                    <dt className="text-sm text-slate-500">Horoscope Source</dt>
                    <dd className="font-medium mt-1 text-capitalize">{consultation.horoscopeSource.replace('_', ' ')}</dd>
                  </div>
                )}
                {consultation.tags.length > 0 && (
                  <div>
                    <dt className="text-sm text-slate-500">Tags</dt>
                    <dd className="mt-1 flex flex-wrap gap-2">
                      {consultation.tags.map((tag: string) => (
                        <span key={tag} className="px-2 py-0.5 text-xs bg-indigo-100 text-indigo-700 rounded-full">
                          {tag}
                        </span>
                      ))}
                    </dd>
                  </div>
                )}
                {consultation.notes && (
                  <div>
                    <dt className="text-sm text-slate-500">Notes</dt>
                    <dd className="font-medium mt-1 text-slate-700">{consultation.notes}</dd>
                  </div>
                )}
              </dl>
            </div>

            {consultation.canonicalContent && (
              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                <h2 className="text-lg font-bold text-slate-900 mb-4">Chart Data</h2>
                <p className="text-slate-600">
                  Horoscope data is loaded and ready for processing.
                </p>
              </div>
            )}
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Client</h2>
            {consultation.client ? (
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-slate-500">Name</p>
                  <p className="font-medium text-slate-900">{consultation.client.name}</p>
                </div>
                {consultation.client.email && (
                  <div>
                    <p className="text-sm text-slate-500">Email</p>
                    <p className="font-medium text-slate-900">{consultation.client.email}</p>
                  </div>
                )}
                {consultation.client.phone && (
                  <div>
                    <p className="text-sm text-slate-500">Phone</p>
                    <p className="font-medium text-slate-900">{consultation.client.phone}</p>
                  </div>
                )}
                {consultation.client.birthData && (
                  <div className="pt-3 border-t border-slate-100">
                    <p className="text-sm text-slate-500">Birth Data</p>
                    <p className="font-medium text-slate-900">
                      {consultation.client.birthData.date} {consultation.client.birthData.time}
                    </p>
                    <p className="text-sm text-slate-500">{consultation.client.birthData.place}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-slate-500 mb-4">No client assigned</p>
                <span className="text-sm text-slate-400">Client assignment not implemented in this view</span>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}