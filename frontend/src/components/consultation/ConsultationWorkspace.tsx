import React, { useState, useEffect, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { useChartStore } from '../../store/useChartStore';
import { apiService } from '../../api/backend';
import { QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';
import { QuestionSelectionPanel } from './QuestionSelectionPanel';
import { ReportStructurePanel } from './ReportStructurePanel';
import { FileText, Eye, MessageCircle } from 'lucide-react';

interface ConsultationWorkspaceProps {
  initialQuestionId?: string;
}

export const ConsultationWorkspace: React.FC<ConsultationWorkspaceProps> = ({
  initialQuestionId,
}) => {
  const location = useLocation();
  const { canonicalContent, machineIndex } = useChartStore();
  
  const [selectedQuestions, setSelectedQuestions] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState<'selection' | 'structure' | 'notes' | 'preview'>('selection');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDomain, setFilterDomain] = useState<string | null>(null);
  const [consultationTitle] = useState('New Consultation');
  
  useEffect(() => {
    if (location.state?.initialQuestionId) {
      setSelectedQuestions(new Set([location.state.initialQuestionId]));
    } else if (initialQuestionId) {
      setSelectedQuestions(new Set([initialQuestionId]));
    }
  }, [location.state, initialQuestionId]);
  
  const consultation = useMemo(() => ({
    id: `consultation-${Date.now()}`,
    version: 1,
    title: consultationTitle,
    client: { name: '', tags: [] },
    birthData: { date: '', time: '', timezone: '', latitude: 0, longitude: 0, place: '' },
    structure: {
      coverPage: { included: true, title: consultationTitle, showClientName: true, showBirthDetails: true, showReportDate: true, branding: { primaryColor: '#1e3a5f', secondaryColor: '#c4963a', showWatermark: false } },
      executiveSummary: { mode: 'auto', includeKeyMetrics: true, includeRecommendations: true },
      chapters: Array.from(selectedQuestions).map((qId, index) => {
        let domainId = 0;
        let label = qId;
        QUESTIONNAIRE_SCHEMA.forEach(domain => {
          const q = domain.questions.find(q => q.id === qId);
          if (q) {
            domainId = parseInt(domain.domainId.replace('marriage', '7').replace('career', '10').replace('wealth', '2').replace('health', '6').replace('children', '8').replace('property', '4').replace('education', '5').replace('travel', '11').replace('spiritual', '12').replace('compatibility', '9').replace('retirement', '10'));
            label = q.label;
          }
        });
        return {
          id: `chapter-${domainId}`,
          title: domainId ? `${domainId}. ${QUESTIONNAIRE_SCHEMA.find(d => parseInt(d.domainId.replace(/\D/g,'')) === domainId)?.domainLabel || `Domain ${domainId}`}` : `Chapter ${index + 1}`,
          order: index + 1,
          included: true,
          questions: [{ questionId: qId, domainId, order: 1, included: true, customLabel: label }],
        };
      }),
      appendices: { birthChart: true, planetaryPositions: true, dashaTimeline: true, transitCalendar: true, vimshottariDetails: false, ashtakavargaGrid: false },
    },
    formatting: {
      pageSize: 'A4',
      orientation: 'portrait',
      margins: { top: 25, right: 25, bottom: 25, left: 30 },
      header: { enabled: true, left: '{reportTitle}', center: '', right: '{chapterTitle}' },
      footer: { enabled: true, left: 'Samartha Vedic AI', center: '{pageNumber}', right: '{clientName}' },
      pageNumbers: { enabled: true, format: 'arabic', position: 'bottom-center' },
      typography: { fontHeading: 'Merriweather', fontBody: 'Inter', fontMono: 'JetBrains Mono', fontSizeBase: 11, lineHeight: 1.5 },
      branding: { primaryColor: '#1e3a5f', secondaryColor: '#c4963a', showWatermark: false },
    },
    metadata: { consultationId: '', version: 1, generatedAt: new Date(), generatedBy: 'user', tags: [] },
    createdAt: new Date(),
    updatedAt: new Date(),
  }), [selectedQuestions, consultationTitle]);

  const onGenerateReport = async () => {
    if (!canonicalContent || !machineIndex) return;
    
    try {
      const response = await apiService.generateReport(canonicalContent, machineIndex);
      console.log('Report generated:', response);
    } catch (error) {
      console.error('Report generation failed:', error);
    }
  };

  const onPreview = () => {
    // Preview logic
  };

  const onPrint = () => {
    window.print();
  };

  const onSave = () => {
    console.log('Save consultation');
  };

  const onExportPDF = async () => {
    // PDF export
  };

  const packages = [
    { id: 'marriage-complete', name: '💍 Marriage Complete', questions: 8 },
    { id: 'career-complete', name: '💼 Career Complete', questions: 8 },
    { id: 'wealth-complete', name: '💰 Wealth Complete', questions: 8 },
    { id: 'health-complete', name: '🏥 Health Complete', questions: 8 },
    { id: 'property-complete', name: '🏠 Property Complete', questions: 11 },
    { id: 'children-complete', name: '👶 Children Complete', questions: 7 },
    { id: 'education-complete', name: '🎓 Education Complete', questions: 8 },
    { id: 'travel-complete', name: '🌍 Travel Complete', questions: 6 },
    { id: 'spiritual-complete', name: '🕉 Spiritual Complete', questions: 7 },
    { id: 'complete-horoscope', name: '📚 Complete Horoscope', questions: 83 },
  ];

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-800">Consultation Workspace</h1>
        </div>
        <div className="flex items-center space-x-2">
          <button onClick={onSave} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Save</button>
          <button onClick={onPreview} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">
            <Eye className="w-4 h-4 mr-1" /> Preview
          </button>
          <button onClick={onGenerateReport} className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">Generate Report</button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-64 border-r border-gray-200 bg-white flex flex-col">
          <nav className="flex-1 p-4 space-y-2">
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'selection' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('selection')}
            >
              <MessageCircle className="w-5 h-5 mr-2 inline" />
              Question Selection
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'structure' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('structure')}
            >
              <FileText className="w-5 h-5 mr-2 inline" />
              Report Structure
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'notes' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => setActiveTab('notes')}
            >
              <MessageCircle className="w-5 h-5 mr-2 inline" />
              Notes & Bookmarks
            </button>
            <button
              className={`w-full text-left px-4 py-2 rounded-md transition-colors ${
                activeTab === 'preview' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
              }`}
              onClick={onPreview}
            >
              <Eye className="w-5 h-5 mr-2 inline" />
              Preview Report
            </button>
          </nav>
          <div className="p-4 border-t border-gray-200">
            <div className="text-sm text-gray-500">
              {selectedQuestions.size} questions selected
            </div>
          </div>
        </div>

        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-auto p-4">
            {activeTab === 'selection' && (
              <QuestionSelectionPanel
                onPackageSelect={() => {}}
                onSearch={setSearchQuery}
                onDomainFilter={setFilterDomain}
                onSelectAll={() => {}}
                onClear={() => setSelectedQuestions(new Set())}
                packages={packages}
                searchQuery={searchQuery}
                filterDomain={filterDomain}
              />
            )}

            {activeTab === 'structure' && (
              <ReportStructurePanel
                consultation={consultation}
                onConsultationChange={(updated) => console.log('Consultation updated:', updated)}
              />
            )}

            {activeTab === 'notes' && (
              <div className="h-full bg-white p-4">
                <p className="text-gray-500">Notes & Bookmarks panel - to be implemented</p>
              </div>
            )}

            {activeTab === 'preview' && (
              <div className="h-full bg-white p-4">
                <div className="max-w-3xl mx-auto">
                  <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
                    <h2 className="text-xl font-bold mb-4">Report Preview</h2>
                    <p className="text-gray-600">Preview of the generated consultation report will appear here.</p>
                    <div className="mt-4 p-4 bg-white border border-gray-200 rounded">
                      <h3 className="font-bold">{consultationTitle}</h3>
                      <p className="text-gray-600 mt-2">Selected Questions: {selectedQuestions.size}</p>
                      <p className="text-gray-600 mt-1">Estimated Pages: {Math.ceil(selectedQuestions.size * 1.2 + 3)}</p>
                      <div className="mt-4 space-y-2">
                        {Array.from(selectedQuestions).slice(0, 5).map(qId => (
                          <div key={qId} className="text-sm text-gray-700 border-b border-gray-100 pb-2">
                            {qId}
                          </div>
                        ))}
                        {selectedQuestions.size > 5 && <p className="text-sm text-gray-500">... and {selectedQuestions.size - 5} more</p>}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t border-gray-200 bg-white flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {selectedQuestions.size} questions selected · Est. {Math.ceil(selectedQuestions.size * 1.2 + 3)} pages
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <select
                value="professional-consultation"
                onChange={() => {}}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm"
              >
                <option value="professional-consultation">Professional Consultation</option>
              </select>
              <button onClick={onPrint} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">Print</button>
              <button onClick={onExportPDF} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Export PDF</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsultationWorkspace;