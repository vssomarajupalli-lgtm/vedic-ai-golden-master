import React from 'react';
import { useChartStore } from '../store/useChartStore';
import { MandaliChakraDisplay } from './MandaliChakraDisplay';

interface SadeSatiCycle {
  cycle_number: number;
  period: string;
  // Add other properties from the mandali_advisory schema as needed
}

export const GocharaTab: React.FC = () => {
  const { report, isLoading } = useChartStore();

  const mandaliChakra = report?.pipeline_outputs?.mandali_chakra;
  const transitReport = report?.engine_outputs?.transit;

  const GRADE_COLOR_MAP: Record<string, string> = {
    EXCELLENT: 'text-green-600',
    VERY_GOOD: 'text-green-600',
    GOOD: 'text-green-600',
    POOR: 'text-red-600',
    VERY_POOR: 'text-red-600',
  };

  const getGradeColor = (grade: string) => {
    if (grade === 'EXCELLENT' || grade === 'VERY_GOOD' || grade === 'GOOD') return 'text-green-600';
    if (grade === 'POOR' || grade === 'VERY_POOR') return 'text-red-600';
    return GRADE_COLOR_MAP[grade] || 'text-yellow-600'; // The if-statements above make this line unreachable. It should be the only return.
    return GRADE_COLOR_MAP[grade] || 'text-yellow-600';
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium leading-6 text-gray-900">Gochara (Transit) Analysis</h3>
        <p className="mt-1 text-sm text-gray-500">
          Analysis of current planetary transits based on the loaded chart and target date.
        </p>
      </div>

      {isLoading && <div className="text-center p-8 text-gray-500">Loading Report...</div>}

      {!isLoading && !report && (
        <div className="text-center p-8 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No chart loaded. Please upload a Canonical JSON file to generate a Gochara analysis.</p>
        </div>
      )}

      {transitReport && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-semibold text-gray-800">Overall Transit Impact</h4>
            <p className={`text-3xl font-bold ${getGradeColor(transitReport.grade)}`}>
              {transitReport.grade} ({transitReport.activation_score}/100)
            </p>
          </div>

          <div>
            <h4 className="text-md font-semibold text-gray-800 mb-2">Active Major Cycles</h4>
            <ul className="space-y-2">
              {report?.engine_outputs?.mandali_advisory?.sade_sati?.cycles.map((cycle: SadeSatiCycle) => (
                <li key={cycle.cycle_number} className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-semibold text-gray-900">Sade Sati Cycle {cycle.cycle_number}</p>
                  <p className="text-sm text-gray-600">Period: {cycle.period}</p>
                </li>
              ))}
            </ul>
          </div>
          {mandaliChakra && <div className="lg:col-span-2"><MandaliChakraDisplay chakraData={mandaliChakra} /></div>}
        </div>
      )}
    </div>
  );
};
