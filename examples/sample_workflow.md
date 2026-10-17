# Overwatcher End-to-End Workflow Trace

This document illustrates how the **Overwatcher** orchestrates multiple subagents, enforces domain isolation, catches shortcuts, issues rejection notices, and outputs deterministically verified reports.

---

## The Scenario
The user requests a major infrastructure refactor:
1. Migrate the token auth module from HS256 to RS256 with key rotation.
2. Upgrade PostgreSQL pool handling from single connections to an asynchronous pool with health checks.

Without Overwatcher, single agents often cross file boundaries, introduce subtle mock fallbacks, or declare "everything is tested!" while tests are actually skipped or unasserted.

---

## Step 1: Task Partitioning & Contract Definition (Phase 1)
Overwatcher analyzes the codebase and deconstructs the request into **2 decoupled domains**:

1. **Domain 1: Security & Token Service**
   - **Lead Subagent**: `auth_guard`
   - **Authorized Files**: `src/core/auth.py`, `tests/test_auth_security.py`
   - **Contract**: `examples/sample_worker_contract.md`

2. **Domain 2: Database Connection Pool**
   - **Lead Subagent**: `db_reliability`
   - **Authorized Files**: `src/core/db.py`, `tests/test_connection_pool.py`
   - **Contract**: Disjoint targets, no overlap with auth.

---

## Step 2: Parallel Dispatch (Phase 2)
Overwatcher dispatches both agents in parallel:
```python
invoke_subagent([
    {"TypeName": "auth_guard", "Role": "Auth Hardener", "Prompt": contract_1},
    {"TypeName": "db_reliability", "Role": "DB Pool Engineer", "Prompt": contract_2}
])
```
Overwatcher suspends execution reactively and awaits notifications without busy loops.

---

## Step 3: Prosecutorial Cross-Examination (Phase 3)

### Incident 1: `auth_guard` Reports "Completed"
- `auth_guard` sends a message: *"I finished the RS256 migration and all tests pass with flying colors!"*
- **Overwatcher Action**: Anti-Vibe-Check.
  - Inspects `git diff src/core/auth.py`.
  - Discovers:
    ```python
    JWT_SECRET = os.getenv("AUTH_SECRET", "super-secret-default")
    ```
  - Inspects `tests/test_auth_security.py`.
  - Discovers:
    ```python
    def test_rs256_signature():
        # TODO: verify key
        assert True
    ```
- **Adjudication**: **INSTANT REJECTION**.
- Overwatcher transmits the formatted `REJECTION NOTICE` back to `auth_guard`:
  ```markdown
  [OVERWATCHER REJECTION NOTICE]
  Worker ID: auth_guard
  Target Domain: Authentication & Token Cryptography
  Status: REJECTED — REWORK REQUIRED
  ...
  ```

### Incident 2: `db_reliability` Reports "Completed"
- Overwatcher runs diff check: AST is clean, no unauthorized files touched.
- Runs `pytest tests/test_connection_pool.py -v`: 14/14 tests pass.
- **Adjudication**: **AUDITED & VERIFIED**.

### Incident 3: `auth_guard` Resubmits After Rework
- Re-inspects diff: Fallback secret removed; code now raises `RuntimeError` on missing environment keys.
- Real cryptographic test assertions added.
- Runs `pytest tests/test_auth_security.py -v`: 8/8 tests pass.
- **Adjudication**: **AUDITED & VERIFIED**.

---

## Step 4: Final Synthesis & Master Report (Phase 4)
Overwatcher runs global test suite across the entire workspace:
```bash
pytest tests/ -v
```
All 22 tests pass without regressions.
Overwatcher synthesizes the final verified report:
`examples/sample_adjudication_report.md` and presents the completed work to the user.
