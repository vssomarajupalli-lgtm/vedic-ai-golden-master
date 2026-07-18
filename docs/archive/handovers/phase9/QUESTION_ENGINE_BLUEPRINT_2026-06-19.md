---
archive_title: "QUESTION ENGINE BLUEPRINT"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# QUESTION ENGINE BLUEPRINT
**Date:** 2026-06-19
**Phase:** 9

## BACKGROUND
The older questionnaire document ("SAMARTHA ASTRO-AI SYSTEM 2.0 QUESTIONNAIRE PIPELINE MAP") defined:
- Universal 24 Canonical Grid
- 12 Bhava based routing
- Bhava lord
- Karaka
- Varga mapping
- Dynamic Dasha timeline routing

**IMPORTANT DECISION:**
The old 24-question model is NOT removed.
It becomes the **"24 MASTER CANONICAL QUESTION NODES"**.
These are permanent parent nodes. Do not replace them.

## FINAL QUESTION ARCHITECTURE

12 Bhava Groups
↓
24 Master Questions (core deterministic routes)
↓
200+ User Facing Questions (child questions)

**Example:**
*Parent:*
Q7 Marriage

*Child questions:*
- When will I get married?
- Early or delayed marriage?
- Which period supports marriage?
- Spouse nature?
- Marriage quality?
- Relationship problems?
- Remedies?

All child questions route through existing parent calculation logic.
**Do NOT create 200 calculation engines.**

## QUESTION REGISTRY PLAN

**Future file:** `question_registry.json`

**Structure:**
- Question ID
- Display Question
- Category
- Parent Node
- House
- Karaka
- Required Varga
- Timing Required
- Engine Route

**Example:**
MARRIAGE_001
- **Question:** "When will marriage happen?"
- **Route:**
  - **Parent:** Q7.1
  - **House:** 7
  - **Karaka:** Venus
  - **Varga:** D9
  - **Uses:** Natal Promise, Dasha Timeline, Varga Refinement

## TIMING GOVERNANCE

For "WHEN" questions, use:

- **Mahadasha (MD)** → Life background period
- **Antardasha (AD)** → Event activation
- **Pratyantardasha (PD)** → Narrow event window

Output should expose:
Current MD:
Current AD:
Current PD:

Favorable Window:
DD.MM.YYYY to DD.MM.YYYY

## QUESTION UI BLUEPRINT

Do NOT keep only blank chat input.
Create future design:
Search Questions

Expandable groups:
▼ Marriage
   - Question 1
   - Question 2
   - Question 3

▼ Career
   - Question list

▼ Finance

▼ Property

▼ Health

Client selects question.
Question Engine answers deterministically.

## ARCHITECTURE LOCKS

Preserve:
- D1 Immutability Principle
- Engine Isolation Principle
- Varga Refinement Principle
- Dosha Preservation Routing
- Functional Nature Governance
- Dasha Timeline Contract
- Mandali Governance
- PipelineRunner orchestration
- Contract Registry

*The Question system is a routing/UX expansion only.*
