# Contributing to Overwatcher

Thank you for your interest in contributing to **Overwatcher**! We welcome improvements to our multi-agent supervisor protocols, contract schemas, language-specific AST heuristics, and automated CLI auditors.

---

## Code of Conduct

All contributors and maintainers are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

---

## Core Contribution Philosophy (The Iron Laws)

Overwatcher enforces zero tolerance for "vibe-check" engineering:
1. **Deterministic Verification Required**: Every PR adding or modifying audit heuristics must include automated unit tests proving that defect detection works.
2. **Zero Slop**: PRs must not contain dead code, commented-out blocks, silent exception suppressors, or trivial placeholder tests (`assert True`).
3. **No Unearned Clutter**: Keep documentation, templates, and CLI tools sharp, functional, and minimal.

---

## Development Workflow

### 1. Prerequisites
- Python 3.8 or higher
- Git

### 2. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/overwatcher.git
cd overwatcher
```

### 3. Create a Targeted Branch
```bash
git checkout -b feature/your-heuristic-name
```

### 4. Running Tests
Overwatcher's test suite uses Python's standard `unittest` framework with zero required third-party dependencies:
```bash
python tests/test_cross_examiner.py
```

All tests must pass before submitting your pull request.

---

## Submitting a Pull Request (PR)

1. Ensure your branch is rebased on the latest `main`.
2. Follow clear, conventional commit messages:
   - `feat(cli): add TypeScript AST boundary check`
   - `fix(heuristics): correct regex for multi-line exception swallows`
   - `docs(templates): refine worker contract acceptance schema`
3. Complete the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md) including reproducible terminal logs from `python tests/test_cross_examiner.py`.
4. Open the PR against `FahadBinNasir/overwatcher:main`.

---

## Questions and Discussions
For architectural suggestions or questions, feel free to open a [Discussion or Issue](https://github.com/FahadBinNasir/overwatcher/issues).
