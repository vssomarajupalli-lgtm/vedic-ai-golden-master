export interface QuestionPackage {
  id: string;
  name: string;
  description: string;
  category: 'life-domain' | 'life-stage' | 'complete' | 'custom';
  tags: string[];
  icon: string;
  questionIds: string[];
  isCustom: boolean;
  createdBy?: string;
  shareable: boolean;
  exportPackage(): string;
  importPackage(json: string): Promise<QuestionPackage>;
}

export interface PackageManager {
  packages: QuestionPackage[];
  getPackage(id: string): QuestionPackage | undefined;
  addPackage(pkg: QuestionPackage): void;
  removePackage(id: string): boolean;
  createCustomPackage(name: string, description: string, questionIds: string[], tags: string[], icon: string): QuestionPackage;
  importPackage(json: string): QuestionPackage;
  exportPackage(id: string): string | null;
}

export interface CreateCustomPackageData {
  name: string;
  description: string;
  questionIds: string[];
  tags?: string[];
  icon?: string;
}