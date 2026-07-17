// BKL-008C.1 — Client Management Foundation
// Client Service: Business logic layer on top of the repository

import { useClientRepository } from './clientRepository';
import type {
  ClientProfile,
  ClientCreateInput,
  ClientUpdateInput,
  ClientSearchFilters,
  ClientStatus,
} from '../../types/client';

export class ClientService {
  /**
   * Create a new client profile.
   */
  static create(input: ClientCreateInput): ClientProfile {
    if (!input.name || input.name.trim().length === 0) {
      throw new Error('Client name is required');
    }
    const id = useClientRepository.getState().createClient(input);
    const client = useClientRepository.getState().getClient(id);
    if (!client) {
      throw new Error('Failed to create client');
    }
    return client;
  }

  /**
   * Update an existing client profile.
   */
  static update(id: string, input: ClientUpdateInput): ClientProfile {
    useClientRepository.getState().updateClient(id, input);
    const updated = useClientRepository.getState().getClient(id);
    if (!updated) {
      throw new Error(`Client not found: ${id}`);
    }
    return updated;
  }

  /**
   * Get a client by ID.
   */
  static get(id: string): ClientProfile | undefined {
    return useClientRepository.getState().getClient(id);
  }

  /**
   * Find a client by birth data hash.
   */
  static findByBirthHash(hash: string): ClientProfile | undefined {
    return useClientRepository.getState().getClientByBirthHash(hash);
  }

  /**
   * Search clients with filters.
   */
  static search(filters: ClientSearchFilters): ClientProfile[] {
    return useClientRepository.getState().search(filters);
  }

  /**
   * List all clients sorted by name.
   */
  static listAll(): ClientProfile[] {
    return useClientRepository.getState().getAllClients().sort((a, b) => a.name.localeCompare(b.name));
  }

  /**
   * List clients by status.
   */
  static listByStatus(status: ClientStatus): ClientProfile[] {
    return useClientRepository.getState().getClientsByStatus(status);
  }

  /**
   * Archive a client.
   */
  static archive(id: string): ClientProfile {
    useClientRepository.getState().archiveClient(id);
    const archived = useClientRepository.getState().getClient(id);
    if (!archived) {
      throw new Error(`Client not found: ${id}`);
    }
    return archived;
  }

  /**
   * Restore an archived client.
   */
  static restore(id: string): ClientProfile {
    useClientRepository.getState().activateClient(id);
    const restored = useClientRepository.getState().getClient(id);
    if (!restored) {
      throw new Error(`Client not found: ${id}`);
    }
    return restored;
  }

  /**
   * Delete a client permanently.
   */
  static delete(id: string): void {
    const deleted = useClientRepository.getState().deleteClient(id);
    if (!deleted) {
      throw new Error(`Client not found: ${id}`);
    }
  }

  /**
   * Link a consultation to a client.
   */
  static linkConsultation(clientId: string, consultationId: string): void {
    const client = useClientRepository.getState().getClient(clientId);
    if (!client) {
      throw new Error(`Client not found: ${clientId}`);
    }
    useClientRepository.getState().linkConsultation(clientId, consultationId);
  }

  /**
   * Unlink a consultation from a client.
   */
  static unlinkConsultation(clientId: string, consultationId: string): void {
    const client = useClientRepository.getState().getClient(clientId);
    if (!client) {
      throw new Error(`Client not found: ${clientId}`);
    }
    useClientRepository.getState().unlinkConsultation(clientId, consultationId);
  }

  /**
   * Get all unique tags across all clients.
   */
  static getAllTags(): string[] {
    return useClientRepository.getState().getAllTags();
  }

  /**
   * Get client repository statistics.
   */
  static getStats(): { total: number; active: number; inactive: number; archived: number } {
    return useClientRepository.getState().getStats();
  }

  /**
   * Find clients linked to a specific consultation.
   */
  static findByConsultation(consultationId: string): ClientProfile[] {
    return useClientRepository.getState().getClientsByConsultationId(consultationId);
  }
}