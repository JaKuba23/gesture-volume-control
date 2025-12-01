"""
macOS Volume Control Module.

Uses AppleScript (osascript) to control system volume on macOS platforms.
Provides safe fallback behavior on non-macOS systems.
"""

import logging
import platform
import shutil
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class VolumeControlError(Exception):
    """Raised when volume control operation fails."""
    pass


class UnsupportedPlatformError(VolumeControlError):
    """Raised when attempting to control volume on unsupported platform."""
    pass


def set_volume(percent: int) -> None:
    """Set macOS output volume (0-100).
    
    Uses AppleScript to control system volume. Only works on macOS with
    osascript binary available. Silently returns on unsupported platforms.
    
    Args:
        percent: Volume level (0-100). Values outside range are clamped.
    
    Raises:
        UnsupportedPlatformError: If not running on macOS.
        VolumeControlError: If osascript command fails.
    
    Example:
        >>> set_volume(50)  # Set volume to 50%
        >>> set_volume(0)   # Mute
        >>> set_volume(100) # Maximum volume
    
    Note:
        On non-Darwin systems, this function logs a warning and returns
        without raising an exception to allow graceful degradation.
    """
    if platform.system() != "Darwin":
        logger.warning(
            "Volume control only supported on macOS. Current platform: %s",
            platform.system()
        )
        return
    
    if shutil.which("osascript") is None:
        logger.error("osascript binary not found. Cannot control volume.")
        raise VolumeControlError(
            "osascript not available. Volume control requires macOS with osascript."
        )
    
    percent = max(0, min(100, int(percent)))
    
    try:
        result = subprocess.run(
            ["osascript", "-e", f'set volume output volume {percent}'],
            capture_output=True,
            check=True,
            timeout=5
        )
        logger.debug("Volume set to %d%%", percent)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to set volume: %s", e.stderr.decode())
        raise VolumeControlError(f"osascript failed: {e.stderr.decode()}") from e
    except subprocess.TimeoutExpired:
        logger.error("osascript command timed out")
        raise VolumeControlError("Volume control command timed out") from None


def get_volume() -> Optional[int]:
    """Get current macOS output volume (0-100).
    
    Returns:
        Current volume level as integer (0-100), or None if unavailable.
    
    Raises:
        UnsupportedPlatformError: If not running on macOS.
        VolumeControlError: If osascript command fails.
    
    Example:
        >>> current_vol = get_volume()
        >>> if current_vol is not None:
        ...     print(f"Current volume: {current_vol}%")
    """
    if platform.system() != "Darwin":
        logger.warning("Volume query only supported on macOS")
        return None
    
    if shutil.which("osascript") is None:
        raise VolumeControlError("osascript not available")
    
    try:
        result = subprocess.run(
            ["osascript", "-e", 'output volume of (get volume settings)'],
            capture_output=True,
            check=True,
            timeout=5,
            text=True
        )
        return int(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        logger.error("Failed to get volume: %s", str(e))
        raise VolumeControlError(f"Failed to query volume: {e}") from e
    except subprocess.TimeoutExpired:
        raise VolumeControlError("Volume query timed out") from None

