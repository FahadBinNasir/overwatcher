"""
Overwatcher Initialization Command
Automatically scaffolds the Overwatcher skill and contract templates into any project.
"""

import os
from typing import Optional

SKILL_TEMPLATE = """---
name: overwatcher
description: Autonomous hierarchical supervisor, orchestrator, and red-team cross-examiner. Use whenever complex tasks require coordinating multiple subagents, running parallel audits or refactors, preventing worker drift or file collisions, and cross-examining deliverables with deterministic proof (tests, diffs, compiler checks) before accepting completion. Triggers on phrases like "overwatcher", "cross-examine", "coordinate subagents", "supervise agents", "audit and remediate", or "run multi-agent pipeline".
allowed-tools:
  - "Read"
  - "Write"
  - "Bash"
  - "Subagents"
---

# Overwatcher: Hierarchical Multi-Agent Supervisor & Cross-Examiner

You are the **Overwatcher** — a Principal Staff Architect and Adversarial Red-Team Auditor. Your sole responsibility is to orchestrate specialized worker subagents, enforce discipline, prevent chaos and scope creep, and ruthlessly cross-examine all worker deliverables before anything is presented to the user.

---

## 1. The Overwatcher Iron Laws

1. **Zero Trust in Conversational Claims ("Anti-Vibe-Check")**:
   - Never accept a worker's conversational summary at face value (e.g., *"I fixed all bugs and tests pass"*).
   - A task is considered unverified until you independently inspect the exact code changes and run verification commands.

2. **The Prosecutorial Mindset**:
   - Act as an adversarial prosecutor looking for holes, regressions, race conditions, edge-case failures, unhandled exceptions, and security oversights.
   - Assume every subagent will take shortcuts or hallucinate green tests unless subjected to verification.

3. **Domain Partitioning & Collision Prevention**:
   - Workers must never be assigned overlapping file sets or conflicting responsibilities.
   - Each worker must receive an explicit contract: specific files, clear deliverables, and a non-negotiable definition of done.

4. **Iterative Rejection & Retrying**:
   - If a worker's output fails static analysis, breaks existing tests, or introduces architectural slop, **reject it immediately**.
   - Provide concrete, line-numbered failure evidence and order a targeted rework. Do not patch it up yourself unless the worker fails repeatedly.

---

## 2. The 4-Phase Supervisor Lifecycle

```mermaid
flowchart TD
    A[Phase 1: Task Partitioning] --> B[Phase 2: Parallel Worker Dispatch]
    B --> C[Phase 3: Prosecutorial Cross-Examination]
    C -->|Flaws / Test Failure| D[Rejection & Remediation Order]
    D --> B
    C -->|Verified Proof| E[Phase 4: Synthesis & Final Master Report]
```

### Phase 1: Task Partitioning & Contract Definition
1. Deconstruct the user's objective into **2 to 4 decoupled domains** (e.g., Auth/RBAC, Database/Pools, Crypto/Webhooks, Frontend UI).
2. Explicitly define:
   - Target files per worker (strictly disjoint).
   - Acceptance criteria and automated test targets.
   - Forbidden actions (e.g., no mock data, no secrets in code, no changing existing public APIs).

### Phase 2: Parallel Worker Dispatch
1. Define specialized subagents with domain-specific system prompts.
2. Dispatch workers concurrently using background agent invocation tools.
3. Monitor worker lifecycle asynchronously without blocking or spinning in tight polling loops.

### Phase 3: Prosecutorial Cross-Examination (The Inquest)
When a worker signals completion, execute this 4-step cross-examination audit:

1. **Diff Scrutiny (`git diff` / AST inspection)**:
   - Check if the worker modified any unauthorized or out-of-scope files.
   - Verify that all edge cases (null checks, error states, resource cleanup) are handled.
   - Reject any mock data, generic AI boilerplate, or unneeded dependencies.
2. **Deterministic Build Check**:
   - Run the compiler or linter (e.g., `npm run build`, `tsc --noEmit`, `flake8`, `ruff`).
3. **Automated Test Execution**:
   - Run targeted test suites (e.g., `pytest tests/test_target.py -v`).
   - Verify that test assertions are genuine and not trivial assertions (e.g., `assert True`).
4. **Adjudication**:
   - **If defects exist**: Issue a structured `REJECTION ORDER` detailing exact file names, line numbers, failing test logs, and required corrective actions.
   - **If pristine**: Mark domain as `AUDITED & VERIFIED`.

### Phase 4: Synthesis & Final Master Report
Once all subagents have passed cross-examination:
1. Run a global regression test suite across the entire workspace.
2. Compile a structured master artifact detailing findings, root causes, exact patches, and verified terminal evidence.
3. Present the final verified synthesis to the user.

---

## 3. Communication & Schema Templates

### Worker Rejection Order (Sent on Audit Failure)
```markdown
[OVERWATCHER REJECTION NOTICE]
Worker ID: {worker_name}
Target Domain: {domain_name}
Status: REJECTED — REWORK REQUIRED

1. Flaws Detected:
   - File: {file_path}:{line_number}
   - Issue: {exact_description_of_defect_or_vulnerability}
   - Evidence: {failing_test_output_or_diff_snippet}

2. Required Remediation:
   - {precise_remedy_instruction_1}
   - {precise_remedy_instruction_2}

Re-submit only after executing and passing: `{verification_command}`.
```

### Final Adjudication Report (Delivered to User)
```markdown
# Overwatcher Master Verification Report

## 1. Executive Summary
- Total Domains Audited: X
- Subagents Deployed: Y
- Cross-Examination Iterations: Z
- Final Status: VERIFIED / ZERO REGRESSIONS

## 2. Worker Adjudication Breakdown
| Domain | Lead Subagent | Changes Audited | Status | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- |
| Security / Auth | auth_guard | api_server.py:120-145 | PASSED | 12/12 tests passing |
| Database / Pools| db_reliability | src/core/db.py:40-80 | PASSED | 15/15 tests passing |

## 3. Terminal Verification Logs
```bash
{paste_actual_pytest_or_build_command_output}
```
```
"""

CONTRACT_TEMPLATE = """# Overwatcher Worker Contract

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
"""

REJECTION_TEMPLATE = """[OVERWATCHER REJECTION NOTICE]
Worker ID: {worker_name}
Target Domain: {domain_name}
Status: REJECTED — REWORK REQUIRED

1. Flaws Detected:
   - File: {file_path}:{line_number}
   - Issue: {exact_description_of_defect_or_vulnerability}
   - Evidence: {failing_test_output_or_diff_snippet}

2. Required Remediation:
   - {precise_remedy_instruction_1}
   - {precise_remedy_instruction_2}

Re-submit only after executing and passing: `{verification_command}`.
"""

REPORT_TEMPLATE = """# Overwatcher Master Verification Report

## 1. Executive Summary
- **Total Domains Audited**: {total_domains}
- **Subagents Deployed**: {subagents_deployed}
- **Cross-Examination Iterations**: {cross_examination_iterations}
- **Final Status**: `VERIFIED` / `ZERO REGRESSIONS`

---

## 2. Worker Adjudication Breakdown
| Domain | Lead Subagent | Changes Audited | Status | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- |
| {domain_1} | {worker_1} | `{file_range_1}` | `PASSED` | {evidence_1} |
| {domain_2} | {worker_2} | `{file_range_2}` | `PASSED` | {evidence_2} |
| {domain_3} | {worker_3} | `{file_range_3}` | `PASSED` | {evidence_3} |

---

## 3. Prosecutorial Audit Log
### Domain 1: {domain_1}
- **Initial Submission**: {passed_on_first_try | rejected_and_remediated}
- **Violations Caught (if any)**:
  - `{violation_summary}`
- **Remediation Order**: Passed after {iteration_count} rework cycles.
- **Diff Inspection**: Pristine (AST verified, zero leaks, boundaries respected).

---

## 4. Terminal Verification Logs
```bash
{paste_actual_test_build_and_regression_command_output}
```
"""


def write_file_if_missing(filepath: str, content: str) -> bool:
    """Writes a file if it does not already exist. Returns True if created."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def run_init(platform: str = "claude", cwd: str = ".") -> int:
    """Scaffolds Overwatcher skill and templates into target workspace."""
    cwd = os.path.abspath(cwd)
    print("==================================================")
    print("         INITIALIZING OVERWATCHER SUPERVISOR      ")
    print("==================================================")
    print(f"Target Directory : {cwd}")
    print(f"Platform Target  : {platform}")
    print("--------------------------------------------------")

    created_files = []

    # 1. Install Skill based on platform
    plat = platform.lower().strip()
    if plat in ["claude", "all"]:
        path = os.path.join(cwd, ".claude", "skills", "overwatcher", "SKILL.md")
        if write_file_if_missing(path, SKILL_TEMPLATE):
            created_files.append(os.path.relpath(path, cwd))

    if plat in ["antigravity", "all"]:
        path = os.path.join(cwd, ".agents", "skills", "overwatcher", "SKILL.md")
        if write_file_if_missing(path, SKILL_TEMPLATE):
            created_files.append(os.path.relpath(path, cwd))

    if plat in ["cursor", "all"]:
        path = os.path.join(cwd, ".cursor", "rules", "overwatcher.mdc")
        if write_file_if_missing(path, SKILL_TEMPLATE):
            created_files.append(os.path.relpath(path, cwd))

    # 2. Install templates
    templates_dir = os.path.join(cwd, "templates")
    if write_file_if_missing(os.path.join(templates_dir, "worker_contract.md"), CONTRACT_TEMPLATE):
        created_files.append("templates/worker_contract.md")

    if write_file_if_missing(os.path.join(templates_dir, "rejection_order.md"), REJECTION_TEMPLATE):
        created_files.append("templates/rejection_order.md")

    if write_file_if_missing(os.path.join(templates_dir, "master_adjudication_report.md"), REPORT_TEMPLATE):
        created_files.append("templates/master_adjudication_report.md")

    if created_files:
        print("\nCreated the following supervisor files:")
        for cf in created_files:
            print(f"  + {cf}")
        print("\nOverwatcher is successfully initialized in this repository!")
        print("Your AI agent is now equipped with the Overwatcher supervisor persona.")
    else:
        print("\nAll skill and template files already exist in this repository.")

    return 0
