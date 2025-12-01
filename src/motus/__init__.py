"""
Motus - Gesture-based volume control for macOS.

A professional machine learning application that uses MediaPipe hand tracking
to control system volume through intuitive hand gestures.
"""

from typing import TYPE_CHECKING, Any

__version__ = "1.0.0"
__author__ = "JaKuba23"

# Typing-only imports — używamy aliasów, żeby nie redefiniować nazw dostępnych w runtime
if TYPE_CHECKING:
    from motus.hand_tracking import HandDetector as _HandDetector
    from motus.mac_controls import set_volume as _set_volume

__all__ = ["__version__", "__author__", "HandDetector", "set_volume"]


def __getattr__(name: str) -> Any:
    """Lazy import for HandDetector and set_volume."""
    if name == "HandDetector":
        from motus.hand_tracking import HandDetector

        return HandDetector
    elif name == "set_volume":
        from motus.mac_controls import set_volume

        return set_volume
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
