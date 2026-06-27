import { Link } from 'react-router-dom';
import { useChartStore } from '../store/useChartStore';
import { ArrowRight, Sparkles, ShieldCheck, Database } from 'lucide-react';

export default function Dashboard() {
  const hasData = useChartStore((state) => state.report !== null);

  return (
    <div className="max-w-4xl mx-auto py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-extrabold text-slate-900 sm:text-5xl mb-6">
          Deterministic Astrological Analysis
        </h1>
        <p className="text-xl text-slate-600 max-w-2xl mx-auto">
          Upload raw JSON chart data and generate mathematically rigorous, stateless Vedic-AI predictions instantly in your browser.
        </p>
        
        <div className="mt-10 flex justify-center gap-4">
          <Link
            to="/upload"
            className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:text-lg transition-colors shadow-sm"
          >
            Start New Analysis
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
          
          {hasData && (
            <Link
              to="/results"
              className="inline-flex items-center justify-center px-8 py-3 border border-slate-300 text-base font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 md:text-lg transition-colors shadow-sm"
            >
              Resume Previous
            </Link>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mt-20">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <ShieldCheck className="w-6 h-6 text-indigo-600" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">Stateless Privacy</h3>
          <p className="text-slate-600">
            No database. No user accounts. Your chart data lives entirely in your browser's local memory.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <Sparkles className="w-6 h-6 text-purple-600" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">Parashari Math</h3>
          <p className="text-slate-600">
            Powered by 617 validated historical test cases executing rigorous deterministic formulas.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="w-12 h-12 bg-sky-100 rounded-lg flex items-center justify-center mb-4">
            <Database className="w-6 h-6 text-sky-600" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">JSON Driven</h3>
          <p className="text-slate-600">
            Ingests standard canonical structures directly from HoroscopeCleaner.
          </p>
        </div>
      </div>
    </div>
  );
}
