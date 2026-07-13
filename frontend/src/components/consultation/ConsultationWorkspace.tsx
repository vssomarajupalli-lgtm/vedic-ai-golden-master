import React, { useState, useEffect, useRef } from 'react';
import { Consultation, ConsultationStructure, Chapter, ChapterQuestion, QuestionPackage, ConsultationNotes } from '../../types/consultation';
import { QuestionPackage, PackageManager } from '../../types/packages';
import { ConsultationNotes, NoteManager } from '../../types/consultation-notes';
import { ModeConfiguration, getModeConfig } from '../../types/report-modes';
import { PrintProfile, PRINT_PROFILES } from '../../types/print-profiles';
import { QuestionItem, QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';

interface ConsultationWorkspaceProps {
  consultation: Consultation;
  onConsultationChange: (consultation: Consultation) => void;
  packages: QuestionPackage[];
  notes: ConsultationNotes;
  mode: 'standard' | 'professional' | 'expert' | 'study';
  onModeChange: (mode: 'standard' | 'professional' | 'expert' | 'study') => void;
  onGenerateReport: () => void;
  onPreview: () => void;
  onPrint: (profile: string) => void;
  onSave: () => void;
  onExportPDF: (profile: string) => void;
}

export const ConsultationWorkspace: React.FC<ConsultationWorkspaceProps> = ({
  consultation,
  onConsultationChange,
  packages,
  notes,
  mode,
  onModeChange,
  onGenerateReport,
  onPreview,
  onPrint,
  onSave,
  onExportPDF,
}) => {
  const [selectedQuestions, setSelectedQuestions] = useState<Set<string>>(new Set(consultation.structure.chapters.flatMap(c => c.questions.map(q => q.questionId))));
  const [activeTab, setActiveTab] = useState<'selection' | 'structure' | 'notes' | 'preview'>('selection');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDomain, setFilterDomain] = useState<string | null>(null);
  const [showFavorites, setShowFavorites] = useState(false);
  const [showPackages, setShowPackages] = useState(true);
  const [customPackageName, setCustomPackageName] = useState('');
  
  const modeConfig = getModeConfig(consultation.metadata.mode || 'standard');
  
  // Auto-save effect
  useEffect(() => {
    const timer = setTimeout(() => {
      onSave();
    }, 2000);
    return () => clearTimeout(timer);
  }, [consultation]);

  // Update consultation when selection changes
  useEffect(() => {
    const updatedConsultation = {
      ...consultation,
      structure: {
        ...consultation.structure,
        chapters: consultation.structure.chapters.map(chapter => ({
          ...chapter,
          questions: chapter.questions.map(q => ({
            ...q,
            included: selectedQuestions.has(q.questionId)
          }))
        }))
      },
      metadata: {
        ...consultation.metadata,
        updatedAt: new Date(),
      }
    };
    onConsultationChange(updatedConsultation);
  }, [selectedQuestions]);

  const handleQuestionToggle = (questionId: string) => {
    const next = new Set(selectedQuestions);
    if (next.has(questionId)) {
      next.delete(questionId);
    } else {
      next.add(questionId);
    }
    setSelectedQuestions(next);
  };

  const handlePackageSelect = (packageId: string, replace = false) => {
    const pkg = packages.find(p => p.id === packageId);
    if (!pkg) return;
    
    const next = replace ? new Set() : new Set(selectedQuestions);
    pkg.questionIds.forEach(id => next.add(id));
    setSelectedQuestions(next);
  };

  const handleCustomPackageCreate = (data: { name: string; description: string; category: 'custom'; tags: string[]; questionIds: string[] }) => {
    // This would call the PackageManager to create a custom package
    console.log('Creating custom package:', data);
  };

  const handleQuestionSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleDomainFilter = (domainId: string | null) => {
    setFilterDomain(domainId);
  };

  const toggleFavorites = () => {
    setShowFavorites(!showFavorites);
  };

  const selectAllVisible = () => {
    // Select all questions matching current filter
    const visibleQuestions = getVisibleQuestions();
    visibleQuestions.forEach(q => selectedQuestions.add(q.id));
    setSelectedQuestions(new Set(selectedQuestions));
  };

  const clearSelection = () => {
    setSelectedQuestions(new Set());
  };

  const getVisibleQuestions = () => {
    let questions: Array<{ id: string; label: string; domainId: string; domainLabel: string }> = [];
    QUESTIONNAIRE_SCHEMA.forEach(domain => {
      if (filterDomain && domain.domainId !== filterDomain) return;
      domain.questions.forEach(q => {
        if (searchQuery && !q.label.toLowerCase().includes(searchQuery.toLowerCase())) return;
        questions.push({
          id: q.id,
          label: q.label,
          domainId: domain.domainId,
          domainLabel: domain.domainLabel
        });
      });
    });
    return questions;
  };

  const visibleQuestions = getVisibleQuestions();
  const selectedCount = selectedQuestions.size;

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-800">{consultation.title}</h1>
          <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">{consultation.metadata.mode || 'standard'}</span>
        </div>
        <div className="flex items-center space-x-2">
          <select
            value={consultation.metadata.mode || 'standard'}
            onChange={(e) => onConsultationChange({ ...consultation, metadata: { ...consultation.metadata, mode: e.target.value as any } })}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="standard">Standard</option>
            <option value="professional">Professional</option>
            <option value="expert">Expert</option>
            <option value="study">Study</option>
          </select>
          <button onClick={onSave} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Save
          </button>
          <button onClick={onPreview} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">
            Preview
          </button>
          <button onClick={onGenerateReport} className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            Generate Report
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Rail */}
        <div className="w-64 border-r border-gray-200 bg-white flex flex-col">
          <nav className="flex-1 p-4 space-y-2">
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'selection' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('selection')}
            >
              Question Selection
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'structure' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('structure')}
            >
              Report Structure
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'notes' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('notes')}
            >
              Notes & Bookmarks
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'preview' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={onPreview}
            >
              Preview Report
            </button>
          </nav>
          <div className="p-4 border-t border-gray-200">
            <div className="text-sm text-gray-500">
              {selectedCount} questions selected
            </div>
          </div>
        </div>

        {/* Main Panel */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Tab Content */}
          <div className="flex-1 overflow-auto p-4">
            {activeTab === 'selection' && (
              <QuestionSelectionPanel
                selectedQuestions={selectedQuestions}
                onQuestionToggle={handleQuestionToggle}
                onPackageSelect={handlePackageSelect}
                onCustomPackageCreate={handleCustomPackageCreate}
                onSearch={handleQuestionSearch}
                onDomainFilter={handleDomainFilter}
                onSelectAll={selectAllVisible}
                onClear={clearSelection}
                onFavoritesToggle={toggleFavorites}
                showFavorites={showFavorites}
                showPackages={showPackages}
                packages={packages}
                selectedQuestions={selectedQuestions}
                searchQuery={searchQuery}
                filterDomain={filterDomain}
                showFavorites={showFavorites}
                packages={packages}
              />
            )}

            {activeTab === 'structure' && (
              <ReportStructurePanel
                consultation={consultation}
                onConsultationChange={onConsultationChange}
                modeConfig={getModeConfig(consultation.metadata.mode || 'standard')}
              />
            )}

            {activeTab === 'notes' && (
              <NotesPanel
                notes={notes}
                onNotesChange={(updatedNotes) => onConsultationChange({ ...consultation, notes: updatedNotes })}
              />
            )}

            {activeTab === 'preview' && (
              <ReportPreview
                consultation={consultation}
                mode={consultation.metadata.mode || 'standard'}
              />
            )}
          </div>

          {/* Footer Actions */}
          <div className="p-4 border-t border-gray-200 bg-white flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {selectedCount} questions selected · Est. {Math.ceil(selectedCount * 1.2)} pages
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <select
                value="professional-consultation"
                onChange={(e) => onPrint(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm"
              >
                <option value="quick-consultation">Quick Consultation</option>
                <option value="professional-consultation">Professional Consultation</option>
                <option value="research-report">Research Report</option>
                <option value="comparison-report">Comparison Report</option>
                <option value="book-format">Book Format</option>
              </select>
              <button onClick={() => onPrint('professional-consultation')} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">
                Print
              </button>
              <button onClick={() => onExportPDF('professional-consultation')} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                Export PDF
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsultationWorkspace;