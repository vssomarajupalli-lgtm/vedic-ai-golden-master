// @ts-nocheck
import React, { useMemo, useCallback } from 'react';
import { 
  BookOpen, Star, Eye, 
  Plus, X, Search, ChevronDown, Archive,
  Copy, Trash2, Tag
} from 'lucide-react';
import { useConsultationRepository } from '../../hooks/useConsultationRepository';

interface ConsultationListProps {
  onLoadConsultation: (consultation: any) => void;
  onNewConsultation: () => void;
}

export const ConsultationList: React.FC<ConsultationListProps> = ({
  onLoadConsultation,
  onNewConsultation,
}) => {
  const { 
    getConsultations, 
    searchConsultations,
    selectedItems,
    toggleSelection,
    clearSelection,
    bulkAction,
    searchQuery,
    setSearchQuery,
    filterCategory,
    setFilterCategory,
    filterStatus,
    setFilterStatus,
    filterTags,
    setFilterTags,
    sortBy,
    setSortBy,
    viewMode,
    setViewMode,
    currentFavorite,
    setCurrentFavorite,
  } = useConsultationRepository();

  // Apply search, filter, sort
  const filteredConsultations = useMemo(() => {
    let consultations: any[] = getConsultations(filterCategory === 'all' ? undefined : filterCategory as any);
    
    if (searchQuery) {
      consultations = searchConsultations(searchQuery);
    }
    
    if (filterStatus !== 'all') {
      consultations = consultations.filter((c: any) => c.status === filterStatus);
    }
    
    if (currentFavorite !== 'all') {
      const isFav = currentFavorite === 'true';
      consultations = consultations.filter((c: any) => c.metadata.isFavorite === isFav);
    }
    
    if (filterTags.length > 0) {
      consultations = consultations.filter((c: any) => 
        filterTags.every((tag: string) => c.metadata.tags.includes(tag))
      );
    }
    
    consultations.sort((a: any, b: any) => {
      let aVal: any, bVal: any;
      switch (sortBy) {
        case 'updatedAt': aVal = new Date(a.updatedAt).getTime(); bVal = new Date(b.updatedAt).getTime(); break;
        case 'createdAt': aVal = new Date(a.createdAt).getTime(); bVal = new Date(b.createdAt).getTime(); break;
        case 'title': aVal = a.metadata.consultationTitle; bVal = b.metadata.consultationTitle; break;
        case 'clientName': aVal = a.metadata.clientName; bVal = b.metadata.clientName; break;
        case 'probability': aVal = a.snapshots[0]?.metadata?.overallProbability?.score || 0; bVal = b.snapshots[0]?.metadata?.overallProbability?.score || 0; break;
        case 'questionCount': aVal = a.structure.selectedQuestionIds.length; bVal = b.structure.selectedQuestionIds.length; break;
        default: aVal = new Date(a.updatedAt).getTime(); bVal = new Date(b.updatedAt).getTime();
      }
      if (aVal < bVal) return 1;
      if (aVal > bVal) return -1;
      return 0;
    });
    
    return consultations;
  }, [getConsultations, searchConsultations, searchQuery, filterCategory, filterStatus, filterTags, currentFavorite, sortBy]);

  const handleClearSelection = useCallback(() => {
    clearSelection();
  }, [clearSelection]);

  const handleBulkAction = useCallback((action: 'favorite' | 'archive' | 'tag' | 'delete' | 'export') => {
    bulkAction(action);
  }, [bulkAction]);

  const handleLoad = useCallback((consultation: any) => {
    onLoadConsultation(consultation);
  }, [onLoadConsultation]);

  const getOverallProbability = (consultation: any): number => {
    return consultation.snapshots[0]?.metadata?.overallProbability?.score || 0;
  };

  const getActivationPercent = (consultation: any): number => {
    return consultation.snapshots[0]?.metadata?.currentTransit?.activationScore || 0;
  };

  const getCurrentDasha = (consultation: any): { md: string; ad: string } => {
    return {
      md: consultation.snapshots[0]?.metadata?.currentDasha?.md || '—',
      ad: consultation.snapshots[0]?.metadata?.currentDasha?.ad || '—',
    };
  };

  const getTransitGrade = (consultation: any): string => {
    return consultation.snapshots[0]?.metadata?.currentTransit?.grade || '—';
  };

  // Empty state
  if (filteredConsultations.length === 0 && !searchQuery && filterCategory === 'all') {
    return (
      <div className="h-full flex flex-col bg-gray-50">
        <ConsultationToolbar 
          onNewConsultation={onNewConsultation}
          onSearchChange={setSearchQuery}
          searchQuery={searchQuery}
          filteredCount={filteredConsultations.length}
          totalCount={getConsultations().length}
        />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center py-16">
            <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No consultations yet</h3>
            <p className="text-gray-500 mb-6">Create your first consultation to get started</p>
            <button onClick={onNewConsultation} className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Create Consultation
            </button>
          </div>
        </div>
      </div>
    );
  }

  // No search results
  if (filteredConsultations.length === 0 && (searchQuery || filterCategory !== 'all' || filterStatus !== 'all' || filterTags.length > 0)) {
    return (
      <div className="h-full flex flex-col bg-gray-50">
        <ConsultationToolbar 
          onNewConsultation={onNewConsultation}
          onSearchChange={setSearchQuery}
          searchQuery={searchQuery}
          filteredCount={filteredConsultations.length}
          totalCount={getConsultations().length}
        />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center py-16">
            <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No consultations found</h3>
            <p className="text-gray-500 mb-6">Adjust your filters or search terms</p>
            <button onClick={() => { setSearchQuery(''); setFilterCategory('all'); setFilterStatus('all'); setFilterTags([]); }} className="px-4 py-2 text-indigo-600 hover:text-indigo-700 underline">
              Clear all filters
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <ConsultationToolbar 
        onNewConsultation={onNewConsultation}
        onSearchChange={setSearchQuery}
        searchQuery={searchQuery}
        filteredCount={filteredConsultations.length}
        totalCount={getConsultations().length}
      />

      {selectedItems.size > 0 && (
        <ConsultationBulkActionsBar 
          selectedCount={selectedItems.size}
          onFavorite={() => handleBulkAction('favorite')}
          onArchive={() => handleBulkAction('archive')}
          onTag={() => handleBulkAction('tag')}
          onExport={() => handleBulkAction('export')}
          onDelete={() => handleBulkAction('delete')}
          onClear={handleClearSelection}
        />
      )}

      <ConsultationFiltersBar
        filterCategory={filterCategory}
        setFilterCategory={setFilterCategory}
        filterStatus={filterStatus}
        setFilterStatus={setFilterStatus}
        currentFavorite={currentFavorite}
        setCurrentFavorite={setCurrentFavorite}
        sortBy={sortBy}
        setSortBy={setSortBy}
        viewMode={viewMode}
        setViewMode={setViewMode}
      />

      <div className="flex-1 overflow-auto p-4">
        {viewMode === 'grid' ? (
          <GridView
            consultations={filteredConsultations}
            onLoad={handleLoad}
            onSelect={toggleSelection}
            selectedItems={selectedItems}
            getOverallProbability={getOverallProbability}
            getActivationPercent={getActivationPercent}
            getCurrentDasha={getCurrentDasha}
            getTransitGrade={getTransitGrade}
            getOutputCount={(c: any) => c.outputs.length}
          />
        ) : (
          <ListView
            consultations={filteredConsultations}
            onLoad={handleLoad}
            onSelect={toggleSelection}
            selectedItems={selectedItems}
            getOverallProbability={getOverallProbability}
            getActivationPercent={getActivationPercent}
            getCurrentDasha={getCurrentDasha}
            getTransitGrade={getTransitGrade}
            getOutputCount={(c: any) => c.outputs.length}
          />
        )}
      </div>
    </div>
  );
};

// ============================================
// TOOLBAR
// ============================================
const ConsultationToolbar: React.FC<{
  onNewConsultation: () => void;
  onSearchChange: (query: string) => void;
  searchQuery: string;
  filteredCount: number;
  totalCount: number;
}> = ({ onNewConsultation, onSearchChange, searchQuery, filteredCount, totalCount }) => (
  <div className="p-4 border-b border-gray-200 bg-white">
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold text-gray-800">Consultation Library</h1>
        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
          {filteredCount} / {totalCount} consultations
        </span>
      </div>
      <button onClick={onNewConsultation} className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 flex items-center gap-2">
        <Plus className="w-4 h-4" />
        New Consultation
      </button>
    </div>

    <div className="relative flex-1 min-w-[250px] max-w-md">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
      <input
        type="text"
        placeholder="Search consultations..."
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
        className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
      />
      {searchQuery && (
        <button
          onClick={() => onSearchChange('')}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
          aria-label="Clear search"
        >
          <X className="w-5 h-5" />
        </button>
      )}
    </div>
  </div>
);

// ============================================
// BULK ACTIONS BAR
// ============================================
const ConsultationBulkActionsBar: React.FC<{
  selectedCount: number;
  onFavorite: () => void;
  onArchive: () => void;
  onTag: () => void;
  onExport: () => void;
  onDelete: () => void;
  onClear: () => void;
}> = ({ selectedCount, onFavorite, onArchive, onTag, onExport, onDelete, onClear }) => (
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

// ============================================
// FILTERS BAR
// ============================================
const ConsultationFiltersBar: React.FC<{
  filterCategory: string;
  setFilterCategory: (category: string) => void;
  filterStatus: string;
  setFilterStatus: (status: string) => void;
  currentFavorite: string;
  setCurrentFavorite: (fav: string) => void;
  sortBy: string;
  setSortBy: (sort: string) => void;
  viewMode: 'grid' | 'list';
  setViewMode: (mode: 'grid' | 'list') => void;
}> = ({
  filterCategory,
  setFilterCategory,
  filterStatus,
  setFilterStatus,
  currentFavorite,
  setCurrentFavorite,
  sortBy,
  setSortBy,
  viewMode,
  setViewMode,
}) => (
  <div className="p-4 border-b border-gray-200 bg-white">
    <div className="flex flex-wrap items-center gap-2 mb-3">
      <select
        value={filterCategory}
        onChange={(e) => setFilterCategory(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 min-w-[140px]"
      >
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="archived">Archived</option>
        <option value="recycle_bin">Recycle Bin</option>
      </select>

      <select
        value={filterStatus}
        onChange={(e) => setFilterStatus(e.target.value)}
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

      <select
        value={currentFavorite}
        onChange={(e) => setCurrentFavorite(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 min-w-[120px]"
      >
        <option value="all">All Favorites</option>
        <option value="true">Favorites Only</option>
        <option value="false">Non-Favorites</option>
      </select>
    </div>

    <div className="flex items-center gap-2">
      <select
        value={sortBy}
        onChange={(e) => setSortBy(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="updatedAt">Last Updated</option>
        <option value="createdAt">Created Date</option>
        <option value="title">Title</option>
        <option value="clientName">Client Name</option>
        <option value="probability">Probability</option>
        <option value="questionCount">Questions</option>
      </select>
      <button
        className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        aria-label="Sort descending"
      >
        ↑
      </button>

      <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1 ml-auto">
        <button
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
    </div>
  </div>
);

// ============================================
// GRID VIEW - Pure presentation
// ============================================
interface GridViewProps {
  consultations: any[];
  onLoad: (consultation: any) => void;
  onSelect: (id: string) => void;
  selectedItems: Set<string>;
  getOverallProbability: (c: any) => number;
  getActivationPercent: (c: any) => number;
  getCurrentDasha: (c: any) => { md: string; ad: string };
  getTransitGrade: (c: any) => string;
  getOutputCount: (c: any) => number;
}

const GridView: React.FC<GridViewProps> = ({
  consultations,
  onLoad,
  onSelect,
  selectedItems,
  getOverallProbability,
  getActivationPercent,
  getCurrentDasha,
  getTransitGrade,
  getOutputCount,
}) => (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
    {consultations.map(consultation => (
      <ConsultationCard
        key={consultation.id}
        consultation={consultation}
        isSelected={selectedItems.has(consultation.id)}
        onSelect={onSelect}
        onLoad={onLoad}
        getOverallProbability={getOverallProbability}
        getActivationPercent={getActivationPercent}
        getCurrentDasha={getCurrentDasha}
        getTransitGrade={getTransitGrade}
        getOutputCount={getOutputCount}
      />
    ))}
  </div>
);

// ============================================
// LIST VIEW - Pure presentation
// ============================================
interface ListViewProps {
  consultations: any[];
  onLoad: (consultation: any) => void;
  onSelect: (id: string) => void;
  selectedItems: Set<string>;
  getOverallProbability: (c: any) => number;
  getActivationPercent: (c: any) => number;
  getCurrentDasha: (c: any) => { md: string; ad: string };
  getTransitGrade: (c: any) => string;
  getOutputCount: (c: any) => number;
}

const ListView: React.FC<ListViewProps> = ({
  consultations,
  onLoad,
  onSelect,
  selectedItems,
  getOverallProbability,
  getActivationPercent,
  getCurrentDasha,
  getTransitGrade,
  getOutputCount,
}) => (
  <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
    <table className="min-w-full">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-10">
            <input
              type="checkbox"
              className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
          </th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Title</th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Client</th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Dasha</th>
          <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider">Activation</th>
          <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider">Transit</th>
          <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider">Probability</th>
          <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider">Outputs</th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Updated</th>
          <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200">
        {consultations.map(consultation => (
          <ConsultationRow
            key={consultation.id}
            consultation={consultation}
            isSelected={selectedItems.has(consultation.id)}
            onSelect={onSelect}
            onLoad={onLoad}
            getOverallProbability={getOverallProbability}
            getActivationPercent={getActivationPercent}
            getCurrentDasha={getCurrentDasha}
            getTransitGrade={getTransitGrade}
            getOutputCount={getOutputCount}
          />
        ))}
      </tbody>
    </table>
  </div>
);

// ============================================
// CONSULTATION CARD - Pure presentation
// ============================================
interface ConsultationCardProps {
  consultation: any;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onLoad: (consultation: any) => void;
  getOverallProbability: (c: any) => number;
  getActivationPercent: (c: any) => number;
  getCurrentDasha: (c: any) => { md: string; ad: string };
  getTransitGrade: (c: any) => string;
  getOutputCount: (c: any) => number;
}

const ConsultationCard: React.FC<ConsultationCardProps> = ({
  consultation,
  isSelected,
  onSelect,
  onLoad,
  getOverallProbability,
  getActivationPercent,
  getCurrentDasha,
  getTransitGrade,
  getOutputCount,
}) => {
  const prob = getOverallProbability(consultation);
  const activation = getActivationPercent(consultation);
  const dasha = getCurrentDasha(consultation);
  const transitGrade = getTransitGrade(consultation);
  const outputCount = getOutputCount(consultation);

  return (
    <div 
      className={`bg-white rounded-xl border p-4 transition-all ${isSelected ? 'border-indigo-500 ring-2 ring-indigo-200' : 'border-gray-200 hover:border-indigo-300'}`}
      onClick={(e) => { if (e.target === e.currentTarget) onSelect(consultation.id); }}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: consultation.metadata.isFavorite ? '#f59e0b' : '#9ca3af' }} />
          <input
            type="checkbox"
            checked={false}
            onChange={() => onSelect(consultation.id)}
            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
          />
        </div>
        <div className="flex items-center gap-1">
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 rounded hover:bg-gray-100" title="Favorite">
            <Star className={`w-4 h-4 ${consultation.metadata.isFavorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`} />
          </button>
        </div>
      </div>

      <h3 className="font-bold text-gray-900 mb-2 line-clamp-1">{consultation.metadata.consultationTitle}</h3>
      <p className="text-sm text-gray-500 mb-1">{consultation.metadata.clientName}</p>
      <p className="text-xs text-gray-400 mb-2">Created: {new Date(consultation.createdAt).toLocaleDateString()}</p>

      <div className="flex items-center gap-2 mb-3">
        <span className={`px-2 py-0.5 text-xs rounded ${consultation.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : consultation.status === 'in_progress' ? 'bg-amber-100 text-amber-700' : consultation.status === 'archived' ? 'bg-gray-100 text-gray-700' : 'bg-blue-100 text-blue-700'}`}>
          {consultation.status}
        </span>
        <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
          {consultation.structure.selectedQuestionIds.length} Qs
        </span>
        <span className="px-2 py-0.5 text-xs bg-purple-100 text-purple-700 rounded">
          {Math.round(prob)}%
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-3 text-xs">
        <div>
          <span className="text-gray-500">MD:</span>
          <span className="font-medium text-gray-900 ml-1">{dasha.md}</span>
        </div>
        <div>
          <span className="text-gray-500">AD:</span>
          <span className="font-medium text-gray-900 ml-1">{dasha.ad}</span>
        </div>
        <div>
          <span className="text-gray-500">Activation:</span>
          <span className="font-medium text-gray-900 ml-1">{Math.round(activation)}%</span>
        </div>
        <div>
          <span className="text-gray-500">Transit:</span>
          <span className="font-medium text-gray-900 ml-1">{transitGrade}</span>
        </div>
      </div>

      <div className="flex flex-wrap gap-1 mb-3">
        {consultation.metadata.tags.slice(0, 4).map((tag: string) => (
          <span key={tag} className="px-2 py-0.5 text-xs bg-indigo-50 text-indigo-700 rounded">
            {tag}
          </span>
        ))}
        {consultation.metadata.tags.length > 4 && (
          <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-500 rounded">
            +{consultation.metadata.tags.length - 4}
          </span>
        )}
      </div>

      <div className="border-t border-gray-100 pt-3">
        <div className="flex items-center gap-2">
          <button onClick={onLoad} className="flex-1 px-2 py-1 text-sm text-indigo-600 hover:text-indigo-700 font-medium">Open</button>
        </div>
        <div className="flex items-center gap-1 mt-2">
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700" title="Duplicate">Copy</button>
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700" title="Export">Export</button>
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700" title="Print">Print</button>
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700" title="Snapshot">Snap</button>
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-gray-500 hover:text-gray-700" title="Archive">
            <Archive className="w-3.5 h-3.5" />
          </button>
          <button onClick={(e) => { e.stopPropagation(); }} className="px-2 py-1 text-xs text-red-500 hover:text-red-700 ml-auto" title="Delete">
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================
// CONSULTATION ROW - Pure presentation
// ============================================
interface ConsultationRowProps {
  consultation: any;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onLoad: (consultation: any) => void;
  getOverallProbability: (c: any) => number;
  getActivationPercent: (c: any) => number;
  getCurrentDasha: (c: any) => { md: string; ad: string };
  getTransitGrade: (c: any) => string;
  getOutputCount: (c: any) => number;
}

const ConsultationRow: React.FC<ConsultationRowProps> = ({
  consultation,
  isSelected,
  onSelect,
  onLoad,
  getOverallProbability,
  getActivationPercent,
  getCurrentDasha,
  getTransitGrade,
  getOutputCount,
}) => {
  const prob = getOverallProbability(consultation);
  const activation = getActivationPercent(consultation);
  const dasha = getCurrentDasha(consultation);
  const transitGrade = getTransitGrade(consultation);
  const outputCount = getOutputCount(consultation);

  return (
    <tr className={isSelected ? 'bg-blue-50' : 'hover:bg-gray-50'}>
      <td className="px-4 py-3">
        <input
          type="checkbox"
          checked={false}
          onChange={() => onSelect(consultation.id)}
          className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
      </td>
      <td className="px-4 py-3">
        <div className="font-medium text-gray-900">{consultation.metadata.consultationTitle}</div>
        <div className="text-xs text-gray-500 flex flex-wrap gap-1">
          {consultation.metadata.tags.slice(0, 3).map((tag: string) => (
            <span key={tag} className="px-1.5 py-0.5 bg-indigo-50 text-indigo-700 text-xs rounded">{tag}</span>
          ))}
        </div>
      </td>
      <td className="px-4 py-3 text-gray-700">{consultation.metadata.clientName}</td>
      <td className="px-4 py-3 text-center">
        <span className="font-mono text-sm text-gray-900">{dasha.md} / {dasha.ad}</span>
      </td>
      <td className="px-4 py-3 text-center">
        <span className={`font-bold ${activation >= 70 ? 'text-emerald-600' : activation >= 50 ? 'text-amber-600' : 'text-red-600'}`}>
          {Math.round(activation)}%
        </span>
      </td>
      <td className="px-4 py-3 text-center">
        <span className={`px-2 py-0.5 text-xs rounded ${transitGrade === 'EXCELLENT' ? 'bg-emerald-100 text-emerald-700' : transitGrade === 'GOOD' ? 'bg-blue-100 text-blue-700' : transitGrade === 'MODERATE' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-700'}`}>
          {transitGrade}
        </span>
      </td>
      <td className="px-4 py-3 text-center">
        <span className={`font-bold ${prob >= 70 ? 'text-emerald-600' : prob >= 50 ? 'text-amber-600' : 'text-red-600'}`}>
          {Math.round(prob)}%
        </span>
      </td>
      <td className="px-4 py-3 text-center">
        <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{consultation.outputs.length}</span>
      </td>
      <td className="px-4 py-3">
        <span className={`px-2 py-0.5 text-xs rounded ${consultation.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : consultation.status === 'in_progress' ? 'bg-amber-100 text-amber-700' : consultation.status === 'archived' ? 'bg-gray-100 text-gray-700' : 'bg-blue-100 text-blue-700'}`}>
          {consultation.status}
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-gray-500">{new Date(consultation.updatedAt).toLocaleDateString()}</td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-1">
          <button onClick={() => console.log('load', consultation.id)} className="p-1 text-gray-400 hover:text-indigo-600" title="Load"><Eye className="w-4 h-4" /></button>
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 text-gray-400 hover:text-yellow-500" title="Favorite"><Star className={`w-4 h-4 ${consultation.metadata.isFavorite ? 'fill-yellow-400' : ''}`} /></button>
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 text-gray-400 hover:text-blue-600" title="Print"><Eye className="w-4 h-4" /></button>
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 text-gray-400 hover:text-gray-600" title="Duplicate"><Copy className="w-4 h-4" /></button>
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 text-gray-400 hover:text-gray-600" title="Archive"><Archive className="w-4 h-4" /></button>
          <button onClick={(e) => { e.stopPropagation(); }} className="p-1 text-gray-400 hover:text-red-600" title="Delete"><Trash2 className="w-4 h-4" /></button>
        </div>
      </td>
    </tr>
  );
};

export default ConsultationList;