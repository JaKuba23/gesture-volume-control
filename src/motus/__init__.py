"""
Motus - Gesture-based volume control for macOS.

A professional machine learning application that uses MediaPipe hand tracking
to control system volume through intuitive hand gestures.
"""

__version__ = "1.0.0"
__author__ = "JaKuba23"

__all__ = ["__version__", "__author__"]


def __getattr__(name: str) -> Any:
    """Lazy import for HandDetector and set_volume.

    This enables lazy loading of heavy dependencies (MediaPipe, OpenCV)
    only when they are actually used, improving import performance.
    """
    if name == "HandDetector":
        from motus.hand_tracking import HandDetector

        return HandDetector
    elif name == "set_volume":
        from motus.mac_controls import set_volume

        return set_volume
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
