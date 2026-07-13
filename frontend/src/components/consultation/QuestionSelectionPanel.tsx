import React, { useMemo } from 'react';
import { QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';

interface QuestionSelectionPanelProps {
  selectedQuestions: Set<string>;
  onQuestionToggle: (questionId: string) => void;
  onPackageSelect: (packageId: string, replace?: boolean) => void;
  onSearch: (query: string) => void;
  onDomainFilter: (domainId: string | null) => void;
  onSelectAll: () => void;
  onClear: () => void;
  onFavoritesToggle: () => void;
  showFavorites: boolean;
  packages: Array<{id: string; name: string; questions: number}>;
  searchQuery: string;
  filterDomain: string | null;
}

export const QuestionSelectionPanel: React.FC<QuestionSelectionPanelProps> = ({
  selectedQuestions,
  onQuestionToggle,
  onPackageSelect,
  onSearch,
  onDomainFilter,
  onSelectAll,
  onClear,
  onFavoritesToggle,
  showFavorites,
  packages,
  searchQuery,
  filterDomain,
}) => {
  const visibleQuestions = useMemo(() => {
    let questions: Array<{
      id: string;
      label: string;
      domainId: string;
      domainLabel: string;
    }> = [];

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
  }, [filterDomain, searchQuery]);

  return (
    <div className="h-full flex flex-col bg-white">
      <div className="p-4 border-b border-gray-200 bg-gray-50 flex flex-wrap gap-2">
        <div className="flex-1 min-w-[200px]">
          <input
            type="text"
            placeholder="Search questions..."
            value={searchQuery}
            onChange={(e) => onSearch(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <select
            value={filterDomain || ''}
            onChange={(e) => onDomainFilter(e.target.value || null)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="">All Domains</option>
            <option value="marriage">Marriage</option>
            <option value="career">Career</option>
            <option value="wealth">Wealth</option>
          </select>
          <button onClick={onSelectAll} className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700">Select All Visible</button>
          <button onClick={onClear} className="px-3 py-1.5 text-sm bg-gray-600 text-white rounded-md hover:bg-gray-700">Clear All</button>
        </div>
      </div>

      <div className="p-3 border-b border-gray-200 flex items-center gap-4 bg-gray-50">
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={false} className="form-checkbox h-4 w-4 text-blue-600" />
          Favorites
        </label>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600" />
          Packages
        </label>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600" />
          Recents
        </label>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600" />
          Recommended
        </label>
      </div>

      <div className="p-3 border-b border-gray-200">
        <div className="mb-2 text-sm font-medium text-gray-700">Quick Packages</div>
        <div className="flex flex-wrap gap-2">
          {[
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
          ].map((pkg) => (
            <button
              key={pkg.id}
              className="px-3 py-1.5 text-xs bg-blue-50 text-blue-700 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
            >
              {pkg.name} ({pkg.questions})
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        <div className="text-center py-8 text-gray-400">
          <p>Question selection panel - implementation in progress</p>
          <p className="text-sm text-gray-500 mt-2">This would display hierarchical checkboxes for all 83 questions across 13 domains</p>
        </div>
      </div>
    </div>
  );
};

export default QuestionSelectionPanel;