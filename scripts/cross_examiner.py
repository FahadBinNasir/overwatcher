#!/usr/bin/env python3
"""
Overwatcher Cross-Examiner
Standalone CLI wrapper delegating to the overwatcher package or fallback engine.
"""

import os
import sys

# Add src/ to path so it can import overwatcher directly if not installed
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from overwatcher.cli import main

if __name__ == "__main__":
    main()
