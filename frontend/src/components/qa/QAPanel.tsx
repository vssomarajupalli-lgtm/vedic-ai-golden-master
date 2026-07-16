// BKL-008A.3 — Deterministic Q&A Engine
// UI Question Panel: React component for Q&A interface

import React, { useState } from 'react';
import { QAService } from '../../services/qa/qaService';
import type { StructuredAnswer } from '../../services/qa/answerGenerator';

interface QAPanelProps {
  consultationId: string;
  engineOutputs: Record<string, unknown> | null;
  className?: string;
}

export const QAPanel: React.FC<QAPanelProps> = ({
  consultationId,
  engineOutputs,
  className = '',
}) => {
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState<StructuredAnswer[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const suggestedQuestions = QAService.getSuggestedQuestions(engineOutputs);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setIsProcessing(true);
    setError(null);

    try {
      const response = await QAService.ask({
        question: question.trim(),
        consultationId,
        engineOutputs,
      });
      setAnswers(prev => [response.answer, ...prev]);
      setQuestion('');
    } catch (err: any) {
      setError(err.message || 'Failed to process question');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const handleSuggestedClick = (q: string) => {
    setQuestion(q);
  };

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Deterministic Q&A Engine
        </h3>
        <p className="text-xs text-gray-500 mt-1">
          Answers based on deterministic engine outputs. No AI calculations. Evidence-based only.
        </p>
      </div>

      {/* Input Area */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your consultation..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            disabled={isProcessing}
          />
          <button
            onClick={handleAsk}
            disabled={isProcessing || !question.trim()}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {isProcessing ? 'Processing...' : 'Ask'}
          </button>
        </div>

        {error && (
          <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Suggested Questions */}
      {answers.length === 0 && (
        <div className="p-4 border-b border-gray-200">
          <p className="text-xs font-medium text-gray-500 mb-2">Suggested Questions</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((q, i) => (
              <button
                key={i}
                onClick={() => handleSuggestedClick(q)}
                className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Answers */}
      <div className="p-4 space-y-4 max-h-[60vh] overflow-y-auto">
        {answers.length === 0 && !isProcessing && (
          <div className="text-center py-12 text-gray-400">
            <svg className="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm">Ask a question about your consultation</p>
            <p className="text-xs mt-1">All answers are based on deterministic engine outputs</p>
          </div>
        )}

        {answers.map((answer, idx) => (
          <AnswerCard key={idx} answer={answer} />
        ))}
      </div>
    </div>
  );
};

interface AnswerCardProps {
  answer: StructuredAnswer;
}

const AnswerCard: React.FC<AnswerCardProps> = ({ answer }) => (
  <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
    {/* Question */}
    <div className="p-4 bg-gray-50 border-b border-gray-200">
      <div className="flex items-center gap-2">
        <span className="text-xs font-medium text-gray-500 uppercase">Q:</span>
        <span className="text-sm font-medium text-gray-900">{answer.question.rawQuestion}</span>
      </div>
      <div className="flex items-center gap-2 mt-1">
        <span className={`px-1.5 py-0.5 text-xs rounded ${
          answer.question.isSupported ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'
        }`}>
          {answer.question.questionClass}
        </span>
        <span className={`px-1.5 py-0.5 text-xs rounded ${
          answer.isDeterministic ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
        }`}>
          {answer.isDeterministic ? 'Deterministic' : 'Limited Evidence'}
        </span>
        <span className="text-xs text-gray-400">
          Confidence: {Math.round(answer.confidence * 100)}%
        </span>
      </div>
    </div>

    {/* Answer Sections */}
    <div className="p-4 space-y-3">
      {answer.sections.map((section) => (
        <div key={section.id}>
          <h4 className="text-sm font-semibold text-gray-700 mb-1">{section.title}</h4>
          <div className="text-sm text-gray-700 whitespace-pre-wrap">{section.content}</div>
          {section.citations.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {section.citations.map((c, i) => (
                <span
                  key={i}
                  className="px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded text-xs font-mono"
                  title={c.description}
                >
                  {c.inline}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>

    {/* Follow-up Questions */}
    {answer.followUpQuestions.length > 0 && (
      <div className="p-3 bg-gray-50 border-t border-gray-200">
        <p className="text-xs font-medium text-gray-500 mb-2">Follow-up questions</p>
        <div className="flex flex-wrap gap-1">
          {answer.followUpQuestions.map((q, i) => (
            <span key={i} className="px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-600">
              {q}
            </span>
          ))}
        </div>
      </div>
    )}
  </div>
);

export default QAPanel;