import React from 'react';
import { PrintFramework } from '../PrintFramework';

interface PrintFrameworkModalProps {
  isOpen: boolean;
  onClose: () => void;
  consultation: any;
}

export const PrintFrameworkModal: React.FC<PrintFrameworkModalProps> = ({
  isOpen,
  onClose,
  consultation,
}) => {
  if (!isOpen) return null;

  return (
    <PrintFramework
      isOpen={isOpen}
      onClose={onClose}
      consultation={consultation}
    />
  );
};

export default PrintFrameworkModal;