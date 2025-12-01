"""Integration tests for full workflow."""

from unittest.mock import Mock, patch

import pytest

from motus.config import AppConfig
from motus.gestures import count_open_fingers
from motus.hand_tracking import HandDetector


@pytest.mark.integration
class TestEndToEndWorkflow:
    """Integration tests for complete gesture detection workflow."""

    @patch("motus.hand_tracking.mp.solutions.hands.Hands")
    def test_hand_detection_to_gesture_recognition(
        self, mock_mp_hands, sample_frame, mock_hand_landmarks
    ):
        """Test complete flow from frame to gesture recognition."""
        # Setup
        detector = HandDetector()

        # Mock hand detection
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_hand = Mock()
        mock_hand.landmark = [mock_landmark] * 21

        detector.hands = Mock()
        detector.hands.process.return_value.multi_hand_landmarks = [mock_hand]

        # Process frame
        result_frame = detector.find_hands(sample_frame, draw=True)
        positions = detector.find_positions(result_frame)

        # Verify we got landmarks
        assert len(positions) == 21

        # Count fingers
        finger_count = count_open_fingers(positions)
        assert 0 <= finger_count <= 5

    @patch("motus.main.cv2.VideoCapture")
    @patch("motus.main.set_volume")
    def test_volume_control_workflow(
        self, mock_set_volume, mock_video_capture, sample_frame
    ):
        """Test workflow from camera to volume control."""
        # Setup mock camera
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, sample_frame)
        mock_video_capture.return_value = mock_cap

        config = AppConfig(headless=True)
        assert config.headless is True

        # Import main to test (avoiding actual execution)
        from motus.main import initialize_camera

        cap = initialize_camera(0)
        assert cap.isOpened()

    def test_smoothing_reduces_jitter(self):
        """Test that volume smoothing reduces jitter."""
        import numpy as np

        # Simulate jittery finger counts
        jittery_values = [3, 5, 3, 4, 3, 5, 4]
        window_size = 5

        history = []
        smoothed_values = []

        for val in jittery_values:
            history.append(val)
            if len(history) > window_size:
                history.pop(0)
            smoothed = np.mean(history)
            smoothed_values.append(smoothed)

        # Verify smoothing reduces variance
        jitter_variance = np.var(jittery_values)
        smooth_variance = np.var(smoothed_values)
        assert smooth_variance < jitter_variance


@pytest.mark.integration
class TestConfigurationIntegration:
    """Integration tests for configuration management."""

    def test_config_affects_detector(self):
        """Test that config values properly configure HandDetector."""
        config = AppConfig(
            min_detection_confidence=0.8,
            max_num_hands=2,
        )

        detector = HandDetector(
            min_detection_confidence=config.min_detection_confidence,
            max_num_hands=config.max_num_hands,
        )

        assert detector.min_detection_confidence == 0.8
        assert detector.max_num_hands == 2

    def test_env_config_integration(self, monkeypatch):
        """Test environment variable configuration."""
        monkeypatch.setenv("CAMERA_SOURCE", "1")
        monkeypatch.setenv("HEADLESS", "1")

        from motus.main import get_config_from_env

        config = get_config_from_env()
        assert config.camera_source == 1
        assert config.headless is True


@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Performance integration tests."""

    @patch("motus.hand_tracking.mp.solutions.hands.Hands")
    def test_frame_processing_performance(self, mock_mp_hands, sample_frame):
        """Test that frame processing is reasonably fast."""
        import time

        detector = HandDetector()
        detector.hands = Mock()
        detector.hands.process.return_value.multi_hand_landmarks = None

        start_time = time.time()
        iterations = 100

        for _ in range(iterations):
            detector.find_hands(sample_frame, draw=False)

        elapsed = time.time() - start_time
        fps = iterations / elapsed

        # Should process at least 30 FPS even with mocks
        assert fps >= 30, f"Too slow: {fps:.1f} FPS"
