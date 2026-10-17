<div align="center">

# <img src="assets/icons/logo.svg" width="32" height="32" align="center" alt="" /> Overwatcher

**A supervisor skill for multi-agent coding workflows. Splits work into disjoint file domains, then rejects any worker output it can't verify by running it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-2563eb.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)

[Quick start](#quick-start) · [How it works](#how-it-works) · [CLI](#cross-examiner-cli) · [Examples](#examples) · [Contributing](#contributing)

</div>

---

## Why

Unsupervised agent pipelines tend to fail in three ways:

- **Drift:** workers edit files outside their task and break shared config.
- **Collisions:** parallel workers edit the same files and create merge conflicts.
- **False "done":** workers report "all tests pass" after deleting assertions, adding `assert True`, or wrapping errors in `except: pass`.

Overwatcher counters each:

| Failure | Defense |
| :-- | :-- |
| Drift | Per-worker contract listing authorized files; out-of-scope diffs are rejected |
| Collisions | Contracts are disjoint; no two workers share a file |
| False "done" | Claims are ignored. Diff, linters, and tests are run and checked |

---

## Quick start

Install as a skill (Claude Code shown; other platforms [below](#platform-install-paths)):

```bash
mkdir -p .claude/skills/overwatcher
cp SKILL.md .claude/skills/overwatcher/SKILL.md
```

Then ask your agent:

> Use the overwatcher skill to refactor auth and the DB layer in parallel.

The agent acts as supervisor: it partitions the task, dispatches workers, audits each result, and returns a verification report.

---

## How it works

```mermaid
flowchart TD
    A[1. Partition & contracts] --> B[2. Parallel dispatch]
    B --> C[3. Cross-examination]
    C -->|fail| D[Rejection notice]
    D --> B
    C -->|pass| E[4. Synthesis & report]
```

### Rules

1. **No trust in summaries.** Output is unverified until inspected and executed.
2. **Adversarial review.** Look for edge cases, race conditions, leaks, and swallowed errors.
3. **Disjoint ownership.** Workers never touch overlapping files.
4. **Reject, don't patch.** Send failures back with line-numbered proof. The supervisor never fixes worker code itself.

### Phases

**1. Partition.** Split the goal into 2–4 independent domains (e.g. Auth, DB, API, UI). Give each worker a [contract](templates/worker_contract.md):
- *Authorized targets:* exact file paths
- *Acceptance criteria:* deliverables and test targets
- *Forbidden:* mock fallbacks, leaked secrets, API breakage

**2. Dispatch.** Start workers concurrently with domain-specific prompts. Wait on completion signals; don't poll.

**3. Cross-examine.** When a worker reports done:
1. **Diff:** confirm changes stay inside the contract; reject mocks, boilerplate, and new dependencies.
2. **Build:** run the project's compilers and linters (`tsc --noEmit`, `ruff`, `flake8`, ...).
3. **Test:** run the targeted tests; check that assertions are real.
4. **Verdict:** `REJECTION NOTICE` on any defect, otherwise `AUDITED & VERIFIED`.

**4. Synthesize.** Run the full regression suite, then produce the [master report](templates/master_adjudication_report.md) with logs.

---

## Cross-examiner CLI

`scripts/cross_examiner.py` runs the deterministic checks (file boundaries, banned patterns, test command) without an LLM.

```bash
python scripts/cross_examiner.py \
  --worker "auth_guard" \
  --domain "Authentication" \
  --allowed-files "src/core/auth.py" "tests/test_auth.py" \
  --verify-cmd "pytest tests/test_auth.py -v"
```

| Flag | Purpose |
| :-- | :-- |
| `--worker` | Worker ID, used in reports |
| `--domain` | Domain name |
| `--allowed-files` | Files the worker may change |
| `--verify-cmd` | Command that must pass |

Run its tests:

```bash
python tests/test_cross_examiner.py
```

---

## Platform install paths

| Platform | Target |
| :-- | :-- |
| Claude Code | `.claude/skills/overwatcher/SKILL.md` |
| Antigravity | `.agents/skills/overwatcher/SKILL.md` |
| Cursor | `.cursor/rules/overwatcher.mdc` |
| Cline / Roo-Code | `.clinerules` or `.roomodes` |
| OpenHands | `.openhands/microagents/overwatcher.md` |
| LangGraph / CrewAI | Call `scripts/cross_examiner.py` from a supervisor node |

---

## Message formats

<details>
<summary><b>Rejection notice</b> (sent to a worker on failure)</summary>

```markdown
[OVERWATCHER REJECTION NOTICE]
Worker ID: {worker_name}
Target Domain: {domain_name}
Status: REJECTED — REWORK REQUIRED

1. Flaws Detected:
   - File: {file_path}:{line_number}
     Issue: {defect}
     Evidence: {failing_test_output_or_diff_snippet}

2. Required Remediation:
   - {instruction}

Re-submit only after passing: `{verification_command}`.
```
</details>

<details>
<summary><b>Master report</b> (delivered to the user)</summary>

```markdown
# Overwatcher Master Verification Report

## Summary
- Domains audited: 2
- Workers: 2
- Cross-examination rounds: 3
- Status: VERIFIED / ZERO REGRESSIONS

## Breakdown
| Domain | Worker | Files | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| Auth | auth_guard | src/core/auth.py | PASSED | 8/8 tests |
| DB | db_reliability | src/core/db.py | PASSED | 14/14 tests |
```
</details>

---

## Examples

| File | Shows |
| :-- | :-- |
| [sample_workflow.md](examples/sample_workflow.md) | End-to-end supervised refactor |
| [sample_worker_contract.md](examples/sample_worker_contract.md) | A filled-in contract |
| [sample_rejection_order.md](examples/sample_rejection_order.md) | A real rejection notice |
| [sample_adjudication_report.md](examples/sample_adjudication_report.md) | A passing report |

---

## Repository layout

```
SKILL.md              # skill spec
templates/            # contract, rejection, report templates
scripts/              # cross_examiner.py
tests/                # cross_examiner tests
examples/             # worked examples
assets/icons/         # logo
```

---

## Contributing

New audit rules, heuristics, and language support are welcome.

1. Fork and branch: `git checkout -b feature/audit-rule`
2. Add tests; run `python tests/test_cross_examiner.py`
3. Open a PR

---

## License

[MIT](LICENSE) © 2026 Fahad Bin Nasir
