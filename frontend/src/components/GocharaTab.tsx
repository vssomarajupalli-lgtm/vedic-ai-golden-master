import React from 'react';
import { useChartStore } from '../store/useChartStore';
import NatalMandaliChart from './NatalMandaliChart';
import CurrentMandaliChart from './CurrentMandaliChart';
import PlanetTransitionTable from './PlanetTransitionTable';

interface SadeSatiCycle {
  cycle_number: number;
  period: string;
}

export const GocharaTab: React.FC = () => {
  const { report, rawOutputs } = useChartStore();

  const mandaliAnalysis = report?.mandali_analysis || null;
  const advisory = rawOutputs?.engine_outputs?.mandali_advisory ||
    rawOutputs?.breakdown?.engine_outputs?.mandali_advisory || null;
  const transitReport = rawOutputs?.engine_outputs?.transit ||
    rawOutputs?.breakdown?.engine_outputs?.transit || null;

  const getGradeColor = (grade: string) => {
    if (grade === 'EXCELLENT' || grade === 'VERY_GOOD' || grade === 'GOOD') return 'text-green-600';
    if (grade === 'POOR' || grade === 'VERY_POOR') return 'text-red-600';
    return 'text-yellow-600';
  };

  const sadeSatiCycles: SadeSatiCycle[] = advisory?.sade_sati?.cycles || [];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium leading-6 text-gray-900">Gochara (Transit) Analysis</h3>
        <p className="mt-1 text-sm text-gray-500">
          Analysis of current planetary transits based on the loaded chart and target date.
        </p>
      </div>

      {!report && !rawOutputs && (
        <div className="text-center p-8 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No chart loaded. Please upload a Canonical JSON file to generate a Gochara analysis.</p>
        </div>
      )}

      {transitReport && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div>
            <h4 className="text-md font-semibold text-gray-800">Overall Transit Impact</h4>
            <p className={`text-3xl font-bold ${getGradeColor(transitReport.grade)}`}>
              {transitReport.grade} ({transitReport.activation_score}/100)
            </p>
          </div>

          {sadeSatiCycles.length > 0 && (
            <div>
              <h4 className="text-md font-semibold text-gray-800 mb-2">Active Major Cycles</h4>
              <ul className="space-y-2">
                {sadeSatiCycles.map((cycle) => (
                  <li key={cycle.cycle_number} className="p-3 bg-gray-50 rounded-lg">
                    <p className="font-semibold text-gray-900">Sade Sati Cycle {cycle.cycle_number}</p>
                    <p className="text-sm text-gray-600">Period: {cycle.period}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="space-y-8">
        {mandaliAnalysis?.natal_chart && (
          <section><NatalMandaliChart data={mandaliAnalysis.natal_chart} /></section>
        )}
        {mandaliAnalysis?.current_chart && (
          <section><CurrentMandaliChart data={mandaliAnalysis.current_chart} /></section>
        )}
        {mandaliAnalysis?.transition_summary && (
          <section><PlanetTransitionTable data={mandaliAnalysis.transition_summary} /></section>
        )}
      </div>
    </div>
  );
};