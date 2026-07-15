import React, { useState, useCallback, useMemo, useEffect } from 'react';
import { useChartStore } from '../store/useChartStore';
import { apiService } from '../api/backend';

interface PrintFrameworkProps {
  isOpen: boolean;
  onClose: () => void;
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

export const PrintFramework: React.FC<PrintFrameworkProps> = ({ isOpen, onClose }) => {
  const { 
    canonicalContent, 
    machineIndex: machineIndexRaw, 
    report,
    questionResults,
  } = useChartStore();
  
  const [selectedProfile] = useState<'quick' | 'standard' | 'professional' | 'research' | 'book'>('professional');
  const [selectedFormat, setSelectedFormat] = useState<'pdf' | 'html' | 'json'>('pdf');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<Partial<any>>({});

  // Build report sections from available data
  const availableSections = useMemo(() => {
    const sections: Array<{id: string; title: string; component: React.ReactNode; landscape?: boolean; pageBreakBefore?: boolean; pageBreakAfter?: boolean; priority: number}> = [];

    sections.push({
      id: 'cover',
      title: 'Cover Page',
      component: <CoverPage metadata={metadata} />,
      pageBreakAfter: true,
      priority: 0,
    });

    sections.push({
      id: 'toc',
      title: 'Table of Contents',
      component: <TableOfContents />,
      pageBreakAfter: true,
      priority: 1,
    });

    if (report?.lifetime_intelligence) {
      sections.push({
        id: 'horoscope-summary',
        title: 'Horoscope Summary',
        component: <HoroscopeSummary report={report} />,
        priority: 2,
      });
    }

    if (questionResults?.length) {
      sections.push({
        id: 'questions',
        title: 'Question Analysis',
        component: <QuestionResultsSection results={questionResults} />,
        priority: 3,
      });
    }

    if (report?.lifetime_intelligence?.timeline?.length) {
      sections.push({
        id: 'activation-timeline',
        title: 'Activation Timeline',
        component: <ActivationTimelineSection timeline={report.lifetime_intelligence.timeline} />,
        priority: 4,
      });
    }

    if (report?.formula_verification?.engine_outputs?.transit) {
      sections.push({
        id: 'gochara',
        title: 'Deterministic Gochara',
        component: <GocharaSection transit={report.formula_verification.engine_outputs.transit} />,
        priority: 5,
      });
    }

    sections.push({
      id: 'notes',
      title: 'Consultation Notes',
      component: <NotesSection />,
      priority: 98,
    });

    sections.push({
      id: 'appendix',
      title: 'Appendix',
      component: <AppendixSection report={report} />,
      priority: 99,
    });

    return sections.sort((a, b) => a.priority - b.priority);
  }, [report, questionResults]);

  // Build metadata from chart data
  useEffect(() => {
    if (canonicalContent && machineIndexRaw) {
      // machineIndex can be array or object - normalize to array
      const machineIndex = Array.isArray(machineIndexRaw) ? machineIndexRaw : [machineIndexRaw];
      const native = machineIndex.find((m: any) => m?.native_info)?.native_info || {};
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
        reportMode: 'professional',
        questionCount: questionResults?.length || 0,
      });
    }
  }, [canonicalContent, machineIndexRaw, questionResults]);

  // Handle print generation
  // Handle print generation
  const handleGenerate = useCallback(async (format: 'pdf' | 'html' | 'json') => {
    setIsGenerating(true);
    setError(null);
   
    try {
      if (format === 'json') {
        const dataStr = JSON.stringify({ metadata, sections: availableSections }, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        downloadBlob(blob, 'report.json');
        return;
      }
      setIsGenerating(true);
     
      const formatParam = format === 'pdf' ? 'pdf' : 'html';
       const blob = await apiService.getReportBlob(
         canonicalContent!,
         machineIndexRaw!,
         formatParam
       );
       const filename = `vedic_ai_report_${new Date().toISOString().split('T')[0]}.${format === 'pdf' ? 'pdf' : 'html'}`;
       downloadBlob(blob, filename);
    } catch (err: any) {
      setError(err.message || 'Failed to generate report');
    } finally {
      setIsGenerating(false);
    }
  }, [canonicalContent, machineIndexRaw]);

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
                    onClick={() => {}}
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
                {[
                  {id: 'cover', title: 'Cover Page', landscape: false, pageBreakBefore: false, pageBreakAfter: true},
                  {id: 'toc', title: 'Table of Contents', landscape: false, pageBreakBefore: false, pageBreakAfter: true},
                  {id: 'horoscope-summary', title: 'Horoscope Summary', landscape: false, pageBreakBefore: false, pageBreakAfter: false},
                  {id: 'questions', title: 'Question Analysis', landscape: false, pageBreakBefore: false, pageBreakAfter: false},
                  {id: 'activation-timeline', title: 'Activation Timeline', landscape: true, pageBreakBefore: true, pageBreakAfter: true},
                  {id: 'gochara', title: 'Deterministic Gochara', landscape: false, pageBreakBefore: false, pageBreakAfter: false},
                  {id: 'notes', title: 'Consultation Notes', landscape: false, pageBreakBefore: false, pageBreakAfter: false},
                  {id: 'appendix', title: 'Appendix', landscape: false, pageBreakBefore: true, pageBreakAfter: false},
                ].map(section => (
                  <label key={section.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
                    <input 
                      type="checkbox" 
                      checked={true} 
                      className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{section.title}</p>
                      <p className="text-xs text-gray-500">{section.id}</p>
                    </div>
                    {section.landscape && <span className="px-2 py-0.5 bg-amber-100 text-amber-800 text-xs rounded">Landscape</span>}
                    {section.pageBreakBefore && <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">Page Break Before</span>}
                    {section.pageBreakAfter && <span className="px-2 py-0.5 bg-green-100 text-green-800 text-xs rounded">Page Break After</span>}
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
                onClick={() => {}}
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

// Section Components
const CoverPage = ({ metadata }: { metadata: any }) => (
  <div className="p-20 text-center">
    <h1 className="text-4xl font-bold text-indigo-900 mb-4">Vedic-AI Intelligence Report</h1>
    <p className="text-xl text-gray-600 mb-8">Professional Consultation</p>
    <div className="text-left max-w-md mx-auto space-y-2 text-gray-700">
      <p><strong>Client:</strong> {metadata.clientName}</p>
      <p><strong>DOB:</strong> {metadata.dob} | TOB: {metadata.tob}</p>
      <p><strong>POB:</strong> {metadata.pob}</p>
      <p><strong>Generated:</strong> {new Date(metadata.generatedAt).toLocaleDateString()}</p>
      <p><strong>Software:</strong> {metadata.softwareVersion}</p>
    </div>
  </div>
);

const TableOfContents = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Table of Contents</h2>
    <ul className="space-y-2">
      {['Cover Page', 'Table of Contents', 'Horoscope Summary', 'Question Analysis', 'Activation Timeline', 'Gochara', 'Consultation Notes', 'Appendix'].map((title, i) => (
        <li key={title} className="flex items-center justify-between py-2 border-b border-gray-100">
          <span className="font-medium">{i + 1}. {title}</span>
          <span className="text-gray-400">Page {i + 2}</span>
        </li>
      ))}
    </ul>
  </div>
);

const HoroscopeSummary = ({ report }: { report: any }) => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Horoscope Summary</h2>
    {report.lifetime_intelligence?.snapshot && (
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {Object.entries(report.lifetime_intelligence.snapshot).map(([key, value]) => (
          <div key={key} className="p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-500 uppercase tracking-wider">{key}</p>
            <p className="font-bold text-lg">{String(value)}</p>
          </div>
        ))}
      </div>
    )}
  </div>
);

const QuestionResultsSection = ({ results }: { results: any[] }) => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Question Analysis</h2>
    <div className="space-y-4">
      {results.map((qr, i) => (
        <div key={i} className="p-4 bg-white border border-gray-200 rounded-lg">
          <h3 className="font-bold text-gray-900 mb-2">{qr.question_title || `Question ${i + 1}`}</h3>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div><span className="text-gray-500">Natal Promise:</span> <span className="font-bold">{qr.natal_promise?.score || '—'}</span></div>
            <div><span className="text-gray-500">Transit:</span> <span className="font-bold">{qr.transit?.activation_score || '—'}</span></div>
            <div><span className="text-gray-500">Final:</span> <span className="font-bold text-indigo-600">{qr.probability?.score || '—'}</span></div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const ActivationTimelineSection = ({ timeline }: { timeline: any[] }) => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Activation Timeline</h2>
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-50">
            <th className="px-4 py-2 text-left">Age</th>
            <th className="px-4 py-2 text-left">Period</th>
            <th className="px-4 py-2 text-left">MD-AD-PD</th>
            <th className="px-4 py-2 text-left">Activation</th>
            <th className="px-4 py-2 text-left">Probability</th>
            <th className="px-4 py-2 text-left">Grade</th>
          </tr>
        </thead>
        <tbody>
          {timeline.slice(0, 20).map((row, i) => (
            <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              <td className="px-4 py-2">{row.age}</td>
              <td className="px-4 py-2">{row.start_date} - {row.end_date}</td>
              <td className="px-4 py-2 font-mono">{row.md}-{row.ad}-{row.pd}</td>
              <td className="px-4 py-2"><span className="px-2 py-0.5 bg-indigo-100 text-indigo-800 rounded text-xs">{row.activation_pct}%</span></td>
              <td className="px-4 py-2"><span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded text-xs">{row.final_probability_pct}%</span></td>
              <td className="px-4 py-2">{row.grade}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const GocharaSection = ({ transit }: { transit: any }) => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Deterministic Gochara</h2>
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="p-4 bg-purple-50 rounded-lg">
        <p className="text-xs text-purple-600 uppercase">Transit Activation</p>
        <p className="text-2xl font-bold text-purple-900">{transit.activation_score || 0}%</p>
      </div>
      <div className="p-4 bg-emerald-50 rounded-lg">
        <p className="text-xs text-emerald-600 uppercase">Overall Strength</p>
        <p className="text-2xl font-bold text-emerald-900">{transit.grade || '—'}</p>
      </div>
      <div className="p-4 bg-amber-50 rounded-lg">
        <p className="text-xs text-amber-600 uppercase">MD Lord Transit</p>
        <p className="text-2xl font-bold text-amber-900">{transit.breakdown?.dasha_sync || 0}%</p>
      </div>
      <div className="p-4 bg-blue-50 rounded-lg">
        <p className="text-xs text-blue-600 uppercase">Timing Confidence</p>
        <p className="text-2xl font-bold text-blue-900">{transit.timing_confidence || 'MODERATE'}</p>
      </div>
    </div>
    <div className="p-4 bg-gray-50 rounded-lg">
      <h3 className="font-bold mb-3">Confidence Flags</h3>
      <div className="flex flex-wrap gap-2">
        {transit.confidence_flags?.map((f: string, i: number) => (
          <span key={i} className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full">
            {f.replace(/_/g, ' ')}
          </span>
        ))}
      </div>
    </div>
  </div>
);

const NotesSection = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Consultation Notes</h2>
    <div className="h-64 bg-gray-50 border border-gray-200 rounded-lg p-4 text-gray-500 italic">
      [Consultation notes will appear here when implemented]
    </div>
  </div>
);

const AppendixSection = ({ report }: { report: any }) => (
  <div className="p-6">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Appendix</h2>
    <div className="space-y-6">
      <div>
        <h3 className="font-bold mb-2">Engine Outputs Summary</h3>
        <pre className="bg-gray-900 text-green-300 p-4 rounded text-xs overflow-auto max-h-64">
          {JSON.stringify(report?.formula_verification?.engine_outputs || {}, null, 2)}
        </pre>
      </div>
      <div>
        <h3 className="font-bold mb-2">Master Probability Breakdown</h3>
        <pre className="bg-gray-900 text-green-300 p-4 rounded text-xs overflow-auto max-h-64">
          {JSON.stringify(report?.formula_verification?.master_probability?.breakdown || {}, null, 2)}
        </pre>
      </div>
    </div>
  </div>
);

export default PrintFramework;