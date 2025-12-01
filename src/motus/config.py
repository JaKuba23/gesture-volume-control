"""
Configuration Module.

Centralized configuration for gesture volume control application.
"""

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class AppConfig:
    """Application configuration with sensible defaults.

    Attributes:
        smoothing_window: Number of frames to average for volume smoothing.
        toggle_cooldown: Minimum seconds between toggle gestures.
        min_detection_confidence: Minimum confidence for hand detection (0.0-1.0).
        min_tracking_confidence: Minimum confidence for hand tracking (0.0-1.0).
        max_num_hands: Maximum number of hands to detect (1-2).
        camera_source: Camera index (int) or video file path (str).
        headless: If True, disables GUI windows (for Docker/CI).
        target_fps: Target frames per second for processing.
    """

    smoothing_window: int = 5
    toggle_cooldown: float = 1.0
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    max_num_hands: int = 1
    camera_source: Union[int, str] = 0
    headless: bool = False
    target_fps: int = 30

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.smoothing_window < 1:
            raise ValueError("smoothing_window must be >= 1")
        if self.toggle_cooldown < 0:
            raise ValueError("toggle_cooldown must be >= 0")
        if not 0.0 <= self.min_detection_confidence <= 1.0:
            raise ValueError("min_detection_confidence must be between 0.0 and 1.0")
        if not 0.0 <= self.min_tracking_confidence <= 1.0:
            raise ValueError("min_tracking_confidence must be between 0.0 and 1.0")
        if self.max_num_hands not in (1, 2):
            raise ValueError("max_num_hands must be 1 or 2")
        if self.target_fps < 1:
            raise ValueError("target_fps must be >= 1")


DEFAULT_CONFIG = AppConfig()
