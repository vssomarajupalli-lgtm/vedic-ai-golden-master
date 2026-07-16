import React, { useMemo, useCallback } from 'react';
import { Search, X, ChevronDown, Tag, Star, Archive } from 'lucide-react';
import { useConsultationRepository } from '../../hooks/useConsultationRepository';

interface ConsultationSearchPanelProps {
  onSearchChange: (query: string) => void;
  placeholder?: string;
}

export const ConsultationSearchPanel: React.FC<ConsultationSearchPanelProps> = ({
  onSearchChange,
  placeholder = 'Search consultations...',
}) => {
  const { searchConsultations } = useConsultationRepository();
  const [query, setQuery] = React.useState('');
  const [suggestions, setSuggestions] = React.useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = React.useState(false);

  // Debounced search
  const debouncedSearch = useMemo(
    () => {
      let timeoutId: ReturnType<typeof setTimeout>;
      return (value: string) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          if (value.trim()) {
            const results = searchConsultations(value);
            const tags = new Set<string>();
            results.forEach((r: any) => r.metadata.tags.forEach((t: string) => tags.add(t)));
            setSuggestions(Array.from(tags).slice(0, 8));
          } else {
            setSuggestions([]);
          }
        }, 200);
      };
    },
    [searchConsultations]
  );

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    onSearchChange(value);
    debouncedSearch(value);
    setShowSuggestions(true);
  }, [onSearchChange, debouncedSearch]);

  const handleFocus = useCallback(() => {
    if (query.trim()) setShowSuggestions(true);
  }, [query]);

  const handleBlur = useCallback(() => {
    setTimeout(() => setShowSuggestions(false), 200);
  }, []);

  const selectSuggestion = useCallback((suggestion: string) => {
    const newQuery = `${query} ${suggestion}`.trim();
    setQuery(newQuery);
    onSearchChange(newQuery);
    setShowSuggestions(false);
  }, [query, onSearchChange]);

  return (
    <div className="relative flex-1 min-w-[250px]">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder={placeholder}
          value={query}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
        />
        {query && (
          <button
            onClick={() => { setQuery(''); onSearchChange(''); setShowSuggestions(false); }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            aria-label="Clear search"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-10 max-h-48 overflow-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => selectSuggestion(suggestion)}
              className="w-full px-3 py-2 text-left text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 flex items-center gap-2"
            >
              <Tag className="w-4 h-4 text-gray-400" />
              <span>#{suggestion}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

interface ConsultationFilterPanelProps {
  onCategoryChange: (category: string) => void;
  onStatusChange: (status: string) => void;
  onTagChange: (tags: string[]) => void;
  onFavoriteToggle: (isFavorite: string) => void;
  currentCategory: string;
  currentStatus: string;
  currentTags: string[];
  currentFavorite: string;
  availableCategories: string[];
  _availableStatuses: string[];
  availableTags: string[];
}

export const ConsultationFilterPanel: React.FC<ConsultationFilterPanelProps> = ({
  onCategoryChange,
  onStatusChange,
  onTagChange,
  onFavoriteToggle,
  currentCategory,
  currentStatus,
  currentTags,
  currentFavorite,
  availableCategories,
  availableTags,
}) => {
  const [showTags, setShowTags] = React.useState(false);
  const [selectedTags, setSelectedTags] = React.useState<string[]>(currentTags);

  const handleTagToggle = (tag: string) => {
    const newTags = selectedTags.includes(tag)
      ? selectedTags.filter(t => t !== tag)
      : [...selectedTags, tag];
    setSelectedTags(newTags);
    onTagChange(newTags);
  };

  const handleTagSelectAll = () => {
    if (selectedTags.length === availableTags.length) {
      setSelectedTags([]);
      onTagChange([]);
    } else {
      setSelectedTags(availableTags);
      onTagChange(availableTags);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Category Filter */}
      <select
        value={currentCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 min-w-[140px]"
      >
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="archived">Archived</option>
        <option value="recycle_bin">Recycle Bin</option>
        {availableCategories.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      {/* Status Filter */}
      <select
        value={currentStatus}
        onChange={(e) => onStatusChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 min-w-[140px]"
      >
        <option value="all">All Status</option>
        <option value="active">Active</option>
        <option value="archived">Archived</option>
        <option value="draft">Draft</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
        <option value="recycle_bin">Recycle Bin</option>
      </select>

      {/* Favorite Filter */}
      <select
        value={currentFavorite}
        onChange={(e) => onFavoriteToggle(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 min-w-[120px]"
      >
        <option value="all">All Favorites</option>
        <option value="true">Favorites Only</option>
        <option value="false">Non-Favorites</option>
      </select>

      {/* Tags Filter */}
      <div className="relative">
        <button
          type="button"
          onClick={() => setShowTags(!showTags)}
          className={`px-3 py-2 border rounded-lg text-sm flex items-center gap-2 ${
            currentTags.length > 0 ? 'border-indigo-300 bg-indigo-50 text-indigo-700' : 'border-gray-300 text-gray-700'
          }`}
        >
          <Tag className="w-4 h-4" />
          <span>{currentTags.length > 0 ? `${currentTags.length} tags` : 'Tags'}</span>
          <ChevronDown className={`w-4 h-4 ${showTags ? 'rotate-180' : ''}`} />
        </button>

        {showTags && (
          <div className="absolute right-0 mt-1 w-56 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-10">
            {availableTags.length === 0 ? (
              <div className="px-3 py-2 text-sm text-gray-500">No tags available</div>
            ) : (
              <>
                <div className="px-3 py-2 border-b border-gray-100 flex items-center justify-between">
                  <span className="text-xs font-medium text-gray-500 uppercase">Available Tags</span>
                  <button
                    onClick={handleTagSelectAll}
                    className="text-xs text-indigo-600 hover:text-indigo-700"
                  >
                    {selectedTags.length === availableTags.length ? 'Deselect All' : 'Select All'}
                  </button>
                </div>
                <div className="max-h-48 overflow-auto">
                  {availableTags.map(tag => (
                    <label
                      key={tag}
                      className={`flex items-center gap-2 px-3 py-2 hover:bg-gray-50 cursor-pointer ${selectedTags.includes(tag) ? 'bg-indigo-50' : ''}`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedTags.includes(tag)}
                        onChange={() => handleTagToggle(tag)}
                        className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <span className="text-sm text-gray-700">{tag}</span>
                    </label>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

interface ConsultationSortPanelProps {
  onSortChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  currentSortBy: string;
  currentSortOrder: 'asc' | 'desc';
}

export const ConsultationSortPanel: React.FC<ConsultationSortPanelProps> = ({
  onSortChange,
  currentSortBy,
  currentSortOrder,
}) => {
  const sortOptions = [
    { value: 'updatedAt', label: 'Last Updated' },
    { value: 'createdAt', label: 'Created Date' },
    { value: 'title', label: 'Title' },
    { value: 'clientName', label: 'Client Name' },
    { value: 'probability', label: 'Probability' },
    { value: 'questionCount', label: 'Questions' },
  ];

  return (
    <div className="flex items-center gap-2">
      <label className="text-sm text-gray-500">Sort by:</label>
      <select
        value={currentSortBy}
        onChange={(e) => onSortChange(e.target.value, currentSortOrder)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        {sortOptions.map(opt => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
      <button
        onClick={() => onSortChange(currentSortBy, currentSortOrder === 'asc' ? 'desc' : 'asc')}
        className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        aria-label={currentSortOrder === 'asc' ? 'Sort descending' : 'Sort ascending'}
      >
        {currentSortOrder === 'asc' ? '↑' : '↓'}
      </button>
    </div>
  );
};

interface ConsultationViewModeToggleProps {
  viewMode: 'grid' | 'list';
  onViewModeChange: (mode: 'grid' | 'list') => void;
}

export const ConsultationViewModeToggle: React.FC<ConsultationViewModeToggleProps> = ({
  viewMode,
  onViewModeChange,
}) => (
  <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
    <button
      onClick={() => onViewModeChange('grid')}
      className={`p-2 rounded ${viewMode === 'grid' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'}`}
      title="Grid View"
      aria-label="Grid View"
    >
      <div className="w-5 h-5 grid grid-cols-2 gap-1">
        <div className="bg-current h-2 rounded"></div>
        <div className="bg-current h-2 rounded"></div>
        <div className="bg-current h-2 rounded"></div>
        <div className="bg-current h-2 rounded"></div>
      </div>
    </button>
    <button
      onClick={() => onViewModeChange('list')}
      className={`p-2 rounded ${viewMode === 'list' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'}`}
      title="List View"
      aria-label="List View"
    >
      <div className="w-5 h-5 flex flex-col justify-between">
        <div className="bg-current h-1.5 rounded w-full"></div>
        <div className="bg-current h-1.5 rounded w-full"></div>
        <div className="bg-current h-1.5 rounded w-full"></div>
      </div>
    </button>
  </div>
);

interface ConsultationBulkActionsProps {
  selectedCount: number;
  onFavorite: () => void;
  onArchive: () => void;
  onTag: () => void;
  onExport: () => void;
  onDelete: () => void;
  onClear: () => void;
}

export const ConsultationBulkActions: React.FC<ConsultationBulkActionsProps> = ({
  selectedCount,
  onFavorite,
  onArchive,
  onTag,
  onExport,
  onDelete,
  onClear,
}) => {
  if (selectedCount === 0) return null;

  return (
    <div className="p-3 bg-blue-50 border-b border-blue-200 flex items-center justify-between flex-wrap gap-2">
      <span className="text-sm text-blue-800 font-medium">
        {selectedCount} consultation{selectedCount !== 1 ? 's' : ''} selected
      </span>
      <div className="flex items-center gap-2 flex-wrap">
        <button onClick={onFavorite} className="px-3 py-1 text-xs bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50 transition-colors">
          <Star className="w-3 h-3 inline mr-1" /> Favorite
        </button>
        <button onClick={onArchive} className="px-3 py-1 text-xs bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50 transition-colors">
          <Archive className="w-3 h-3 inline mr-1" /> Archive
        </button>
        <button onClick={onTag} className="px-3 py-1 text-xs bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50 transition-colors">
          <Tag className="w-3 h-3 inline mr-1" /> Tag
        </button>
        <button onClick={onExport} className="px-3 py-1 text-xs bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50 transition-colors">
          Export
        </button>
        <button onClick={onDelete} className="px-3 py-1 text-xs bg-white border border-red-300 text-red-700 rounded hover:bg-red-50 transition-colors">
          Delete
        </button>
        <button onClick={onClear} className="px-3 py-1 text-xs text-gray-500 hover:text-gray-700">
          Clear
        </button>
      </div>
    </div>
  );
};

export default {
  ConsultationSearchPanel,
  ConsultationFilterPanel,
  ConsultationSortPanel,
  ConsultationViewModeToggle,
  ConsultationBulkActions,
};