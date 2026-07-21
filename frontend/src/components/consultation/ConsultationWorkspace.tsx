import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, AlertCircle, MoreVertical, Edit, Copy, Archive, Trash2, Download, Eye, Printer, Settings, Save, Pin, Star, HelpCircle, X } from 'lucide-react';
import { useConsultationStore } from '../../store/useConsultationStore';
import type { Consultation } from '../../types/consultation';
import { RenameConsultationModal, DeleteConfirmModal, ConsultationEditModal } from '../../components/consultation/ConsultationModals';
import { PrintFrameworkModal } from '../../components/consultation/PrintFrameworkModal';

export default function ConsultationWorkspace() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { openConsultation } = useConsultationStore();
  const { updateConsultation, duplicateConsultation, archiveConsultation, deleteConsultation, togglePin, markSaved } = useConsultationStore();
  
  const [consultation, setConsultation] = useState<Consultation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Action menu state
  const [actionMenuOpen, setActionMenuOpen] = useState(false);
  const [showRenameModal, setShowRenameModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [showEditMetadata, setShowEditMetadata] = useState(false);
  const [activeTab, setActiveTab] = useState<'details' | 'report'>('details');
  const [showShortcuts, setShowShortcuts] = useState(false);

  // Action handlers
  const handleRename = () => {
    setActionMenuOpen(false);
    setShowRenameModal(true);
  };

  const handleDuplicate = () => {
    setActionMenuOpen(false);
    if (!consultation) return;
    try {
      const duplicate = duplicateConsultation(consultation.id);
      navigate(`/consultation/${duplicate.id}`);
    } catch (err) {
      console.error('Failed to duplicate consultation:', err);
      setError('Failed to duplicate consultation');
    }
  };

  const handleArchive = () => {
    setActionMenuOpen(false);
    if (!consultation) return;
    try {
      archiveConsultation(consultation.id);
      setConsultation(prev => prev ? { ...prev, status: 'archived', updatedAt: new Date().toISOString() } : null);
    } catch (err) {
      console.error('Failed to archive consultation:', err);
      setError('Failed to archive consultation');
    }
  };

  const handleDelete = () => {
    setActionMenuOpen(false);
    setShowDeleteConfirm(true);
  };

  const handleRenameConfirm = (consultationId: string, newName: string) => {
    updateConsultation(consultationId, { name: newName });
    setConsultation(prev => prev ? { ...prev, name: newName, updatedAt: new Date().toISOString() } : null);
  };

  const handleDeleteConfirm = (consultationId: string) => {
    deleteConsultation(consultationId);
    navigate('/dashboard');
  };

  const handleSave = () => {
    if (!consultation) return;
    markSaved(consultation.id);
    setConsultation(prev => prev ? { ...prev, hasUnsavedChanges: false, updatedAt: new Date().toISOString() } : null);
  };

  const handleTogglePin = () => {
    if (!consultation) return;
    togglePin(consultation.id);
    setConsultation(prev => prev ? { ...prev, isPinned: !prev.isPinned, updatedAt: new Date().toISOString() } : null);
  };

  const handleEditMetadata = () => {
    setActionMenuOpen(false);
    setShowEditMetadata(true);
  };

  const handleEditMetadataSave = (consultationId: string, metadata: { consultationTitle: string; tags: string[]; status: string; isFavorite: boolean }) => {
    updateConsultation(consultationId, {
      name: metadata.consultationTitle,
      status: metadata.status as Consultation['status'],
      tags: metadata.tags,
    });
    setConsultation(prev => prev ? { 
      ...prev, 
      name: metadata.consultationTitle,
      status: metadata.status as Consultation['status'],
      tags: metadata.tags,
      updatedAt: new Date().toISOString() 
    } : null);
  };

  // Keyboard shortcuts
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    // Don't trigger shortcuts when typing in inputs
    if (event.target instanceof HTMLInputElement || 
        event.target instanceof HTMLTextAreaElement || 
        event.target instanceof HTMLSelectElement) {
      return;
    }

    const isCtrl = event.ctrlKey || event.metaKey;
    const isShift = event.shiftKey;

    if (event.key === '?' && !isCtrl && !isShift) {
      event.preventDefault();
      setShowShortcuts(true);
      return;
    }

    if (event.key === 'Escape') {
      if (showShortcuts) {
        setShowShortcuts(false);
        return;
      }
      // Close any open modals via existing close handlers
      if (showRenameModal) setShowRenameModal(false);
      if (showDeleteConfirm) setShowDeleteConfirm(false);
      if (showReportModal) setShowReportModal(false);
      if (showEditMetadata) setShowEditMetadata(false);
      if (actionMenuOpen) setActionMenuOpen(false);
      return;
    }

    if (!isCtrl) return;

    switch (event.key.toLowerCase()) {
      case 's':
        event.preventDefault();
        if (consultation?.hasUnsavedChanges) handleSave();
        break;
      case 'd':
        if (isShift) {
          event.preventDefault();
          handleDelete();
        } else {
          event.preventDefault();
          handleDuplicate();
        }
        break;
      case 'p':
        event.preventDefault();
        handleTogglePin();
        break;
      case 'f':
        event.preventDefault();
        handleRename();
        break;
      case 'a':
        event.preventDefault();
        handleArchive();
        break;
    }
  }, [consultation, showShortcuts, showRenameModal, showDeleteConfirm, showReportModal, showEditMetadata, actionMenuOpen, handleSave, handleDuplicate, handleDelete, handleTogglePin, handleRename, handleArchive]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

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

  const ShortcutRow: React.FC<{ keys: string[]; description: string }> = ({ keys, description }) => (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm text-slate-600">{description}</span>
      <div className="flex items-center gap-1">
        {keys.map((key, i) => (
          <span key={key} className="flex items-center gap-1">
            <kbd className="px-2 py-1 bg-slate-100 text-slate-700 rounded border border-slate-200 font-mono text-xs">
              {key}
            </kbd>
            {i < keys.length - 1 && <span className="text-slate-400 text-xs">+</span>}
          </span>
        ))}
      </div>
    </div>
  );

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
              
              {/* Unsaved Changes Indicator */}
              {consultation.hasUnsavedChanges && (
                <span className="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-800 rounded-full flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-pulse" />
                  Unsaved changes
                </span>
              )}
              
              {/* Save Button */}
              {consultation.hasUnsavedChanges && (
                <button
                  onClick={handleSave}
                  className="px-3 py-1.5 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 flex items-center gap-1 transition-colors"
                  title="Save changes"
                >
                  <Save className="w-3.5 h-3.5" />
                  Save
                </button>
              )}
              
              {/* Pin Toggle */}
              <button
                onClick={handleTogglePin}
                className={`p-2 rounded-lg transition-colors ${
                  consultation.isPinned
                    ? 'bg-amber-100 text-amber-600'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100'
                }`}
                title={consultation.isPinned ? 'Unpin consultation' : 'Pin consultation'}
                aria-label={consultation.isPinned ? 'Unpin consultation' : 'Pin consultation'}
              >
                <Pin className={`w-5 h-5 ${consultation.isPinned ? 'fill-current' : ''}`} />
              </button>
              
              {/* Favorite Toggle */}
              <button
                onClick={() => {
                  const newFavorite = !consultation.isFavorite;
                  updateConsultation(consultation.id, { isFavorite: newFavorite });
                  setConsultation(prev => prev ? { 
                    ...prev, 
                    isFavorite: newFavorite,
                    updatedAt: new Date().toISOString() 
                  } : null);
                }}
                className={`p-2 rounded-lg transition-colors ${
                  consultation.isFavorite
                    ? 'bg-amber-100 text-amber-600'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100'
                }`}
                title={consultation.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                aria-label={consultation.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
              >
                <Star className={`w-5 h-5 ${consultation.isFavorite ? 'fill-current' : ''}`} />
              </button>
              
              {/* Help Button */}
              <button
                onClick={() => setShowShortcuts(true)}
                className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
                title="Keyboard shortcuts (?)"
                aria-label="Keyboard shortcuts"
              >
                <HelpCircle className="w-5 h-5" />
              </button>
              
              {/* Action Menu */}
              <div className="relative">
                <button
                  onClick={() => setActionMenuOpen(!actionMenuOpen)}
                  className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
                  aria-label="Consultation actions"
                >
                  <MoreVertical className="w-5 h-5" />
                </button>
                
                {actionMenuOpen && (
                  <>
                    <div className="fixed inset-0 z-10" onClick={() => setActionMenuOpen(false)} />
                    <div className="absolute right-0 top-full mt-1 z-20 bg-white border border-slate-200 rounded-lg shadow-lg py-1 min-w-[200px]">
                      <button
                        onClick={handleRename}
                        className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2">
                          <Edit className="w-4 h-4" />
                          Rename
                        </span>
                        <kbd className="px-1.5 py-0.5 text-xs bg-slate-100 text-slate-500 rounded border border-slate-200 font-mono">F2</kbd>
                      </button>
                      <button
                        onClick={handleDuplicate}
                        className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2">
                          <Copy className="w-4 h-4" />
                          Duplicate
                        </span>
                        <kbd className="px-1.5 py-0.5 text-xs bg-slate-100 text-slate-500 rounded border border-slate-200 font-mono">Ctrl+D</kbd>
                      </button>
                      <button
                        onClick={handleArchive}
                        className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2">
                          <Archive className="w-4 h-4" />
                          {consultation.status === 'archived' ? 'Restore' : 'Archive'}
                        </span>
                        <kbd className="px-1.5 py-0.5 text-xs bg-slate-100 text-slate-500 rounded border border-slate-200 font-mono">Ctrl+A</kbd>
                      </button>
                      <button
                        onClick={handleDelete}
                        className="w-full px-3 py-2 text-left text-sm text-rose-600 hover:bg-rose-50 flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2">
                          <Trash2 className="w-4 h-4" />
                          Delete
                        </span>
                        <kbd className="px-1.5 py-0.5 text-xs bg-slate-100 text-slate-500 rounded border border-slate-200 font-mono">Ctrl+Shift+D</kbd>
                      </button>
                      <hr className="my-1 border-slate-200" />
                      <button
                        onClick={handleTogglePin}
                        className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center justify-between gap-2"
                      >
                        <span className="flex items-center gap-2">
                          <Pin className={`w-4 h-4 ${consultation.isPinned ? 'fill-current' : ''}`} />
                          {consultation.isPinned ? 'Unpin' : 'Pin'}
                        </span>
                        <kbd className="px-1.5 py-0.5 text-xs bg-slate-100 text-slate-500 rounded border border-slate-200 font-mono">Ctrl+P</kbd>
                      </button>
                      <button
                        onClick={handleEditMetadata}
                        className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                      >
                        <Edit className="w-4 h-4" />
                        Edit Metadata
                      </button>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-6 border-b border-slate-200">
          <nav className="flex gap-1" role="tablist">
            <button
              onClick={() => setActiveTab('details')}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                activeTab === 'details'
                  ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-600'
                  : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
              }`}
              role="tab"
              aria-selected={activeTab === 'details'}
            >
              Details
            </button>
            <button
              onClick={() => setActiveTab('report')}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                activeTab === 'report'
                  ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-600'
                  : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
              }`}
              role="tab"
              aria-selected={activeTab === 'report'}
            >
              Report
            </button>
          </nav>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            {activeTab === 'details' && (
              <>
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
              </>
            )}

            {activeTab === 'report' && (
              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-bold text-slate-900">Consultation Report</h2>
                  <button
                    onClick={() => setShowReportModal(true)}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2"
                  >
                    <Printer className="w-4 h-4" />
                    Generate / View Report
                  </button>
                </div>

                {consultation.report ? (
                  <div className="space-y-4">
                    <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                          <FileText className="w-5 h-5 text-emerald-600" />
                        </div>
                        <div>
                          <h3 className="font-medium text-emerald-800">Report Available</h3>
                          <p className="text-sm text-emerald-600">A generated report is associated with this consultation.</p>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-white border border-slate-200 rounded-lg p-4">
                        <h4 className="font-medium text-slate-900 mb-3">Report Summary</h4>
                        <dl className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-slate-500">Client</span>
                            <span className="font-medium text-slate-900">{consultation.client?.name || 'Unknown'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Questions Answered</span>
                            <span className="font-medium text-slate-900">{consultation.questionResults?.length || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Status</span>
                            <span className="font-medium text-slate-900">{getStatusBadge(consultation.status)}</span>
                          </div>
                        </dl>
                      </div>
                      <div className="bg-white border border-slate-200 rounded-lg p-4">
                        <h4 className="font-medium text-slate-900 mb-3">Actions</h4>
                        <div className="space-y-2">
                          <button
                            onClick={() => setShowReportModal(true)}
                            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center justify-center gap-2"
                          >
                            <Eye className="w-4 h-4" />
                            View Full Report
                          </button>
                          <button
                            className="w-full px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 flex items-center justify-center gap-2"
                          >
                            <Download className="w-4 h-4" />
                            Download PDF
                          </button>
                          <button
                            className="w-full px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 flex items-center justify-center gap-2"
                          >
                            <Settings className="w-4 h-4" />
                            Regenerate Report
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-slate-900 mb-2">No Report Generated</h3>
                    <p className="text-slate-500 mb-6 max-w-md mx-auto">
                      This consultation doesn't have a generated report yet. Use the button above to generate a professional consultation report with charts, question analysis, and timing insights.
                    </p>
                    <button
                      onClick={() => setShowReportModal(true)}
                      className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center justify-center gap-2 mx-auto"
                    >
                      <Printer className="w-4 h-4" />
                      Generate Report
                    </button>
                  </div>
                )}
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

      {/* Modals */}
      <RenameConsultationModal
        isOpen={showRenameModal}
        consultation={consultation}
        onClose={() => setShowRenameModal(false)}
        onRename={handleRenameConfirm}
      />
      <DeleteConfirmModal
        isOpen={showDeleteConfirm}
        consultation={consultation}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={handleDeleteConfirm}
      />
      <ConsultationEditModal
        isOpen={showEditMetadata}
        consultation={consultation}
        onClose={() => setShowEditMetadata(false)}
        onSave={handleEditMetadataSave}
        onDelete={() => {}}
        onDuplicate={() => {}}
      />
      <PrintFrameworkModal
        isOpen={showReportModal}
        onClose={() => setShowReportModal(false)}
        consultation={consultation}
      />
      
      {/* Keyboard Shortcuts Help Modal */}
      {showShortcuts && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/50" onClick={() => setShowShortcuts(false)} />
          <div className="relative w-full max-w-md bg-white rounded-xl shadow-2xl">
            <div className="p-4 border-b border-slate-200 flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <HelpCircle className="w-5 h-5 text-indigo-600" />
                Keyboard Shortcuts
              </h2>
              <button onClick={() => setShowShortcuts(false)} className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-4 space-y-4">
              <p className="text-sm text-slate-600">Press <kbd className="px-1.5 py-0.5 bg-slate-100 text-slate-700 rounded border border-slate-200 font-mono">?</kbd> anytime to reopen this dialog</p>
              <div className="space-y-3">
                <ShortcutRow keys={['Ctrl', 'S']} description="Save changes" />
                <ShortcutRow keys={['Ctrl', 'D']} description="Duplicate consultation" />
                <ShortcutRow keys={['Ctrl', 'Shift', 'D']} description="Delete consultation" />
                <ShortcutRow keys={['Ctrl', 'P']} description="Toggle pin" />
                <ShortcutRow keys={['Ctrl', 'A']} description="Archive / Restore" />
                <ShortcutRow keys={['F2']} description="Rename consultation" />
                <ShortcutRow keys={['?']} description="Show this help" />
                <ShortcutRow keys={['Esc']} description="Close modals / menus" />
              </div>
            </div>
            <div className="p-4 border-t border-slate-200 flex justify-end">
              <button onClick={() => setShowShortcuts(false)} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                Got it
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}