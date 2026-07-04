---
description: Standard operating workflow for the Samartha Vedic AI Golden Master repository. Guides repository-first engineering, evidence-based architecture, constitutional governance, and controlled refinement.
---

# Samartha Vedic AI – Golden Master Workflow
## Scope

This workflow governs how the AI performs engineering work.

It guides behavior and decision-making.

It does not replace the Golden Master repository documents, which remain the authoritative source of architecture, governance, and project knowledge.

---

## Purpose

Follow this workflow whenever working inside the Golden Master repository.

The repository is the single source of truth.

Do not rely on previous chat history if repository evidence exists.

---

# Standard Operating Procedure

## Step 1 – Understand Current State

Before performing any work:

- Read PROJECT_CONTINUITY.md (if available).
- Verify the Git working tree is clean.
- Identify the latest Git tag.
- Identify the current milestone.
- Read the latest completed backlog item.
- Determine the next backlog item.

If information is missing or ambiguous, STOP and ask the user.

---

## Step 2 – Repository First

Architectural decisions must be supported by repository evidence.

Never invent architecture.

Never assume ownership.

Always identify the canonical owner before recommending changes.

---

## Step 3 – Standard Engineering Lifecycle

Every repository refinement follows:

Backlog

↓

Execution Package

↓

Architectural Evaluation

↓

User Approval

↓

Implementation

↓

Independent Audit

↓

Git Checkpoint

Never skip a stage.

---

## Step 4 – Repository Protection

Preserve knowledge before cleanup.

One Formula → One Canonical Owner.

One Engine → One Responsibility.

Do not delete or merge repository knowledge without approval.

---

## Step 5 – Ambiguity Rule

If architecture, ownership, implementation strategy, or requirements are ambiguous:

STOP.

Explain the ambiguity.

Present reasonable alternatives supported by repository evidence.

Ask the user before proceeding.

Do not guess.

---

## Step 6 – Document Standards

Every newly created or updated repository document must include:

- Creation Date
- Creation Time (IST)
- Last Updated Date
- Last Updated Time (IST)
- Version
- Status

---

## Step 7 – End of Working Session

Before closing work:

- Verify Git working tree is clean.
- Push completed work.
- Create a Git tag when a backlog item or milestone is completed.
- Update PROJECT_CONTINUITY.md.
- Commit and push the continuity update.

This ensures any future AI session can continue without relying on previous chat history.