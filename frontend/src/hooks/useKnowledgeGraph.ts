import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';
import { Node, EnrichedNode, KnowledgeSearchResponse } from '../schemas/knowledge';

// Debounce utility
function debounce<F extends (...args: any[]) => any>(func: F, waitFor: number) {
  let timeout: ReturnType<typeof setTimeout> | null = null;

  const debounced = (...args: Parameters<F>) => {
    if (timeout !== null) {
      clearTimeout(timeout);
      timeout = null;
    }
    timeout = setTimeout(() => func(...args), waitFor);
  };

  return debounced;
}

export function useNode(nodeId: string | null) {
  const [data, setData] = useState<EnrichedNode | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!nodeId) {
      setData(null);
      return;
    }
    const fetchNode = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const nodeData = await apiService.get<EnrichedNode>(`/knowledge/nodes/${nodeId}`);
        setData(nodeData);
      } catch (e) { setError(e as Error); }
      finally { setIsLoading(false); }
    };
    fetchNode();
  }, [nodeId]);

  return { data, isLoading, error };
}

export function useNodes() {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const fetchNodes = useCallback(async (query: string = "") => {
        setIsLoading(true);
        setError(null);
        try {
            const result = query
                ? (await apiService.post<KnowledgeSearchResponse>('/knowledge/search', { query })).nodes
                : await apiService.get<Node[]>('/knowledge/nodes?enrich=false');
            setNodes(result);
        } catch (e) { setError(e as Error); }
        finally { setIsLoading(false); }
    }, []);

    useEffect(() => { fetchNodes(); }, [fetchNodes]);

    return { nodes, isLoading, error, search: debounce(fetchNodes, 300) };
}