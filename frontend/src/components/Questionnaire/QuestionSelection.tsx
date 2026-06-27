import React, { useState } from 'react';
import { QUESTIONNAIRE_SCHEMA } from '../../config/questionnaireSchema';

interface Props {
  onSelectionChange: (selectedIds: string[]) => void;
}

export const QuestionSelection: React.FC<Props> = ({ onSelectionChange }) => {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  const handleToggle = (id: string) => {
    const next = new Set(selectedIds);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    setSelectedIds(next);
    onSelectionChange(Array.from(next));
  };

  return (
    <div className="w-full bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Select Questions</h2>
      <div className="space-y-2">
        {QUESTIONNAIRE_SCHEMA.map(domain => (
          <details key={domain.domainId} className="group bg-gray-50 rounded-md border border-gray-200">
            <summary className="cursor-pointer font-semibold p-3 hover:bg-gray-100 flex items-center justify-between">
              <span>{domain.domainLabel}</span>
              <span className="transition group-open:rotate-180">▼</span>
            </summary>
            <div className="p-3 bg-white border-t border-gray-200">
              {domain.questions.map(q => (
                <label key={q.id} className="flex items-center space-x-3 mb-2 cursor-pointer hover:bg-blue-50 p-1 rounded">
                  <input
                    type="checkbox"
                    className="form-checkbox h-4 w-4 text-blue-600 rounded"
                    checked={selectedIds.has(q.id)}
                    onChange={() => handleToggle(q.id)}
                  />
                  <span className="text-gray-700">{q.label}</span>
                </label>
              ))}
            </div>
          </details>
        ))}
      </div>
    </div>
  );
};
