// BKL-008C.2 — Client Management UI
// Client Dashboard: Main orchestration component

import React, { useState, useMemo, useCallback } from 'react';
import { Plus, Users, TrendingUp, Archive, Inbox } from 'lucide-react';
import { useClientRepository } from '../../services/clients/clientRepository';
import type { ClientProfile, ClientSearchFilters, ClientCreateInput } from '../../types/client';
import { ClientSearchFilterSort } from './ClientSearchFilterSort';
import { ClientList } from './ClientList';
import { ClientCreateModal, ClientEditModal, ClientDeleteConfirmModal } from './ClientModals';
import { ClientDetailsDrawer } from './ClientDetailsDrawer';

export const ClientDashboard: React.FC = () => {
  const {
    clients,
    createClient,
    updateClient,
    deleteClient,
    archiveClient,
    restoreClient,
    getAllTags,
    getStats,
  } = useClientRepository();

  // UI state
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [filters, setFilters] = useState<ClientSearchFilters>({});

  // Modal state
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingClient, setEditingClient] = useState<ClientProfile | null>(null);
  const [deletingClient, setDeletingClient] = useState<ClientProfile | null>(null);
  const [viewingClient, setViewingClient] = useState<ClientProfile | null>(null);

  // Derived
  const allTags = getAllTags();
  const stats = getStats();

  const filteredClients = useMemo(() => {
    let results = [...clients];
    if (filters.query) {
      const lower = filters.query.toLowerCase();
      results = results.filter(c =>
        c.name.toLowerCase().includes(lower) ||
        c.tags.some(t => t.toLowerCase().includes(lower)) ||
        (c.email && c.email.toLowerCase().includes(lower))
      );
    }
    if (filters.status) {
      results = results.filter(c => c.status === filters.status);
    }
    if (filters.tags && filters.tags.length > 0) {
      results = results.filter(c => filters.tags!.some(t => c.tags.includes(t)));
    }
    return results.sort((a, b) => a.name.localeCompare(b.name));
  }, [clients, filters]);

  // Handlers
  const handleSearchChange = useCallback((newFilters: ClientSearchFilters) => {
    setFilters(newFilters);
  }, []);

  const handleCreate = useCallback((input: ClientCreateInput) => {
    createClient(input);
  }, [createClient]);

  const handleEdit = useCallback((client: ClientProfile) => {
    setEditingClient(client);
  }, []);

  const handleSaveEdit = useCallback((id: string, updates: Partial<ClientProfile>) => {
    updateClient(id, updates);
    setEditingClient(null);
  }, [updateClient]);

  const handleDelete = useCallback((id: string) => {
    const client = clients.find(c => c.id === id);
    if (client) setDeletingClient(client);
  }, [clients]);

  const handleConfirmDelete = useCallback((id: string) => {
    deleteClient(id);
    setDeletingClient(null);
    setSelectedIds(prev => {
      const next = new Set(prev);
      next.delete(id);
      return next;
    });
  }, [deleteClient]);

  const handleArchive = useCallback((id: string) => {
    archiveClient(id);
  }, [archiveClient]);

  const handleRestore = useCallback((id: string) => {
    restoreClient(id);
  }, [restoreClient]);

  const handleView = useCallback((client: ClientProfile) => {
    setViewingClient(client);
  }, []);

  const handleSelect = useCallback((id: string) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const handleSelectAll = useCallback(() => {
    setSelectedIds(new Set(filteredClients.map(c => c.id)));
  }, [filteredClients]);

  const handleClearSelection = useCallback(() => {
    setSelectedIds(new Set());
  }, []);

  const statCards = [
    { label: 'Total', value: stats.total, icon: Users, color: 'bg-indigo-50 text-indigo-600' },
    { label: 'Active', value: stats.active, icon: TrendingUp, color: 'bg-emerald-50 text-emerald-600' },
    { label: 'Inactive', value: stats.inactive, icon: Inbox, color: 'bg-amber-50 text-amber-600' },
    { label: 'Archived', value: stats.archived, icon: Archive, color: 'bg-gray-50 text-gray-600' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Client Management</h1>
          <p className="text-sm text-gray-500 mt-1">
            Manage client profiles and linked consultations
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Client
        </button>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {statCards.map(card => (
          <div
            key={card.label}
            className="bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-4"
          >
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${card.color}`}>
              <card.icon className="w-5 h-5" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{card.value}</p>
              <p className="text-xs text-gray-500">{card.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Search / Filter / Sort */}
      <ClientSearchFilterSort
        onSearchChange={handleSearchChange}
        viewMode={viewMode}
        onViewModeChange={setViewMode}
        allTags={allTags}
      />

      {/* Bulk selection info */}
      {selectedIds.size > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg px-4 py-2 flex items-center justify-between">
          <span className="text-sm text-indigo-800">
            {selectedIds.size} client{selectedIds.size !== 1 ? 's' : ''} selected
          </span>
          <button
            onClick={handleClearSelection}
            className="text-xs text-indigo-600 hover:text-indigo-800 underline"
          >
            Clear selection
          </button>
        </div>
      )}

      {/* Client List */}
      <ClientList
        clients={filteredClients}
        viewMode={viewMode}
        selectedIds={selectedIds}
        onSelect={handleSelect}
        onSelectAll={handleSelectAll}
        onClearSelection={handleClearSelection}
        onView={handleView}
        onEdit={handleEdit}
        onArchive={handleArchive}
        onRestore={handleRestore}
        onDelete={handleDelete}
      />

      {/* Create Modal */}
      <ClientCreateModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreate}
      />

      {/* Edit Modal */}
      <ClientEditModal
        isOpen={editingClient !== null}
        client={editingClient}
        onClose={() => setEditingClient(null)}
        onSave={handleSaveEdit}
      />

      {/* Delete Confirm */}
      <ClientDeleteConfirmModal
        isOpen={deletingClient !== null}
        client={deletingClient}
        onClose={() => setDeletingClient(null)}
        onConfirm={handleConfirmDelete}
      />

      {/* Details Drawer */}
      <ClientDetailsDrawer
        client={viewingClient}
        onClose={() => setViewingClient(null)}
        onEdit={(client) => {
          setViewingClient(null);
          setEditingClient(client);
        }}
        onArchive={(id) => {
          handleArchive(id);
          setViewingClient(null);
        }}
        onRestore={(id) => {
          handleRestore(id);
          setViewingClient(null);
        }}
        onDelete={(id) => {
          setViewingClient(null);
          const client = clients.find(c => c.id === id);
          if (client) setDeletingClient(client);
        }}
      />
    </div>
  );
};

export default ClientDashboard;