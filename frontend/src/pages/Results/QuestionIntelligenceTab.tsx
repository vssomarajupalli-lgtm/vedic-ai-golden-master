import { HelpCircle } from 'lucide-react';
import { QuestionResultCard } from '../../components/Questionnaire/QuestionResultCard';

export default function QuestionIntelligenceTab({ questions }: { questions: any[] }) {
  if (!questions || questions.length === 0) {
    return (
      <div className="mt-8 text-center p-12 bg-white rounded-xl shadow-sm border border-slate-200">
        <HelpCircle className="w-12 h-12 text-slate-300 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-slate-800">No question selected.</h3>
        <p className="text-slate-500 mt-2">Generate a specific query (e.g., Marriage, Career, Finance) to receive targeted insights.</p>
      </div>
    );
  }

  return (
    <div className="mt-6 space-y-6 animate-in fade-in duration-500 pb-20">
      {questions.map((q: any, idx: number) => (
        <QuestionResultCard key={idx} result={q} />
      ))}
    </div>
  );
}
