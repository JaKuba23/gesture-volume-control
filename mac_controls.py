"""
macOS Volume Control Module
Uses AppleScript to control system volume.
"""

import subprocess


def set_volume(percent: int) -> None:
    """
    Set macOS output volume (0-100).
    
    Args:
        percent: Volume level (0-100)
    """
    percent = max(0, min(100, int(percent)))
    subprocess.run(
        ["osascript", "-e", f'set volume output volume {percent}'],
        capture_output=True
    )
