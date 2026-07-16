// BKL-008A.1 — AI Assistant Foundation
// Prompt Version Manager: Manage prompt versions, history, and rollback
// AP-002 VG-01–VG-07 Compliant: Versioned prompts with audit trail

import type { PromptTemplate } from './promptRegistry';

export interface PromptVersionRecord {
  promptId: string;
  version: string;
  previousVersion: string | null;
  changeType: 'MAJOR' | 'MINOR' | 'PATCH';
  changeDescription: string;
  changedAt: string;
  changedBy: string;
  promptContent: PromptTemplate;
}

export class PromptVersionManager {
  private versionHistory: Map<string, PromptVersionRecord[]> = new Map();

  /** Record a new version of a prompt */
  recordVersion(record: PromptVersionRecord): void {
    const history = this.versionHistory.get(record.promptId) || [];
    history.push(record);
    this.versionHistory.set(record.promptId, history);
  }

  /** Get version history for a prompt */
  getVersionHistory(promptId: string): PromptVersionRecord[] {
    return this.versionHistory.get(promptId) || [];
  }

  /** Get the latest version of a prompt */
  getLatestVersion(promptId: string): PromptVersionRecord | undefined {
    const history = this.getVersionHistory(promptId);
    return history[history.length - 1];
  }

  /** Get the version active at a specific point in time */
  getVersionAtTime(promptId: string, timestamp: string): PromptVersionRecord | undefined {
    const history = this.getVersionHistory(promptId);
    return history
      .filter(r => r.changedAt <= timestamp)
      .sort((a, b) => b.changedAt.localeCompare(a.changedAt))[0];
  }

  /** Determine the version bump type based on changes */
  determineBumpType(
    oldPrompt: PromptTemplate,
    newPrompt: Partial<PromptTemplate>,
  ): 'MAJOR' | 'MINOR' | 'PATCH' {
    // AP-002 VG: Version bump triggers
    if (
      newPrompt.interactionType !== undefined &&
      newPrompt.interactionType !== oldPrompt.interactionType
    ) {
      return 'MAJOR'; // New interaction type = major change
    }
    if (
      newPrompt.systemInstructions !== undefined &&
      newPrompt.systemInstructions !== oldPrompt.systemInstructions
    ) {
      return 'MAJOR'; // System instruction change = major change
    }
    if (
      newPrompt.requiredVariables !== undefined &&
      JSON.stringify(newPrompt.requiredVariables) !== JSON.stringify(oldPrompt.requiredVariables)
    ) {
      return 'MAJOR'; // Variable requirement change = major change
    }
    if (
      newPrompt.userPromptTemplate !== undefined &&
      newPrompt.userPromptTemplate !== oldPrompt.userPromptTemplate
    ) {
      return 'MINOR'; // Template change = minor change
    }
    if (
      newPrompt.governanceRules !== undefined &&
      JSON.stringify(newPrompt.governanceRules) !== JSON.stringify(oldPrompt.governanceRules)
    ) {
      return 'MINOR'; // Governance rule change = minor change
    }
    return 'PATCH'; // Everything else is a patch
  }

  /** Validate that a prompt version bump follows semantic versioning */
  validateVersionBump(
    oldVersion: string,
    newVersion: string,
    bumpType: 'MAJOR' | 'MINOR' | 'PATCH',
  ): boolean {
    const [oldMajor, oldMinor, oldPatch] = oldVersion.split('.').map(Number);
    const [newMajor, newMinor, newPatch] = newVersion.split('.').map(Number);

    switch (bumpType) {
      case 'MAJOR':
        return newMajor === oldMajor + 1 && newMinor === 0 && newPatch === 0;
      case 'MINOR':
        return newMajor === oldMajor && newMinor === oldMinor + 1 && newPatch === 0;
      case 'PATCH':
        return newMajor === oldMajor && newMinor === oldMinor && newPatch === oldPatch + 1;
    }
  }
}

export const promptVersionManager = new PromptVersionManager();