import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Heart, Clock, ChevronDown, ChevronRight, MessageCircle, AlertCircle } from 'lucide-react';
import { apiService } from '../api/backend';
import { useChartStore } from '../store/useChartStore';

interface Question {
  question_id: string;
  domain_id: number;
  domain_name: string;
  question_name: string;
}

export default function QuestionBrowser() {
  const navigate = useNavigate();
  const { rawOutputs } = useChartStore();
  
  const [registry, setRegistry] = useState<Question[]>([]);
  const [favorites, setFavorites] = useState<Question[]>([]);
  const [recents, setRecents] = useState<Question[]>([]);
  
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'browse' | 'favorites' | 'recent'>('browse');
  const [expandedDomains, setExpandedDomains] = useState<number[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [regData, favData, recData] = await Promise.all([
          apiService.fetchRegistry(),
          apiService.fetchFavorites(),
          apiService.fetchRecents()
        ]);
        setRegistry(regData);
        setFavorites(favData);
        setRecents(recData);
      } catch (err: any) {
        setError('Failed to load question registry data. Ensure backend is running.');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setExpandedDomains([]);
      return;
    }
    
    try {
      const result = await apiService.searchQuestions(searchQuery);
      if (result.status === 'success' && result.matched_domain_id) {
        setExpandedDomains([result.matched_domain_id]);
        setActiveTab('browse');
      }
    } catch (err: any) {
      // Ignore or show small toast
    }
  };

  const toggleFavorite = async (e: React.MouseEvent, question: Question) => {
    e.stopPropagation();
    const isFav = favorites.some(f => f.question_id === question.question_id);
    try {
      if (isFav) {
        await apiService.removeFavorite(question.question_id);
        setFavorites(favorites.filter(f => f.question_id !== question.question_id));
      } else {
        const newFav = await apiService.addFavorite(question.question_id);
        setFavorites([...favorites, newFav]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const groupedByDomain = useMemo(() => {
    const groups: Record<number, { domain_name: string, questions: Question[] }> = {};
    registry.forEach(q => {
      if (!groups[q.domain_id]) {
        groups[q.domain_id] = { domain_name: q.domain_name, questions: [] };
      }
      groups[q.domain_id].questions.push(q);
    });
    return Object.entries(groups).sort((a, b) => Number(a[0]) - Number(b[0]));
  }, [registry]);

  const toggleDomain = (domainId: number) => {
    setExpandedDomains(prev => 
      prev.includes(domainId) ? prev.filter(id => id !== domainId) : [...prev, domainId]
    );
  };

  const handleAsk = () => {
    if (!selectedQuestion) return;
    navigate('/engine', {
      state: {
        initialQuestionId: selectedQuestion.question_id,
        initialQuestionText: selectedQuestion.question_name
      }
    });
  };

  if (loading) {
    return <div className="p-10 text-center">Loading Question Registry...</div>;
  }

  if (error) {
    return (
      <div className="p-10 text-center text-red-600">
        <AlertCircle className="mx-auto h-10 w-10 mb-2" />
        {error}
      </div>
    );
  }

  const renderQuestionList = (questions: Question[]) => (
    <div className="space-y-2">
      {questions.length === 0 && <p className="text-slate-500 italic p-4 text-center">No questions found.</p>}
      {questions.map(q => {
        const isSelected = selectedQuestion?.question_id === q.question_id;
        const isFav = favorites.some(f => f.question_id === q.question_id);
        
        return (
          <div 
            key={q.question_id}
            onClick={() => setSelectedQuestion(q)}
            className={`p-4 rounded-lg border cursor-pointer transition-colors flex justify-between items-center ${
              isSelected 
                ? 'bg-indigo-50 border-indigo-500 ring-1 ring-indigo-500' 
                : 'bg-white border-slate-200 hover:border-indigo-300'
            }`}
          >
            <div>
              <div className="text-xs text-indigo-600 font-semibold mb-1">ID: {q.question_id}</div>
              <div className={`font-medium ${isSelected ? 'text-indigo-900' : 'text-slate-800'}`}>
                {q.question_name}
              </div>
            </div>
            <button 
              onClick={(e) => toggleFavorite(e, q)}
              className="p-2 rounded-full hover:bg-slate-100"
            >
              <Heart className={`w-5 h-5 ${isFav ? 'fill-rose-500 text-rose-500' : 'text-slate-400'}`} />
            </button>
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto pb-24 relative min-h-[80vh]">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
        
        {/* Header & Search */}
        <div className="bg-indigo-600 p-6 text-white">
          <h1 className="text-2xl font-bold mb-4 flex items-center">
            <MessageCircle className="w-6 h-6 mr-2" /> Ask the Stars
          </h1>
          <form onSubmit={handleSearch} className="relative">
            <input 
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search domains (e.g. Marriage, Career)..."
              className="w-full pl-10 pr-4 py-3 rounded-lg text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
            <Search className="absolute left-3 top-3.5 text-slate-400 w-5 h-5" />
            <button type="submit" className="hidden">Search</button>
          </form>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-200 bg-slate-50">
          <button 
            className={`flex-1 py-3 text-sm font-semibold text-center border-b-2 ${activeTab === 'browse' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500'}`}
            onClick={() => setActiveTab('browse')}
          >
            Browse All
          </button>
          <button 
            className={`flex-1 py-3 text-sm font-semibold text-center border-b-2 flex justify-center items-center ${activeTab === 'favorites' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500'}`}
            onClick={() => setActiveTab('favorites')}
          >
            <Heart className="w-4 h-4 mr-1" /> Favorites
          </button>
          <button 
            className={`flex-1 py-3 text-sm font-semibold text-center border-b-2 flex justify-center items-center ${activeTab === 'recent' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500'}`}
            onClick={() => setActiveTab('recent')}
          >
            <Clock className="w-4 h-4 mr-1" /> Recent
          </button>
        </div>

        {/* Content Area */}
        <div className="p-4 bg-slate-50 min-h-[400px]">
          
          {activeTab === 'favorites' && renderQuestionList(favorites)}
          
          {activeTab === 'recent' && renderQuestionList(recents)}

          {activeTab === 'browse' && (
            <div className="space-y-2">
              {groupedByDomain.map(([domainIdStr, group]) => {
                const domainId = Number(domainIdStr);
                const isExpanded = expandedDomains.includes(domainId);
                return (
                  <div key={domainId} className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm">
                    <button 
                      onClick={() => toggleDomain(domainId)}
                      className="w-full px-4 py-4 flex justify-between items-center hover:bg-slate-50 transition-colors"
                    >
                      <div className="font-semibold text-slate-800">
                        {domainId}. {group.domain_name} <span className="text-slate-400 font-normal ml-2">({group.questions.length})</span>
                      </div>
                      {isExpanded ? <ChevronDown className="w-5 h-5 text-slate-500" /> : <ChevronRight className="w-5 h-5 text-slate-500" />}
                    </button>
                    
                    {isExpanded && (
                      <div className="p-4 bg-slate-50 border-t border-slate-100">
                        {renderQuestionList(group.questions)}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Sticky Footer for Selection */}
      {selectedQuestion && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-50">
          <div className="max-w-2xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex-1 text-center sm:text-left">
              <div className="text-xs text-indigo-600 font-bold uppercase tracking-wider mb-1">
                Selected Question • {selectedQuestion.question_id}
              </div>
              <div className="text-lg font-medium text-slate-800">
                "{selectedQuestion.question_name}"
              </div>
            </div>
            <button 
              onClick={handleAsk}
              disabled={!rawOutputs}
              className="w-full sm:w-auto px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg shadow-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Ask Question
            </button>
          </div>
          {!rawOutputs && (
            <div className="text-center mt-2 text-xs text-rose-500">
              Please calculate your chart first.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
