import React, { useState, useCallback, useEffect } from 'react';
import { useChartStore } from '../store/useChartStore';
import { apiService } from '../api/backend';
import { useConsultationRepository } from '../hooks/useConsultationRepository';

interface ConsultationData {
  id: string;
  metadata: {
    clientName: string;
    birthDataHash: string;
    consultationTitle: string;
  };
  structure: {
    questionPackageId: string;
    selectedQuestionIds: string[];
  };
  snapshots: any[];
}

interface PrintFrameworkProps {
  isOpen: boolean;
  onClose: () => void;
  consultation?: ConsultationData | null;
}

const PROFILE_LABELS: Record<string, string> = {
  quick: 'Quick Consultation',
  standard: 'Standard Consultation',
  professional: 'Professional Consultation',
  research: 'Research Report',
  book: 'Book Format',
};

const PROFILE_DESCRIPTIONS: Record<string, string> = {
  quick: '1-3 pages, core insights only',
  standard: 'Complete with charts, questions, evidence',
  professional: 'Client-ready with headers, footers, TOC',
  research: 'Everything including formula evidence',
  book: 'Book layout with large margins',
};

const PROFILE_ICONS: Record<string, React.ReactNode> = {
  quick: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>,
  standard: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>,
  professional: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>,
  research: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>,
  book: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>,
};

export const PrintFramework: React.FC<PrintFrameworkProps> = ({ isOpen, onClose, consultation }) => {
  const { 
    canonicalContent, 
    machineIndex: machineIndexRaw, 
    report,
    questionResults,
  } = useChartStore();
  
  const { recordOutput } = useConsultationRepository();
  
  const [selectedProfile] = useState<'quick' | 'standard' | 'professional' | 'research' | 'book'>('professional');
  const [selectedFormat, setSelectedFormat] = useState<'pdf' | 'html' | 'json'>('pdf');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<Partial<any>>({});
  const [sections, setSections] = useState<any[]>([]);
  const [selectedSections, setSelectedSections] = useState<string[]>([]);

  // Build report sections from available data
  useEffect(() => {
    const availableSections: any[] = [];
    
    // Determine the source data - either from consultation snapshot or current chart store
    const sourceReport = consultation?.snapshots?.[0]?.report || report;
    const sourceQuestionResults = consultation?.snapshots?.[0]?.questions || questionResults;

    // Cover page - always included
    availableSections.push({
      id: 'cover',
      title: 'Cover Page',
      component: 'cover',
      pageBreakAfter: true,
      priority: 0,
    });

    // Table of Contents - always included
    availableSections.push({
      id: 'toc',
      title: 'Table of Contents',
      component: 'toc',
      pageBreakAfter: true,
      priority: 1,
    });

    // Horoscope Summary - if report has lifetime_intelligence
    if (sourceReport?.lifetime_intelligence) {
      availableSections.push({
        id: 'horoscope-summary',
        title: 'Horoscope Summary',
        component: 'horoscope-summary',
        priority: 2,
      });
    }

    // Question Analysis - if question results exist
    if (sourceQuestionResults?.length) {
      availableSections.push({
        id: 'questions',
        title: 'Question Analysis',
        component: 'questions',
        priority: 3,
      });
    }

    // Activation Timeline - if timeline exists
    if (sourceReport?.lifetime_intelligence?.timeline?.length) {
      availableSections.push({
        id: 'activation-timeline',
        title: 'Activation Timeline',
        component: 'activation-timeline',
        priority: 4,
      });
    }

    // Deterministic Gochara - if transit data exists
    if (sourceReport?.formula_verification?.engine_outputs?.transit) {
      availableSections.push({
        id: 'gochara',
        title: 'Deterministic Gochara',
        component: 'gochara',
        priority: 5,
      });
    }

    // Consultation Notes - placeholder
    availableSections.push({
      id: 'notes',
      title: 'Consultation Notes',
      component: 'notes',
      priority: 98,
    });

    // Appendix - always included
    availableSections.push({
      id: 'appendix',
      title: 'Appendix',
      component: 'appendix',
      priority: 99,
    });

    const sortedSections = availableSections.sort((a, b) => a.priority - b.priority);
    setSections(sortedSections);
    // Default all sections selected
    setSelectedSections(sortedSections.map(s => s.id));
  }, [consultation, report, questionResults, canonicalContent]);

  // Build metadata from chart data or consultation
  useEffect(() => {
    let native: any = {};
    
    if (consultation?.metadata) {
      native = {
        name: consultation.metadata.clientName,
        dob: 'Unknown',
        tob: 'Unknown',
        pob: 'Unknown',
        latitude: 0,
        longitude: 0,
        timezone: 'UTC',
      };
    } else if (canonicalContent && machineIndexRaw) {
      const machineIndex = Array.isArray(machineIndexRaw) ? machineIndexRaw : [machineIndexRaw];
      native = machineIndex.find((m: any) => m?.native_info)?.native_info || {};
    }

    setMetadata({
      clientName: native.name || 'Unknown',
      dob: native.dob || 'Unknown',
      tob: native.tob || 'Unknown',
      pob: native.pob || 'Unknown',
      latitude: native.latitude || 0,
      longitude: native.longitude || 0,
      timezone: native.timezone || 'UTC',
      generatedAt: new Date().toISOString(),
      softwareVersion: 'Golden Master v1.2',
      reportMode: selectedProfile,
      questionCount: questionResults?.length || consultation?.structure?.selectedQuestionIds?.length || 0,
    });
  }, [consultation, canonicalContent, machineIndexRaw, questionResults, selectedProfile]);

  // Handle print generation
  const handleGenerate = useCallback(async (format: 'pdf' | 'html' | 'json') => {
    setIsGenerating(true);
    setError(null);
  
    try {
      if (format === 'json') {
        const dataStr = JSON.stringify({ 
          metadata, 
          sections: sections.filter(s => selectedSections.includes(s.id)),
          consultationId: consultation?.id,
          repositoryVersion: 1,
          goldenMasterVersion: 'v1.2.0',
          architectureVersion: '1.2.0',
          formulaRegistryVersion: '1.0.0',
          calibrationProfileVersion: 'v1.0.0',
          gitCommit: 'unknown',
          gitTag: 'gm-007-development',
          deterministic: true,
        }, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        downloadBlob(blob, `report_${consultation?.metadata?.consultationTitle || 'consultation'}.json`);
       
        // Record output history
        if (consultation) {
          await recordOutput(consultation.id, {
            profile: selectedProfile,
            format: 'json',
            generatedAt: new Date().toISOString(),
            checksum: 'json-' + Date.now(),
            sections: selectedSections,
            fileSizeBytes: dataStr.length,
            repositoryVersion: 1,
            gitCommit: 'unknown',
            gitTag: 'gm-007-development',
          });
        }
        return;
      }
      setIsGenerating(true);
    
      const formatParam = format === 'pdf' ? 'pdf' : 'html';
      
      // Use the canonical content from chart store for backend generation
      const blob = await apiService.getReportBlob(
        canonicalContent!,
        machineIndexRaw!,
        formatParam
      );
      const filename = `vedic_ai_report_${new Date().toISOString().split('T')[0]}.${format === 'pdf' ? 'pdf' : 'html'}`;
      downloadBlob(blob, filename);
     
      // Record output history
      if (consultation) {
        await recordOutput(consultation.id, {
          profile: selectedProfile,
          format: format,
          generatedAt: new Date().toISOString(),
          checksum: 'blob-' + Date.now(),
          sections: selectedSections,
          fileSizeBytes: blob.size,
          repositoryVersion: 1,
          gitCommit: 'unknown',
          gitTag: 'gm-007-development',
        });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to generate report');
    } finally {
      setIsGenerating(false);
    }
  }, [canonicalContent, machineIndexRaw, metadata, sections, selectedSections, consultation, selectedProfile, recordOutput]);

  const handlePrint = useCallback(() => {
    window.print();
  }, []);

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4" onClick={onClose}>
        <div 
          className="bg-white rounded-xl shadow-2xl max-w-5xl w-full max-h-[90vh] flex flex-col overflow-hidden"
          onClick={e => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <h2 className="text-xl font-bold text-gray-900">Print & Export Framework</h2>
              <span className="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded-full">
                Golden Master Output Framework
              </span>
            </div>
            <button 
              onClick={onClose} 
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
              aria-label="Close"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-auto p-6">
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                <strong>Error:</strong> {error}
                <button onClick={() => setError(null)} className="ml-2 text-red-500 hover:underline">Dismiss</button>
              </div>
            )}

            {/* Profile Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">Output Profile</label>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                {[
                  {id: 'quick', label: 'Quick Consultation'},
                  {id: 'standard', label: 'Standard Consultation'},
                  {id: 'professional', label: 'Professional Consultation'},
                  {id: 'research', label: 'Research Report'},
                  {id: 'book', label: 'Book Format'},
                ].map(profile => (
                  <button
                    key={profile.id}
                    onClick={() => {}} // Profile selection handled via state
                    className={`relative p-4 rounded-xl border-2 transition-all ${
                      selectedProfile === profile.id
                        ? 'border-indigo-500 bg-indigo-50 shadow-lg'
                        : 'border-gray-200 hover:border-indigo-300 bg-white'
                    }`}
                  >
                    <div className="absolute -top-2 -right-2">
                      {selectedProfile === profile.id && (
                        <div className="w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7"/></svg>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center justify-center gap-2 mb-2">
                      {PROFILE_ICONS[profile.id]}
                    </div>
                    <h4 className="font-medium text-gray-900 text-center">{PROFILE_LABELS[profile.id]}</h4>
                    <p className="text-xs text-gray-500 text-center mt-1">{PROFILE_DESCRIPTIONS[profile.id]}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Format Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">Output Format</label>
              <div className="flex gap-4">
                {[
                  { value: 'pdf', label: 'PDF', desc: 'Best for printing & sharing' },
                  { value: 'html', label: 'HTML', desc: 'For offline viewing' },
                  { value: 'json', label: 'JSON', desc: 'Raw data for developers' },
                ].map(opt => (
                  <button
                    key={opt.value}
                    onClick={() => setSelectedFormat(opt.value as 'pdf' | 'html' | 'json')}
                    className={`flex-1 flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                      selectedFormat === opt.value
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-indigo-300 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                      <span className="font-medium text-gray-900">{opt.label}</span>
                    </div>
                    <p className="text-xs text-gray-500 text-center">{opt.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Sections to Include */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">Sections to Include</label>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {sections.map(section => (
                  <label key={section.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
                    <input 
                      type="checkbox" 
                      checked={selectedSections.includes(section.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedSections([...selectedSections, section.id]);
                        } else {
                          setSelectedSections(selectedSections.filter(id => id !== section.id));
                        }
                      }}
                      className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{section.title}</p>
                      <p className="text-xs text-gray-500">{section.id}</p>
                    </div>
                    {section.pageBreakAfter && <span className="px-2 py-0.5 bg-green-100 text-green-800 text-xs rounded">Page Break After</span>}
                    {section.pageBreakBefore && <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">Page Break Before</span>}
                    {section.landscape && <span className="px-2 py-0.5 bg-amber-100 text-amber-800 text-xs rounded">Landscape</span>}
                  </label>
                ))}
              </div>
            </div>

            {/* Advanced Options */}
            <div className="mb-6">
              <h4 className="text-sm font-medium text-gray-700 mb-3">Advanced Options</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { label: 'Include TOC', checked: true },
                  { label: 'Page Numbers', checked: true },
                  { label: 'Headers/Footers', checked: true },
                  { label: 'Bookmarks', checked: true },
                  { label: 'Formula Transparency', checked: false },
                  { label: 'Calibration Transparency', checked: false },
                  { label: 'High Quality PDF', checked: true },
                  { label: 'Embed Fonts', checked: true },
                ].map((opt, i) => (
                  <label key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded-lg cursor-pointer">
                    <input type="checkbox" checked={opt.checked} className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500" />
                    <span className="text-sm text-gray-700">{opt.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-200">
              <button
                onClick={() => {}} // Preview not yet implemented
                disabled={isGenerating}
                className="flex-1 min-w-[160px] py-3 px-6 bg-gray-100 border border-gray-300 text-gray-700 rounded-xl font-medium hover:bg-gray-200 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                Preview
              </button>
              <button
                onClick={() => handleGenerate('html')}
                disabled={isGenerating}
                className="flex-1 min-w-[160px] py-3 px-6 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                {isGenerating ? 'Generating...' : 'Download HTML'}
              </button>
              <button
                onClick={() => handleGenerate('pdf')}
                disabled={isGenerating}
                className="flex-1 min-w-[160px] py-3 px-6 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2H7z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 12v4m0 0l-3-3m3 3l3-3"/></svg>
                {isGenerating ? 'Generating...' : 'Download PDF'}
              </button>
              <button
                onClick={handlePrint}
                disabled={isGenerating}
                className="flex-1 min-w-[160px] py-3 px-6 bg-green-600 text-white rounded-xl font-medium hover:bg-green-700 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2h2"/></svg>
                {isGenerating ? 'Printing...' : 'Print Direct'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export default PrintFramework;