#!/usr/bin/env python3
"""
Overwatcher Cross-Examiner
Deterministic Red-Team Auditor and Contract Validator for AI Multi-Agent Pipelines.
"""

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from typing import List, Dict, Tuple, Optional


# Forbidden anti-patterns that indicate worker drift, slop, or fake tests
FORBIDDEN_DIFF_PATTERNS = [
    (r"^\+\s*except\s*:\s*pass", "Bare exception swallowing (`except: pass`)"),
    (r"^\+\s*except\s+Exception\s*:\s*pass", "Exception swallowing (`except Exception: pass`)"),
    (r"^\+\s*catch\s*\([^)]*\)\s*\{\s*\}", "Silent catch block (`catch (e) {}`)"),
    (r"^\+\s*assert\s+True\b", "Trivial test assertion (`assert True`)"),
    (r"^\+\s*assert\s+1\s*==\s*1\b", "Trivial test assertion (`assert 1 == 1`)"),
    (r"^\+\s*expect\s*\(\s*true\s*\)\.toBe\s*\(\s*true\s*\)", "Trivial test assertion (`expect(true).toBe(true)`)"),
    (r"^\+\s*debugger\b", "Leftover debugger statement"),
    (r"^\+\s*breakpoint\(\)", "Leftover breakpoint() statement"),
]


def run_command(cmd: str, cwd: Optional[str] = None) -> Tuple[int, str]:
    """Execute a shell command and return (exit_code, output)."""
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return proc.returncode, proc.stdout
    except Exception as e:
        return 1, str(e)


def get_git_modified_files(cwd: str, base_ref: str = "HEAD") -> List[str]:
    """Return list of modified or untracked files relative to base_ref or working tree."""
    # Check working tree changes
    code, out = run_command("git status --porcelain", cwd=cwd)
    files = []
    if code == 0:
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            # Git porcelain format: XY PATH or XY "PATH"
            parts = line[2:].strip().split(" -> ")
            filepath = parts[-1].strip().strip('"')
            files.append(filepath.replace("\\", "/"))
    return sorted(list(set(files)))


def get_git_diff(cwd: str) -> str:
    """Return the current unstaged and staged git diff."""
    code, out = run_command("git diff -U3 HEAD", cwd=cwd)
    if code != 0 or not out.strip():
        # Fallback to unstaged diff
        code, out = run_command("git diff -U3", cwd=cwd)
    return out


def check_file_boundaries(
    modified_files: List[str],
    allowed_patterns: List[str]
) -> List[str]:
    """Identify files modified outside the allowed contract boundaries."""
    violations = []
    for f in modified_files:
        norm_f = f.replace("\\", "/")
        matched = False
        for pat in allowed_patterns:
            pat = pat.replace("\\", "/").strip()
            if not pat:
                continue
            if fnmatch.fnmatch(norm_f, pat) or fnmatch.fnmatch(os.path.basename(norm_f), pat):
                matched = True
                break
        if not matched:
            violations.append(norm_f)
    return violations


def audit_diff_for_slop(diff_text: str) -> List[Dict[str, str]]:
    """Inspect git diff for anti-patterns and forbidden shortcuts."""
    issues = []
    current_file = "unknown"
    current_line = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            current_line = 0
            continue
        elif line.startswith("@@"):
            # @@ -a,b +c,d @@
            m = re.search(r"\+(\d+)", line)
            if m:
                current_line = int(m.group(1))
            continue

        if line.startswith("+") and not line.startswith("+++"):
            for pattern, description in FORBIDDEN_DIFF_PATTERNS:
                if re.search(pattern, line):
                    issues.append({
                        "file": current_file,
                        "line": str(current_line),
                        "issue": description,
                        "evidence": line.strip()
                    })
            current_line += 1
        elif not line.startswith("-"):
            current_line += 1

    return issues


def format_rejection_notice(
    worker_id: str,
    domain: str,
    flaws: List[Dict[str, str]],
    verification_cmd: str,
    remediations: List[str]
) -> str:
    """Generate structured Overwatcher Rejection Notice."""
    flaw_lines = []
    for f in flaws:
        flaw_lines.append(
            f"   - File: {f.get('file', 'N/A')}:{f.get('line', 'N/A')}\n"
            f"     Issue: {f.get('issue', 'Defect detected')}\n"
            f"     Evidence: `{f.get('evidence', '').strip()}`"
        )
    flaws_formatted = "\n".join(flaw_lines)

    remedy_lines = [f"   - {r}" for r in remediations]
    remedy_formatted = "\n".join(remedy_lines)

    return (
        f"[OVERWATCHER REJECTION NOTICE]\n"
        f"Worker ID: {worker_id}\n"
        f"Target Domain: {domain}\n"
        f"Status: REJECTED — REWORK REQUIRED\n\n"
        f"1. Flaws Detected:\n"
        f"{flaws_formatted}\n\n"
        f"2. Required Remediation:\n"
        f"{remedy_formatted}\n\n"
        f"Re-submit only after executing and passing: `{verification_cmd}`.\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Overwatcher Cross-Examiner: Deterministic Red-Team Agent Auditor"
    )
    parser.add_argument("--worker", default="worker_subagent", help="Worker subagent ID or role")
    parser.add_argument("--domain", default="core", help="Target domain name")
    parser.add_argument("--allowed-files", nargs="*", default=[], help="Allowed file path glob patterns")
    parser.add_argument("--verify-cmd", default="", help="Command to execute for verification (e.g. pytest, npm test)")
    parser.add_argument("--repo-dir", default=".", help="Path to target git repository")

    args = parser.parse_args()
    repo_dir = os.path.abspath(args.repo_dir)

    print("==================================================")
    print("      OVERWATCHER ADVERSARIAL CROSS-EXAMINATION   ")
    print("==================================================")
    print(f"Worker Subagent : {args.worker}")
    print(f"Target Domain   : {args.domain}")
    print(f"Repository Root : {repo_dir}")
    print("--------------------------------------------------")

    flaws = []
    remediations = []

    # 1. Boundary Check
    if args.allowed_files:
        modified = get_git_modified_files(repo_dir)
        violations = check_file_boundaries(modified, args.allowed_files)
        if violations:
            for v in violations:
                flaws.append({
                    "file": v,
                    "line": "1",
                    "issue": "Contract Boundary Breach: Unauthorized file modified outside worker contract",
                    "evidence": f"Modified file '{v}' is not in allowed list: {args.allowed_files}"
                })
            remediations.append("Revert changes in unauthorized files using `git checkout -- <file>`.")

    # 2. Diff Slop & Anti-pattern Check
    diff_content = get_git_diff(repo_dir)
    if diff_content:
        diff_issues = audit_diff_for_slop(diff_content)
        if diff_issues:
            flaws.extend(diff_issues)
            remediations.append("Remove all silent exception catchers, trivial assertions, or leftover debuggers.")

    # 3. Verification Command Check
    if args.verify_cmd:
        print(f"[*] Executing verification command: {args.verify_cmd}")
        code, out = run_command(args.verify_cmd, cwd=repo_dir)
        if code != 0:
            flaws.append({
                "file": "Workspace Test Suite",
                "line": "N/A",
                "issue": f"Verification command failed with exit code {code}",
                "evidence": "\n".join(out.strip().splitlines()[-10:])
            })
            remediations.append(f"Fix failing test cases and ensure `{args.verify_cmd}` exits 0.")

    # 4. Adjudication
    if flaws:
        print("\n❌ ADJUDICATION RESULT: REJECTED\n")
        notice = format_rejection_notice(
            worker_id=args.worker,
            domain=args.domain,
            flaws=flaws,
            verification_cmd=args.verify_cmd or "git diff",
            remediations=remediations
        )
        print(notice)
        sys.exit(1)
    else:
        print("\n✅ ADJUDICATION RESULT: AUDITED & VERIFIED")
        print("All contract boundaries respected. No slop anti-patterns detected.")
        if args.verify_cmd:
            print("Verification command passed with exit code 0.")
        sys.exit(0)


if __name__ == "__main__":
    main()
