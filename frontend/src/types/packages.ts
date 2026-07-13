import type { ReportFormatting } from './consultation';

export interface QuestionPackage {
  id: string;
  name: string;
  description: string;
  category: 'life-domain' | 'life-stage' | 'complete' | 'custom';
  tags: string[];
  icon: string;
  questionIds: string[];
  structure: PackageStructure;
  formatting?: Partial<ReportFormatting>;
  estimatedPages: number;
  estimatedTimeMinutes: number;
  isCustom: boolean;
  createdBy?: string;
  createdAt?: Date;
  updatedAt?: Date;
  shareable: boolean;
  version: number;
}

interface PackageStructure {
  chapters: PackageChapter[];
}

interface PackageChapter {
  title: string;
  questionIds: string[];
  customIntro?: string;
}

export interface PackageManager {
  getAllPackages(): QuestionPackage[];
  getPackageById(id: string): QuestionPackage | undefined;
  createCustomPackage(data: CreateCustomPackageData): Promise<QuestionPackage>;
  updateCustomPackage(id: string, data: Partial<QuestionPackage>): Promise<QuestionPackage>;
  deleteCustomPackage(id: string): Promise<void>;
  exportPackage(id: string): string;
  importPackage(json: string): Promise<QuestionPackage>;
  duplicatePackage(id: string, newName: string): Promise<QuestionPackage>;
}

interface CreateCustomPackageData {
  name: string;
  description: string;
  category: 'custom';
  tags: string[];
  questionIds: string[];
  structure: PackageStructure;
  formatting?: Partial<ReportFormatting>;
  icon?: string;
}

export interface PackageSelectorProps {
  selectedQuestions: Set<string>;
  onPackageSelect: (packageId: string, replace?: boolean) => void;
  onCustomPackageCreate: (data: CreateCustomPackageData) => void;
}