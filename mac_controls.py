"""
macOS Volume Control Module
Uses AppleScript to control system volume.
"""

import subprocess
import platform
import shutil


def set_volume(percent: int) -> None:
    """
    Set macOS output volume (0-100).
    
    Args:
        percent: Volume level (0-100)
    """
    # Only attempt on macOS with osascript present
    if platform.system() != "Darwin":
        return
    if shutil.which("osascript") is None:
        return

    percent = max(0, min(100, int(percent)))
    subprocess.run(
        ["osascript", "-e", f'set volume output volume {percent}'],
        capture_output=True
    )
