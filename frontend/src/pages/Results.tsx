import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useChartStore } from '../store/useChartStore';
import { User, Award, Home, HelpCircle, Terminal } from 'lucide-react';
import LifetimeIntelligenceTab from './Results/LifetimeIntelligenceTab';
import QuestionIntelligenceTab from './Results/QuestionIntelligenceTab';
import DeveloperConsoleTab from './Results/DeveloperConsoleTab';

export default function Results() {
  const report = useChartStore((state) => state.report);
  const [activeTab, setActiveTab] = useState<'LIFETIME' | 'QUESTIONS' | 'DEVELOPER'>('LIFETIME');

  if (!report) {
    return <Navigate to="/upload" replace />;
  }

  const {
    client_profile,
    executive_summary,
    question_responses,
    formula_verification
  } = report;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in fade-in duration-500">
      
      {/* Universal Client Header */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 flex items-center">
            <User className="w-6 h-6 mr-2 text-indigo-600" />
            {client_profile?.name || 'Anonymous Client'}
          </h2>
          <p className="text-slate-500 mt-1">DOB: {client_profile?.dob || 'Unknown'} | POB: {client_profile?.pob || 'Unknown'}</p>
        </div>
        <div className="text-right">
          <div className="inline-flex items-center justify-center px-4 py-2 bg-indigo-50 border border-indigo-100 rounded-lg">
            <Award className="w-5 h-5 text-indigo-600 mr-2" />
            <span className="font-bold text-indigo-900">
              Score: {executive_summary?.overall_score || 0}
            </span>
          </div>
        </div>
      </div>

      {/* Tabbed Navigation */}
      <div className="flex space-x-1 bg-slate-100 p-1 rounded-xl mb-8">
        <button
          onClick={() => setActiveTab('LIFETIME')}
          className={`flex-1 flex items-center justify-center py-3 px-4 rounded-lg font-bold transition-all ${
            activeTab === 'LIFETIME' 
              ? 'bg-white text-indigo-700 shadow-sm' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'
          }`}
        >
          <Home className="w-5 h-5 mr-2" />
          Lifetime Blueprint
        </button>
        <button
          onClick={() => setActiveTab('QUESTIONS')}
          className={`flex-1 flex items-center justify-center py-3 px-4 rounded-lg font-bold transition-all ${
            activeTab === 'QUESTIONS' 
              ? 'bg-white text-indigo-700 shadow-sm' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'
          }`}
        >
          <HelpCircle className="w-5 h-5 mr-2" />
          Question Insights
        </button>
        <button
          onClick={() => setActiveTab('DEVELOPER')}
          className={`flex-1 flex items-center justify-center py-3 px-4 rounded-lg font-bold transition-all ${
            activeTab === 'DEVELOPER' 
              ? 'bg-white text-slate-900 shadow-sm' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'
          }`}
        >
          <Terminal className="w-5 h-5 mr-2" />
          Developer Console
        </button>
      </div>

      {/* Tab Content Render */}
      <div className="mt-4">
        {activeTab === 'LIFETIME' && <LifetimeIntelligenceTab report={report} />}
        {activeTab === 'QUESTIONS' && <QuestionIntelligenceTab questions={question_responses} />}
        {activeTab === 'DEVELOPER' && <DeveloperConsoleTab formula_verification={formula_verification} />}
      </div>

    </div>
  );
}
