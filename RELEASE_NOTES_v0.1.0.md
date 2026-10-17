## Overwatcher v0.1.0: Hierarchical Multi-Agent Supervisor & Adversarial Cross-Examiner

> **Autonomous supervisor, orchestrator, and red-team cross-examiner for multi-agent AI coding pipelines.**

Overwatcher solves the fundamental problem of agent drift, file collisions, and "conversational vibe-checks" by acting as an adversarial prosecutor. It enforces strict domain contracts and cross-examines all deliverables with deterministic proof before accepting completion.

---

### What's Included in v0.1.0

#### 1. Core Skill Specification (`SKILL.md`)
- **The 4 Overwatcher Iron Laws**: Zero Trust in Summaries ("Anti-Vibe-Check"), Prosecutorial Mindset, Disjoint Domain Ownership, and Iterative Rejection.
- **The 4-Phase Lifecycle**:
  1. *Task Partitioning & Contracts*: Splitting tasks into 2–4 decoupled domains with strictly disjoint file boundaries.
  2. *Parallel Worker Dispatch*: Non-blocking asynchronous worker orchestration.
  3. *Prosecutorial Cross-Examination*: AST & diff scrutiny, compiler checks, and targeted automated test execution.
  4. *Synthesis & Certification*: Global regression verification and master executive reporting.

#### 2. Standardized Communication & Contract Schemas (`templates/`)
- **`worker_contract.md`**: Contract template assigning disjoint target files, acceptance criteria, test targets, and strictly forbidden actions (no mocks, no secrets, no API breakage).
- **`rejection_order.md`**: Structured, line-numbered rejection notice dispatched to failing subagents ordering targeted rework.
- **`master_adjudication_report.md`**: Executive synthesis report compiling domain breakdown and verified terminal logs.

#### 3. Deterministic Cross-Examiner CLI (`scripts/cross_examiner.py`)
- Standalone Python 3.8+ command-line auditor with zero heavy external dependencies.
- **Boundary Verification**: Cross-references modified files against authorized glob patterns using `fnmatch`.
- **Anti-Pattern Slop Scanner**: Scans diffs for banned shortcuts:
  - Bare exception swallowing (`except: pass`, `except Exception: pass`, empty `catch`)
  - Trivial assertions (`assert True`, `assert 1 == 1`, `expect(true).toBe(true)`)
  - Leftover debuggers (`debugger`, `breakpoint()`)
- **Deterministic Test Verification**: Executes targeted test/build commands and captures failing output snippets.
- **Automated Rejection Formatting**: Automatically prints structured `[OVERWATCHER REJECTION NOTICE]` markdown on failure with exit code `1`.

#### 4. Reference Implementations & Worked Examples (`examples/`)
- `sample_workflow.md`: Realistic end-to-end trace showing an auth/database refactor, an anti-pattern catch, a rejection order, and final verification.
- `sample_worker_contract.md`: Production example of an active worker contract.
- `sample_rejection_order.md`: Production example of an issued rejection notice.
- `sample_adjudication_report.md`: Production example of a green master verification report.

#### 5. Automated CI/CD & Testing Matrix (`.github/workflows/`)
- **CI Test Suite**: Automated verification across Python 3.8, 3.9, 3.10, 3.11, and 3.12.
- **Automated Packaging**: Release workflow packaging `.tar.gz` and `.zip` distribution bundles.

---

### Quick Installation

```bash
# For Claude Code
mkdir -p .claude/skills/overwatcher
cp SKILL.md .claude/skills/overwatcher/SKILL.md

# For Antigravity
mkdir -p .agents/skills/overwatcher
cp SKILL.md .agents/skills/overwatcher/SKILL.md

# For Cursor
cp SKILL.md .cursor/rules/overwatcher.mdc
```

---

### Verification
- **Automated Tests**: 4/4 tests passing in `tests/test_cross_examiner.py`.
- **License**: MIT © 2026 Fahad Bin Nasir.
