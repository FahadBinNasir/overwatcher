# Changelog

All notable changes to the **Overwatcher** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v0.1.0] - 2026-10-17

### Added
- **Core Specification (`SKILL.md`)**: Full hierarchical multi-agent supervisor persona, Iron Laws, 4-phase lifecycle, and communication schemas.
- **Contract Templates (`templates/`)**:
  - `worker_contract.md`: Disjoint file boundary and acceptance contract.
  - `rejection_order.md`: Line-numbered rejection notice for automated subagent rework.
  - `master_adjudication_report.md`: Final synthesis and execution report template.
- **Cross-Examiner CLI (`scripts/cross_examiner.py`)**:
  - Boundary violation detection against git status.
  - Diff anti-pattern scanner (`except: pass`, trivial `assert True`, `debugger`, `breakpoint()`).
  - Automated test and build execution with exit code checking.
- **Vector Icons (`assets/icons/`)**: Custom SVG icons for clean, emoji-free markdown rendering.
- **Test Suite (`tests/test_cross_examiner.py`)**: 100% passing unit tests.
- **CI/CD Automation (`.github/workflows/`)**:
  - Automated CI test matrix across Python 3.8 - 3.12.
  - Automated GitHub Releases packaging `.tar.gz` and `.zip` distribution bundles.
