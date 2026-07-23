import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, Filter, 
  MoreVertical, Pin, Archive, Copy, Trash2,
  Calendar, Tag, Clock, Eye, Plus
} from 'lucide-react';
import { useConsultationStore } from '../../store/useConsultationStore';
import type { Consultation, ConsultationSearchFilters, ConsultationStatus, ViewMode } from '../../types/consultation';

interface SearchFiltersLocal {
  text: string;
  status: ConsultationStatus | '';
  tags: string[];
  dateFrom: string;
  dateTo: string;
}

export const ConsultationList: React.FC<{
  onSelect?: (consultation: Consultation) => void;
  showActions?: boolean;
  className?: string;
  consultations?: Consultation[];
  searchFilters?: ConsultationSearchFilters;
  viewMode?: ViewMode;
  selectedConsultationId?: string | null;
  setSearchFilters?: (filters: Partial<ConsultationSearchFilters>) => void;
  setViewMode?: (mode: ViewMode) => void;
  archiveConsultation?: (id: string) => void;
  duplicateConsultation?: (id: string) => Consultation;
  deleteConsultation?: (id: string) => void;
  getAllTags?: () => string[];
}> = ({ 
  onSelect, 
  showActions = true, 
  className = '',
  consultations: externalConsultations,
  searchFilters: externalSearchFilters,
  viewMode: externalViewMode,
  selectedConsultationId: externalSelectedConsultationId,
  setSearchFilters: externalSetSearchFilters,
  setViewMode: externalSetViewMode,
  archiveConsultation: externalArchiveConsultation,
  duplicateConsultation: externalDuplicateConsultation,
  deleteConsultation: externalDeleteConsultation,
  getAllTags: externalGetAllTags,
} = {}) => {
  const navigate = useNavigate();
  const {
    consultations: storeConsultations,
    searchFilters: storeSearchFilters,
    viewMode: storeViewMode,
    selectedConsultationId: storeSelectedConsultationId,
    setSearchFilters: storeSetSearchFilters,
    setViewMode: storeSetViewMode,
    archiveConsultation: storeArchiveConsultation,
    duplicateConsultation: storeDuplicateConsultation,
    deleteConsultation: storeDeleteConsultation,
    getAllTags: storeGetAllTags,
  } = useConsultationStore();

  // Use external props if provided, otherwise use store
  const consultations = externalConsultations ?? storeConsultations;
  const searchFilters = externalSearchFilters ?? storeSearchFilters;
  const viewMode = externalViewMode ?? storeViewMode;
  const selectedConsultationId = externalSelectedConsultationId ?? storeSelectedConsultationId;
  const setSearchFilters = externalSetSearchFilters ?? storeSetSearchFilters;
  const setViewMode = externalSetViewMode ?? storeSetViewMode;
  const archiveConsultation = externalArchiveConsultation ?? storeArchiveConsultation;
  const duplicateConsultation = externalDuplicateConsultation ?? storeDuplicateConsultation;
  const deleteConsultation = externalDeleteConsultation ?? storeDeleteConsultation;
  const getAllTags = externalGetAllTags ?? storeGetAllTags;

  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  const [localFilters, setLocalFilters] = useState<SearchFiltersLocal>({
    text: searchFilters.text || '',
    status: searchFilters.status || '',
    tags: searchFilters.tags || [],
    dateFrom: searchFilters.dateFrom || '',
    dateTo: searchFilters.dateTo || '',
  });
  
  const allTags = getAllTags();
  
  const getFilteredConsultations = useConsultationStore(s => s.getFilteredConsultations);
  const filteredConsultations = getFilteredConsultations();
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const text = e.target.value;
    setLocalFilters(prev => ({ ...prev, text }));
    setSearchFilters({ ...searchFilters, text });
  };
  
  const handleStatusChange = (status: SearchFiltersLocal['status']) => {
    setLocalFilters(prev => ({ ...prev, status }));
    setSearchFilters({ ...searchFilters, status: status || undefined });
  };
  
  const handleTagToggle = (tag: string) => {
    setLocalFilters(prev => {
      const tags = prev.tags.includes(tag) 
        ? prev.tags.filter(t => t !== tag)
        : [...prev.tags, tag];
      return { ...prev, tags };
    });
    setSearchFilters({
      ...searchFilters,
      tags: searchFilters.tags?.includes(tag)
        ? searchFilters.tags!.filter(t => t !== tag)
        : [...(searchFilters.tags || []), tag]
    });
  };
  
  const handleDateChange = (field: 'dateFrom' | 'dateTo', value: string) => {
    setLocalFilters(prev => ({ ...prev, [field]: value }));
    setSearchFilters({ ...searchFilters, [field]: value || undefined });
  };
  
  const clearFilters = () => {
    const emptyFilters: SearchFiltersLocal = {
      text: '',
      status: '',
      tags: [],
      dateFrom: '',
      dateTo: '',
    };
    setLocalFilters(emptyFilters);
    setSearchFilters({});
  };
  
  const hasActiveFilters = searchFilters.text || searchFilters.status || 
    (searchFilters.tags && searchFilters.tags.length > 0) || searchFilters.dateFrom || searchFilters.dateTo;
  
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };
  
  const getStatusBadge = (status: Consultation['status']) => {
    switch (status) {
      case 'active':
        return <span className="px-2 py-0.5 text-xs font-medium bg-emerald-100 text-emerald-800 rounded-full">Active</span>;
      case 'completed':
        return <span className="px-2 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-800 rounded-full">Completed</span>;
      case 'archived':
        return <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 text-slate-800 rounded-full">Archived</span>;
      case 'draft':
        return <span className="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-800 rounded-full">Draft</span>;
      default:
        return <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 text-slate-800 rounded-full">{status}</span>;
    }
  };
  
  const renderGridItem = (consultation: Consultation) => (
    <div
      key={consultation.id}
      onClick={() => {
        if (onSelect) onSelect(consultation);
        else navigate(`/consultation/${consultation.id}`);
      }}
      className={`group bg-white rounded-xl border shadow-sm transition-all hover:shadow-md ${
        selectedConsultationId === consultation.id 
          ? 'ring-2 ring-indigo-500 border-indigo-500' 
          : 'border-slate-200 hover:border-indigo-300'
      } ${showActions ? 'cursor-pointer' : ''}`}
    >
      <div className="p-5">
        <div className="flex items-start justify-between mb-3">
          <h3 className="font-semibold text-slate-900 text-lg line-clamp-1">
            {consultation.name}
          </h3>
          <div className="flex items-center gap-1">
            {consultation.isPinned && (
              <Pin className="w-4 h-4 text-amber-500" />
            )}
            {consultation.status === 'archived' && (
              <Archive className="w-4 h-4 text-slate-400" />
            )}
          </div>
        </div>
        
        {consultation.client?.name && (
          <p className="text-sm text-slate-500 mb-2 flex items-center gap-1">
            <span>👤</span>
            {consultation.client.name}
          </p>
        )}
        
        <div className="flex flex-wrap gap-1.5 mb-3">
          {getStatusBadge(consultation.status)}
          {consultation.tags.slice(0, 3).map(tag => (
            <span key={tag} className="px-2 py-0.5 text-xs bg-slate-100 text-slate-600 rounded-full">
              {tag}
            </span>
          ))}
          {consultation.tags.length > 3 && (
            <span className="px-2 py-0.5 text-xs bg-slate-100 text-slate-500 rounded-full">
              +{consultation.tags.length - 3}
            </span>
          )}
        </div>
        
        <div className="text-xs text-slate-400 flex items-center gap-2">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            Updated {formatDate(consultation.updatedAt)}
          </span>
          {consultation.lastOpenedAt && (
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              Opened {formatDate(consultation.lastOpenedAt)}
            </span>
          )}
        </div>
      </div>
      
      {showActions && (
        <div className="border-t border-slate-100 px-3 py-2 bg-slate-50 rounded-b-xl">
          <div className="flex items-center justify-between">
            <div className="flex gap-1">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/consultation/${consultation.id}`);
                }}
                className="p-2 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                title="Open Consultation"
              >
                <Eye className="w-4 h-4" />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  duplicateConsultation(consultation.id);
                }}
                className="p-2 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                title="Duplicate"
              >
                <Copy className="w-4 h-4" />
              </button>
            </div>
            <div className="relative">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setExpandedId(expandedId === consultation.id ? null : consultation.id);
                }}
                className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-200 rounded-lg transition-colors"
              >
                <MoreVertical className="w-4 h-4" />
              </button>
              {expandedId === consultation.id && (
                <div className="absolute right-0 top-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-10 min-w-[140px]">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/consultation/${consultation.id}`);
                      setExpandedId(null);
                    }}
                    className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                  >
                    <Eye className="w-4 h-4" /> Open
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      duplicateConsultation(consultation.id);
                      setExpandedId(null);
                    }}
                    className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                  >
                    <Copy className="w-4 h-4" /> Duplicate
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      archiveConsultation(consultation.id);
                      setExpandedId(null);
                    }}
                    className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                  >
                    <Archive className="w-4 h-4" /> Archive
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm('Delete this consultation? This cannot be undone.')) {
                        deleteConsultation(consultation.id);
                      }
                      setExpandedId(null);
                    }}
                    className="w-full px-3 py-2 text-left text-sm text-rose-600 hover:bg-rose-50 flex items-center gap-2"
                  >
                    <Trash2 className="w-4 h-4" /> Delete
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
  
  const renderListItem = (consultation: Consultation) => (
    <div
      key={consultation.id}
      onClick={() => {
        if (onSelect) onSelect(consultation);
        else navigate(`/consultation/${consultation.id}`);
      }}
      className={`group flex items-center gap-4 p-4 bg-white rounded-lg border shadow-sm transition-all ${
        selectedConsultationId === consultation.id 
          ? 'ring-2 ring-indigo-500 border-indigo-500' 
          : 'border-slate-200 hover:border-indigo-300 hover:bg-slate-50'
      } ${showActions ? 'cursor-pointer' : ''}`}
    >
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="font-medium text-slate-900 truncate">{consultation.name}</h3>
          {getStatusBadge(consultation.status)}
          {consultation.isPinned && <Pin className="w-4 h-4 text-amber-500" />}
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-500">
          {consultation.client?.name && (
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5" />
              {consultation.client.name}
            </span>
          )}
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            Updated {formatDate(consultation.updatedAt)}
          </span>
          <span className="flex items-center gap-1 flex-wrap">
            <Tag className="w-3.5 h-3.5" />
            {consultation.tags.slice(0, 2).join(', ')}
            {consultation.tags.length > 2 && <span>+{consultation.tags.length - 2}</span>}
          </span>
        </div>
      </div>
      
      {showActions && (
        <div className="flex items-center gap-1 ml-4">
          <button
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/consultation/${consultation.id}`);
            }}
            className="p-2 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
            title="Open"
          >
            <Eye className="w-4 h-4" />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              duplicateConsultation(consultation.id);
            }}
            className="p-2 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
            title="Duplicate"
          >
            <Copy className="w-4 h-4" />
          </button>
          <div className="relative">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setExpandedId(expandedId === consultation.id ? null : consultation.id);
              }}
              className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-200 rounded-lg transition-colors"
            >
              <MoreVertical className="w-4 h-4" />
            </button>
            {expandedId === consultation.id && (
              <div className="absolute right-0 top-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-10 min-w-[140px]">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/consultation/${consultation.id}`);
                    setExpandedId(null);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                >
                  <Eye className="w-4 h-4" /> Open
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    duplicateConsultation(consultation.id);
                    setExpandedId(null);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                >
                  <Copy className="w-4 h-4" /> Duplicate
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    archiveConsultation(consultation.id);
                    setExpandedId(null);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                >
                  <Archive className="w-4 h-4" /> Archive
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Delete this consultation? This cannot be undone.')) {
                      deleteConsultation(consultation.id);
                    }
                    setExpandedId(null);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-rose-600 hover:bg-rose-50 flex items-center gap-2"
                >
                  <Trash2 className="w-4 h-4" /> Delete
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
  
  if (filteredConsultations.length === 0) {
    return (
      <div className={className}>
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
          <Calendar className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-1">
            {consultations.length === 0 ? 'No consultations yet' : 'No consultations match your filters'}
          </h3>
          <p className="text-slate-500 mb-6">
            {consultations.length === 0 
              ? 'Create your first consultation to get started'
              : 'Try adjusting your search or filters'}
          </p>
          {consultations.length === 0 && (
            <button
              onClick={() => navigate('/upload')}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              <Plus className="w-5 h-5" />
              Create Consultation
            </button>
          )}
          {hasActiveFilters && (
            <button 
              onClick={clearFilters}
              className="mt-4 text-sm text-indigo-600 hover:text-indigo-800 underline"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>
    );
  }
  
  return (
    <div className={className}>
      {/* Search & Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 mb-4 shadow-sm">
        <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              value={localFilters.text}
              onChange={handleSearchChange}
              placeholder="Search consultations..."
              className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          
          {/* Status Filter */}
          <select
            value={localFilters.status}
            onChange={(e) => handleStatusChange(e.target.value as SearchFiltersLocal['status'])}
            className="px-4 py-2 border border-slate-300 rounded-lg text-slate-900 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[160px]"
          >
            <option value="">All Statuses</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
            <option value="draft">Draft</option>
            <option value="archived">Archived</option>
          </select>
          
          {/* Tag Filter */}
          <div className="relative flex-1 min-w-[180px] max-w-[280px]">
            <Tag className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <select
              value=""
              onChange={(e) => { if (e.target.value) handleTagToggle(e.target.value); e.target.value = ''; }}
              className="w-full pl-10 pr-8 py-2 border border-slate-300 rounded-lg text-slate-900 bg-white appearance-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="" disabled>Filter by tag...</option>
              {allTags.map(tag => (
                <option key={tag} value={tag}>
                  {tag} {localFilters.tags.includes(tag) ? '✓' : ''}
                </option>
              ))}
            </select>
            {localFilters.tags.length > 0 && (
              <div className="absolute right-8 top-1/2 -translate-y-1/2 flex gap-1">
                {localFilters.tags.map(tag => (
                  <span key={tag} className="px-2 py-0.5 text-xs bg-indigo-100 text-indigo-700 rounded-full flex items-center gap-1">
                    {tag}
                    <button onClick={(e) => { e.stopPropagation(); handleTagToggle(tag); }} className="hover:text-indigo-900">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>
          
          {/* View Toggle */}
          <div className="flex items-center gap-1 bg-slate-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded transition-colors ${viewMode === 'grid' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              title="Grid View"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <rect x="3" y="3" width="7" height="7" rx="1" strokeWidth="2" />
                <rect x="14" y="3" width="7" height="7" rx="1" strokeWidth="2" />
                <rect x="3" y="14" width="7" height="7" rx="1" strokeWidth="2" />
                <rect x="14" y="14" width="7" height="7" rx="1" strokeWidth="2" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded transition-colors ${viewMode === 'list' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              title="List View"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <line x1="4" y1="6" x2="20" y2="6" strokeWidth="2" strokeLinecap="round" />
                <line x1="4" y1="12" x2="20" y2="12" strokeWidth="2" strokeLinecap="round" />
                <line x1="4" y1="18" x2="20" y2="18" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </div>
          
          {/* Advanced Filters Toggle */}
          <button
            onClick={() => setShowFilterPanel(!showFilterPanel)}
            className={`p-2 rounded-lg transition-colors ${showFilterPanel || hasActiveFilters ? 'bg-indigo-50 text-indigo-600' : 'text-slate-500 hover:bg-slate-100'}`}
            title={showFilterPanel ? 'Hide filters' : 'Show advanced filters'}
          >
            <Filter className="w-5 h-5" />
            {hasActiveFilters && <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-white text-[10px] rounded-full flex items-center justify-center">•</span>}
          </button>
        </div>
        
        {/* Advanced Filter Panel */}
        {showFilterPanel && (
          <div className="mt-4 pt-4 border-t border-slate-100 animate-in slide-in-from-top duration-200">
            <div className="flex flex-wrap gap-4 items-end">
              <div className="flex-1 min-w-[200px]">
                <label className="block text-xs font-medium text-slate-500 mb-1">From Date</label>
                <input
                  type="date"
                  value={localFilters.dateFrom}
                  onChange={(e) => handleDateChange('dateFrom', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div className="flex-1 min-w-[200px]">
                <label className="block text-xs font-medium text-slate-500 mb-1">To Date</label>
                <input
                  type="date"
                  value={localFilters.dateTo}
                  onChange={(e) => handleDateChange('dateTo', e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <button
                onClick={clearFilters}
                className="px-4 py-2 text-sm text-slate-600 hover:text-slate-900 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
              >
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>
      
      {/* Results */}
      <div className="space-y-3">
        {viewMode === 'grid' ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filteredConsultations.map(renderGridItem)}
          </div>
        ) : (
          <div className="space-y-2">
            {filteredConsultations.map(renderListItem)}
          </div>
        )}
      </div>
      
      {/* Results Count */}
      <div className="mt-4 text-sm text-slate-500 text-center">
        Showing {filteredConsultations.length} of {consultations.length} consultation{consultations.length !== 1 ? 's' : ''}
      </div>
    </div>
  );
};

export default ConsultationList;