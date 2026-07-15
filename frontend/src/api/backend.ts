import axios from 'axios';
import type { ChartProcessResponse, FinalReportSchema, QuestionResponse, StructuredQuestionResponse } from '../types/schema';

// Use an environment variable or fallback to local backend for development
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const backendApi = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const apiService = {
  /**
   * Generates the massive chart report (Returns JSON formatting)
   */
  async generateReport(canonical: any, machine: any): Promise<FinalReportSchema> {
    const response = await backendApi.post<FinalReportSchema>('/generate-report?format=json', {
      canonical_content: canonical,
      machine_index: machine
    });
    return response.data;
  },

  /**
   * Processes the chart to get the raw math arrays (Required for question grounding)
   */
  async processChart(canonical: any, machine: any): Promise<ChartProcessResponse> {
    const response = await backendApi.post<ChartProcessResponse>('/process-chart', {
      canonical_content: canonical,
      machine_index: machine
    });
    return response.data;
  },

  /**
   * Asks a natural language question grounded in the raw math arrays
   */
  async askQuestion(questionText: string | null, questionId: string | null, engineOutputs: any): Promise<QuestionResponse> {
    const payload: any = {
      engine_outputs: engineOutputs
    };
    if (questionText) payload.question_text = questionText;
    if (questionId) payload.question_id = questionId;

    const response = await backendApi.post<QuestionResponse>('/ask-question', payload);
    return response.data;
  },

  /**
   * Asks a structured question using Phase 14H.1 structured display format
   */
  async askStructuredQuestion(questionId: string, engineOutputs: any): Promise<StructuredQuestionResponse> {
    const payload: any = {
      engine_outputs: engineOutputs,
      question_id: questionId
    };

    const response = await backendApi.post<StructuredQuestionResponse>('/ask-structured-question', payload);
    return response.data;
  },

  /**
   * Triggers a browser download for the generated PDF or HTML report
   */
   async getReportBlob(canonical: any, machine: any, format: 'pdf' | 'html'): Promise<Blob> {
     const response = await backendApi.post(`/generate-report?format=${format}`, {
       canonical_content: canonical,
       machine_index: machine
     }, {
       responseType: 'blob' // Important for file downloads
     });

     return response.data as Blob;
   },

   /**
    * Triggers a browser download for the generated PDF or HTML report
    */
   async downloadReport(canonical: any, machine: any, format: 'pdf' | 'html'): Promise<void> {
     const blob = await this.getReportBlob(canonical, machine, format);
     const url = window.URL.createObjectURL(blob);
     const link = document.createElement('a');
     link.href = url;
     link.setAttribute('download', `vedic_ai_report.${format}`);
     document.body.appendChild(link);
     link.click();
     link.remove();
   },

   // --- Browser Endpoints ---

  async fetchRegistry(): Promise<any[]> {
    const response = await backendApi.get<any[]>('/browser/registry');
    return response.data;
  },

  async searchQuestions(query: string): Promise<any> {
    const response = await backendApi.post<any>('/browser/search', { query });
    return response.data;
  },

  async fetchFavorites(): Promise<any[]> {
    const response = await backendApi.get<any[]>('/browser/favorites');
    return response.data;
  },

  async addFavorite(questionId: string): Promise<any> {
    const response = await backendApi.post<any>('/browser/favorites', { question_id: questionId });
    return response.data;
  },

  async removeFavorite(questionId: string): Promise<any> {
    const response = await backendApi.delete<any>(`/browser/favorites/${questionId}`);
    return response.data;
  },

  async fetchRecents(): Promise<any[]> {
    const response = await backendApi.get<any[]>('/browser/recents');
    return response.data;
  }
};

