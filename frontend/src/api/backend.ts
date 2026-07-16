import axios from 'axios';
import type { ChartProcessResponse, FinalReportSchema, QuestionResponse, StructuredQuestionResponse } from '../types/schema';
import type { KnowledgeNode, KnowledgeRelationship } from '../services/knowledge';

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
  },

  // --- Knowledge Graph Endpoints ---

  async listKnowledgeNodes(type?: string, domain?: string, source?: string): Promise<KnowledgeNode[]> {
    const params: Record<string, string> = {};
    if (type) params.node_type = type;
    if (domain) params.domain = domain;
    if (source) params.source = source;
    const response = await backendApi.get<KnowledgeNode[]>('/knowledge/nodes', { params });
    return response.data;
  },

  async getKnowledgeNode(nodeId: string): Promise<KnowledgeNode> {
    const response = await backendApi.get<KnowledgeNode>(`/knowledge/nodes/${nodeId}`);
    return response.data;
  },

  async createKnowledgeNode(data: Record<string, unknown>): Promise<KnowledgeNode> {
    const response = await backendApi.post<KnowledgeNode>('/knowledge/nodes', data);
    return response.data;
  },

  async updateKnowledgeNode(nodeId: string, data: Record<string, unknown>): Promise<KnowledgeNode> {
    const response = await backendApi.patch<KnowledgeNode>(`/knowledge/nodes/${nodeId}`, data);
    return response.data;
  },

  async deleteKnowledgeNode(nodeId: string): Promise<void> {
    await backendApi.delete(`/knowledge/nodes/${nodeId}`);
  },

  async listKnowledgeRelationships(nodeId?: string, relType?: string): Promise<KnowledgeRelationship[]> {
    const params: Record<string, string> = {};
    if (nodeId) params.node_id = nodeId;
    if (relType) params.rel_type = relType;
    const response = await backendApi.get<KnowledgeRelationship[]>('/knowledge/relationships', { params });
    return response.data;
  },

  async createKnowledgeRelationship(data: Record<string, unknown>): Promise<KnowledgeRelationship> {
    const response = await backendApi.post<KnowledgeRelationship>('/knowledge/relationships', data);
    return response.data;
  },

  async deleteKnowledgeRelationship(relId: string): Promise<void> {
    await backendApi.delete(`/knowledge/relationships/${relId}`);
  },

  async searchKnowledge(query: string, nodeType?: string, domain?: string, limit: number = 50): Promise<{ nodes: KnowledgeNode[]; total: number }> {
    const response = await backendApi.post<{ nodes: KnowledgeNode[]; total: number }>('/knowledge/search', { query, node_type: nodeType, domain, limit });
    return response.data;
  },

  async getEvidenceChain(nodeId: string): Promise<{ formula_id: string; chain: Array<{ step: number; description: string; node_id: string; relationship_id: string; evidence: string }> }> {
    const response = await backendApi.get(`/knowledge/evidence-chain/${nodeId}`);
    return response.data;
  },

  async getCrossReferences(nodeId: string): Promise<Array<{ node: KnowledgeNode; relationship: KnowledgeRelationship; related_node: KnowledgeNode; relevance: string }>> {
    const response = await backendApi.get(`/knowledge/cross-references/${nodeId}`);
    return response.data;
  },

  async getDomainInsights(domain: string): Promise<{ domain: string; node_count: number; relationship_count: number; key_concepts: string[]; coverage_score: number }> {
    const response = await backendApi.get(`/knowledge/insights/${domain}`);
    return response.data;
  },

  async listDomainInsights(): Promise<Array<{ domain: string; node_count: number; relationship_count: number; key_concepts: string[]; coverage_score: number }>> {
    const response = await backendApi.get('/knowledge/insights');
    return response.data;
  },

  async getKnowledgeIntegrity(): Promise<{ valid: boolean; issues: string[]; node_count: number; relationship_count: number; checked_at: string }> {
    const response = await backendApi.get('/knowledge/integrity');
    return response.data;
  },

  async getKnowledgeState(): Promise<{ nodes: KnowledgeNode[]; relationships: KnowledgeRelationship[]; version: number; node_count: number; relationship_count: number }> {
    const response = await backendApi.get('/knowledge/state');
    return response.data;
  },

  async seedKnowledgeGraph(): Promise<{ status: string; node_count?: number; relationship_count?: number; message?: string }> {
    const response = await backendApi.post('/knowledge/seed');
    return response.data;
  }
};

