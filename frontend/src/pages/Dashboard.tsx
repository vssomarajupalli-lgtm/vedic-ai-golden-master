import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ShieldCheck, Database, Clock, Pin, Plus, FileText, Search } from 'lucide-react';
import { useConsultationStore } from '../store/useConsultationStore';
import { ConsultationList } from '../components/consultation/ConsultationList';

export default function Dashboard() {
  const navigate = useNavigate();
  const { consultations, getRecentConsultations, getPinnedConsultations, openConsultation } = useConsultationStore();
  
  const recentConsultations = getRecentConsultations(5);
  const pinnedConsultations = getPinnedConsultations();
  
  const hasAnyData = consultations.length > 0;
  const hasRecent = recentConsultations.length > 0;
  const hasPinned = pinnedConsultations.length > 0;

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="mb-12">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900 sm:text-4xl mb-3">
              Consultation Workspace
            </h1>
            <p className="text-lg text-slate-600 max-w-2xl">
              Manage your astrological consultations with full persistence, search, and export capabilities.
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/upload"
              className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm"
            >
              <Plus className="w-5 h-5 mr-2" />
              New Consultation
            </Link>
            <Link
              to="/consultation/library"
              className="inline-flex items-center justify-center px-6 py-3 border border-slate-300 text-base font-medium rounded-lg text-slate-700 bg-white hover:bg-slate-50 transition-colors shadow-sm"
            >
              <FileText className="w-5 h-5 mr-2" />
              Browse All
            </Link>
          </div>
        </div>
        
        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Total Consultations</p>
                <p className="text-2xl font-bold text-slate-900">{consultations.length}</p>
              </div>
              <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-indigo-600" />
              </div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Active</p>
                <p className="text-2xl font-bold text-slate-900">
                  {consultations.filter(c => c.status === 'active').length}
                </p>
              </div>
              <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                <Clock className="w-5 h-5 text-emerald-600" />
              </div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Pinned</p>
                <p className="text-2xl font-bold text-slate-900">{pinnedConsultations.length}</p>
              </div>
              <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                <Pin className="w-5 h-5 text-amber-600" />
              </div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Completed</p>
                <p className="text-2xl font-bold text-slate-900">
                  {consultations.filter(c => c.status === 'completed').length}
                </p>
              </div>
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Search className="w-5 h-5 text-purple-600" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Pinned Consultations */}
      {hasPinned && (
        <section className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Pin className="w-5 h-5 text-amber-500" />
              Pinned Consultations
            </h2>
            <Link
              to="/consultation/library"
              className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              View all →
            </Link>
          </div>
          <ConsultationList
            consultations={pinnedConsultations}
            onSelect={(c) => { openConsultation(c.id); navigate(`/consultation/${c.id}`); }}
            showActions={false}
          />
        </section>
      )}

      {/* Recent Consultations */}
      {hasRecent && (
        <section className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Clock className="w-5 h-5 text-sky-500" />
              Recent Consultations
            </h2>
            <Link
              to="/consultation/library"
              className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              View all →
            </Link>
          </div>
          <ConsultationList
            consultations={recentConsultations}
            onSelect={(c) => { openConsultation(c.id); navigate(`/consultation/${c.id}`); }}
            showActions={false}
          />
        </section>
      )}

      {/* Empty State */}
      {!hasAnyData && (
        <div className="bg-white rounded-2xl border border-slate-200 p-16 text-center">
          <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <FileText className="w-10 h-10 text-indigo-600" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-3">No Consultations Yet</h2>
          <p className="text-slate-600 mb-8 max-w-md mx-auto">
            Create your first consultation by uploading chart data from HoroscopeCleaner.
            All your work will be automatically saved and restored.
          </p>
          <Link
            to="/upload"
            className="inline-flex items-center justify-center px-8 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
          >
            <Plus className="w-5 h-5 mr-2" />
            Start New Consultation
          </Link>
        </div>
      )}

      {/* Features Grid - only show if no data */}
      {!hasAnyData && (
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <ShieldCheck className="w-6 h-6 text-indigo-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Automatic Persistence</h3>
            <p className="text-slate-600">
              Every change saves automatically. Browser refresh never loses your work.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Full Search & Filter</h3>
            <p className="text-slate-600">
              Find any consultation instantly with text search, status filters, tags, and date ranges.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <div className="w-12 h-12 bg-sky-100 rounded-lg flex items-center justify-center mb-4">
              <Database className="w-6 h-6 text-sky-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Client Management</h3>
            <p className="text-slate-600">
              Link consultations to clients. One client, many consultations. Full history tracking.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

function ConsultationCard({ consultation, onClick }: { consultation: any; onClick: () => void }) {
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getStatusBadge = (status: string) => {
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

  return (
    <button
      onClick={onClick}
      className="group bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md hover:border-indigo-300 transition-all text-left"
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-slate-900 text-base line-clamp-1 group-hover:text-indigo-700 transition-colors">
          {consultation.name}
        </h3>
        <div className="flex items-center gap-1">
          {consultation.isPinned && <Pin className="w-4 h-4 text-amber-500" />}
          {consultation.status === 'archived' && <span className="w-4 h-4 text-slate-400" title="Archived">📦</span>}
        </div>
      </div>
      
      {consultation.client?.name && (
        <p className="text-sm text-slate-500 mb-3 flex items-center gap-1">
          <span className="w-3.5 h-3.5">👤</span>
          {consultation.client.name}
        </p>
      )}
      
      <div className="flex flex-wrap gap-1.5 mb-3">
        {getStatusBadge(consultation.status)}
        {consultation.tags.slice(0, 2).map(tag => (
          <span key={tag} className="px-2 py-0.5 text-xs bg-slate-100 text-slate-600 rounded-full">
            {tag}
          </span>
        ))}
        {consultation.tags.length > 2 && (
          <span className="px-2 py-0.5 text-xs bg-slate-100 text-slate-500 rounded-full">
            +{consultation.tags.length - 2}
          </span>
        )}
      </div>
      
      <div className="text-xs text-slate-400 flex items-center gap-3 border-t border-slate-100 pt-3">
        <span className="flex items-center gap-1">
          <span className="w-3.5 h-3.5">🕐</span>
          Updated {formatDate(consultation.updatedAt)}
        </span>
        {consultation.lastOpenedAt && (
          <span className="flex items-center gap-1">
            <span className="w-3.5 h-3.5">👁</span>
            Opened {formatDate(consultation.lastOpenedAt)}
          </span>
        )}
      </div>
    </button>
  );
}