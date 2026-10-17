# Overwatcher Worker Contract: Auth Hardening

> **Contract ID**: `CTR-2026-SEC-001`  
> **Target Domain**: `Authentication & Token Cryptography`  
> **Assigned Worker**: `auth_guard` (Subagent)  
> **Status**: `ASSIGNED`

---

## 1. Scope & File Boundaries (Strictly Disjoint)

### Authorized Write Targets
- `src/core/auth.py`
- `src/core/jwt_service.py`
- `tests/test_auth_security.py`

### Read-Only Reference Context
- `src/config/settings.py`
- `src/models/user.py`

---

## 2. Deliverables & Definition of Done
1. Implement asymmetric RS256 token verification with signature expiration guards.
2. Remove legacy symmetric HS256 fallback.
3. Write test cases for expired tokens, altered signatures, and replay attack scenarios.
4. Pass `pytest tests/test_auth_security.py -v` with 100% green exit code.

---

## 3. Forbidden Actions
- ❌ Do not touch `src/models/user.py` or database schemas.
- ❌ Do not use fallback secret keys (`os.getenv("SECRET", "default_secret")`).
- ❌ Do not suppress exceptions with empty `except:` blocks.
- ❌ No conversational assertions ("tests pass") without terminal evidence.

---

## 4. Verification Command
```bash
pytest tests/test_auth_security.py -v --tb=short
```
