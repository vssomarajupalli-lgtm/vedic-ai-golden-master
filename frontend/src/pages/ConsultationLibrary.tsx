import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, Filter, Tag, 
  Plus, Database, FileText
} from 'lucide-react';
import { ConsultationList } from '../components/consultation/ConsultationList.tsx';
import { useConsultationStore } from '../store/useConsultationStore.ts';
import type { Consultation } from '../types/consultation.ts';

interface SearchFiltersLocal {
  text: string;
  status: '' | 'active' | 'completed' | 'draft' | 'archived';
  tags: string[];
  dateFrom: string;
  dateTo: string;
};

export default function ConsultationLibrary() {
  const navigate = useNavigate();
  const {
    consultations,
    searchFilters,
    setSearchFilters,
    getAllTags,
  } = useConsultationStore();
  
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  const [localFilters, setLocalFilters] = useState<SearchFiltersLocal>({
    text: searchFilters.text || '',
    status: searchFilters.status || '',
    tags: searchFilters.tags || [],
    dateFrom: searchFilters.dateFrom || '',
    dateTo: searchFilters.dateTo || '',
  });
  const [creating, setCreating] = useState(false);
  const [newConsultationName, setNewConsultationName] = useState('');
  
  const allTags = useMemo(() => getAllTags(), [consultations, getAllTags]);
  
  const filteredConsultations = useConsultationStore((s: { getFilteredConsultations: () => Consultation[] }) => s.getFilteredConsultations());
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const text = e.target.value;
    setLocalFilters(prev => ({ ...prev, text }));
    setSearchFilters({ ...searchFilters, text });
  };
  
  const handleTagToggle = (tag: string) => {
    setLocalFilters((prev: SearchFiltersLocal) => {
      const tags = prev.tags.includes(tag) 
        ? prev.tags.filter(t => t !== tag)
        : [...prev.tags, tag];
      return { ...prev, tags };
    });
    const tags = searchFilters.tags?.includes(tag)
      ? searchFilters.tags.filter((t: string) => t !== tag)
      : [...(searchFilters.tags || []), tag];
    setSearchFilters({ ...searchFilters, tags });
  };
  
  const handleDateChange = (field: 'dateFrom' | 'dateTo', value: string) => {
    setLocalFilters((prev: SearchFiltersLocal) => ({ ...prev, [field]: value }));
    setSearchFilters({ ...searchFilters, [field]: value });
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
  
  const handleCreate = async () => {
    if (!newConsultationName.trim()) return;
    
    setCreating(true);
    try {
      const { createConsultation } = useConsultationStore.getState();
      const newConsultation = await createConsultation({
        clientId: 'new',
        name: newConsultationName.trim(),
        client: { name: '' },
        status: 'draft',
      });
      setNewConsultationName('');
      setCreating(false);
      navigate(`/consultation/${newConsultation.id}`);
    } catch (err) {
      console.error(err);
      setCreating(false);
    }
  };
  
  return (
    <div className="max-w-7xl mx-auto pb-24 relative min-h-[80vh]">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
        <div className="bg-indigo-600 p-6 text-white">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold mb-1 flex items-center gap-2">
                <Database className="w-6 h-6" /> Consultation Library
              </h1>
              <p className="text-indigo-100">
                Manage all your astrological consultations with full search, filter, and persistence.
              </p>
            </div>
            <button
              onClick={() => setCreating(true)}
              className="px-6 py-3 bg-white text-indigo-600 font-bold rounded-lg hover:bg-indigo-50 transition-colors flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              New Consultation
            </button>
          </div>
        </div>
        
        {/* Search & Filter Bar */}
        <div className="p-4 border-b border-slate-100">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center">
            {/* Search */}
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                value={localFilters.text}
                onChange={handleSearchChange}
                placeholder="Search consultations by name, notes, or tags..."
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            
            {/* Status Filter */}
            <select
              value={localFilters.status}
              onChange={(e) => {
                const status = e.target.value as SearchFiltersLocal['status'];
                setLocalFilters(prev => ({ ...prev, status }));
                setSearchFilters({ ...searchFilters, status: status === '' ? undefined : status });
              }}
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
                {allTags.map((tag: string) => (
                  <option key={tag} value={tag}>
                    {tag} {localFilters.tags.includes(tag) ? '✓' : ''}
                  </option>
                ))}
              </select>
              {localFilters.tags.length > 0 && (
                <div className="absolute right-8 top-1/2 -translate-y-1/2 flex gap-1">
                  {localFilters.tags.map((tag: string) => (
                    <span key={tag} className="px-2 py-0.5 text-xs bg-indigo-100 text-indigo-700 rounded-full flex items-center gap-1">
                      {tag}
                      <button onClick={(e) => { e.stopPropagation(); handleTagToggle(tag); }} className="hover:text-indigo-900">×</button>
                    </span>
                  ))}
                </div>
              )}
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
      </div>
      
      {/* Create Modal */}
      {creating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 animate-in fade-in">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4 animate-in slide-in-from-bottom">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Create New Consultation</h2>
            <input
              type="text"
              value={newConsultationName}
              onChange={(e) => setNewConsultationName(e.target.value)}
              placeholder="Consultation name"
              className="w-full px-4 py-2 border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
              autoFocus
            />
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => { setCreating(false); setNewConsultationName(''); }}
                className="px-4 py-2 text-slate-600 hover:text-slate-900 border border-slate-300 rounded-lg hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={!newConsultationName.trim() || creating}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                {creating ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Results */}
      {consultations.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
          <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="w-6 h-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-medium text-slate-900 mb-1">
            No consultations yet
          </h3>
          <p className="text-slate-500 mb-6">
            Create your first consultation to get started
          </p>
          <button
            onClick={() => setCreating(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            <Plus className="w-5 h-5" />
            Create Consultation
          </button>
        </div>
      ) : (
        <>
          <div className="mb-4 text-sm text-slate-500 text-center">
            Showing {filteredConsultations.length} of {consultations.length} consultation{consultations.length !== 1 ? 's' : ''}
          </div>
          <ConsultationList
            onSelect={(c: Consultation) => navigate(`/consultation/${c.id}`)}
            showActions={true}
          />
        </>
      )}
    </div>
  );
}