"""Unit tests for main module."""

import os
from unittest.mock import Mock, patch

import cv2
import numpy as np
import pytest

from motus.config import AppConfig
from motus.main import (
    draw_ui,
    get_camera_source,
    get_config_from_env,
    initialize_camera,
    process_frame,
)


class TestGetCameraSource:
    """Tests for get_camera_source function."""
    
    def test_get_camera_source_default(self, monkeypatch):
        """Test default camera source."""
        monkeypatch.delenv("CAMERA_SOURCE", raising=False)
        assert get_camera_source() == 0
    
    def test_get_camera_source_int(self, monkeypatch):
        """Test integer camera source from env."""
        monkeypatch.setenv("CAMERA_SOURCE", "1")
        assert get_camera_source() == 1
    
    def test_get_camera_source_file(self, monkeypatch):
        """Test file path camera source from env."""
        monkeypatch.setenv("CAMERA_SOURCE", "/path/to/video.mp4")
        assert get_camera_source() == "/path/to/video.mp4"


class TestGetConfigFromEnv:
    """Tests for get_config_from_env function."""
    
    def test_default_config(self, monkeypatch):
        """Test default config from environment."""
        monkeypatch.delenv("CAMERA_SOURCE", raising=False)
        monkeypatch.delenv("HEADLESS", raising=False)
        
        config = get_config_from_env()
        assert config.camera_source == 0
        assert config.headless is False
    
    def test_headless_config(self, monkeypatch):
        """Test headless config from environment."""
        monkeypatch.setenv("HEADLESS", "1")
        monkeypatch.setenv("CAMERA_SOURCE", "2")
        
        config = get_config_from_env()
        assert config.camera_source == 2
        assert config.headless is True


class TestInitializeCamera:
    """Tests for initialize_camera function."""
    
    @patch("cv2.VideoCapture")
    def test_initialize_camera_success(self, mock_video_capture):
        """Test successful camera initialization."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap
        
        cap = initialize_camera(0)
        assert cap.isOpened()
    
    @patch("cv2.VideoCapture")
    def test_initialize_camera_fallback(self, mock_video_capture):
        """Test camera initialization with fallback."""
        mock_cap_fail = Mock()
        mock_cap_fail.isOpened.return_value = False
        
        mock_cap_success = Mock()
        mock_cap_success.isOpened.return_value = True
        
        mock_video_capture.side_effect = [mock_cap_fail, mock_cap_success]
        
        cap = initialize_camera(0)
        assert cap.isOpened()
    
    @patch("cv2.VideoCapture")
    def test_initialize_camera_failure(self, mock_video_capture):
        """Test camera initialization failure."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap
        
        with pytest.raises(RuntimeError, match="No camera found"):
            initialize_camera(0)


class TestDrawUI:
    """Tests for draw_ui function."""
    
    def test_draw_ui_enabled(self, sample_frame):
        """Test UI drawing when control is enabled."""
        draw_ui(sample_frame, control_enabled=True, volume=50, fingers=3)
        # Just verify no exceptions (actual drawing tested visually)
    
    def test_draw_ui_disabled(self, sample_frame):
        """Test UI drawing when control is disabled."""
        draw_ui(sample_frame, control_enabled=False)
        # Just verify no exceptions


class TestProcessFrame:
    """Tests for process_frame function."""
    
    def test_process_frame_no_hand(self, sample_frame):
        """Test frame processing when no hand detected."""
        mock_detector = Mock()
        mock_detector.find_hands.return_value = sample_frame
        mock_detector.find_positions.return_value = []
        
        config = AppConfig()
        enabled, last_time, history = process_frame(
            mock_detector, sample_frame, [], config, False, 0.0
        )
        
        assert enabled is False
        assert isinstance(history, list)
    
    @patch("motus.main.set_volume")
    def test_process_frame_with_hand_control_enabled(
        self, mock_set_volume, sample_frame, mock_hand_landmarks
    ):
        """Test frame processing with hand detected and control enabled."""
        mock_detector = Mock()
        mock_detector.find_hands.return_value = sample_frame
        mock_detector.find_positions.return_value = mock_hand_landmarks
        
        config = AppConfig()
        enabled, last_time, history = process_frame(
            mock_detector, sample_frame, [], config, True, 0.0
        )
        
        assert enabled is True
        assert len(history) > 0
        mock_set_volume.assert_called()
    
    @patch("motus.main.set_volume")
    @patch("motus.main.time.time")
    def test_process_frame_toggle_gesture(
        self, mock_time, mock_set_volume, sample_frame, mock_thumbs_up_landmarks
    ):
        """Test frame processing with thumbs up toggle."""
        mock_time.return_value = 10.0
        
        mock_detector = Mock()
        mock_detector.find_hands.return_value = sample_frame
        mock_detector.find_positions.return_value = mock_thumbs_up_landmarks
        
        config = AppConfig()
        enabled, last_time, history = process_frame(
            mock_detector, sample_frame, [], config, False, 0.0
        )
        
        assert enabled is True
        assert last_time == 10.0

