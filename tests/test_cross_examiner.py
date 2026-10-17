import unittest
import os
import sys

# Add src and scripts directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

import overwatcher
from overwatcher import (
    CrossExaminer,
    check_file_boundaries,
    audit_diff_for_slop,
    format_rejection_notice,
)


class TestOverwatcherCrossExaminer(unittest.TestCase):
    def test_package_metadata(self):
        self.assertEqual(overwatcher.__version__, "0.1.0")
        self.assertEqual(overwatcher.__author__, "Fahad Bin Nasir")

    def test_file_boundaries_clean(self):
        modified = ["src/auth/jwt.py", "tests/test_jwt.py"]
        allowed = ["src/auth/*", "tests/*"]
        violations = check_file_boundaries(modified, allowed)
        self.assertEqual(violations, [])

    def test_file_boundaries_breach(self):
        modified = ["src/auth/jwt.py", "src/database/models.py", "tests/test_jwt.py"]
        allowed = ["src/auth/*", "tests/*"]
        violations = check_file_boundaries(modified, allowed)
        self.assertEqual(violations, ["src/database/models.py"])

    def test_audit_diff_slop_detection(self):
        diff_sample = """--- a/src/auth.py
+++ b/src/auth.py
@@ -10,4 +10,7 @@ def verify_token():
+    try:
+        decrypt()
+    except: pass
+    assert True
+    debugger
"""
        issues = audit_diff_for_slop(diff_sample)
        self.assertTrue(len(issues) >= 3)
        issues_text = " ".join(i["issue"] for i in issues)
        self.assertIn("Bare exception swallowing", issues_text)
        self.assertIn("Trivial test assertion", issues_text)
        self.assertIn("Leftover debugger statement", issues_text)

    def test_format_rejection_notice(self):
        flaws = [{
            "file": "src/auth.py",
            "line": "12",
            "issue": "Bare exception swallowing",
            "evidence": "except: pass"
        }]
        remediations = ["Catch specific exceptions and log the error."]
        notice = format_rejection_notice(
            worker_id="worker_auth",
            domain="security",
            flaws=flaws,
            verification_cmd="pytest tests/test_auth.py",
            remediations=remediations
        )
        self.assertIn("[OVERWATCHER REJECTION NOTICE]", notice)
        self.assertIn("Worker ID: worker_auth", notice)
        self.assertIn("Bare exception swallowing", notice)
        self.assertIn("pytest tests/test_auth.py", notice)

    def test_cross_examiner_class_clean(self):
        examiner = CrossExaminer(
            allowed_files=["*"],
            verify_cmd="python -c \"exit(0)\"",
            worker_id="tester",
            domain="unit_test"
        )
        # Test basic instantiation and properties
        self.assertEqual(examiner.worker_id, "tester")
        self.assertEqual(examiner.domain, "unit_test")


if __name__ == "__main__":
    unittest.main()
