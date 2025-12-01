"""Unit tests for config module."""

import pytest

from motus.config import AppConfig


class TestAppConfig:
    """Tests for AppConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AppConfig()
        assert config.smoothing_window == 5
        assert config.toggle_cooldown == 1.0
        assert config.min_detection_confidence == 0.7
        assert config.min_tracking_confidence == 0.5
        assert config.max_num_hands == 1
        assert config.camera_source == 0
        assert config.headless is False
        assert config.target_fps == 30
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = AppConfig(
            smoothing_window=10,
            toggle_cooldown=2.0,
            camera_source="/path/to/video.mp4",
            headless=True,
        )
        assert config.smoothing_window == 10
        assert config.toggle_cooldown == 2.0
        assert config.camera_source == "/path/to/video.mp4"
        assert config.headless is True
    
    def test_invalid_smoothing_window(self):
        """Test that invalid smoothing_window raises ValueError."""
        with pytest.raises(ValueError, match="smoothing_window must be >= 1"):
            AppConfig(smoothing_window=0)
    
    def test_invalid_toggle_cooldown(self):
        """Test that negative toggle_cooldown raises ValueError."""
        with pytest.raises(ValueError, match="toggle_cooldown must be >= 0"):
            AppConfig(toggle_cooldown=-1.0)
    
    def test_invalid_detection_confidence(self):
        """Test that invalid detection confidence raises ValueError."""
        with pytest.raises(ValueError, match="min_detection_confidence"):
            AppConfig(min_detection_confidence=1.5)
        
        with pytest.raises(ValueError, match="min_detection_confidence"):
            AppConfig(min_detection_confidence=-0.1)
    
    def test_invalid_tracking_confidence(self):
        """Test that invalid tracking confidence raises ValueError."""
        with pytest.raises(ValueError, match="min_tracking_confidence"):
            AppConfig(min_tracking_confidence=1.5)
    
    def test_invalid_max_num_hands(self):
        """Test that invalid max_num_hands raises ValueError."""
        with pytest.raises(ValueError, match="max_num_hands must be 1 or 2"):
            AppConfig(max_num_hands=3)
    
    def test_invalid_target_fps(self):
        """Test that invalid target_fps raises ValueError."""
        with pytest.raises(ValueError, match="target_fps must be >= 1"):
            AppConfig(target_fps=0)
    
    def test_config_is_frozen(self):
        """Test that AppConfig is immutable (frozen)."""
        config = AppConfig()
        with pytest.raises(Exception):  # FrozenInstanceError
            config.smoothing_window = 10

