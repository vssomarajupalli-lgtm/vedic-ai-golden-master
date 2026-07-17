// BKL-008C.2 — Client Management UI
// Client Search / Filter / Sort Bar

import React, { useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';
import type { ClientStatus, ClientSearchFilters } from '../../types/client';

interface ClientSearchFilterSortProps {
  onSearchChange: (filters: ClientSearchFilters) => void;
  viewMode: 'grid' | 'list';
  onViewModeChange: (mode: 'grid' | 'list') => void;
  allTags: string[];
}

export const ClientSearchFilterSort: React.FC<ClientSearchFilterSortProps> = ({
  onSearchChange,
  viewMode,
  onViewModeChange,
  allTags,
}) => {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState<ClientStatus | ''>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);

  const applyFilters = (
    newQuery: string,
    newStatus: ClientStatus | '',
    newTags: string[],
  ) => {
    const filters: ClientSearchFilters = {};
    if (newQuery.trim()) filters.query = newQuery;
    if (newStatus) filters.status = newStatus as ClientStatus;
    if (newTags.length > 0) filters.tags = newTags;
    onSearchChange(filters);
  };

  const handleQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);
    applyFilters(val, status, selectedTags);
  };

  const handleStatusChange = (newStatus: ClientStatus | '') => {
    setStatus(newStatus);
    applyFilters(query, newStatus, selectedTags);
  };

  const handleTagToggle = (tag: string) => {
    const newTags = selectedTags.includes(tag)
      ? selectedTags.filter(t => t !== tag)
      : [...selectedTags, tag];
    setSelectedTags(newTags);
    applyFilters(query, status, newTags);
  };

  const handleClearAll = () => {
    setQuery('');
    setStatus('');
    setSelectedTags([]);
    onSearchChange({});
  };

  const hasActiveFilters = query || status || selectedTags.length > 0;

  return (
    <div className="space-y-3">
      {/* Search + View Toggle Row */}
      <div className="flex flex-wrap gap-3">
        <div className="flex-1 min-w-[250px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search clients by name, email, tags..."
            value={query}
            onChange={handleQueryChange}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          />
        </div>

        <select
          value={status}
          onChange={(e) => handleStatusChange(e.target.value as ClientStatus | '')}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="archived">Archived</option>
        </select>

        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`px-3 py-2 border rounded-lg text-sm flex items-center gap-2 transition-colors ${
            showFilters || selectedTags.length > 0
              ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
              : 'border-gray-300 text-gray-600 hover:bg-gray-50'
          }`}
        >
          <SlidersHorizontal className="w-4 h-4" />
          Tags {selectedTags.length > 0 && `(${selectedTags.length})`}
        </button>

        {/* View Toggle */}
        <div className="flex items-center border border-gray-300 rounded-lg overflow-hidden">
          <button
            onClick={() => onViewModeChange('grid')}
            className={`px-3 py-2 text-sm transition-colors ${
              viewMode === 'grid'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
            title="Grid view"
          >
            <svg className="w-4 h-4" viewBox="0 0 16 16" fill="currentColor">
              <rect x="1" y="1" width="6" height="6" rx="1" />
              <rect x="9" y="1" width="6" height="6" rx="1" />
              <rect x="1" y="9" width="6" height="6" rx="1" />
              <rect x="9" y="9" width="6" height="6" rx="1" />
            </svg>
          </button>
          <button
            onClick={() => onViewModeChange('list')}
            className={`px-3 py-2 text-sm transition-colors ${
              viewMode === 'list'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
            title="List view"
          >
            <svg className="w-4 h-4" viewBox="0 0 16 16" fill="currentColor">
              <rect x="1" y="2" width="14" height="2" rx="1" />
              <rect x="1" y="7" width="14" height="2" rx="1" />
              <rect x="1" y="12" width="14" height="2" rx="1" />
            </svg>
          </button>
        </div>
      </div>

      {/* Tag Filter Panel */}
      {showFilters && allTags.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">
              Filter by Tags
            </span>
            {selectedTags.length > 0 && (
              <button
                onClick={() => {
                  setSelectedTags([]);
                  applyFilters(query, status, []);
                }}
                className="text-xs text-indigo-600 hover:text-indigo-800"
              >
                Clear tags
              </button>
            )}
          </div>
          <div className="flex flex-wrap gap-2">
            {allTags.map(tag => (
              <button
                key={tag}
                onClick={() => handleTagToggle(tag)}
                className={`px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                  selectedTags.includes(tag)
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Active Filters Summary */}
      {hasActiveFilters && (
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span>Filters active:</span>
          {query && (
            <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
              &ldquo;{query}&rdquo;
            </span>
          )}
          {status && (
            <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded-full text-xs">
              {status}
            </span>
          )}
          {selectedTags.map(tag => (
            <span key={tag} className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded-full text-xs">
              {tag}
            </span>
          ))}
          <button
            onClick={handleClearAll}
            className="text-xs text-red-500 hover:text-red-700 underline"
          >
            Clear all
          </button>
        </div>
      )}
    </div>
  );
};

export default ClientSearchFilterSort;