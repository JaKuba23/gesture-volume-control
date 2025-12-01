"""
Motus - Backwards compatibility entry point.

This file maintains backwards compatibility for users running:
    python main.py

For new installations, use:
    python -m motus
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from motus.main import main

if __name__ == "__main__":
    main()
