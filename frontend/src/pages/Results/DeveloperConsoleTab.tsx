import { useState } from 'react';
import { Terminal } from 'lucide-react';

export default function DeveloperConsoleTab({ formula_verification }: { formula_verification: any }) {
  const [enabled, setEnabled] = useState(false);

  if (!enabled) {
    return (
      <div className="mt-8 text-center p-12 bg-slate-50 rounded-xl shadow-sm border border-slate-200">
        <Terminal className="w-12 h-12 text-slate-400 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-slate-800 mb-4">Developer Mode is Disabled</h3>
        <button 
          onClick={() => setEnabled(true)}
          className="px-6 py-2 bg-slate-800 text-white rounded-lg font-bold hover:bg-slate-900 transition-colors"
        >
          Enable Developer Mode
        </button>
      </div>
    );
  }

  return (
    <div className="mt-6 animate-in fade-in duration-500 pb-20">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-900 flex items-center">
          <Terminal className="w-6 h-6 mr-2 text-slate-700" />
          Formula Verification Console
        </h2>
        <button 
          onClick={() => setEnabled(false)}
          className="px-4 py-2 bg-rose-100 text-rose-800 rounded-lg font-bold hover:bg-rose-200 transition-colors text-sm"
        >
          Disable Developer Mode
        </button>
      </div>
      
      <div className="bg-slate-900 text-emerald-400 p-6 rounded-xl font-mono text-sm overflow-x-auto shadow-inner border border-slate-700">
        <pre className="whitespace-pre-wrap">{JSON.stringify(formula_verification, null, 2)}</pre>
      </div>
    </div>
  );
}
