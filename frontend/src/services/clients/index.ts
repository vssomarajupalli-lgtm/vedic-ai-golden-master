// BKL-008C.1 — Client Management Foundation
// Barrel Export

export { useClientRepository } from './clientRepository';
export { ClientService } from './clientService';

export type {
  ClientProfile,
  ClientCreateInput,
  ClientUpdateInput,
  ClientSearchFilters,
  ClientStatus,
  ClientAudit,
} from '../../types/client';

export { DEFAULT_CLIENT_STATUS } from '../../types/client';