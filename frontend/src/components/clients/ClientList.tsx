// BKL-008C.2 — Client Management UI
// Client List: Grid cards + List table views

import React from 'react';
import {
  Users, Mail, Phone, Hash, Calendar,
  Eye, Edit, Archive, RotateCcw, Trash2,
} from 'lucide-react';
import type { ClientProfile, ClientStatus } from '../../types/client';

interface ClientListProps {
  clients: ClientProfile[];
  viewMode: 'grid' | 'list';
  selectedIds: Set<string>;
  onSelect: (id: string) => void;
  onSelectAll: () => void;
  onClearSelection: () => void;
  onView: (client: ClientProfile) => void;
  onEdit: (client: ClientProfile) => void;
  onArchive: (id: string) => void;
  onRestore: (id: string) => void;
  onDelete: (id: string) => void;
}

export const ClientList: React.FC<ClientListProps> = ({
  clients,
  viewMode,
  selectedIds,
  onSelect,
  onSelectAll,
  onClearSelection,
  onView,
  onEdit,
  onArchive,
  onRestore,
  onDelete,
}) => {
  if (clients.length === 0) {
    return (
      <div className="text-center py-16">
        <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No clients found</h3>
        <p className="text-gray-500">Create your first client or adjust your filters</p>
      </div>
    );
  }

  if (viewMode === 'grid') {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {clients.map(client => (
          <ClientGridCard
            key={client.id}
            client={client}
            isSelected={selectedIds.has(client.id)}
            onSelect={() => onSelect(client.id)}
            onView={() => onView(client)}
            onEdit={() => onEdit(client)}
            onArchive={client.status !== 'archived' ? () => onArchive(client.id) : undefined}
            onRestore={client.status === 'archived' ? () => onRestore(client.id) : undefined}
            onDelete={() => onDelete(client.id)}
          />
        ))}
      </div>
    );
  }

  // List view
  const allSelected = clients.length > 0 && selectedIds.size === clients.length;

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <table className="min-w-full">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-10">
              <input
                type="checkbox"
                checked={allSelected}
                onChange={allSelected ? onClearSelection : onSelectAll}
                className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Client
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Contact
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Tags
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Consultations
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Updated
            </th>
            <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {clients.map(client => (
            <tr
              key={client.id}
              className={selectedIds.has(client.id) ? 'bg-blue-50' : 'hover:bg-gray-50'}
            >
              <td className="px-4 py-3">
                <input
                  type="checkbox"
                  checked={selectedIds.has(client.id)}
                  onChange={() => onSelect(client.id)}
                  className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
              </td>
              <td className="px-4 py-3">
                <div className="font-medium text-gray-900">{client.name}</div>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-col gap-0.5 text-sm text-gray-500">
                  {client.email && (
                    <span className="flex items-center gap-1">
                      <Mail className="w-3 h-3" /> {client.email}
                    </span>
                  )}
                  {client.phone && (
                    <span className="flex items-center gap-1">
                      <Phone className="w-3 h-3" /> {client.phone}
                    </span>
                  )}
                  {!client.email && !client.phone && <span className="text-gray-400">—</span>}
                </div>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-wrap gap-1">
                  {client.tags.length > 0 ? (
                    client.tags.slice(0, 3).map(tag => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-400 text-xs">—</span>
                  )}
                  {client.tags.length > 3 && (
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs">
                      +{client.tags.length - 3}
                    </span>
                  )}
                </div>
              </td>
              <td className="px-4 py-3">
                <StatusBadge status={client.status} />
              </td>
              <td className="px-4 py-3">
                <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded text-sm font-medium">
                  {client.consultationIds.length}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-gray-500">
                {new Date(client.audit.updatedAt).toLocaleDateString()}
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => onView(client)}
                    className="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded"
                    title="View details"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => onEdit(client)}
                    className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
                    title="Edit"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  {client.status !== 'archived' ? (
                    <button
                      onClick={() => onArchive(client.id)}
                      className="p-1.5 text-gray-400 hover:text-amber-600 hover:bg-amber-50 rounded"
                      title="Archive"
                    >
                      <Archive className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => onRestore(client.id)}
                      className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded"
                      title="Restore"
                    >
                      <RotateCcw className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    onClick={() => onDelete(client.id)}
                    className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// ────────────────────────────────────────
// Grid Card
// ────────────────────────────────────────

interface ClientGridCardProps {
  client: ClientProfile;
  isSelected: boolean;
  onSelect: () => void;
  onView: () => void;
  onEdit: () => void;
  onArchive?: () => void;
  onRestore?: () => void;
  onDelete: () => void;
}

const ClientGridCard: React.FC<ClientGridCardProps> = ({
  client,
  isSelected,
  onSelect,
  onView,
  onEdit,
  onArchive,
  onRestore,
  onDelete,
}) => (
  <div
    className={`relative bg-white rounded-xl border shadow-sm transition-all cursor-pointer ${
      isSelected
        ? 'ring-2 ring-indigo-500 border-indigo-500'
        : 'border-gray-200 hover:border-indigo-300 hover:shadow-md'
    }`}
    onClick={onSelect}
  >
    {/* Selection checkbox */}
    <div className="absolute top-3 right-3">
      <input
        type="checkbox"
        checked={isSelected}
        onChange={(e) => { e.stopPropagation(); onSelect(); }}
        className="w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
      />
    </div>

    <div className="p-4">
      {/* Status + Name */}
      <div className="flex items-start justify-between mb-2">
        <StatusBadge status={client.status} />
      </div>

      <h3 className="font-bold text-gray-900 mb-1 line-clamp-1">{client.name}</h3>

      {/* Contact */}
      <div className="flex flex-col gap-0.5 text-xs text-gray-500 mb-3">
        {client.email && (
          <span className="flex items-center gap-1 truncate">
            <Mail className="w-3 h-3 flex-shrink-0" /> {client.email}
          </span>
        )}
        {client.phone && (
          <span className="flex items-center gap-1 truncate">
            <Phone className="w-3 h-3 flex-shrink-0" /> {client.phone}
          </span>
        )}
        {client.birthDataHash && (
          <span className="flex items-center gap-1 truncate">
            <Hash className="w-3 h-3 flex-shrink-0" /> Birth data linked
          </span>
        )}
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-1 mb-3">
        {client.tags.length > 0 ? (
          <>
            {client.tags.slice(0, 3).map(tag => (
              <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                {tag}
              </span>
            ))}
            {client.tags.length > 3 && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs">
                +{client.tags.length - 3}
              </span>
            )}
          </>
        ) : (
          <span className="text-xs text-gray-400 italic">No tags</span>
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
        <div className="flex items-center gap-3 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <Users className="w-3 h-3" />
            {client.consultationIds.length}
          </span>
          <span className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            {new Date(client.audit.updatedAt).toLocaleDateString()}
          </span>
        </div>
      </div>
    </div>

    {/* Action bar */}
    <div className="px-4 pb-3 border-t border-gray-100 flex items-center gap-1">
      <button
        onClick={(e) => { e.stopPropagation(); onView(); }}
        className="flex-1 px-2 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-xs font-medium flex items-center justify-center gap-1"
      >
        <Eye className="w-3 h-3" />
        View
      </button>
      <button
        onClick={(e) => { e.stopPropagation(); onEdit(); }}
        className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
        title="Edit"
      >
        <Edit className="w-3.5 h-3.5" />
      </button>
      {onArchive && (
        <button
          onClick={(e) => { e.stopPropagation(); onArchive(); }}
          className="p-1.5 text-gray-400 hover:text-amber-600 hover:bg-amber-50 rounded"
          title="Archive"
        >
          <Archive className="w-3.5 h-3.5" />
        </button>
      )}
      {onRestore && (
        <button
          onClick={(e) => { e.stopPropagation(); onRestore(); }}
          className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded"
          title="Restore"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      )}
      <button
        onClick={(e) => { e.stopPropagation(); onDelete(); }}
        className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
        title="Delete"
      >
        <Trash2 className="w-3.5 h-3.5" />
      </button>
    </div>
  </div>
);

// ────────────────────────────────────────
// Shared: Status Badge
// ────────────────────────────────────────

const statusColors: Record<ClientStatus, string> = {
  active: 'bg-emerald-100 text-emerald-800',
  inactive: 'bg-amber-100 text-amber-800',
  archived: 'bg-gray-100 text-gray-500',
};

const StatusBadge: React.FC<{ status: ClientStatus }> = ({ status }) => (
  <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColors[status]}`}>
    {status}
  </span>
);

export default ClientList;