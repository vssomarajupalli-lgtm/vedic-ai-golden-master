import { Link, Outlet, useLocation } from 'react-router-dom';
import { useChartStore } from '../../store/useChartStore';
import { Home, Upload, FileText, MessageSquare, Download, Terminal, GitGraph } from 'lucide-react';
import { FileText as FileTextIcon } from 'lucide-react';

export default function Layout() {
  const location = useLocation();
  const hasData = useChartStore((state) => state.report !== null);

  const navLinks = [
    { name: 'Dashboard', path: '/', icon: Home, show: true },
    { name: 'Upload Data', path: '/upload', icon: Upload, show: true },
    { name: 'Results', path: '/results', icon: FileText, show: hasData },
    { name: 'Ask Question', path: '/browse', icon: MessageSquare, show: hasData },
    { name: 'Export Report', path: '/export', icon: Download, show: hasData },
    { name: 'Formula Verification', path: '/verify', icon: Terminal, show: hasData },
    { name: 'Consultation', path: '/consultation', icon: FileTextIcon, show: hasData },
    { name: 'Knowledge Graph', path: '/knowledge', icon: GitGraph, show: true },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link to="/" className="text-xl font-bold text-indigo-600 flex items-center gap-2">
                  <span className="text-2xl">✨</span> Vedic-AI
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navLinks.filter(link => link.show).map((link) => {
                  const Icon = link.icon;
                  const isActive = location.pathname === link.path;
                  return (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors ${
                        isActive
                          ? 'border-indigo-500 text-indigo-600'
                          : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                      }`}
                    >
                      <Icon className="w-4 h-4 mr-2" />
                      {link.name}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Render nested routes here */}
        <Outlet />
      </main>

      <footer className="bg-white border-t border-slate-200 mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-slate-500">
            Deterministic Astrological Analysis Platform. Version 1.0.0
          </p>
        </div>
      </footer>
    </div>
  );
}
