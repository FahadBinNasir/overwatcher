[OVERWATCHER REJECTION NOTICE]
Worker ID: auth_guard
Target Domain: Authentication & Token Cryptography
Status: REJECTED — REWORK REQUIRED

1. Flaws Detected:
   - File: src/core/auth.py:84
     Issue: Insecure fallback secret detected in violation of Forbidden Actions.
     Evidence: `JWT_SECRET = os.getenv("AUTH_SECRET", "super-secret-default")`
   - File: tests/test_auth_security.py:42
     Issue: Trivial assertion detected without verifying public key cryptographic signature.
     Evidence: `assert True  # TODO: verify signature`

2. Required Remediation:
   - Raise a `RuntimeError("AUTH_SECRET environment variable is missing")` when the secret is unset instead of falling back to a default value.
   - Replace the placeholder assertion in `test_auth_security.py` with an actual verification check against an invalid signature.

Re-submit only after executing and passing: `pytest tests/test_auth_security.py -v --tb=short`.
