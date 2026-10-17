# Overwatcher Worker Contract

> **Contract ID**: `{CONTRACT_UUID}`  
> **Target Domain**: `{DOMAIN_NAME}`  
> **Assigned Worker**: `{WORKER_NAME_OR_TYPE}`  
> **Status**: `ASSIGNED` | `UNDER_AUDIT` | `REWORK_REQUIRED` | `VERIFIED`

---

## 1. Scope & File Boundaries (Strictly Disjoint)
The assigned worker is strictly authorized to inspect and modify **only** the following paths. Touching any file outside this list constitutes an automatic audit failure.

### Authorized Write Targets
- `{path/to/target/file_1}`
- `{path/to/target/file_2}`
- `{tests/test_target_file.py}`

### Read-Only Reference Context
- `{path/to/reference/interface.ts}`
- `{path/to/database/schema.sql}`

---

## 2. Deliverables & Definition of Done
The work is considered ready for Phase 3 Prosecutorial Cross-Examination only when all criteria below are deterministically met:

1. **Functional Implementation**:
   - `{Specific requirement 1}`
   - `{Specific requirement 2}`
2. **Automated Test Coverage**:
   - New unit and integration tests written and passing.
   - Genuine assertions covering happy paths and failure/edge conditions (no trivial `assert True`).
3. **Static Analysis & Hygiene**:
   - Zero linter or type-checker errors.
   - Clean git diff with zero leftover debug prints, temporary files, or commented-out code.

---

## 3. Forbidden Actions (Zero Tolerance)
Any of the following infractions will trigger an immediate **Rejection Order**:
- ❌ Modifying files outside the authorized target list.
- ❌ Introducing mock fallbacks or silent error swallowing (`try...except: pass`).
- ❌ Committing hardcoded credentials, mock secrets, or dummy tokens.
- ❌ Altering existing public APIs or breaking contracts with other domains.
- ❌ Submitting conversational claims without verifiable execution output.

---

## 4. Verification Command
The worker must execute and verify the following command before reporting completion:
```bash
{deterministic_verification_command}
```
