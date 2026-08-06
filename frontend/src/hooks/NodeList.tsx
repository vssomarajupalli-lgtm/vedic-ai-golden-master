import React, { useState, useEffect } from 'react';
import { useNodes } from '../../hooks/useKnowledgeGraph'; // Assuming correct path

interface Node { id: string; label: string; type: string; }

interface NodeListProps {
  onSelectNode: (nodeId: string) => void;
  selectedNodeId: string | null;
}

export const NodeList: React.FC<NodeListProps> = ({ onSelectNode, selectedNodeId }) => {
  const { nodes, isLoading, error, search } = useNodes();
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Debounced search from the hook
    search(searchTerm);
  }, [searchTerm, search]);

  if (isLoading) {
    return <div className="p-4 text-gray-500">Loading nodes...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error.message}</div>;
  }

  return (
    <div>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search nodes..."
          className="w-full p-2 border border-gray-300 rounded-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <ul className="space-y-1 max-h-[calc(100vh-12rem)] overflow-y-auto">
        {nodes.map(node => (
          <li
            key={node.id}
            onClick={() => onSelectNode(node.id)}
            className={`p-2 rounded-md cursor-pointer transition-colors ${
              selectedNodeId === node.id
                ? 'bg-indigo-100 text-indigo-800 font-semibold'
                : 'hover:bg-gray-100'
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="text-sm">{node.label}</span>
              <span className="px-2 py-0.5 text-xs font-medium bg-gray-200 text-gray-800 rounded-full">{node.type}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};