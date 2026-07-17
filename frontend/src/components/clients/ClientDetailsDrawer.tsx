// BKL-008C.2 — Client Management UI
// Client Details Drawer: Side panel for viewing client profile details

import React from 'react';
import {
  X, Mail, Phone, Hash, Calendar, Clock, Users,
  Edit, Archive, RotateCcw, Trash2, ExternalLink,
} from 'lucide-react';
import type { ClientProfile } from '../../types/client';

interface ClientDetailsDrawerProps {
  client: ClientProfile | null;
  onClose: () => void;
  onEdit: (client: ClientProfile) => void;
  onArchive: (id: string) => void;
  onRestore: (id: string) => void;
  onDelete: (id: string) => void;
}

const statusColors: Record<string, string> = {
  active: 'bg-emerald-100 text-emerald-800',
  inactive: 'bg-amber-100 text-amber-800',
  archived: 'bg-gray-100 text-gray-500',
};

export const ClientDetailsDrawer: React.FC<ClientDetailsDrawerProps> = ({
  client,
  onClose,
  onEdit,
  onArchive,
  onRestore,
  onDelete,
}) => {
  if (!client) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/30 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="relative w-full max-w-lg h-full bg-white shadow-2xl flex flex-col animate-slide-in-right">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
              <span className="text-lg font-bold text-indigo-600">
                {client.name.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">{client.name}</h2>
              <span className={`px-2 py-0.5 text-xs rounded ${statusColors[client.status]}`}>
                {client.status}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6 space-y-6">
          {/* Contact Info */}
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Contact Information
            </h3>
            <div className="space-y-3">
              {client.email && (
                <div className="flex items-center gap-3 text-sm">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <a href={`mailto:${client.email}`} className="text-indigo-600 hover:underline">
                    {client.email}
                  </a>
                </div>
              )}
              {client.phone && (
                <div className="flex items-center gap-3 text-sm">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <a href={`tel:${client.phone}`} className="text-gray-900">
                    {client.phone}
                  </a>
                </div>
              )}
              {!client.email && !client.phone && (
                <p className="text-sm text-gray-400 italic">No contact information</p>
              )}
              {client.birthDataHash && (
                <div className="flex items-center gap-3 text-sm">
                  <Hash className="w-4 h-4 text-gray-400" />
                  <span className="font-mono text-xs text-gray-600 break-all">
                    {client.birthDataHash}
                  </span>
                </div>
              )}
            </div>
          </section>

          {/* Tags */}
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Tags
            </h3>
            <div className="flex flex-wrap gap-2">
              {client.tags.length > 0 ? client.tags.map(tag => (
                <span
                  key={tag}
                  className="px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-medium"
                >
                  {tag}
                </span>
              )) : (
                <p className="text-sm text-gray-400 italic">No tags</p>
              )}
            </div>
          </section>

          {/* Notes */}
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Notes
            </h3>
            {client.notes ? (
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{client.notes}</p>
              </div>
            ) : (
              <p className="text-sm text-gray-400 italic">No notes</p>
            )}
          </section>

          {/* Consultations */}
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Linked Consultations
            </h3>
            <div className="flex items-center gap-3 text-sm">
              <Users className="w-4 h-4 text-gray-400" />
              <span className="text-gray-900 font-medium">
                {client.consultationIds.length}
              </span>
              <span className="text-gray-500">
                consultation{client.consultationIds.length !== 1 ? 's' : ''} linked
              </span>
            </div>
          </section>

          {/* Audit Trail */}
          <section>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Audit Trail
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-3">
                <Calendar className="w-4 h-4 text-gray-400" />
                <span className="text-gray-500">Created:</span>
                <span className="text-gray-900">
                  {new Date(client.audit.createdAt).toLocaleDateString(undefined, {
                    year: 'numeric', month: 'long', day: 'numeric',
                  })}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <Clock className="w-4 h-4 text-gray-400" />
                <span className="text-gray-500">Updated:</span>
                <span className="text-gray-900">
                  {new Date(client.audit.updatedAt).toLocaleDateString(undefined, {
                    year: 'numeric', month: 'long', day: 'numeric',
                  })}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <Hash className="w-4 h-4 text-gray-400" />
                <span className="text-gray-500">Version:</span>
                <span className="text-gray-900 font-mono">{client.version}</span>
              </div>
              <div className="flex items-center gap-3">
                <ExternalLink className="w-4 h-4 text-gray-400" />
                <span className="text-gray-500">ID:</span>
                <span className="text-gray-900 font-mono text-xs break-all">{client.id}</span>
              </div>
            </div>
          </section>
        </div>

        {/* Action Buttons */}
        <div className="border-t border-gray-200 p-4 flex flex-wrap gap-2">
          <button
            onClick={() => onEdit(client)}
            className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium flex items-center justify-center gap-2"
          >
            <Edit className="w-4 h-4" />
            Edit
          </button>

          {client.status !== 'archived' ? (
            <button
              onClick={() => onArchive(client.id)}
              className="px-4 py-2 border border-amber-300 text-amber-700 rounded-lg hover:bg-amber-50 text-sm font-medium flex items-center gap-2"
            >
              <Archive className="w-4 h-4" />
              Archive
            </button>
          ) : (
            <button
              onClick={() => onRestore(client.id)}
              className="px-4 py-2 border border-green-300 text-green-700 rounded-lg hover:bg-green-50 text-sm font-medium flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              Restore
            </button>
          )}

          <button
            onClick={() => onDelete(client.id)}
            className="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 text-sm font-medium flex items-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClientDetailsDrawer;