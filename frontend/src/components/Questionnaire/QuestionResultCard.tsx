import React from 'react';

export interface StructuredQuestionResult {
  question_title: string;
  domain: string;
  executive_summary: {
    promise_display: string;
    current_support_display: string;
    best_future_opportunity_display: string;
    best_future_window: string;
    main_strength: string;
    main_weakness: string;
    recommendation: string;
    current_period_remaining: string;
    overall_lifetime_direction: string;
  };
  current_dasha_status: {
    current_md: string;
    current_ad: string;
    current_pd: string;
    current_activation_display: string;
    current_probability_display: string;
    remaining_duration: string;
    ends_on: string;
  };
  future_opportunities: Array<{
    rank: number;
    start_date: string;
    end_date: string;
    age: string;
    mahadasha: string;
    antardasha: string;
    pratyantardasha: string;
    final_probability_display: string;
    astrological_driver: string;
  }>;
  detailed_analysis: {
    natural_language_explanation: string;
  };
  supporting_factors: Array<{
    title: string;
    explanation: string;
    impact: string;
  }>;
  attention_factors: Array<{
    reason: string;
    impact: string;
    severity: string;
    recommendation: string;
  }>;
  lifetime_summary: {
    strong_period_count: number;
    moderate_period_count: number;
    weak_period_count: number;
    highest_activation_display: string;
    highest_probability_display: string;
    best_lifetime_window: string;
    longest_strong_window: string;
    current_lifetime_rank: string;
  };
  formula_verification: {
    data_lineage: Record<string, any>;
  };
}

interface Props {
  result: StructuredQuestionResult;
}

export const QuestionResultCard: React.FC<Props> = ({ result }) => {
  return (
    <div className="w-full bg-white shadow-lg rounded-xl overflow-hidden mb-6 border border-gray-200">
      <div className="bg-blue-900 p-4 text-white">
        <h2 className="text-xl font-bold">Question: {result.question_title}</h2>
      </div>

      <div className="p-4 space-y-4 text-gray-800">
        {/* A. Executive Summary */}
        <details className="group border border-gray-200 rounded-lg" open>
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-blue-800 rounded-t-lg group-open:border-b border-gray-200">
            A. Executive Summary
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><span className="font-semibold text-gray-500">Promise:</span> <br/>
              <span className="text-lg font-bold text-gray-800">{result.executive_summary.promise_display}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Current Support:</span> <br/>
              <span className="text-lg font-bold text-gray-800">{result.executive_summary.current_support_display}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Best Future Window:</span> <br/>
              <span className="text-lg font-bold text-gray-800">{result.executive_summary.best_future_window}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Best Future Opportunity:</span> <br/>
              <span className="text-lg font-bold text-gray-800">{result.executive_summary.best_future_opportunity_display}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Main Strength:</span> <br/>
              <span className="text-gray-800">{result.executive_summary.main_strength}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Main Weakness:</span> <br/>
              <span className="text-gray-800">{result.executive_summary.main_weakness}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Current Period Remaining:</span> <br/>
              <span className="text-gray-800">{result.executive_summary.current_period_remaining}</span>
            </div>
            <div><span className="font-semibold text-gray-500">Overall Lifetime Direction:</span> <br/>
              <span className="text-gray-800">{result.executive_summary.overall_lifetime_direction}</span>
            </div>
            <div className="md:col-span-2 bg-blue-50 p-3 rounded mt-2">
              <span className="font-semibold text-blue-800">Recommendation:</span> <br/>
              {result.executive_summary.recommendation}
            </div>
          </div>
        </details>

        {/* B. Current Dasha Status */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-blue-800 rounded-t-lg group-open:border-b border-gray-200">
            B. Current Dasha Status
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4 bg-green-50">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div><span className="font-semibold text-gray-500">MD-AD-PD:</span><br/>
                <span className="font-bold">{result.current_dasha_status.current_md} - {result.current_dasha_status.current_ad} - {result.current_dasha_status.current_pd}</span>
              </div>
              <div><span className="font-semibold text-gray-500">Activation:</span><br/>
                <span className="font-bold">{result.current_dasha_status.current_activation_display}</span>
              </div>
              <div><span className="font-semibold text-gray-500">Probability:</span><br/>
                <span className="font-bold">{result.current_dasha_status.current_probability_display}</span>
              </div>
              <div><span className="font-semibold text-gray-500">Ends On:</span><br/>
                <span className="font-bold">{result.current_dasha_status.ends_on} ({result.current_dasha_status.remaining_duration})</span>
              </div>
            </div>
          </div>
        </details>

        {/* C. Future Opportunity Windows */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-blue-800 rounded-t-lg group-open:border-b border-gray-200">
            C. Future Opportunity Windows
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4">
            <div className="hidden md:block overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Start</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">End</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MD-AD-PD</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Driver</th>
                    <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prob %</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {result.future_opportunities.map((row, idx) => (
                    <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      <td className="px-3 py-2 whitespace-nowrap">{row.rank}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{row.start_date}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{row.end_date}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{row.age}</td>
                      <td className="px-3 py-2 whitespace-nowrap">{row.mahadasha}-{row.antardasha}-{row.pratyantardasha}</td>
                      <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-600">{row.astrological_driver}</td>
                      <td className="px-3 py-2 whitespace-nowrap font-bold">{row.final_probability_display}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {/* Mobile Cards */}
            <div className="md:hidden space-y-4">
              {result.future_opportunities.map((row, idx) => (
                <div key={idx} className="bg-white border rounded shadow-sm p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-bold text-gray-700">Rank #{row.rank}</span>
                    <span className="font-bold text-blue-600">{row.final_probability_display}</span>
                  </div>
                  <div className="text-sm text-gray-600 mb-1">
                    <span className="font-semibold text-gray-500">Period:</span> {row.start_date} to {row.end_date} (Age: {row.age})
                  </div>
                  <div className="text-sm text-gray-600 mb-1">
                    <span className="font-semibold text-gray-500">Dashas:</span> {row.mahadasha}-{row.antardasha}-{row.pratyantardasha}
                  </div>
                  <div className="text-sm text-gray-600">
                    <span className="font-semibold text-gray-500">Driver:</span> {row.astrological_driver}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </details>

        {/* D. Detailed Astrological Analysis */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-blue-800 rounded-t-lg group-open:border-b border-gray-200">
            D. Detailed Astrological Analysis
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4">
            <p className="text-gray-700">{result.detailed_analysis.natural_language_explanation}</p>
          </div>
        </details>

        {/* E. Supporting Factors */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-green-700 rounded-t-lg group-open:border-b border-gray-200">
            E. Supporting Factors
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4 space-y-3">
            {result.supporting_factors.length === 0 ? <p>No specific supporting factors.</p> : null}
            {result.supporting_factors.map((factor, idx) => (
              <div key={idx} className="bg-green-50 p-3 rounded">
                <div className="font-bold text-green-800">{factor.title}</div>
                <div className="text-sm text-green-700 mb-1">Impact: {factor.impact}</div>
                <p className="text-gray-700">{factor.explanation}</p>
              </div>
            ))}
          </div>
        </details>

        {/* F. Attention Factors */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-orange-700 rounded-t-lg group-open:border-b border-gray-200">
            F. Attention Factors
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4 space-y-3">
            {result.attention_factors.length === 0 ? <p>No major attention factors.</p> : null}
            {result.attention_factors.map((factor, idx) => (
              <div key={idx} className="bg-orange-50 p-3 rounded border border-orange-100">
                <div className="font-bold text-orange-800 mb-1">Severity: {factor.severity}</div>
                <div className="text-sm text-gray-700 mb-1"><span className="font-semibold">Reason:</span> {factor.reason}</div>
                <div className="text-sm text-gray-700 mb-2"><span className="font-semibold">Impact:</span> {factor.impact}</div>
                <div className="text-sm text-gray-800 bg-orange-100 p-2 rounded">
                  <span className="font-semibold">Recommendation:</span> {factor.recommendation}
                </div>
              </div>
            ))}
          </div>
        </details>

        {/* G. Lifetime Summary */}
        <details className="group border border-gray-200 rounded-lg">
          <summary className="bg-gray-50 p-4 font-bold text-lg cursor-pointer flex justify-between items-center text-blue-800 rounded-t-lg group-open:border-b border-gray-200">
            G. Lifetime Summary
            <span className="transition group-open:rotate-180">▼</span>
          </summary>
          <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div><span className="font-semibold text-gray-500">Strong Periods:</span><br/><span className="text-green-600 font-bold text-lg">{result.lifetime_summary.strong_period_count}</span></div>
            <div><span className="font-semibold text-gray-500">Moderate Periods:</span><br/><span className="text-orange-500 font-bold text-lg">{result.lifetime_summary.moderate_period_count}</span></div>
            <div><span className="font-semibold text-gray-500">Weak Periods:</span><br/><span className="text-red-600 font-bold text-lg">{result.lifetime_summary.weak_period_count}</span></div>
            <div><span className="font-semibold text-gray-500">Highest Prob:</span><br/><span className="text-gray-800 font-bold text-lg">{result.lifetime_summary.highest_probability_display}</span></div>
            <div className="col-span-2"><span className="font-semibold text-gray-500">Best Window:</span><br/><span className="text-gray-800 font-bold text-lg">{result.lifetime_summary.best_lifetime_window}</span></div>
            <div className="col-span-2"><span className="font-semibold text-gray-500">Rank:</span><br/><span className="text-gray-800 font-bold text-lg">{result.lifetime_summary.current_lifetime_rank}</span></div>
          </div>
        </details>

      </div>
    </div>
  );
};
