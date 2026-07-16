// BKL-008A.2 — Deterministic Explainability Engine
// ExplanationPanel: React component for displaying explanations at any level

import React, { useState } from 'react';
import { ExplanationService } from '../../services/explainability/explanationService';
import type { ExplanationLevel, ExplanationResult, ExplanationResultSection } from '../../services/explainability';

interface ExplanationPanelProps {
  consultation: {
    id: string;
    clientName: string;
    consultationTitle: string;
    consultationDate: string;
  };
  engineOutputs: Record<string, unknown> | null;
  defaultLevel?: ExplanationLevel;
  className?: string;
}

export const ExplanationPanel: React.FC<ExplanationPanelProps> = ({
  consultation,
  engineOutputs,
  defaultLevel = 'L2',
  className = '',
}) => {
  const [selectedLevel, setSelectedLevel] = useState<ExplanationLevel>(defaultLevel);
  const [explanation, setExplanation] = useState<ExplanationResult | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    setIsGenerating(true);
    const result = ExplanationService.generateExplanation({
      consultation,
      engineOutputs,
      level: selectedLevel,
    });
    setExplanation(result);
    setIsGenerating(false);
  };

  const levels: { level: ExplanationLevel; label: string; desc: string }[] = [
    { level: 'L1', label: 'L1 — Simple', desc: 'Client-friendly summary' },
    { level: 'L2', label: 'L2 — Professional', desc: 'Practitioner-level' },
    { level: 'L3', label: 'L3 — Advanced', desc: 'Detailed breakdown' },
    { level: 'L4', label: 'L4 — Formula', desc: 'Formula transparency' },
    { level: 'L5', label: 'L5 — Research', desc: 'Complete data' },
  ];

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Deterministic Explainability Engine
        </h3>
        <p className="text-xs text-gray-500 mt-1">GM-007 engine outputs explained. No AI calculations. Evidence-based only.</p>
      </div>

      {/* Level Selection */}
      <div className="p-4 border-b border-gray-200">
        <label className="block text-sm font-medium text-gray-700 mb-2">Explanation Level</label>
        <div className="flex flex-wrap gap-2">
          {levels.map(({ level, label, desc }) => (
            <button
              key={level}
              onClick={() => setSelectedLevel(level)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                selectedLevel === level
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              title={desc}
            >
              {label}
            </button>
          ))}
        </div>
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 text-sm"
        >
          {isGenerating ? 'Generating...' : 'Generate Explanation'}
        </button>
      </div>

      {/* Explanation Content */}
      {explanation && (
        <div className="p-4 space-y-4">
          {explanation.sections.map((section, idx) => (
            <ExplanationSectionCard key={section.id} section={section} index={idx} />
          ))}

          {/* Attributions Footer */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-xs font-medium text-gray-500 uppercase">Source Attributions</span>
            </div>
            <div className="space-y-1">
              {explanation.attributions.map((attr, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-gray-600">
                  <span className="px-1.5 py-0.5 bg-gray-100 rounded font-mono">{attr.id}</span>
                  <span>{attr.contribution}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Metadata Footer */}
          <div className="text-xs text-gray-400 flex items-center gap-4">
            <span>Generated: {new Date(explanation.generatedAt).toLocaleString()}</span>
            <span>GM: {explanation.metadata.goldenMasterVersion}</span>
            <span>Formula: {explanation.metadata.formulaRegistryVersion}</span>
            <span>Calibration: {explanation.metadata.calibrationProfileVersion}</span>
            <span className="px-1.5 py-0.5 bg-emerald-100 text-emerald-700 rounded">Deterministic</span>
          </div>
        </div>
      )}
    </div>
  );
};

interface ExplanationSectionCardProps {
  section: ExplanationResultSection;
  index: number;
}

const ExplanationSectionCard: React.FC<ExplanationSectionCardProps> = ({ section, index }) => (
  <div className="bg-white border border-gray-200 rounded-lg p-4">
    <div className="flex items-center gap-2 mb-2">
      <span className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs font-bold">
        {index + 1}
      </span>
      <h4 className="font-semibold text-gray-900">{section.title}</h4>
    </div>
    <div className="text-sm text-gray-700 whitespace-pre-wrap">
      {section.content}
    </div>
    {section.sources.length > 0 && (
      <div className="mt-2 flex flex-wrap gap-1">
        {section.sources.map((source, i) => (
          <span
            key={i}
            className="px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded text-xs font-mono"
            title={source.contribution}
          >
            {source.id}
          </span>
        ))}
      </div>
    )}
  </div>
);

export default ExplanationPanel;