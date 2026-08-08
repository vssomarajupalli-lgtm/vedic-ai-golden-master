# Repository Policy

# Samartha Vedic AI — Golden Master

## Repository Development Policy

**Version:** v1.0.0

**Applies to:** All development on the Samartha Vedic AI Golden Master repository.

---

## 1. Main Branch Policy

- `main` is **production**.
- **No direct development** is permitted on `main`.
- Commits to `main` are restricted to:
  - Approved production release commits.
  - Merge commits from reviewed feature branches.
  - Release baseline documentation artifacts.
- `main` must always be deployable and must always reflect a verified, deterministic state.

---

## 2. Feature Branch Policy

Every development task starts from a dedicated branch, never from `main` directly.

Branch naming:

```
GM-XXX-feature-name
feature/<feature-name>
```

Rules:

- Create the branch from the current production baseline (`main`).
- Keep the branch scoped to one feature or task.
- Keep the branch synchronized with `main` before merge.
- Delete the branch after a successful merge.

---

## 3. Merge Policy

A branch may be merged into `main` **only after** all of the following are satisfied:

- **Code Review** — changes reviewed and approved.
- **Regression Verification** — protected modules verified unchanged.
- **Testing** — backend test suite and frontend build pass.

Scope verification is mandatory before merge:

- Only the intended files may be modified.
- No protected module may be altered.
- Any unexpected file change stops the merge immediately.

---

## 4. Commit Policy

- Prefer **small, logical commits** that each represent one coherent change.
- Write **meaningful commit messages** describing what changed and why.
- Follow the established milestone message convention, e.g.:

```
GM-XXXX: Short descriptive title
```

- Never commit secrets, build artifacts, or unrelated changes.
- Commit only after the working tree scope has been verified.

---

## 5. Release Policy

- **Tag every production release** with an annotated tag.
- Tag name convention:

```
GM-XXXX
```

- Tag message includes the release name and purpose.
- The tag must point to the exact commit that becomes the production baseline.
- Tags are **permanent and immutable** — they are never deleted, rewritten, or retargeted.
- Push the tag to `origin` so it is available as a recovery point.

---

## 6. Rollback Policy

- Rollback is permitted **only to production tags**.
- Select the nearest production tag at or before the broken commit.
- Restore the repository to that tag and verify the baseline.
- No rollback to arbitrary branch points, unreleased commits, or feature branches.
- Every rollback must be recorded and verified against the regression requirement.

---

## 7. Protected Areas

The following are **frozen** and must not be modified without an approved engineering change:

- Astrology Engines
- Pipeline Runner
- Formula Registry
- Formula Verification
- Results Calculations
- Consultation Calculations
- Current Gochara
- Planet Strength
- House Strength
- MD / AD / PD
- Swiss Ephemeris
- Calibration
- Knowledge Store (backend)
- Backend Report JSON Schema
- Report DTOs

---

## 8. Regression Requirement

Every feature merge must verify that the following remain identical/unchanged against the last production baseline:

- Results
- Formula Verification
- Consultation
- Current Gochara
- Questionnaire
- Knowledge Graph
- Print Framework

Regression verification must use the deterministic baseline comparison and must report a **PASS** before merge is approved.
