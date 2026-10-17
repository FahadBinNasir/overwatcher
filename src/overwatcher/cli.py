"""
Overwatcher CLI Entrypoint
"""

import argparse
import os
import sys
from overwatcher.cross_examiner import CrossExaminer


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="overwatcher",
        description="Overwatcher: Hierarchical Multi-Agent Supervisor & Adversarial Red-Team Cross-Examiner"
    )
    parser.add_argument("--worker", default="worker_subagent", help="Worker subagent ID or role")
    parser.add_argument("--domain", default="core", help="Target domain name")
    parser.add_argument("--allowed-files", nargs="*", default=[], help="Allowed file path glob patterns")
    parser.add_argument("--verify-cmd", default="", help="Command to execute for verification (e.g. pytest, npm test)")
    parser.add_argument("--repo-dir", default=".", help="Path to target git repository")

    args = parser.parse_args(argv)
    repo_dir = os.path.abspath(args.repo_dir)

    print("==================================================")
    print("      OVERWATCHER ADVERSARIAL CROSS-EXAMINATION   ")
    print("==================================================")
    print(f"Worker Subagent : {args.worker}")
    print(f"Target Domain   : {args.domain}")
    print(f"Repository Root : {repo_dir}")
    print("--------------------------------------------------")

    examiner = CrossExaminer(
        repo_dir=repo_dir,
        allowed_files=args.allowed_files,
        verify_cmd=args.verify_cmd,
        worker_id=args.worker,
        domain=args.domain
    )

    passed, notice, flaws = examiner.run_audit()

    if not passed:
        print("\nADJUDICATION RESULT: REJECTED\n")
        print(notice)
        sys.exit(1)
    else:
        print("\nADJUDICATION RESULT: AUDITED & VERIFIED")
        print("All contract boundaries respected. No slop anti-patterns detected.")
        if args.verify_cmd:
            print("Verification command passed with exit code 0.")
        sys.exit(0)


if __name__ == "__main__":
    main()
