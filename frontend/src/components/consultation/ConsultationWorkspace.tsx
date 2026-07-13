import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useChartStore } from '../../store/useChartStore';
import { apiService } from '../../api/backend';
import { QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';
import { QuestionSelectionPanel } from './QuestionSelectionPanel';
import { ReportStructurePanel } from './ReportStructurePanel';
import { PRINT_PROFILES } from '../../types/print-profiles';
import { FileText, Download, Printer, Eye, MessageCircle } from 'lucide-react';

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
  const [showFavorites, setShowFavorites] = useState(false);
  const [mode, setMode] = useState<'standard' | 'professional' | 'expert' | 'study'>('professional');
  const [consultationTitle, setConsultationTitle] = useState('New Consultation');
  
  useEffect(() => {
    if (location.state?.initialQuestionId) {
      setSelectedQuestions(new Set([location.state.initialQuestionId]));
    }
  }, [location.state]);
  
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

  const handleQuestionToggle = (questionId: string) => {
    const next = new Set(selectedQuestions);
    if (next.has(questionId)) next.delete(questionId);
    else next.add(questionId);
    setSelectedQuestions(next);
  };

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
          <button onClick={() => {}} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Save</button>
          <button onClick={() => {}} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">Preview</button>
          <button onClick={() => {}} className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">Generate Report</button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-64 border-r border-gray-200 bg-white flex flex-col">
          <nav className="flex-1 p-4 space-y-2">
            <button className="w-full text-left px-4 py-2 rounded-md transition-colors bg-blue-50 text-blue-700">
              Question Selection
            </button>
            <button className="w-full text-left px-4 py-2 rounded-md transition-colors text-gray-700 hover:bg-gray-50">
              Report Structure
            </button>
            <button className="w-full text-left px-4 py-2 rounded-md transition-colors text-gray-700 hover:bg-gray-50">
              Notes & Bookmarks
            </button>
            <button className="w-full text-left px-4 py-2 rounded-md transition-colors text-gray-700 hover:bg-gray-50">
              Preview Report
            </button>
          </nav>
          <div className="p-4 border-t border-gray-200">
            <div className="text-sm text-gray-500">0 questions selected</div>
          </div>
        </div>

        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-auto p-4">
            <QuestionSelectionPanel
              selectedQuestions={new Set()}
              onQuestionToggle={() => {}}
              onPackageSelect={() => {}}
              onSearch={() => {}}
              onDomainFilter={() => {}}
              onSelectAll={() => {}}
              onClear={() => {}}
              onFavoritesToggle={() => {}}
              showFavorites={false}
              packages={[]}
              searchQuery=""
              filterDomain={null}
              />
              </div>

          <div className="p-4 border-t border-gray-200 bg-white flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">0 questions selected</span>
            </div>
            <div className="flex items-center space-x-2">
              <select className="px-3 py-1 border border-gray-300 rounded-md text-sm">
                <option value="professional-consultation">Professional Consultation</option>
              </select>
              <button className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">Print</button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Export PDF</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsultationWorkspace;