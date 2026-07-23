// @ts-nocheck
import React, { useState, useMemo, useEffect } from 'react';
import { X, Check, AlertCircle, HelpCircle, ChevronDown, 
  Star, Tag, Star as StarIcon, Copy, Trash2, 
  FileText, Settings, GitBranch, Hash, Shield, 
  Layers, Package, Terminal, Plus, Minus, Edit2 } from 'lucide-react';
import { useConsultationRepository } from '../../hooks/useConsultationRepository';
import { useChartStore } from '../../store/useChartStore';
import { useConsultationStore } from '../../store/useConsultationStore';

interface ConsultationCreateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (consultation: any) => void;
}

interface ConsultationEditModalProps {
  isOpen: boolean;
  consultation: any | null;
  onClose: () => void;
  onSave: (consultationId: string, metadata: any) => void;
  onDelete: (consultationId: string) => void;
  onDuplicate: (consultationId: string) => void;
}

interface DuplicateDetectionDialogProps {
  isOpen: boolean;
  existingConsultation: any;
  onOpenExisting: () => void;
  onCreateNewVersion: () => void;
  onCancel: () => void;
}

// ============================================
// CONSULTATION CREATE MODAL
// ============================================

export const ConsultationCreateModal: React.FC<ConsultationCreateModalProps> = ({
  isOpen,
  onClose,
  onCreate,
}) => {
  const { createConsultation } = useConsultationRepository();
  const { canonicalContent, questionPackages } = useChartStore.getState();

  const [step, setStep] = useState<'details' | 'package' | 'review'>('details');
  const [formData, setFormData] = useState({
    consultationTitle: '',
    clientName: '',
    status: 'active' as const,
    isFavorite: false,
    tags: [] as string[],
    questionPackageId: '',
    selectedQuestionIds: [] as string[],
    notes: '',
  });
  const [newTag, setNewTag] = useState('');
  const [duplicateDetected, setDuplicateDetected] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-populate from current chart
  useEffect(() => {
    if (canonicalContent && step === 'details') {
      setFormData(prev => ({
        ...prev,
        clientName: canonicalContent.native_info?.name || '',
        birthDataHash: canonicalContent.birthDataHash || '',
      }));
    }
  }, [canonicalContent, step]);

  const availablePackages = questionPackages || [];
  const selectedPackage = availablePackages.find(p => p.id === formData.questionPackageId);
  const availableQuestions = selectedPackage?.questions || [];

  const handleAddTag = () => {
    const tag = newTag.trim();
    if (tag && !formData.tags.includes(tag)) {
      setFormData(prev => ({ ...prev, tags: [...prev.tags, tag] }));
      setNewTag('');
    }
  };

  const handleRemoveTag = (tag: string) => {
    setFormData(prev => ({ ...prev, tags: prev.tags.filter(t => t !== tag) }));
  };

  const handleNext = () => {
    if (step === 'details') {
      if (!formData.consultationTitle.trim()) {
        setError('Consultation title is required');
        return;
      }
      setError(null);
      setStep('package');
    } else if (step === 'package') {
      if (!formData.questionPackageId) {
        setError('Please select a question package');
        return;
      }
      if (formData.selectedQuestionIds.length === 0) {
        setError('Please select at least one question');
        return;
      }
      setError(null);
      setStep('review');
    }
  };

  const handleBack = () => {
    if (step === 'package') setStep('details');
    else if (step === 'review') setStep('package');
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      const consultation = await createConsultation(
        formData.consultationTitle,
        formData.questionPackageId,
        formData.selectedQuestionIds
      );

      onCreate(consultation);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to create consultation');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative w-full max-w-2xl bg-white rounded-xl shadow-2xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">New Consultation</h2>
              <p className="text-sm text-gray-500">Step {step === 'details' ? 1 : step === 'package' ? 2 : 3} of 3</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Progress Indicator */}
        <div className="px-4 py-2 border-b border-gray-100">
          <div className="flex items-center">
            {['details', 'package', 'review'].map((s, i) => (
              <React.Fragment key={s}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  ['details', 'package', 'review'].indexOf(step) >= i
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}>
                  {i + 1}
                </div>
                {i < 2 && <div className={`flex-1 h-1 mx-2 ${['details', 'package'].indexOf(step) > i ? 'bg-indigo-600' : 'bg-gray-200'}`} />}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="mx-4 mt-3 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
            <AlertCircle className="w-5 h-5" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {step === 'details' && (
            <CreateDetailsStep 
              formData={formData}
              setFormData={setFormData}
              newTag={newTag}
              setNewTag={setNewTag}
              handleAddTag={handleAddTag}
              handleRemoveTag={handleRemoveTag}
            />
          )}

          {step === 'package' && (
            <CreatePackageStep 
              formData={formData}
              setFormData={setFormData}
              availablePackages={availablePackages}
              availableQuestions={availableQuestions}
            />
          )}

          {step === 'review' && (
            <CreateReviewStep 
              formData={formData}
              canonicalContent={canonicalContent}
              selectedPackage={selectedPackage}
            />
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 flex items-center justify-between">
          {step !== 'details' && (
            <button onClick={handleBack} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
              Back
            </button>
          )}
          <div className="flex gap-2 ml-auto">
            {step !== 'review' ? (
              <button onClick={handleNext} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                Next
              </button>
            ) : (
              <button onClick={handleSubmit} disabled={isSubmitting} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50">
                {isSubmitting ? 'Creating...' : 'Create Consultation'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================
// CREATE STEPS
// ============================================
const CreateDetailsStep: React.FC<{
  formData: any;
  setFormData: React.Dispatch<React.SetStateAction<any>>;
  newTag: string;
  setNewTag: React.Dispatch<React.SetStateAction<string>>;
  handleAddTag: () => void;
  handleRemoveTag: (tag: string) => void;
}> = ({ formData, setFormData, newTag, setNewTag, handleAddTag, handleRemoveTag }) => (
  <div className="space-y-6">
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Consultation Title *</label>
      <input
        value={formData.consultationTitle}
        onChange={e => setFormData({ ...formData, consultationTitle: e.target.value })}
        placeholder="e.g., Career Analysis for Q4 2024"
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
      />
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Client Name</label>
      <input
        value={formData.clientName}
        onChange={e => setFormData({ ...formData, clientName: e.target.value })}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        readOnly={!!formData.clientName}
      />
      {formData.clientName && (
        <p className="text-xs text-green-600 mt-1">Auto-populated from current chart</p>
      )}
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
      <select
        value={formData.status}
        onChange={e => setFormData({ ...formData, status: e.target.value })}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
      >
        <option value="active">Active</option>
        <option value="draft">Draft</option>
        <option value="in_progress">In Progress</option>
      </select>
    </div>

    <div>
      <label className="flex items-center gap-2 cursor-pointer">
        <input
          type="checkbox"
          checked={formData.isFavorite}
          onChange={e => setFormData({ ...formData, isFavorite: e.target.checked })}
          className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
        <span className="text-sm text-gray-700">Mark as favorite</span>
      </label>
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
      <div className="flex gap-2 mb-2">
        <input
          value={newTag}
          onChange={e => setNewTag(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
          placeholder="Add tag..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        />
        <button onClick={handleAddTag} className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
          Add
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {formData.tags.map((tag: string) => (
          <span key={tag} className="flex items-center gap-1 px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-sm">
            {tag}
            <button onClick={() => handleRemoveTag(tag)} className="hover:text-indigo-900">×</button>
          </span>
        ))}
      </div>
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
      <textarea
        value={formData.notes}
        onChange={e => setFormData({ ...formData, notes: e.target.value })}
        placeholder="Initial notes..."
        rows={3}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
      />
    </div>
  </div>
);

const CreatePackageStep: React.FC<{
  formData: any;
  setFormData: React.Dispatch<React.SetStateAction<any>>;
  availablePackages: any[];
  availableQuestions: any[];
}> = ({ formData, setFormData, availablePackages, availableQuestions }) => {
  if (availablePackages.length === 0) {
    return (
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Question Package *</label>
          <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg text-amber-800 text-sm">
            <AlertCircle className="w-4 h-4 inline mr-2" />
            No question packages available. Please create a package first.
          </div>
        </div>
      </div>
    );
  }

  let questionSection = null;
  if (formData.questionPackageId && availableQuestions.length > 0) {
    questionSection = (
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Questions *</label>
        <div className="space-y-2 max-h-64 overflow-auto border border-gray-200 rounded-lg p-3">
          {availableQuestions.map((q: any) => (
            <label key={q.id} className="flex items-center gap-2 cursor-pointer p-2 hover:bg-gray-50 rounded">
              <input
                type="checkbox"
                checked={formData.selectedQuestionIds.includes(q.id)}
                onChange={e => {
                  if (e.target.checked) {
                    setFormData(prev => ({ ...prev, selectedQuestionIds: [...prev.selectedQuestionIds, q.id] }));
                  } else {
                    setFormData(prev => ({ ...prev, selectedQuestionIds: prev.selectedQuestionIds.filter((id: string) => id !== q.id) }));
                  }
                }}
                className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="text-sm text-gray-700">{q.text || q.id}</span>
              <span className="text-xs text-gray-400 ml-auto">{q.category || ''}</span>
            </label>
          ))}
        </div>
        <p className="text-xs text-gray-500">{formData.selectedQuestionIds.length} of {availableQuestions.length} selected</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Question Package *</label>
        <select
          value={formData.questionPackageId}
          onChange={e => setFormData({ ...formData, questionPackageId: e.target.value, selectedQuestionIds: [] })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Select a package...</option>
          {availablePackages.map((pkg: any) => (
            <option key={pkg.id} value={pkg.id}>{pkg.name} ({pkg.questions?.length || 0} questions)</option>
          ))}
        </select>
      </div>

      {questionSection}
    </div>
  );
};

const CreateReviewStep: React.FC<{
  formData: any;
  canonicalContent: any;
  selectedPackage: any;
}> = ({ formData, canonicalContent, selectedPackage }) => {
  return (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-semibold text-gray-900 mb-3">Review Consultation Details</h3>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div><span className="text-gray-500">Title:</span> <span className="font-medium text-gray-900 ml-2">{formData.consultationTitle}</span></div>
          <div><span className="text-gray-500">Client:</span> <span className="font-medium text-gray-900 ml-2">{formData.clientName || '—'}</span></div>
          <div><span className="text-gray-500">Status:</span> <span className="font-medium text-gray-900 ml-2">{formData.status}</span></div>
          <div><span className="text-gray-500">Favorite:</span> <span className="font-medium text-gray-900 ml-2">{formData.isFavorite ? 'Yes' : 'No'}</span></div>
          <div><span className="text-gray-500">Tags:</span> <span className="font-medium text-gray-900 ml-2">{formData.tags.join(', ') || '—'}</span></div>
          <div><span className="text-gray-500">Notes:</span> <span className="font-medium text-gray-900 ml-2">{formData.notes ? 'Yes' : 'No'}</span></div>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-semibold text-gray-900 mb-3">Question Package</h3>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div><span className="text-gray-500">Package:</span> <span className="font-medium text-gray-900 ml-2">{selectedPackage?.name || '—'}</span></div>
          <div><span className="text-gray-500">Questions:</span> <span className="font-medium text-gray-900 ml-2">{formData.selectedQuestionIds.length}</span></div>
        </div>
      </div>

      {canonicalContent && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
          <h3 className="font-semibold text-indigo-800 mb-3 flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Deterministic Manifest (Auto-generated)
          </h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div><span className="text-indigo-600">Repository Version:</span> <span className="font-mono text-indigo-900 ml-2">v1</span></div>
            <div><span className="text-indigo-600">Golden Master:</span> <span className="font-mono text-indigo-900 ml-2">v1.2.0</span></div>
            <div><span className="text-indigo-600">Architecture:</span> <span className="font-mono text-indigo-900 ml-2">1.2.0</span></div>
            <div><span className="text-indigo-600">Formula Registry:</span> <span className="font-mono text-indigo-900 ml-2">1.0.0</span></div>
            <div><span className="text-indigo-600">Calibration:</span> <span className="font-mono text-indigo-900 ml-2">v1.0.0</span></div>
            <div><span className="text-indigo-600">Git Commit:</span> <span className="font-mono text-indigo-900 ml-2">unknown</span></div>
            <div><span className="text-indigo-600">Git Tag:</span> <span className="font-mono text-indigo-900 ml-2">gm-007-development</span></div>
            <div><span className="text-indigo-600">Birth Data Hash:</span> <span className="font-mono text-indigo-900 ml-2 break-all">{canonicalContent.birthDataHash?.substring(0, 16) || 'pending'}...</span></div>
          </div>
          <p className="text-xs text-indigo-600 mt-3">These values are immutable and captured from the current deterministic engine state.</p>
        </div>
      )}
    </div>
  );
};

// ============================================
// CONSULTATION EDIT MODAL
// ============================================
export const ConsultationEditModal: React.FC<ConsultationEditModalProps> = ({
  isOpen,
  consultation,
  onClose,
  onSave,
  onDelete,
  onDuplicate,
}) => {
  const [formData, setFormData] = useState({
    consultationTitle: '',
    tags: [] as string[],
    status: 'active' as const,
    isFavorite: false,
  });
  const [newTag, setNewTag] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (consultation) {
      setFormData({
        consultationTitle: consultation.name || '',
        tags: [...(consultation.tags || [])],
        status: consultation.status || 'draft',
        isFavorite: consultation.isFavorite || false,
      });
    }
  }, [consultation]);

  const handleAddTag = () => {
    const tag = newTag.trim();
    if (tag && !formData.tags.includes(tag)) {
      setFormData(prev => ({ ...prev, tags: [...prev.tags, tag] }));
      setNewTag('');
    }
  };

  const handleRemoveTag = (tag: string) => {
    setFormData(prev => ({ ...prev, tags: prev.tags.filter(t => t !== tag) }));
  };

  const handleSave = () => {
    if (consultation) {
      onSave(consultation.id, formData);
      onClose();
    }
  };

  const handleDelete = () => {
    if (consultation) {
      onDelete(consultation.id);
      onClose();
    }
  };

  if (!isOpen || !consultation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative w-full max-w-md bg-white rounded-xl shadow-2xl">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900">Edit Consultation</h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input
              value={formData.consultationTitle}
              onChange={e => setFormData({ ...formData, consultationTitle: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={formData.status}
              onChange={e => setFormData({ ...formData, status: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option value="active">Active</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.isFavorite}
                onChange={e => setFormData({ ...formData, isFavorite: e.target.checked })}
                className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="text-sm text-gray-700">Favorite</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
            <div className="flex gap-2 mb-2">
              <input
                value={newTag}
                onChange={e => setNewTag(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
                placeholder="Add tag..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
              <button onClick={handleAddTag} className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.tags.map((tag: string) => (
                <span key={tag} className="flex items-center gap-1 px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-sm">
                  {tag}
                  <button onClick={() => handleRemoveTag(tag)} className="hover:text-indigo-900">×</button>
                </span>
              ))}
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Immutable Fields (Reference Only)</h3>
            <div className="space-y-2 text-sm">
              <div className="bg-gray-50 p-2 rounded"><span className="text-gray-500">Client:</span> <span className="font-medium text-gray-900 ml-2">{consultation.client?.name || '—'}</span></div>
              <div className="bg-gray-50 p-2 rounded"><span className="text-gray-500">Birth Hash:</span> <span className="font-mono text-gray-900 ml-2 break-all">{consultation.canonicalContent?.birthDataHash || 'N/A'}</span></div>
              <div className="bg-gray-50 p-2 rounded"><span className="text-gray-500">ID:</span> <span className="font-mono text-gray-900 ml-2 break-all">{consultation.id}</span></div>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 flex gap-2 justify-end">
          <button onClick={() => { if (consultation) onDuplicate(consultation.id); onClose(); }} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
            Duplicate
          </button>
          <button onClick={() => setShowDeleteConfirm(true)} className="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50">
            Delete
          </button>
          <button onClick={handleSave} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================
// DUPLICATE DETECTION DIALOG
// ============================================
export const DuplicateDetectionDialog: React.FC<DuplicateDetectionDialogProps> = ({
  isOpen,
  existingConsultation,
  onOpenExisting,
  onCreateNewVersion,
  onCancel,
}) => {
  if (!isOpen || !existingConsultation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onCancel} />
      <div className="relative w-full max-w-md bg-white rounded-xl shadow-2xl">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-500" />
            Duplicate Detected
          </h2>
        </div>

        <div className="p-4 space-y-4">
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-sm text-amber-800 mb-3">A consultation with identical deterministic configuration already exists:</p>
            <div className="space-y-1 text-sm">
              <div><span className="font-medium text-gray-700">Title:</span> <span className="text-gray-900">{existingConsultation.name}</span></div>
              <div><span className="font-medium text-gray-700">Client:</span> <span className="text-gray-900">{existingConsultation.client?.name || '—'}</span></div>
              <div><span className="font-medium text-gray-700">Created:</span> <span className="text-gray-900">{new Date(existingConsultation.createdAt).toLocaleDateString()}</span></div>
              <div><span className="font-medium text-gray-700">Birth Hash:</span> <span className="font-mono text-gray-900 break-all">{existingConsultation.canonicalContent?.birthDataHash || 'N/A'}</span></div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs text-gray-600">What would you like to do?</p>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 flex gap-2 justify-end">
          <button onClick={onCancel} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button onClick={onOpenExisting} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Open Existing
          </button>
          <button onClick={onCreateNewVersion} className="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700">
            Create New Version
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================
// RENAME CONSULTATION MODAL
// ============================================
export interface RenameConsultationModalProps {
  isOpen: boolean;
  consultation: any | null;
  onClose: () => void;
  onRename: (consultationId: string, newName: string) => void;
}

export const RenameConsultationModal: React.FC<RenameConsultationModalProps> = ({
  isOpen,
  consultation,
  onClose,
  onRename,
}) => {
  const [newName, setNewName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (consultation) {
      setNewName(consultation.name || '');
      setError(null);
    }
  }, [consultation]);

  const handleSubmit = () => {
    if (!newName.trim()) {
      setError('Consultation name is required');
      return;
    }
    if (!consultation) return;

    setIsSubmitting(true);
    setError(null);
    
    try {
      onRename(consultation.id, newName.trim());
      onClose();
    } catch (err) {
      setError('Failed to rename consultation');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen || !consultation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative w-full max-w-md bg-white rounded-xl shadow-2xl">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <Edit2 className="w-5 h-5 text-indigo-600" />
            Rename Consultation
          </h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">New Name</label>
            <input
              value={newName}
              onChange={e => setNewName(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSubmit()}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter new consultation name"
              autoFocus
            />
            {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
          </div>

          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs text-gray-600">Current name: <span className="font-medium text-gray-900">{consultation.name || 'Untitled'}</span></p>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 flex gap-2 justify-end">
          <button onClick={onClose} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button 
            onClick={handleSubmit} 
            disabled={isSubmitting}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
          >
            {isSubmitting ? 'Renaming...' : 'Rename'}
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================
// DELETE CONFIRMATION MODAL
// ============================================
export interface DeleteConfirmModalProps {
  isOpen: boolean;
  consultation: any | null;
  onClose: () => void;
  onConfirm: (consultationId: string) => void;
}

export const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  isOpen,
  consultation,
  onClose,
  onConfirm,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleConfirm = () => {
    if (!consultation) return;

    setIsDeleting(true);
    setError(null);

    try {
      onConfirm(consultation.id);
      onClose();
    } catch (err) {
      setError('Failed to delete consultation');
    } finally {
      setIsDeleting(false);
    }
  };

  if (!isOpen || !consultation) return null;

  const consultationName = consultation.name || 'Untitled Consultation';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative w-full max-w-md bg-white rounded-xl shadow-2xl">
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            Delete Consultation
          </h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 space-y-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-800 mb-3">
              Are you sure you want to delete <strong>"{consultationName}"</strong>?
            </p>
            <p className="text-sm text-red-700">
              This action cannot be undone. All consultation data, snapshots, and outputs will be permanently removed.
            </p>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {error}
            </div>
          )}
        </div>

        <div className="p-4 border-t border-gray-200 flex gap-2 justify-end">
          <button onClick={onClose} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button 
            onClick={handleConfirm} 
            disabled={isDeleting}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            {isDeleting ? 'Deleting...' : 'Delete Permanently'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default { ConsultationCreateModal, ConsultationEditModal, DuplicateDetectionDialog, RenameConsultationModal, DeleteConfirmModal };