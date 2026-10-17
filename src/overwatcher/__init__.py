"""
Overwatcher
Hierarchical Multi-Agent Supervisor & Adversarial Red-Team Cross-Examiner.
"""

__version__ = "0.1.1"
__author__ = "Fahad Bin Nasir"

from overwatcher.cross_examiner import (
    CrossExaminer,
    check_file_boundaries,
    audit_diff_for_slop,
    format_rejection_notice,
    FORBIDDEN_DIFF_PATTERNS,
)

__all__ = [
    "__version__",
    "CrossExaminer",
    "check_file_boundaries",
    "audit_diff_for_slop",
    "format_rejection_notice",
    "FORBIDDEN_DIFF_PATTERNS",
]
