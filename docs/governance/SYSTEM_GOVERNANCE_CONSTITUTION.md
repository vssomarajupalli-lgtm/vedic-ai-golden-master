# GM-008 SYSTEM GOVERNANCE CONSTITUTION
**Samartha Vedic AI — Golden Master Program**
**Version 1.0.0 — Effective 2026-07-16**

---

## PREAMBLE

This Constitution establishes the permanent, non-negotiable rules that govern the entire Samartha Vedic AI Golden Master platform. It codifies the engineering discipline that has been practiced since GM-001 and formalizes it for all future milestones through GM-010 and beyond.

This Constitution is **hierarchical** — it sits above all other governance documents. The AI Governance Constitution (AP-002), Formula Governance, Calibration Governance, and all other domain-specific governance documents must comply with this Constitution.

### Founding Principle

> **Deterministic integrity is the platform's single most valuable asset. Every rule in this Constitution exists to protect it.**

---

## 1. ARCHITECTURE GOVERNANCE

### 1.1 Architecture Authority

| Rule | Description |
|------|-------------|
| **AG-01** | The Chief Architect is the final authority on all architecture decisions |
| **AG-02** | Architecture decisions are recorded in the Decision Register (ADR format) |
| **AG-03** | Architecture changes that affect frozen modules require Chief Architect approval |
| **AG-04** | Architecture Review is mandatory before any feature implementation begins |
| **AG-05** | The System Architecture document (`docs/SYSTEM_ARCHITECTURE.md`) is the single source of truth for architecture |

### 1.2 Architecture Layers

```
╔══════════════════════════════════════════════════════════════╗
║ LAYER 4: PRESENTATION (GM-008)                              ║
║ Read-only consumption of deterministic outputs               ║
║ UI, AI Assistant, Reports, Analytics, Client Management      ║
╠══════════════════════════════════════════════════════════════╣
║ LAYER 3: APPLICATION (GM-007+)                              ║
║ Read-only consumption of deterministic outputs               ║
║ Consultation Workspace, Timeline, Gochara, Comparison,       ║
║ Repository, Print Framework, Verification Console            ║
╠══════════════════════════════════════════════════════════════╣
║ LAYER 2: PIPELINE (GM-007)                                  ║
║ Orchestration, sequencing, data flow, store contracts        ║
║ PipelineRunner, ChartStore, ReportBuilder                    ║
╠══════════════════════════════════════════════════════════════╣
║ LAYER 1: DETERMINISTIC CORE (GM-001 — GM-007)               ║
║ PERMANENTLY FROZEN                                           ║
║ Engines, Formulas, Calibration, Question Catalog,            ║
║ Decision Layer, Formula Registry                             ║
╚══════════════════════════════════════════════════════════════╝
```

### 1.3 Layer Rules

| Layer | Write Access | Read Access | Modification Process |
|-------|-------------|-------------|---------------------|
| **Layer 1: Core** | Only Chief Architect with formal freeze exception | All layers (read-only) | Freeze Exception Process (section 19) |
| **Layer 2: Pipeline** | GM-007 authorized modules | All layers | Architecture Review + Feature Approval |
| **Layer 3: Application** | GM-007+ authorized modules | All layers | Standard Feature Approval |
| **Layer 4: Presentation** | GM-008 authorized modules | Layer 1-3 read-only | Standard Feature Approval |

### 1.4 Architecture Decision Records (ADRs)

| Rule | Description |
|------|-------------|
| **AG-06** | Every architecture decision that affects multiple modules must produce an ADR |
| **AG-07** | ADRs follow the format: Context → Decision → Rationale → Consequences → Status |
| **AG-08** | ADRs are stored in `docs/architecture/decisions/ADR-NNN.md` |
| **AG-09** | ADRs are numbered sequentially; deprecated ADRs reference their replacement |
| **AG-10** | The ADR Inventory (`docs/architecture/ADR_INVENTORY_v1.0.md`) is updated on every ADR change |

---

## 2. REPOSITORY GOVERNANCE

### 2.1 Repository as Single Source of Truth

| Rule | Description |
|------|-------------|
| **RG-01** | The repository (`D:\vedic-ai-golden-master`) is the single source of truth for all code, documentation, configuration, and governance |
| **RG-02** | No external system may hold authoritative data not represented in the repository |
| **RG-03** | All generated artifacts (build outputs, test reports, logs) are excluded via `.gitignore` |
| **RG-04** | The repository structure follows the documented file tree (`docs/status/PROJECT_FILE_TREE_*.md`) |

### 2.2 Branch Governance

| Rule | Description |
|------|-------------|
| **RG-05** | `main` is the only production branch |
| **RG-06** | Feature work is done on `feature/<bkl-id>-<description>` branches |
| **RG-07** | Merges to `main` require: build passing, TypeScript clean, tests passing, architecture review |
| **RG-08** | Direct commits to `main` are prohibited (PR only) |
| **RG-09** | Squash merging is preferred; each merge produces one clean commit |

### 2.3 Commit Governance

| Rule | Description |
|------|-------------|
| **RG-10** | Commit messages follow the format: `<BKL-ID>: <Description> — <Status>` |
| **RG-11** | Every commit that completes a milestone must be tagged |
| **RG-12** | Tags follow the format: `gm-<NNN>-<bkl-id>-<description>` |
| **RG-13** | Tags are annotated (not lightweight) |
| **RG-14** | Force-push to `main` is prohibited |

### 2.4 Repository Hygiene

| Rule | Description |
|------|-------------|
| **RG-15** | Repository hygiene audit is performed at the completion of every GM milestone |
| **RG-16** | Dead code, legacy files, and obsolete documentation are identified and removed or archived |
| **RG-17** | The `.gitignore` is maintained to exclude all generated artifacts |
| **RG-18** | No secrets, credentials, or API keys in the repository |

---

## 3. DECISION REGISTER GOVERNANCE

### 3.1 Decision Register Authority

| Rule | Description |
|------|-------------|
| **DR-01** | The Decision Register (`docs/governance/DECISION_REGISTER.md`) is the authoritative record of all governance decisions |
| **DR-02** | Every decision that affects architecture, process, or policy must have a Decision Register entry |
| **DR-03** | Decision entries include: ID, Date, Decision, Rationale, Authority, Status, Impact |
| **DR-04** | Decision Register entries are immutable — changes require a new entry referencing the original |

### 3.2 Decision Hierarchy

```
Chief Architect Decision
        │
        ├── Architecture Decision Records (ADRs)
        │       └── Stored in docs/architecture/decisions/
        │
        ├── Governance Decisions
        │       └── Stored in Decision Register
        │
        ├── Feature Decisions
        │       └── Stored in BKL Execution Packages
        │
        └── Implementation Decisions
                └── Stored in commit messages and PR descriptions
```

---

## 4. CALIBRATION GOVERNANCE

### 4.1 Calibration Authority

| Rule | Description |
|------|-------------|
| **CG-01** | The `CalibrationManager` is the single source of truth for all calibration constants |
| **CG-02** | Calibration constants are stored in versioned profiles (`v1.0_current.json`) |
| **CG-03** | Calibration changes require Chief Architect approval |
| **CG-04** | Calibration changes must include: rationale, impact analysis, before/after comparison |
| **CG-05** | Calibration version is recorded in every consultation snapshot |

### 4.2 Calibration Change Process

```
1. PROPOSAL: Document proposed change with astrological rationale
2. IMPACT ANALYSIS: Run all affected formulas with old and new constants
3. REVIEW: Chief Architect reviews impact on existing consultations
4. APPROVAL: Chief Architect approves or rejects
5. VERSION BUMP: New calibration profile version created
6. REGISTRY UPDATE: Calibration constant inventory updated
7. DECISION REGISTER: Change recorded as Decision Register entry
8. BACKWARD COMPAT: Existing consultations retain old calibration version
```

### 4.3 Calibration Versioning

| Rule | Description |
|------|-------------|
| **CG-06** | Calibration profiles follow semantic versioning: MAJOR.MINOR.PATCH |
| **CG-07** | MAJOR: Changes that alter the interpretation of results (requires all consultations reviewed) |
| **CG-08** | MINOR: New constants or domains added (backward compatible) |
| **CG-09** | PATCH: Bug fixes or precision improvements (no behavioral change) |

---

## 5. FORMULA GOVERNANCE

### 5.1 Formula Registry Authority

| Rule | Description |
|------|-------------|
| **FG-01** | The Formula Registry is the authoritative catalog of all astrological formulas |
| **FG-02** | Every formula has a unique ID, version, domain, evidence chain, and calibration dependency |
| **FG-03** | Formulas are immutable once registered — changes create a new formula version |
| **FG-04** | Formula changes require Chief Architect approval |

### 5.2 Formula Evidence Chain

Every formula must document:

```
Formula ID: <DOMAIN>-<TYPE>-<NNN>
    │
    ├── Classical Source: Reference to classical text and verse
    ├── Astrological Rationale: Why this formula exists
    ├── Inputs: What engine outputs it consumes
    ├── Computation: Mathematical expression
    ├── Calibration Dependencies: Which constants affect it
    ├── Output: What it produces
    ├── Evidence: Traceability to astrological principles
    └── Cross-references: Related formulas and dependencies
```

### 5.3 Formula Lifecycle

```
PROPOSED → REVIEW → APPROVED → ACTIVE → DEPRECATED → RETIRED
    │         │         │         │          │           │
    │         │         │         │          │           └── No longer used;
    │         │         │         │          │               retained for history
    │         │         │         │          │
    │         │         │         │          └── Superseded by new formula;
    │         │         │         │              existing consultations unchanged
    │         │         │         │
    │         │         │         └── In production use
    │         │         │
    │         │         └── Chief Architect approved
    │         │
    │         └── Under architecture review
    │
    └── Proposed by domain expert or astrologer
```

---

## 6. KNOWLEDGE GOVERNANCE

### 6.1 Knowledge Classification

| Knowledge Type | Authority | Storage | Access |
|---------------|-----------|---------|--------|
| **Engine Knowledge** | `docs/knowledge/*/` | Knowledge packages per engine | Read-only (frozen) |
| **Formula Knowledge** | Formula Registry | Formula evidence chains | Read-only (frozen) |
| **Domain Knowledge** | Knowledge Graph (GM-008) | Graph database | Read-only for AI |
| **Architecture Knowledge** | `docs/architecture/` | ADRs, architecture reports | Read-only (governed) |
| **Implementation Knowledge** | `docs/engineering/` | Implementation records | Read-only (historical) |
| **Governance Knowledge** | `docs/governance/` | Governance documents | Read-only (governed) |

### 6.2 Knowledge Derivation Rules

| Rule | Description |
|------|-------------|
| **KG-01** | All astrological knowledge must be traceable to engine outputs, formulas, or calibration constants |
| **KG-02** | Knowledge derived from AI must be explicitly labeled and never treated as authoritative |
| **KG-03** | Contradictions in knowledge must be resolved by the Chief Architect |
| **KG-04** | Knowledge Graph edges represent relationships defined by the Formula Registry |

---

## 7. VERSION GOVERNANCE

### 7.1 Version Hierarchy

```
Golden Master Version: GM-<NNN>           (e.g., GM-007, GM-008)
    │
    ├── Architecture Version: X.Y.Z       (e.g., 1.2.0)
    │
    ├── Calibration Version: X.Y.Z        (e.g., 1.0.0)
    │
    ├── Formula Registry Version: X.Y.Z   (e.g., 1.0.0)
    │
    ├── Question Catalog Version: X.Y.Z   (e.g., 1.0.0)
    │
    └── Component Versions: X.Y.Z         (per module)
```

### 7.2 Version Bump Rules

| Component | MAJOR Trigger | MINOR Trigger | PATCH Trigger |
|-----------|---------------|---------------|---------------|
| **Golden Master** | New milestone (GM-NNN) | — | — |
| **Architecture** | Breaking change to API or data contracts | New module or layer | Clarification or fix |
| **Calibration** | Changes that alter result interpretation | New constants or domains | Bug fix or precision |
| **Formula Registry** | Breaking change to formula interface | New formula added | Formula bug fix |
| **Question Catalog** | New domain or question type | Question added | Question text fix |

### 7.3 Version Recording

| Rule | Description |
|------|-------------|
| **VG-01** | Every consultation snapshot records all active versions at creation time |
| **VG-02** | Every engine output records the formula and calibration versions used |
| **VG-03** | Version changes are recorded in the audit trail |
| **VG-04** | Old versions remain available for consultation history consistency |

---

## 8. CHANGE MANAGEMENT

### 8.1 Change Classification

| Change Type | Process | Approval Required | Example |
|-------------|---------|-------------------|---------|
| **Type A: Freeze Exception** | Full governance review | Chief Architect | Modify an engine or formula |
| **Type B: Architecture Change** | ADR + Architecture Review | Chief Architect | New layer, new API contract |
| **Type C: Feature Addition** | Feature Approval Workflow | Chief Architect | New module, new capability |
| **Type D: Enhancement** | Standard PR + Review | Senior Developer | Improve existing feature |
| **Type E: Bug Fix** | Standard PR + Tests | Developer | Fix defect, no behavior change |
| **Type F: Documentation** | Direct commit or PR | Self-review | Update docs, fix typos |

### 8.2 Change Impact Analysis

Every Type A, B, or C change must include:

1. **Scope**: What modules are affected?
2. **Backward Compatibility**: Will existing consultations be affected?
3. **Migration**: What migration is required (if any)?
4. **Testing**: What tests validate the change?
5. **Documentation**: What docs need updating?
6. **Risk**: What could go wrong?

### 8.3 Change Window

| Change Type | Merge Window | Deployment |
|-------------|-------------|------------|
| **Type A** | After full governance review | Planned deployment window |
| **Type B** | After ADR approval | Planned deployment window |
| **Type C** | After feature approval | At milestone completion |
| **Type D** | Any time | Continuous |
| **Type E** | Any time (emergency) | Continuous |

---

## 9. BACKWARD COMPATIBILITY

### 9.1 Compatibility Guarantees

| Rule | Description |
|------|-------------|
| **BC-01** | All existing consultations must produce identical deterministic outputs after any change |
| **BC-02** | API contracts are versioned; breaking changes require a new API version |
| **BC-03** | Store contracts (Zustand stores, repository schemas) are additive — fields may be added, never removed |
| **BC-04** | Frontend components must render existing consultation data without modification |

### 9.2 Compatibility Testing

| Rule | Description |
|------|-------------|
| **BC-05** | Every change must pass backward compatibility tests against a golden set of existing consultations |
| **BC-06** | Golden set consultations are stored in `backend/tests/fixtures/golden_consultations/` |
| **BC-07** | Golden set is expanded when new consultation types are introduced |
| **BC-08** | Backward compatibility test failure blocks merge |

### 9.3 Breaking Change Process

If a breaking change is unavoidable:

1. Document the breaking change with full impact analysis
2. Propose migration path for existing consultations
3. Chief Architect approval required
4. New API/store version created
5. Old version maintained for existing consultations
6. Migration tool provided for affected consultations
7. Decision Register entry created

---

## 10. MIGRATION RULES

### 10.1 When Migration is Required

| Trigger | Migration Type | Automation |
|---------|---------------|------------|
| Repository schema change | Data migration | Automated script |
| Calibration version change | Re-evaluation | Optional (consultation retains old version) |
| Formula version change | Re-calculation | Optional (consultation retains old version) |
| API version change | Client update | Manual (breaking) or auto (non-breaking) |

### 10.2 Migration Rules

| Rule | Description |
|------|-------------|
| **MG-01** | Every migration must have a rollback plan |
| **MG-02** | Migrations are tested against the golden consultation set before production |
| **MG-03** | Migration scripts are versioned and stored in `backend/scripts/migrations/` |
| **MG-04** | Data is backed up before any migration |
| **MG-05** | Migration completion is verified and recorded |

---

## 11. FEATURE APPROVAL WORKFLOW

### 11.1 Workflow Stages

```
PROPOSAL ──→ DISCOVERY ──→ ARCHITECTURE ──→ EXECUTION ──→ VALIDATION ──→ GIT
   │            │              │                │              │            │
   │            │              │                │              │            │
   ▼            ▼              ▼                ▼              ▼            ▼
Document    Repository     Architecture    Implementation   Build/Test    Commit
feature     scan for       design +        (code,          verification  + Tag +
request     existing       ADR if          components,     + integration Push
            artifacts      required        modules)        testing
```

### 11.2 Stage Gates

| Gate | Criteria | Approval |
|------|----------|----------|
| **PROPOSAL → DISCOVERY** | Feature clearly defined; scope documented | Chief Architect |
| **DISCOVERY → ARCHITECTURE** | Repository scan complete; no conflicts found | Chief Architect |
| **ARCHITECTURE → EXECUTION** | Architecture approved; ADR (if required) created | Chief Architect |
| **EXECUTION → VALIDATION** | Build passing; TypeScript clean; tests passing | Automated |
| **VALIDATION → GIT** | All tests pass; backward compatibility verified | Chief Architect |

### 11.3 Phase Authorization Required

| Rule | Description |
|------|-------------|
| **FA-01** | Each phase must be explicitly authorized before work begins |
| **FA-02** | No work may begin on a subsequent phase until the current phase is authorized |
| **FA-03** | Phase authorization is recorded as a Decision Register entry |
| **FA-04** | Unauthorized work is treated as a governance violation |

---

## 12. ENGINEERING REVIEW WORKFLOW

### 12.1 Review Requirements

| Change Type | Reviewers Required | Checklist |
|-------------|-------------------|-----------|
| **Freeze Exception (A)** | Chief Architect + 2 Senior | Full governance checklist |
| **Architecture Change (B)** | Chief Architect + 1 Senior | ADR + impact analysis |
| **Feature Addition (C)** | Chief Architect + 1 Senior | Feature checklist |
| **Enhancement (D)** | 1 Senior Developer | Standard PR checklist |
| **Bug Fix (E)** | Self-review or 1 peer | Test verification |
| **Documentation (F)** | Self-review | Readability |

### 12.2 Pull Request Checklist

- [ ] Build passes (`npm run build`)
- [ ] TypeScript clean (`npx tsc --noEmit`)
- [ ] Tests pass (relevant test suites)
- [ ] No unused imports or variables
- [ ] No implicit `any` types
- [ ] Backward compatibility verified
- [ ] No modifications to frozen modules
- [ ] Documentation updated if applicable
- [ ] Commit message follows format

---

## 13. RELEASE GOVERNANCE

### 13.1 Release Types

| Release Type | Trigger | Process |
|-------------|---------|---------|
| **Milestone Release** | GM milestone completion | Full governance: freeze, audit, tag, report |
| **Patch Release** | Bug fix or minor enhancement | Standard PR + release notes |
| **Hotfix Release** | Critical production issue | Emergency Hotfix Process (section 20) |

### 13.2 Milestone Release Process

```
1. FEATURE FREEZE: No new features after this point
2. FINAL BUILD: Full build and test suite
3. REPOSITORY AUDIT: Hygiene check, dead code, configs
4. BACKWARD COMPAT: Golden set verification
5. DOCUMENTATION: Update PROJECT_STATUS_MASTER, ROADMAP
6. GIT TAG: Annotated tag with milestone identifier
7. RELEASE REPORT: Final Freeze Report
8. CHIEF ARCHITECT CERTIFICATION: Formal sign-off
```

### 13.3 Release Artifacts

| Artifact | Location | Required |
|----------|----------|----------|
| Final Freeze Report | `docs/status/GM-NNN_FINAL_FREEZE_REPORT.md` | ✅ |
| Release Candidate Audit | `GM-NNN_RELEASE_CANDIDATE_AUDIT.md` | ✅ |
| Module Inventory (updated) | Freeze Report | ✅ |
| Git Tag | `gm-NNN-*` | ✅ |
| Updated Roadmap | `GM-NNN_MASTER_DEVELOPMENT_ROADMAP.md` | If planning done |

---

## 14. QUALITY GATES

### 14.1 Build Gates

| Gate | Criteria | Automated |
|------|----------|-----------|
| **TypeScript Compilation** | Zero errors (`tsc -b` and `tsc --noEmit`) | ✅ |
| **Frontend Build** | Successful (`npm run build`) | ✅ |
| **Backend Tests** | All tests passing (critical path) | ✅ |
| **Linting** | Zero warnings (ESLint) | ✅ |
| **Bundle Size** | Within acceptable thresholds | ⚠️ (manual check) |

### 14.2 Architecture Gates

| Gate | Criteria | Automated |
|------|----------|-----------|
| **Frozen Module Integrity** | No modifications to frozen modules | ⚠️ (diff check) |
| **Store Contract Compliance** | Read/write patterns match architecture | ⚠️ (review) |
| **Single Source of Truth** | No duplicate data or calculations | ⚠️ (review) |
| **Backward Compatibility** | Golden set consultations produce identical outputs | ✅ (test) |

### 14.3 Quality Metrics

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| TypeScript errors | 0 | Build pipeline |
| Test coverage (critical path) | 100% | Coverage report |
| Build time | < 5 minutes | CI pipeline |
| Bundle size increase | < 10% per milestone | Build output |
| Dead code | 0 known unused files | Repository audit |

---

## 15. TESTING CONSTITUTION

### 15.1 Test Hierarchy

```
                    ┌──────────────────┐
                    │  GOLDEN MASTER   │ ← Backward compatibility
                    │  VERIFICATION    │    against known consultations
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  INTEGRATION     │ ← Module-to-module data flow
                    │  TESTS           │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  ENGINE TESTS    │ ← Individual engine correctness
                    │                  │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  UNIT TESTS      │ ← Function-level verification
                    └──────────────────┘
```

### 15.2 Test Requirements by Layer

| Layer | Test Type | Coverage Requirement | Golden Set Required |
|-------|-----------|---------------------|---------------------|
| **Layer 1: Core** | Unit + Engine + Golden Master | 100% critical path | ✅ |
| **Layer 2: Pipeline** | Integration + Golden Master | 100% data flow paths | ✅ |
| **Layer 3: Application** | Integration | Key workflows | ⚠️ |
| **Layer 4: Presentation** | Component + E2E | Key user journeys | — |

### 15.3 Testing Rules

| Rule | Description |
|------|-------------|
| **TC-01** | Every engine must have a test suite that validates deterministic outputs |
| **TC-02** | Golden set tests must pass before any merge to `main` |
| **TC-03** | Tests are run in CI pipeline; failing tests block merge |
| **TC-04** | Test data fixtures are version-controlled |
| **TC-05** | New features must include tests |
| **TC-06** | Bug fixes must include a regression test |

---

## 16. DOCUMENTATION CONSTITUTION

### 16.1 Documentation Categories

| Category | Location | Primary Document | Update Trigger |
|----------|----------|-----------------|----------------|
| **System Architecture** | `docs/architecture/` | `SYSTEM_ARCHITECTURE.md` | Architecture change |
| **Project Status** | `docs/status/` | `PROJECT_STATUS_MASTER.md` | Milestone completion |
| **Governance** | `docs/governance/` | `DECISION_REGISTER.md` | Governance decision |
| **Knowledge** | `docs/knowledge/` | Engine-specific packages | Engine change |
| **Implementation** | `docs/engineering/` | Phase reports | Phase completion |
| **Roadmap** | Root | `GM-NNN_MASTER_DEVELOPMENT_ROADMAP.md` | GM milestone start |

### 16.2 Documentation Rules

| Rule | Description |
|------|-------------|
| **DC-01** | Every module must have a documented purpose, interface, and dependencies |
| **DC-02** | Architecture decisions must produce an ADR |
| **DC-03** | Governance decisions must produce a Decision Register entry |
| **DC-04** | Milestone completion must produce a Final Freeze Report |
| **DC-05** | Documentation is version-controlled alongside code |
| **DC-06** | Contradictory documentation must be resolved immediately |

### 16.3 Documentation Quality Standards

| Standard | Description |
|----------|-------------|
| **Accuracy** | Document reflects current implementation state |
| **Completeness** | All required sections are present |
| **Consistency** | No contradictions with other documents |
| **Traceability** | References to source code, ADRs, and decisions |
| **Currency** | Updated when underlying implementation changes |

---

## 17. TECHNICAL DEBT POLICY

### 17.1 Debt Classification

| Severity | Definition | Response Timeline | Examples |
|----------|-----------|-------------------|----------|
| **Critical** | Blocks production deployment or causes data corruption | Fix immediately (hotfix) | Build failure, data loss risk |
| **High** | Degrades system reliability or security | Fix within current milestone | Memory leak, security vulnerability |
| **Medium** | Reduces developer productivity or code quality | Fix within next milestone | Unused code, deprecated patterns |
| **Low** | Cosmetic or convenience | Defer to future milestone | Naming inconsistencies, minor duplication |

### 17.2 Debt Management Rules

| Rule | Description |
|------|-------------|
| **TD-01** | Technical debt is documented in the Release Candidate Audit report |
| **TD-02** | Critical and High debt blocks milestone completion |
| **TD-03** | Medium debt is scheduled for the next milestone |
| **TD-04** | Low debt may be deferred indefinitely; recorded for visibility |
| **TD-05** | No new High or Critical debt may be introduced without explicit Chief Architect approval |

---

## 18. DEPRECATION POLICY

### 18.1 Deprecation Lifecycle

```
ACTIVE ──→ DEPRECATED ──→ REMOVED
   │            │             │
   │            │             │
   ▼            ▼             ▼
In use     Warning      Physically
           issued;       removed;
           replacement   all references
           available     updated
```

### 18.2 Deprecation Rules

| Rule | Description |
|------|-------------|
| **DP-01** | Deprecated components display a console warning referencing the replacement |
| **DP-02** | Deprecated components are documented in the Release Candidate Audit |
| **DP-03** | Deprecated components remain functional for at least one full milestone |
| **DP-04** | Removal happens in the milestone after deprecation |
| **DP-05** | Removal must include migration guidance for any affected consultations |

### 18.3 Deprecation Timeline

| Milestone | Action |
|-----------|--------|
| **GM-NNN** | Component marked DEPRECATED; warning issued; replacement available |
| **GM-NNN+1** | Component removed; all references updated; migration complete |

---

## 19. FREEZE POLICY

### 19.1 Freeze Levels

| Level | Scope | Trigger | Duration |
|-------|-------|---------|----------|
| **Permanent Freeze** | Layer 1 (engines, formulas, calibration, catalog) | GM-007 completion | Forever |
| **Milestone Freeze** | All modules completed in the current milestone | Milestone completion | Until next milestone |
| **Release Freeze** | All code | Before release | During release process |
| **Emergency Freeze** | All code | Critical issue | Until resolved |

### 19.2 Freeze Exception Process

A permanent freeze exception requires:

1. **Documentation**: Why the freeze must be broken
2. **Impact Analysis**: What existing consultations are affected
3. **Migration Plan**: How affected consultations will be handled
4. **Backward Compatibility**: How existing outputs are preserved
5. **Chief Architect Approval**: Formal documented approval
6. **Decision Register**: Permanent record of the exception
7. **Version Bump**: All affected versions incremented
8. **Freeze Report Update**: Freeze status updated

### 19.3 Freeze Rules

| Rule | Description |
|------|-------------|
| **FZ-01** | Layer 1 (Deterministic Core) is permanently frozen as of GM-007 |
| **FZ-02** | Freeze exceptions require Chief Architect approval |
| **FZ-03** | Freeze exceptions are extraordinary — not routine |
| **FZ-04** | Every freeze exception is recorded in the Decision Register for permanent accountability |

---

## 20. EMERGENCY HOTFIX POLICY

### 20.1 Hotfix Definition

A hotfix is an emergency change to fix:

- Data corruption or loss
- Security vulnerability (actively exploited)
- Critical build failure blocking all development
- Production outage

### 20.2 Hotfix Process

```
1. DETECTION: Issue identified and severity assessed
       │
2. NOTIFICATION: Chief Architect notified immediately
       │
3. ISOLATION: Issue scoped; affected modules identified
       │
4. FIX: Minimal fix applied on hotfix branch
       │
5. VERIFICATION: Build, tests, backward compatibility verified
       │
6. APPROVAL: Chief Architect approves emergency merge
       │
7. MERGE: Hotfix merged to main (bypass standard workflow)
       │
8. POST-MORTEM: Root cause analysis within 24 hours
       │
9. PREVENTION: Process or code change to prevent recurrence
       │
10. DECISION REGISTER: Hotfix recorded for permanent record
```

### 20.3 Hotfix Rules

| Rule | Description |
|------|-------------|
| **HF-01** | Hotfixes are for critical issues only — never for features or enhancements |
| **HF-02** | Hotfixes are the minimum change necessary to resolve the issue |
| **HF-03** | Hotfixes must not introduce new features or modify frozen modules |
| **HF-04** | Every hotfix produces a post-mortem within 24 hours |
| **HF-05** | Repeated hotfixes for the same area trigger a formal review |
| **HF-06** | Hotfixes are recorded in the Decision Register |

---

## 21. COMPLIANCE CHECKLIST

### Milestone Start Checklist

- [ ] Roadmap approved by Chief Architect
- [ ] Architecture review complete
- [ ] Dependencies identified and documented
- [ ] Feature approval workflow initiated
- [ ] BKL backlog items created

### Phase Authorization Checklist

- [ ] Previous phase gates passed
- [ ] Architecture constraints verified
- [ ] Frozen modules confirmed untouched
- [ ] Chief Architect authorization received

### Implementation Checklist

- [ ] Build passes (frontend + backend)
- [ ] TypeScript zero errors
- [ ] Tests pass
- [ ] No modifications to frozen modules
- [ ] Backward compatibility verified
- [ ] Code review complete

### Milestone Completion Checklist

- [ ] All phase gates passed
- [ ] Final freeze report generated
- [ ] Release candidate audit complete
- [ ] Git tag created
- [ ] Documentation updated
- [ ] Technical debt documented
- [ ] Chief Architect certification received

---

## 22. DEFINITION OF DONE

A Golden Master milestone is **DONE** when:

1. **All features implemented**: Every BKL backlog item completed
2. **Build passes**: `npm run build` and `npx tsc --noEmit` zero errors
3. **Tests pass**: All critical path tests pass; golden set verified
4. **Backward compatibility**: Existing consultations produce identical outputs
5. **Architecture intact**: No violations of frozen modules or layer boundaries
6. **Repository clean**: Hygiene audit passed; dead code removed or archived
7. **Documentation current**: All governance documents updated
8. **Git tagged**: Annotated tag with milestone identifier
9. **Freeze report**: Final freeze report published
10. **Chief Architect certified**: Formal sign-off recorded
11. **Decision Register updated**: All decisions recorded
12. **Release Candidate Audit**: All gates passed

---

## AMENDMENT PROCESS

This Constitution may be amended only through the following process:

1. Proposed amendment documented with rationale and impact analysis
2. Amendment reviewed by Chief Architect
3. If approved, Constitution version incremented (MAJOR for new rules, MINOR for clarifications)
4. Amendment recorded in the Decision Register
5. All governed processes re-validated against amended Constitution

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         AP-003 COMPLETE                                      ║
║                                                                              ║
║    Document: GM-008_SYSTEM_GOVERNANCE_CONSTITUTION.md                       ║
║    Version: 1.0.0                                                            ║
║    Status: ACTIVE — Effective immediately                                    ║
║                                                                              ║
║    Sections: 22 (Architecture through Definition of Done)                   ║
║    Rules: 120+ governance rules across all domains                          ║
║    Governs: Entire Golden Master Platform (GM-001 through GM-010+)          ║
║                                                                              ║
║    This is the supreme governance document.                                 ║
║    All other constitutions, policies, and processes must comply.            ║
║                                                                              ║
║    No code generated. No repository modified.                               ║
║    Architecture governance only.                                             ║
║                                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```