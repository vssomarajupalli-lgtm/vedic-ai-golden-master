import React, { useState, useMemo } from 'react';
import { QuestionPackage, PackageManager, CreateCustomPackageData } from '../../types/packages';
import { QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';

interface QuestionSelectionPanelProps {
  selectedQuestions: Set<string>;
  onQuestionToggle: (questionId: string) => void;
  onPackageSelect: (packageId: string, replace?: boolean) => void;
  onCustomPackageCreate: (data: any) => void;
  onSearch: (query: string) => void;
  onDomainFilter: (domainId: string | null) => void;
  onSelectAll: () => void;
  onClear: () => void;
  onFavoritesToggle: () => void;
  showFavorites: boolean;
  showPackages: boolean;
  packages: any[];
  selectedQuestions: Set<string>;
  searchQuery: string;
  filterDomain: string | null;
  showFavorites: boolean;
}

export const QuestionSelectionPanel: React.FC<QuestionSelectionPanelProps> = ({
  selectedQuestions,
  onQuestionToggle,
  onPackageSelect,
  onCustomPackageCreate,
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
  const [showCustomPackageDialog, setShowCustomPackageDialog] = useState(false);
  const [customPackageName, setCustomPackageName] = useState('');
  const [customPackageDescription, setCustomPackageDescription] = useState('');
  const [customPackageTags, setCustomPackageTags] = useState('');
  const [selectedPackageQuestions, setSelectedPackageQuestions] = useState<Set<string>>(new Set());

  const filteredQuestions = useMemo(() => {
    let questions: Array<{
      id: string;
      label: string;
      domainId: string;
      domainLabel: string;
      isFavorite?: boolean;
      recentlyUsed?: boolean;
      recommended?: boolean;
    }> = [];

    // This would come from the questionnaire schema
    const allQuestions = [
      // This would be populated from the questionnaire schema
    ];

    return allQuestions;
  }, []);

  const domainGroups = useMemo(() => {
    const groups: Record<string, { domainId: string; label: string; questions: any[] }> = {};
    return groups;
  }, []);

  const handlePackageSelect = (packageId: string) => {
    // This would be handled by the parent
  };

  const handleCustomPackageSubmit = (e: React.FormEvent) => {
    e.preventDefault();
  };

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Toolbar */}
      <div className="p-4 border-b border-gray-200 bg-gray-50 flex flex-wrap gap-2">
        <div className="flex-1 min-w-[200px]">
          <input
            type="text"
            placeholder="Search questions..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Search questions..."
            onChange={(e) => console.log('Search:', e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <select
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
            onChange={(e) => console.log('Domain filter:', e.target.value)}
          >
            <option value="">All Domains</option>
            <option value="marriage">Marriage</option>
            <option value="career">Career</option>
            <option value="wealth">Wealth</option>
          </select>
          <button
            onClick={() => {}}
            className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Select All Visible
          </button>
          <button
            onClick={() => {}}
            className="px-3 py-1.5 text-sm bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            Clear All
          </button>
        </div>
      </div>

      {/* Favorites & Package Toggle */}
      <div className="p-3 border-b border-gray-200 flex items-center gap-4 bg-gray-50">
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" className="form-checkbox h-4 w-4 text-blue-600" />
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

      {/* Package Selector */}
      <div className="p-3 border-b border-gray-200">
        <div className="mb-2 text-sm font-medium text-gray-700">Quick Packages</div>
        <div className="flex flex-wrap gap-2">
          {[
            { id: 'marriage-complete', name: '💍 Marriage Complete', questions: 8 },
            { id: 'career-complete', name: '💼 Career Complete', questions: 8 },
            { id: 'wealth-complete', name: '💰 Wealth Complete', questions: 8 },
            { id: 'health-complete', name: '🏥 Health Complete', questions: 8 },
            { id: 'property-complete', name: '🏠 Property Complete', questions: 11 },
            { id: 'complete-horoscope', name: '📚 Complete Horoscope', questions: 83 },
          ].map((pkg) => (
            <button
              key={pkg.id}
              onClick={() => {}}
              className="px-3 py-1.5 text-xs bg-blue-50 text-blue-700 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
            >
              {pkg.name} ({pkg.questions})
            </button>
          ))}
        </div>
      </div>

      {/* Custom Package Dialog */}
      {showCustomPackageDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold mb-4">Create Custom Package</h3>
            <form onSubmit={handleCustomPackageSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Package Name</label>
                <input
                  type="text"
                  value={customPackageName}
                  onChange={(e) => setCustomPackageName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., My Premium Consultation"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={customPackageDescription}
                  onChange={(e) => setCustomPackageDescription(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  placeholder="Brief description of this package"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tags (comma-separated)</label>
                <input
                  type="text"
                  value={customPackageTags}
                  onChange={(e) => setCustomPackageTags(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  placeholder="marriage, career, premium"
                />
              </div>
              <div className="flex justify-end gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCustomPackageDialog(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Create Package
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Question List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {/* Domain groups would go here */}
        <div className="text-center py-8 text-gray-400">
          <p>Question selection panel - implementation in progress</p>
          <p className="text-sm text-gray-500 mt-2">This would display hierarchical checkboxes for all 83 questions across 13 domains</p>
        </div>
      </div>
    </div>
  );
};

export default QuestionSelectionPanel;