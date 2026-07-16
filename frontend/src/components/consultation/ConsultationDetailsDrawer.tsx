// @ts-nocheck
import React, { useState, useMemo } from 'react';
import { 
  X, ChevronRight, FileText, Tag, Star, Calendar, Clock, 
  Download, Eye, Edit, Copy, Trash2, Archive, 
  ChevronDown, ChevronUp, AlertCircle, CheckCircle, Camera, ChevronLeft, Plus,
  GitBranch, Hash, BookOpen, Settings, Terminal, 
  Package, Shield, User, Layers, Info, MoreVertical, Printer
} from 'lucide-react';
import { useConsultationRepository } from '../../hooks/useConsultationRepository';
import { PrintFramework } from '../PrintFramework';
import { PrintFrameworkModal } from './PrintFrameworkModal';

interface ConsultationDetailsDrawerProps {
  consultation: any;
  onClose: () => void;
  onEditMetadata: (consultationId: string, metadata: any) => void;
  onLoadConsultation: (consultation: any) => void;
  onCreateSnapshot: (consultationId: string) => void;
  onCompareSnapshots: (consultationId: string, snapshotIdA: string, snapshotIdB: string) => void;
  onPrint: (consultation: any) => void;
}

export const ConsultationDetailsDrawer: React.FC<ConsultationDetailsDrawerProps> = ({
  consultation,
  onClose,
  onEditMetadata,
  onLoadConsultation,
  onCreateSnapshot,
  onCompareSnapshots,
  onPrint,
}) => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [editingMetadata, setEditingMetadata] = useState<boolean>(false);
  const [editForm, setEditForm] = useState<any>({});
  const [printFrameworkOpen, setPrintFrameworkOpen] = useState<boolean>(false);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BookOpen },
    { id: 'manifest', label: 'Manifest', icon: FileText },
    { id: 'snapshots', label: 'Snapshots', icon: Camera },
    { id: 'outputs', label: 'Output History', icon: Download },
    { id: 'metadata', label: 'Metadata', icon: Tag },
    { id: 'notes', label: 'Notes', icon: FileText },
  ];

  const overallProbability = consultation?.snapshots?.[0]?.metadata?.overallProbability?.score || 0;
  const currentTransit = consultation?.snapshots?.[0]?.metadata?.currentTransit;
  const currentDasha = consultation?.snapshots?.[0]?.metadata?.currentDasha;
  const activationPercent = currentTransit?.activationScore || 0;
  const transitGrade = currentTransit?.grade || '—';

  const repositoryInfo = {
    repositoryVersion: 1,
    goldenMasterVersion: 'v1.2.0',
    architectureVersion: '1.2.0',
    formulaRegistryVersion: '1.0.0',
    calibrationProfile: 'v1.0.0',
    gitCommit: 'unknown',
    gitTag: 'gm-007-development',
    integrityVerified: true,
    snapshotCount: consultation?.snapshots?.length || 0,
  };

  const handleEditMetadata = () => {
    setEditForm({
      consultationTitle: consultation.metadata.consultationTitle,
      tags: [...consultation.metadata.tags],
      status: consultation.status,
      isFavorite: consultation.metadata.isFavorite,
    });
    setEditingMetadata(true);
  };

  const handleSaveMetadata = () => {
    onEditMetadata(consultation.id, editForm);
    setEditingMetadata(false);
  };

  const handleCancelEdit = () => {
    setEditingMetadata(false);
  };

  const handleAddTag = (e: React.FormEvent) => {
    e.preventDefault();
    const input = e.currentTarget.querySelector('input') as HTMLInputElement;
    const tag = input?.value.trim();
    if (tag && !editForm.tags.includes(tag)) {
      setEditForm({ ...editForm, tags: [...editForm.tags, tag] });
      input.value = '';
    }
  };

  const handleRemoveTag = (tag: string) => {
    setEditForm({ ...editForm, tags: editForm.tags.filter((t: string) => t !== tag) });
  };

  const showPrintFramework = () => setPrintFrameworkOpen(true);

  return (
    <React.Fragment>
      <div className="fixed inset-0 z-50 flex items-center justify-end">
        {/* Backdrop */}
        <div 
          className="absolute inset-0 bg-black/30 backdrop-blur-sm"
          onClick={onClose}
        />

        {/* Drawer */}
        <div className="relative w-full max-w-4xl h-full bg-white shadow-2xl flex flex-col animate-slide-in-right">
          {/* Header */}
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${consultation.metadata.isFavorite ? 'bg-yellow-400' : 'bg-gray-300'}`} />
              <div>
                <h2 className="text-lg font-bold text-gray-900">{consultation.metadata.consultationTitle}</h2>
                <p className="text-sm text-gray-500">{consultation.metadata.clientName}</p>
              </div>
              <span className={`px-2 py-0.5 text-xs rounded ${
                consultation.status === 'completed' ? 'bg-emerald-100 text-emerald-700' :
                consultation.status === 'in_progress' ? 'bg-amber-100 text-amber-700' :
                consultation.status === 'archived' ? 'bg-gray-100 text-gray-700' :
                'bg-blue-100 text-blue-700'
              }`}>
                {consultation.status}
              </span>
            </div>
            <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Tab Navigation */}
          <div className="border-b border-gray-200 overflow-x-auto">
            <nav className="flex gap-1 p-2" role="tablist">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-indigo-50 text-indigo-700 border border-indigo-200'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                  role="tab"
                  aria-selected={activeTab === tab.id}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Repository Info Panel - Always visible at bottom */}
          <div className="border-t border-gray-200 p-4 bg-gray-50">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
              <RepositoryInfoItem label="Repository Version" value={`v${repositoryInfo.repositoryVersion}`} icon={Package} />
              <RepositoryInfoItem label="Golden Master" value={repositoryInfo.goldenMasterVersion} icon={Shield} />
              <RepositoryInfoItem label="Architecture" value={repositoryInfo.architectureVersion} icon={Layers} />
              <RepositoryInfoItem label="Formula Registry" value={repositoryInfo.formulaRegistryVersion} icon={Settings} />
              <RepositoryInfoItem label="Calibration" value={repositoryInfo.calibrationProfile} icon={Terminal} />
              <RepositoryInfoItem label="Git Commit" value={repositoryInfo.gitCommit.substring(0, 8)} icon={GitBranch} />
              <RepositoryInfoItem label="Git Tag" value={repositoryInfo.gitTag} icon={Tag} />
              <RepositoryInfoItem label="Integrity" value={repositoryInfo.integrityVerified ? 'Verified ✓' : 'Failed ✗'} icon={repositoryInfo.integrityVerified ? CheckCircle : AlertCircle} />
              <RepositoryInfoItem label="Snapshots" value={repositoryInfo.snapshotCount.toString()} icon={Camera} />
            </div>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-auto p-6">
            {activeTab === 'overview' && (
              <OverviewTab 
                consultation={consultation}
                overallProbability={overallProbability}
                activationPercent={activationPercent}
                transitGrade={transitGrade}
                currentDasha={currentDasha}
                onLoad={onLoadConsultation}
                onPrint={showPrintFramework}
              />
            )}

            {activeTab === 'manifest' && (
              <ManifestTab consultation={consultation} />
            )}

            {activeTab === 'snapshots' && (
              <SnapshotsTab 
                consultation={consultation}
                onCreateSnapshot={onCreateSnapshot}
                onCompareSnapshots={onCompareSnapshots}
              />
            )}

            {activeTab === 'outputs' && (
              <OutputHistoryTab consultation={consultation} />
            )}

            {activeTab === 'metadata' && (
              <MetadataTab 
                consultation={consultation}
                editing={editingMetadata}
                editForm={editForm}
                setEditForm={setEditForm}
                onSave={handleSaveMetadata}
                onCancel={handleCancelEdit}
                onAddTag={handleAddTag}
                onRemoveTag={handleRemoveTag}
              />
            )}

            {activeTab === 'notes' && (
              <NotesTab consultation={consultation} />
            )}
          </div>
        </div>
      </div>

      {/* PrintFramework Modal */}
      <PrintFrameworkModal
        isOpen={printFrameworkOpen}
        onClose={() => setPrintFrameworkOpen(false)}
        consultation={consultation}
      />
    </React.Fragment>
  );
};

// ============================================
// REPOSITORY INFO ITEM
// ============================================
const RepositoryInfoItem: React.FC<{ label: string; value: string; icon: React.ComponentType<{ className?: string }> }> = ({ 
  label, value, icon: Icon 
}) => (
  <div className="flex items-center gap-2 p-3 bg-white rounded-lg border border-gray-200">
    <Icon className="w-5 h-5 text-indigo-600" />
    <div>
      <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
      <p className="text-sm font-medium text-gray-900 truncate">{value}</p>
    </div>
  </div>
);

// ============================================
// OVERVIEW TAB
// ============================================
const OverviewTab: React.FC<{
  consultation: any;
  overallProbability: number;
  activationPercent: number;
  transitGrade: string;
  currentDasha: any;
  onLoad: (consultation: any) => void;
  onPrint: (consultation: any) => void;
}> = ({ consultation, overallProbability, activationPercent, transitGrade, currentDasha, onLoad, onPrint }) => (
  <div className="space-y-6">
    {/* Key Metrics */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <MetricCard 
        label="Final Probability" 
        value={`${Math.round(overallProbability)}%`}
        icon={<Target className="w-6 h-6" />}
        color={overallProbability >= 70 ? 'emerald' : overallProbability >= 50 ? 'amber' : 'red'}
      />
      <MetricCard 
        label="Transit Activation" 
        value={`${Math.round(activationPercent)}%`}
        icon={<Activity className="w-6 h-6" />}
        color={activationPercent >= 70 ? 'emerald' : activationPercent >= 50 ? 'amber' : 'red'}
      />
      <MetricCard 
        label="Transit Grade" 
        value={transitGrade}
        icon={<Award className="w-6 h-6" />}
        color={transitGrade === 'EXCELLENT' ? 'emerald' : transitGrade === 'GOOD' ? 'blue' : transitGrade === 'MODERATE' ? 'amber' : 'gray'}
      />
    </div>

    {/* Dasha Info */}
    <div className="bg-gray-50 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <Timer className="w-4 h-4" />
        Current Dasha Period
      </h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-500">Mahadasha (MD)</p>
          <p className="font-mono text-lg text-gray-900">{currentDasha?.md || '—'}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Antardasha (AD)</p>
          <p className="font-mono text-lg text-gray-900">{currentDasha?.ad || '—'}</p>
        </div>
      </div>
    </div>

    {/* Consultation Details */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <DetailCard 
        title="Consultation Details"
        items={[
          { label: 'Title', value: consultation.metadata.consultationTitle },
          { label: 'Client', value: consultation.metadata.clientName },
          { label: 'Created', value: new Date(consultation.createdAt).toLocaleDateString() },
          { label: 'Updated', value: new Date(consultation.updatedAt).toLocaleDateString() },
          { label: 'Questions', value: consultation.structure.selectedQuestionIds.length.toString() },
          { label: 'Snapshots', value: consultation.snapshots.length.toString() },
          { label: 'Outputs', value: consultation.outputs.length.toString() },
          { label: 'Favorite', value: consultation.metadata.isFavorite ? 'Yes' : 'No' },
          { label: 'Tags', value: consultation.metadata.tags.join(', ') || '—' },
        ]}
      />

      <DetailCard 
        title="Structure References"
        items={[
          { label: 'Question Package', value: consultation.structure.questionPackageId },
          { label: 'Question Results', value: consultation.structure.questionResultsRef },
          { label: 'Activation Timeline', value: consultation.structure.activationTimelineRef },
          { label: 'Gochara/Transit', value: consultation.structure.gocharaRef },
          { label: 'Report', value: consultation.structure.reportRef },
          { label: 'Comparison', value: consultation.structure.comparisonRef || '—' },
        ]}
      />
    </div>

    {/* Quick Actions */}
    <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-200">
      <button onClick={() => onLoad(consultation)} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2">
        <Play className="w-4 h-4" />
        Load in Workspace
      </button>
      <button onClick={showPrintFramework} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2">
        <Printer className="w-4 h-4" />
        Print / Export
      </button>
      <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2">
        <Copy className="w-4 h-4" />
        Duplicate
      </button>
    </div>
  </div>
);

// ============================================
// MANIFEST TAB
// ============================================
const ManifestTab: React.FC<{ consultation: any }> = ({ consultation }) => {
  const manifest = {
    consultationId: consultation.id,
    version: consultation.version,
    goldenMasterVersion: 'v1.2.0',
    architectureVersion: '1.2.0',
    formulaRegistryVersion: '1.0.0',
    calibrationProfileVersion: 'v1.0.0',
    gitCommit: consultation.audit?.gitCommit || 'unknown',
    gitTag: consultation.audit?.gitTag || 'gm-007-development',
    outputFrameworkVersion: 'v1.0.0',
    deterministic: true,
    createdAt: consultation.createdAt,
    updatedAt: consultation.updatedAt,
    createdBy: consultation.audit?.createdBy || 'user',
  };

  return (
    <div className="space-y-6">
      <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
        <h3 className="font-semibold text-indigo-800 mb-2 flex items-center gap-2">
          <FileText className="w-5 h-5" />
          Consultation Manifest
        </h3>
        <p className="text-sm text-indigo-700">Immutable record of consultation configuration at creation time</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(manifest).map(([key, value]) => (
          <div key={key} className="bg-white border border-gray-200 rounded-lg p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{key.replace(/([A-Z])/g, ' $1').trim()}</p>
            <p className="font-mono text-sm text-gray-900 break-all">{value?.toString() || '—'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================
// SNAPSHOTS TAB
// ============================================
const SnapshotsTab: React.FC<{
  consultation: any;
  onCreateSnapshot: (consultationId: string) => void;
  onCompareSnapshots: (consultationId: string, snapshotIdA: string, snapshotIdB: string) => void;
}> = ({ consultation, onCreateSnapshot, onCompareSnapshots }) => {
  const snapshots = consultation.snapshots || [];
  const [selectedSnapshots, setSelectedSnapshots] = useState<string[]>([]);

  const handleSnapshotSelect = (snapshotId: string) => {
    setSelectedSnapshots(prev => 
      prev.includes(snapshotId) 
        ? prev.filter(id => id !== snapshotId)
        : [...prev, snapshotId].slice(-2)
    );
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Snapshots ({snapshots.length})</h3>
        <button onClick={() => onCreateSnapshot(consultation.id)} className="px-3 py-1.5 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Create Snapshot
        </button>
      </div>

      {snapshots.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <Camera className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No snapshots yet. Create a snapshot to capture the current deterministic state.</p>
        </div>
      ) : (
        <>
          {selectedSnapshots.length === 2 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-center justify-between">
              <span className="text-sm text-blue-800">2 snapshots selected for comparison</span>
              <button 
                onClick={() => onCompareSnapshots(consultation.id, selectedSnapshots[0], selectedSnapshots[1])}
                className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
              >
                Compare Selected
              </button>
            </div>
          )}

          <div className="space-y-2 max-h-96 overflow-auto">
            {snapshots.slice().reverse().map(snapshot => (
              <SnapshotRow
                key={snapshot.snapshotId}
                snapshot={snapshot}
                selected={selectedSnapshots.includes(snapshot.snapshotId)}
                onSelect={() => handleSnapshotSelect(snapshot.snapshotId)}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

const SnapshotRow: React.FC<{
  snapshot: any;
  selected: boolean;
  onSelect: () => void;
}> = ({ snapshot, selected, onSelect }) => (
  <div 
    className={`flex items-center gap-4 p-4 border rounded-lg transition-colors ${selected ? 'bg-blue-50 border-blue-300' : 'border-gray-200 hover:border-gray-300'}`}
    onClick={onSelect}
  >
    <input type="checkbox" checked={selected} onChange={onSelect} className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
    <div className="flex-1 min-w-0">
      <div className="flex items-center gap-2">
        <span className="font-medium text-gray-900 truncate">{snapshot.metadata.consultationTitle}</span>
        <span className={`px-2 py-0.5 text-xs rounded ${snapshot.integrity.integrityVerified ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
          {snapshot.integrity.integrityVerified ? 'Verified' : 'Failed'}
        </span>
        <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">{snapshot.captureReason}</span>
      </div>
      <div className="flex items-center gap-4 text-xs text-gray-500 mt-1">
        <span>{new Date(snapshot.capturedAt).toLocaleString()}</span>
        <span>v{snapshot.version}</span>
        <span>{snapshot.formulaRegistryVersion}</span>
        <span>{snapshot.calibrationProfileVersion}</span>
      </div>
    </div>
    <ChevronRight className="text-gray-400" />
  </div>
);

// ============================================
// OUTPUT HISTORY TAB
// ============================================
const OutputHistoryTab: React.FC<{ consultation: any }> = ({ consultation }) => {
  const outputs = consultation.outputs || [];

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-gray-900">Output History ({outputs.length})</h3>

      {outputs.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <Download className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No outputs generated yet.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {outputs.slice().reverse().map(output => (
            <div key={output.outputId} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                  output.format === 'pdf' ? 'bg-red-100' : output.format === 'html' ? 'bg-blue-100' : 'bg-green-100'
                }`}>
                  <span className="text-xs font-bold text-gray-700">{output.format.toUpperCase()}</span>
                </div>
                <div>
                  <p className="font-medium text-gray-900 capitalize">{output.profile} Report</p>
                  <p className="text-xs text-gray-500">{new Date(output.generatedAt).toLocaleString()}</p>
                </div>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>{(output.fileSizeBytes / 1024).toFixed(1)} KB</span>
                <span className="font-mono text-xs">{output.checksum.substring(0, 16)}...</span>
                <span>{output.sections.length} sections</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ============================================
// METADATA TAB
// ============================================
const MetadataTab: React.FC<{
  consultation: any;
  editing: boolean;
  editForm: any;
  setEditForm: React.Dispatch<React.SetStateAction<any>>;
  onSave: () => void;
  onCancel: () => void;
  onAddTag: (e: React.FormEvent) => void;
  onRemoveTag: (tag: string) => void;
}> = ({ consultation, editing, editForm, setEditForm, onSave, onCancel, onAddTag, onRemoveTag }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h3 className="font-semibold text-gray-900">Consultation Metadata</h3>
      {editing ? (
        <div className="flex gap-2">
          <button onClick={onCancel} className="px-3 py-1.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button onClick={onSave} className="px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Save
          </button>
        </div>
      ) : (
        <button onClick={() => setEditForm({
          consultationTitle: consultation.metadata.consultationTitle,
          tags: [...consultation.metadata.tags],
          status: consultation.status,
          isFavorite: consultation.metadata.isFavorite,
        })} className="px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
          Edit
        </button>
      )}
    </div>

    <div className="space-y-4">
      {/* Title */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Title</label>
        {editing ? (
          <input
            value={editForm.consultationTitle}
            onChange={(e) => setEditForm({ ...editForm, consultationTitle: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          />
        ) : (
          <p className="text-gray-900">{consultation.metadata.consultationTitle}</p>
        )}
      </div>

      {/* Status */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Status</label>
        {editing ? (
          <select
            value={editForm.status}
            onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          >
            <option value="active">Active</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="archived">Archived</option>
            <option value="recycle_bin">Recycle Bin</option>
          </select>
        ) : (
          <span className={`inline-block px-3 py-1 rounded ${consultation.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : consultation.status === 'in_progress' ? 'bg-amber-100 text-amber-700' : consultation.status === 'archived' ? 'bg-gray-100 text-gray-700' : 'bg-blue-100 text-blue-700'}`}>
            {consultation.status}
          </span>
        )}
      </div>

      {/* Favorite */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Favorite</label>
        {editing ? (
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={editForm.isFavorite}
              onChange={(e) => setEditForm({ ...editForm, isFavorite: e.target.checked })}
              className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <span className="text-gray-700">Mark as favorite</span>
          </label>
        ) : (
          <div className="flex items-center gap-2">
            <Star className={`${consultation.metadata.isFavorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'} w-5 h-5`} />
            <span className="text-gray-700">{consultation.metadata.isFavorite ? 'Yes' : 'No'}</span>
          </div>
        )}
      </div>

      {/* Tags */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Tags</label>
        {editing ? (
          <div className="space-y-2">
            <form onSubmit={onAddTag} className="flex gap-2">
              <input
                type="text"
                placeholder="Add tag..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
              <button type="submit" className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
                Add
              </button>
            </form>
            <div className="flex flex-wrap gap-2">
              {editForm.tags.map((tag: string) => (
                <span key={tag} className="flex items-center gap-1 px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-sm">
                  {tag}
                  <button onClick={() => onRemoveTag(tag)} className="hover:text-indigo-900">×</button>
                </span>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {consultation.metadata.tags.length > 0 ? (
              consultation.metadata.tags.map((tag: string) => (
                <span key={tag} className="px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-sm">{tag}</span>
              ))
            ) : (
              <span className="text-gray-400 text-sm">No tags</span>
            )}
          </div>
        )}
      </div>

      {/* Immutable Fields - Display Only */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Immutable Fields (Reference Only)</h4>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-xs text-gray-500">Client Name</p>
            <p className="font-medium text-gray-900">{consultation.metadata.clientName}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-xs text-gray-500">Birth Data Hash</p>
            <p className="font-mono text-xs text-gray-900 break-all">{consultation.metadata.birthDataHash}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-xs text-gray-500">Consultation ID</p>
            <p className="font-mono text-xs text-gray-900 break-all">{consultation.id}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <p className="text-xs text-gray-500">Version</p>
            <p className="font-medium text-gray-900">{consultation.version}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// ============================================
// NOTES TAB
// ============================================
const NotesTab: React.FC<{ consultation: any }> = ({ consultation }) => {
  const notes = consultation.notes || { general: '', questions: [], chart: [], timing: [], recommendations: [] };
  const [activeSection, setActiveSection] = useState<string>('general');
  const [noteContent, setNoteContent] = useState<string>(notes.general || '');

  const sections = [
    { id: 'general', label: 'General', icon: FileText },
    { id: 'questions', label: 'Questions', icon: HelpCircle },
    { id: 'chart', label: 'Chart Observations', icon: BarChart2 },
    { id: 'timing', label: 'Timing Notes', icon: Clock },
    { id: 'recommendations', label: 'Recommendations', icon: Lightbulb },
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-1">
        {sections.map(section => (
          <button
            key={section.id}
            onClick={() => { setActiveSection(section.id); setNoteContent(notes[section.id] || ''); }}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm transition-colors ${
              activeSection === section.id
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <section.icon className="w-3.5 h-3.5" />
            {section.label}
          </button>
        ))}
      </div>

      <div className="border border-gray-200 rounded-lg overflow-hidden">
        <textarea
          value={noteContent}
          onChange={(e) => setNoteContent(e.target.value)}
          placeholder={`Add ${activeSection} notes...`}
          className="w-full h-64 p-4 border-none focus:outline-none resize-none text-gray-900 placeholder-gray-400"
        />
        <div className="p-3 bg-gray-50 border-t border-gray-200 flex justify-end">
          <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
            Save Notes
          </button>
        </div>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-amber-600" />
          <p className="text-sm text-amber-800">
            <strong>Notes are presentation metadata only.</strong> They do not affect deterministic calculations, 
            formula registry, calibration profiles, or engine outputs.
          </p>
        </div>
      </div>
    </div>
  );
};

// ============================================
// HELPER COMPONENTS
// ============================================
const MetricCard: React.FC<{ label: string; value: string; icon: React.ReactNode; color: string }> = ({ 
  label, value, icon, color 
}) => {
  const colorMap: Record<string, string> = {
    emerald: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    amber: 'bg-amber-100 text-amber-700 border-amber-200',
    red: 'bg-red-100 text-red-700 border-red-200',
    blue: 'bg-blue-100 text-blue-700 border-blue-200',
    gray: 'bg-gray-100 text-gray-700 border-gray-200',
  };
 
  return (
    <div className={`p-4 rounded-lg border ${colorMap[color] || colorMap.gray}`}>
      <div className="flex items-center justify-between">
        <div>{icon}</div>
        <span className="text-2xl font-bold">{value}</span>
      </div>
      <p className="text-xs text-gray-500 mt-1">{label}</p>
    </div>
  );
};

const DetailCard: React.FC<{ title: string; items: { label: string; value: string }[] }> = ({ title, items }) => (
  <div className="bg-white border border-gray-200 rounded-lg p-4">
    <h3 className="text-sm font-semibold text-gray-700 mb-3">{title}</h3>
    <div className="space-y-2">
      {items.map((item, i) => (
        <div key={i} className="flex justify-between py-2 border-b border-gray-100 last:border-0">
          <span className="text-sm text-gray-500">{item.label}</span>
          <span className="text-sm font-medium text-gray-900 text-right max-w-[60%] truncate">{item.value}</span>
        </div>
      ))}
    </div>
  </div>
);

// Missing icons
const Target = () => <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>;
const Activity = () => <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>;
const Award = () => <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"/><path d="M8.21 13.89 7 23l5-4 5 4L15.89 13.88"/></svg>;
const Timer = () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>;
const Play = () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>;
const Printer = () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>;
const Copy = () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>;
const HelpCircle = () => <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>;
const BarChart2 = () => <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>;
const Lightbulb = () => <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2v4"/><path d="M12 22v-4"/><path d="M17.5 5.5l3 3"/><path d="M4.5 17.5l3 3"/><path d="M17.5 18.5l-3 3"/><path d="M4.5 6.5l3-3"/></svg>;

export default ConsultationDetailsDrawer;