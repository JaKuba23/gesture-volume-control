"""
Motus - Gesture-based volume control for macOS.

A professional machine learning application that uses MediaPipe hand tracking
to control system volume through intuitive hand gestures.
"""

__version__ = "1.0.0"
__author__ = "JaKuba23"

from motus.hand_tracking import HandDetector
from motus.mac_controls import set_volume

__all__ = ["HandDetector", "set_volume", "__version__"]

