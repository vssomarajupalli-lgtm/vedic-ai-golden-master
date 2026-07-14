// @ts-nocheck
import React, { useState, useMemo } from 'react';
import { 
  Plus, Trash2, 
  Search, 
  FileText, Star, Calendar,
  Eye, Edit, Copy, Download
} from 'lucide-react';

interface ConsultationLibraryProps {
  onLoadConsultation: (consultation: any) => void;
  onNewConsultation: () => void;
}

export const ConsultationLibrary: React.FC<ConsultationLibraryProps> = ({
  onLoadConsultation,
  onNewConsultation
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState<'date' | 'title' | 'questions'>('date');

  // Mock data - in production would come from backend/localStorage
  const consultations = useMemo(() => [
    {
      id: 'cons-001',
      title: 'Marriage Timing Analysis',
      client: 'Priya Sharma',
      birthData: { date: '1992-03-15', time: '14:30', place: 'Mumbai, India' },
      questions: ['marriage_timing', 'marriage_quality', 'spouse_characteristics'],
      questionCount: 8,
      createdAt: '2026-01-15',
      updatedAt: '2026-01-15',
      tags: ['marriage', 'timing', 'relationship'],
      isFavorite: true,
      status: 'completed',
      reportGenerated: true
    },
    {
      id: 'cons-002',
      title: 'Career & Wealth Assessment',
      client: 'Rajesh Kumar',
      birthData: { date: '1985-07-22', time: '09:15', place: 'Delhi, India' },
      questions: ['career_promise', 'wealth_accumulation', 'business_partnership'],
      questionCount: 12,
      createdAt: '2026-01-10',
      updatedAt: '2026-01-12',
      tags: ['career', 'wealth', 'business'],
      isFavorite: false,
      status: 'completed',
      reportGenerated: true
    },
    {
      id: 'cons-003',
      title: 'Health & Longevity Consultation',
      client: 'Sunita Devi',
      birthData: { date: '1978-11-03', time: '18:45', place: 'Kolkata, India' },
      questions: ['health_promise', 'longevity', 'chronic_conditions'],
      questionCount: 6,
      createdAt: '2026-01-08',
      updatedAt: '2026-01-08',
      tags: ['health', 'longevity'],
      isFavorite: true,
      status: 'draft',
      reportGenerated: false
    },
    {
      id: 'cons-004',
      title: 'Property Purchase Timing',
      client: 'Amit Patel',
      birthData: { date: '1990-01-20', time: '11:20', place: 'Ahmedabad, India' },
      questions: ['property_timing', 'property_type', 'investment_return'],
      questionCount: 5,
      createdAt: '2026-01-05',
      updatedAt: '2026-01-06',
      tags: ['property', 'timing', 'investment'],
      isFavorite: false,
      status: 'completed',
      reportGenerated: true
    },
    {
      id: 'cons-005',
      title: 'Complete Horoscope Analysis',
      client: 'Meera Singh',
      birthData: { date: '1995-09-12', time: '06:30', place: 'Bangalore, India' },
      questions: Array.from({ length: 83 }, (_, i) => `q_${i + 1}`),
      questionCount: 83,
      createdAt: '2026-01-01',
      updatedAt: '2026-01-03',
      tags: ['complete', 'all-domains'],
      isFavorite: true,
      status: 'in_progress',
      reportGenerated: false
    }
  ], []);

  const filteredConsultations = consultations
    .filter(c => {
      const matchesSearch = c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.client.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.tags.some((tag: string) => tag.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesCategory = filterCategory === 'all' || 
        (filterCategory === 'favorites' && c.isFavorite) ||
        (filterCategory === 'completed' && c.status === 'completed') ||
        (filterCategory === 'draft' && c.status === 'draft') ||
        (filterCategory === 'in_progress' && c.status === 'in_progress');
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      if (sortBy === 'date') return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      return b.questionCount - a.questionCount;
    });

  const toggleSelection = (id: string) => {
    setSelectedItems(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectAll = () => {
    setSelectedItems(new Set(filteredConsultations.map(c => c.id)));
  };

  const clearSelection = () => {
    setSelectedItems(new Set());
  };

  const bulkAction = (action: 'favorite' | 'duplicate' | 'delete' | 'export') => {
    console.log(`Bulk ${action}:`, Array.from(selectedItems));
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-gray-800">Consultation Library</h1>
            <span className="px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
              {consultations.length} consultations
            </span>
          </div>
          <button onClick={onNewConsultation} className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 flex items-center gap-2">
            <Plus className="w-4 h-4" />
            New Consultation
          </button>
        </div>

        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-[250px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search consultations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="all">All</option>
            <option value="favorites">Favorites</option>
            <option value="completed">Completed</option>
            <option value="in_progress">In Progress</option>
            <option value="draft">Draft</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="date">Sort by Date</option>
            <option value="title">Sort by Title</option>
            <option value="questions">Sort by Questions</option>
          </select>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded ${viewMode === 'grid' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:bg-gray-100'}`}
            >
              <div className="w-5 h-5 flex flex-col justify-between">
                <div className="h-1 bg-current rounded"></div>
                <div className="h-1 bg-current rounded"></div>
                <div className="h-1 bg-current rounded"></div>
              </div>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded ${viewMode === 'list' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:bg-gray-100'}`}
            >
              <div className="w-5 h-5 flex flex-col justify-between">
                <div className="h-1.5 bg-current rounded w-full"></div>
                <div className="h-1.5 bg-current rounded w-full"></div>
                <div className="h-1.5 bg-current rounded w-full"></div>
              </div>
            </button>
          </div>
        </div>
      </div>

      {selectedItems.size > 0 && (
        <div className="p-4 bg-blue-50 border-b border-blue-200 flex items-center justify-between">
          <span className="text-sm text-blue-800">
            {selectedItems.size} selected
          </span>
          <div className="flex items-center gap-2">
            <button onClick={() => bulkAction('favorite')} className="px-3 py-1 text-sm bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50">Favorite</button>
            <button onClick={() => bulkAction('duplicate')} className="px-3 py-1 text-sm bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50">Duplicate</button>
            <button onClick={() => bulkAction('export')} className="px-3 py-1 text-sm bg-white border border-blue-300 text-blue-700 rounded hover:bg-blue-50">Export</button>
            <button onClick={() => bulkAction('delete')} className="px-3 py-1 text-sm bg-white border border-red-300 text-red-700 rounded hover:bg-red-50">Delete</button>
            <button onClick={clearSelection} className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700">Clear</button>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-auto p-4">
        {filteredConsultations.length === 0 ? (
          <div className="text-center py-16">
            <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No consultations found</h3>
            <p className="text-gray-500 mb-6">Create your first consultation or adjust your filters</p>
            <button onClick={onNewConsultation} className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Create Consultation
            </button>
          </div>
        ) : (
          viewMode === 'grid' ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filteredConsultations.map(consultation => (
                <ConsultationCard
                  key={consultation.id}
                  consultation={consultation}
                  isSelected={selectedItems.has(consultation.id)}
                  onSelect={toggleSelection}
                  onLoad={() => onLoadConsultation(consultation)}
                  onFavorite={() => console.log('Toggle favorite:', consultation.id)}
                />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-10">
                      <input
                        type="checkbox"
                        checked={selectedItems.size === filteredConsultations.length && filteredConsultations.length > 0}
                        onChange={selectedItems.size === filteredConsultations.length ? clearSelection : selectAll}
                        className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Title</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Client</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Questions</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Updated</th>
                    <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredConsultations.map(consultation => (
                    <tr key={consultation.id} className={selectedItems.has(consultation.id) ? 'bg-blue-50' : 'hover:bg-gray-50'}>
                      <td className="px-4 py-3">
                        <input
                          type="checkbox"
                          checked={selectedItems.has(consultation.id)}
                          onChange={() => toggleSelection(consultation.id)}
                          className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <div className="font-medium text-gray-900">{consultation.title}</div>
                        <div className="text-sm text-gray-500 flex flex-wrap gap-1">
                          {consultation.tags.map((tag: string) => (
                            <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">{tag}</span>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-gray-700">{consultation.client}</td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-sm font-medium">
                          {consultation.questionCount} questions
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          consultation.status === 'completed' ? 'bg-green-100 text-green-800' :
                          consultation.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {consultation.status.replace('_', ' ')}
                        </span>
                        {consultation.reportGenerated && (
                          <span className="ml-1 px-1.5 py-0.5 bg-amber-100 text-amber-800 rounded text-[10px] font-medium">PDF</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {new Date(consultation.updatedAt).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1">
                          <button onClick={() => onLoadConsultation(consultation)} className="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded" title="Load">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button onClick={() => console.log('Edit:', consultation.id)} className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded" title="Edit">
                            <Edit className="w-4 h-4" />
                          </button>
                          <button onClick={() => console.log('Duplicate:', consultation.id)} className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded" title="Duplicate">
                            <Copy className="w-4 h-4" />
                          </button>
                          <button onClick={() => console.log('Delete:', consultation.id)} className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded" title="Delete">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )
        )}
      </div>
    </div>
  );
};

interface ConsultationCardProps {
  consultation: any;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onLoad: () => void;
  onFavorite: () => void;
}

const ConsultationCard: React.FC<ConsultationCardProps> = ({
  consultation,
  isSelected,
  onSelect,
  onLoad,
  onFavorite
}) => (
  <div
    className={`relative bg-white rounded-xl border shadow-sm transition-all ${
      isSelected ? 'ring-2 ring-indigo-500 border-indigo-500' : 'border-gray-200 hover:border-indigo-300 hover:shadow-md'
    }`}
    onClick={() => onSelect(consultation.id)}
  >
    <div className="absolute top-3 right-3 flex flex-col gap-1">
      <button
        onClick={(e) => { e.stopPropagation(); onFavorite(); }}
        className={`p-1.5 rounded-full ${consultation.isFavorite ? 'text-amber-500 bg-amber-50' : 'text-gray-400 bg-gray-50 hover:text-amber-500'}`}
      >
        <Star className={`w-4 h-4 ${consultation.isFavorite ? 'fill-current' : ''}`} />
      </button>
      <input
        type="checkbox"
        checked={isSelected}
        onChange={(e) => { e.stopPropagation(); onSelect(consultation.id); }}
        className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
      />
    </div>

    <div className="p-4">
      <div className="flex items-start justify-between mb-3">
        <span className={`px-2 py-0.5 rounded text-xs font-medium ${
          consultation.status === 'completed' ? 'bg-green-100 text-green-800' :
          consultation.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {consultation.status.replace('_', ' ')}
        </span>
      </div>

      <h3 className="font-bold text-gray-900 mb-2 line-clamp-2">{consultation.title}</h3>
      
      <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
        <span className="flex items-center gap-1">
          <FileText className="w-3.5 h-3.5" />
          {consultation.questionCount} questions
        </span>
        <span className="flex items-center gap-1">
          <Calendar className="w-3.5 h-3.5" />
          {new Date(consultation.updatedAt).toLocaleDateString()}
        </span>
      </div>

      <div className="flex flex-wrap gap-1 mb-4">
        {consultation.tags.slice(0, 4).map(tag => (
          <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">{tag}</span>
        ))}
        {consultation.tags.length > 4 && (
          <span className="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs">
            +{consultation.tags.length - 4}
          </span>
        )}
      </div>

      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <span>Client:</span>
          <span className="font-medium text-gray-700">{consultation.client}</span>
        </div>
        {consultation.reportGenerated && (
          <span className="px-2 py-0.5 bg-amber-100 text-amber-800 rounded text-xs font-medium flex items-center gap-1">
            <Download className="w-3 h-3" />
            PDF
          </span>
        )}
      </div>
    </div>

    <div className="px-4 pb-4 border-t border-gray-100">
      <button
        onClick={(e) => { e.stopPropagation(); onLoad(); }}
        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium flex items-center justify-center gap-2"
      >
        <Eye className="w-4 h-4" />
        Load Consultation
      </button>
    </div>
  </div>
);

export default ConsultationLibrary;
