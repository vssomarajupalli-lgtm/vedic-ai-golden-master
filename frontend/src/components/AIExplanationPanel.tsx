// GM-012D.6 — AI Explanation Frontend Integration
// AIExplanationPanel: React component for displaying AI-generated explanations

import React, { useState, useCallback } from 'react';
import { apiService } from '../api/backend';
import type { 
  ExplanationRequest, 
  ExplanationResponse,
  ExplanationCitation
} from '../types/schema';

interface AIExplanationPanelProps {
  /** Question ID from the Question Registry (optional if questionText provided) */
  questionId?: string;
  /** Free-text question (optional if questionId provided) */
  questionText?: string;
  /** Full pipeline output from /process-chart or /generate-report */
  pipelineOutput: Record<string, unknown> | null;
  /** Target date for transit/dasha calculations (ISO 8601 UTC) */
  targetDateUtc?: string;
  /** Optional custom className */
  className?: string;
  /** Callback when explanation is generated */
  onExplanationGenerated?: (response: ExplanationResponse) => void;
  /** Callback on error */
  onError?: (error: Error) => void;
}

export const AIExplanationPanel: React.FC<AIExplanationPanelProps> = ({
  questionId,
  questionText,
  pipelineOutput,
  targetDateUtc,
  className = '',
  onExplanationGenerated,
  onError,
}) => {
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateExplanation = useCallback(async () => {
    if (!pipelineOutput) {
      setError('Pipeline output is required to generate explanation');
      return;
    }

    if (!questionId && !questionText) {
      setError('Either questionId or questionText must be provided');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const request: ExplanationRequest = {
        pipeline_output: pipelineOutput,
      };

      if (questionId) request.question_id = questionId;
      if (questionText) request.question_text = questionText;
      if (targetDateUtc) request.target_date_utc = targetDateUtc;

      const response = await apiService.generateExplanation(request);
      setExplanation(response);
      onExplanationGenerated?.(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate explanation';
      setError(errorMessage);
      onError?.(err instanceof Error ? err : new Error(errorMessage));
    } finally {
      setIsLoading(false);
    }
  }, [pipelineOutput, questionId, questionText, targetDateUtc, onExplanationGenerated, onError]);

  const handleRetry = () => {
    generateExplanation();
  };

  const confidenceColors: Record<string, string> = {
    HIGH: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    MEDIUM: 'bg-amber-100 text-amber-700 border-amber-200',
    LOW: 'bg-red-100 text-red-700 border-red-200',
  };

  const citationTypeColors: Record<string, string> = {
    engine_output: 'bg-blue-100 text-blue-700',
    kg_node: 'bg-purple-100 text-purple-700',
    evidence_chain: 'bg-green-100 text-green-700',
    formula_registry: 'bg-orange-100 text-orange-700',
    calibration_registry: 'bg-pink-100 text-pink-700',
    report_template: 'bg-gray-100 text-gray-700',
  };

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <h3 className="font-semibold text-gray-900">AI Explanation</h3>
          </div>
          <span className="px-2 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-700 rounded">
            Powered by Deterministic Pipeline
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-1">Grounded in engine outputs. No AI calculations. Evidence-based only.</p>
      </div>

      {/* Trigger & Input Summary */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex flex-wrap items-center gap-3 mb-3">
          {(questionId || questionText) && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-500">Question:</span>
              <span className="font-medium text-gray-900 truncate max-w-xs">
                {questionId ? `ID: ${questionId}` : questionText}
              </span>
            </div>
          )}
          {targetDateUtc && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-500">Target Date:</span>
              <span className="font-mono text-gray-700">{targetDateUtc}</span>
            </div>
          )}
        </div>

        <button
          onClick={generateExplanation}
          disabled={isLoading || !pipelineOutput || (!questionId && !questionText)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium transition-colors"
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating...
            </span>
          ) : (
            'Generate Explanation'
          )}
        </button>

        {error && (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium text-red-800">Error</span>
            </div>
            <p className="text-sm text-red-700">{error}</p>
            <button
              onClick={handleRetry}
              className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
            >
              Retry
            </button>
          </div>
        )}
      </div>

      {/* Explanation Content */}
      {explanation && (
        <div className="p-4 space-y-4">
          {/* Confidence Badge */}
          <div className="flex items-center gap-3">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${confidenceColors[explanation.confidence] || confidenceColors.MEDIUM}`}>
              Confidence: {explanation.confidence}
            </span>
            <span className="text-xs text-gray-500">
              Domain: {explanation.domain} • {explanation.routed ? 'Routed' : 'Free-text'}
            </span>
            <span className="text-xs text-gray-500 ml-auto">
              {explanation.processing_time_ms}ms
            </span>
          </div>

          {/* Main Explanation */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-2">Explanation</h4>
            <p className="text-sm text-gray-700 whitespace-pre-wrap">{explanation.explanation}</p>
          </div>

          {/* Evidence Summary */}
          <details className="group">
            <summary className="flex items-center gap-2 cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
              <svg className="w-4 h-4 text-gray-400 group-open:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              Evidence Summary ({explanation.evidence_summary.total_citations} citations)
            </summary>
            <div className="mt-3 ml-6 space-y-2 text-sm text-gray-600 border-l-2 border-gray-200 pl-3">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <div className="bg-gray-50 p-2 rounded">
                  <div className="text-xs text-gray-500">Total</div>
                  <div className="font-mono font-semibold">{explanation.evidence_summary.total_citations}</div>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <div className="text-xs text-gray-500">Engine Outputs</div>
                  <div className="font-mono font-semibold">{explanation.evidence_summary.engine_output_citations}</div>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <div className="text-xs text-gray-500">KG Nodes</div>
                  <div className="font-mono font-semibold">{explanation.evidence_summary.kg_node_citations}</div>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <div className="text-xs text-gray-500">Evidence Chains</div>
                  <div className="font-mono font-semibold">{explanation.evidence_summary.evidence_chain_citations}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">Highest Evidence Level:</span>
                <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 text-xs font-mono rounded">
                  {explanation.evidence_summary.highest_evidence_level}
                </span>
              </div>
              {Object.entries(explanation.evidence_summary.by_type).length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {Object.entries(explanation.evidence_summary.by_type).map(([type, count]: [string, number]) => (
                    <span key={type} className={`px-2 py-0.5 text-xs rounded ${citationTypeColors[type] || 'bg-gray-100 text-gray-700'}`}>
                      {type}: {count}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </details>

          {/* Citations */}
          <details className="group">
            <summary className="flex items-center gap-2 cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
              <svg className="w-4 h-4 text-gray-400 group-open:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              Citations ({explanation.citations.length})
            </summary>
            <div className="mt-3 ml-6 space-y-2 text-sm text-gray-600 border-l-2 border-gray-200 pl-3">
              {explanation.citations.map((citation: ExplanationCitation, index: number) => (
                <div key={index} className="bg-gray-50 p-3 rounded border border-gray-100">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`px-1.5 py-0.5 text-xs rounded ${citationTypeColors[citation.type] || 'bg-gray-100 text-gray-700'}`}>
                      {citation.type}
                    </span>
                    {citation.evidence_level && (
                      <span className="px-1.5 py-0.5 bg-indigo-100 text-indigo-700 text-xs font-mono rounded">
                        {citation.evidence_level}
                      </span>
                    )}
                  </div>
                  {citation.path && (
                    <div className="text-xs font-mono text-gray-700">Path: {citation.path}</div>
                  )}
                  {citation.value !== undefined && (
                    <div className="text-xs font-mono text-gray-700">Value: {citation.value}</div>
                  )}
                  {citation.node_id && (
                    <div className="text-xs font-mono text-gray-700">Node: {citation.node_id}</div>
                  )}
                  {citation.chain && citation.chain.length > 0 && (
                    <div className="text-xs text-gray-600 mt-1">
                      Chain: {citation.chain.join(' → ')}
                    </div>
                  )}
                </div>
              ))}
              {explanation.citations.length === 0 && (
                <p className="text-gray-500 italic">No citations provided</p>
              )}
            </div>
          </details>

          {/* Metadata */}
          <details className="group">
            <summary className="flex items-center gap-2 cursor-pointer text-xs text-gray-500 hover:text-gray-700">
              <svg className="w-3 h-3 group-open:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              Metadata
            </summary>
            <div className="mt-2 ml-5 space-y-1 text-xs text-gray-500 font-mono">
              <div>Provider: {explanation.metadata.provider}</div>
              <div>Model: {explanation.metadata.model}</div>
              <div>Prompt Tokens: {explanation.metadata.prompt_tokens}</div>
              <div>Completion Tokens: {explanation.metadata.completion_tokens}</div>
              <div>Total Tokens: {explanation.metadata.total_tokens}</div>
              <div>Processing Time: {explanation.metadata.processing_time_ms}ms</div>
              <div>Grounding Hash: {explanation.metadata.grounding_package_hash || 'N/A'}</div>
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

export default AIExplanationPanel;