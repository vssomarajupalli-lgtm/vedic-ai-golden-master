import { create } from 'zustand';
import type { ChartProcessResponse, FinalReportSchema } from '../types/schema';

interface ChartState {
  // Raw uploaded JSONs
  canonicalContent: any | null;
  machineIndex: any | null;
  
  // The mathematical breakdown (for QuestionEngine grounding)
  rawOutputs: ChartProcessResponse | null;
  
  // The generated human-readable report (for rendering)
  report: FinalReportSchema | null;
  
  // Results from structured questions
  questionResults: any[];
  
  // Actions
  setUploads: (canonical: any, machine: any) => void;
  setResults: (outputs: ChartProcessResponse, report: FinalReportSchema) => void;
  setChartData: (canonical: any, machine: any) => void;
  setEngineOutputs: (outputs: ChartProcessResponse) => void;
  setReport: (report: FinalReportSchema) => void;
  setQuestionResults: (results: any[]) => void;
  addQuestionResult: (result: any) => void;
  clearState: () => void;
}

export const useChartStore = create<ChartState>((set) => ({
  canonicalContent: null,
  machineIndex: null,
  rawOutputs: null,
  report: null,
  questionResults: [],
  
  setUploads: (canonical, machine) => set({ 
    canonicalContent: canonical, 
    machineIndex: machine 
  }),
  
  setResults: (outputs, report) => set({ 
    rawOutputs: outputs, 
    report: report 
  }),
  
  setChartData: (canonical, machine) => set({
    canonicalContent: canonical,
    machineIndex: machine,
  }),
  
  setEngineOutputs: (outputs) => set({
    rawOutputs: outputs,
  }),
  
  setReport: (report) => set({
    report: report,
  }),
  
  setQuestionResults: (results) => set({
    questionResults: results
  }),
  
  addQuestionResult: (result) => set((state) => ({
    questionResults: [...state.questionResults, result]
  })),
  
  clearState: () => set({ 
    canonicalContent: null, 
    machineIndex: null, 
    rawOutputs: null, 
    report: null,
    questionResults: []
  })
}));
