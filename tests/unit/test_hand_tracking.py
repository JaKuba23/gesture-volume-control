"""Unit tests for hand_tracking module."""

from unittest.mock import MagicMock, patch

import numpy as np

from motus.hand_tracking import HandDetector


class TestHandDetectorInit:
    """Tests for HandDetector initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        detector = HandDetector()
        assert detector.static_image_mode is False
        assert detector.max_num_hands == 1
        assert detector.min_detection_confidence == 0.6
        assert detector.min_tracking_confidence == 0.5
        assert detector.model_complexity == 0

    def test_init_with_custom_params(self):
        """Test initialization with custom parameters."""
        detector = HandDetector(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7,
            model_complexity=1,
        )
        assert detector.static_image_mode is True
        assert detector.max_num_hands == 2
        assert detector.min_detection_confidence == 0.8
        assert detector.min_tracking_confidence == 0.7
        assert detector.model_complexity == 1


class TestFindHands:
    """Tests for find_hands method."""

    @patch("motus.hand_tracking.mp.solutions.hands.Hands")
    def test_find_hands_no_detection(self, mock_mp_hands, sample_frame):
        """Test find_hands when no hands detected."""
        detector = HandDetector()
        detector.hands = MagicMock()
        detector.hands.process.return_value.multi_hand_landmarks = None

        result = detector.find_hands(sample_frame, draw=False)
        assert result.shape == sample_frame.shape

    @patch("motus.hand_tracking.mp.solutions.hands.Hands")
    def test_find_hands_with_detection(self, mock_mp_hands, sample_frame):
        """Test find_hands when hands are detected."""
        detector = HandDetector()

        # Mock hand detection
        mock_landmark = MagicMock()
        detector.hands = MagicMock()
        detector.hands.process.return_value.multi_hand_landmarks = [mock_landmark]

        result = detector.find_hands(sample_frame, draw=True)
        assert result is not None
        assert isinstance(result, np.ndarray)


class TestFindPositions:
    """Tests for find_positions method."""

    def test_find_positions_no_hands(self, sample_frame):
        """Test find_positions when no hands detected."""
        detector = HandDetector()
        detector.results = None

        positions = detector.find_positions(sample_frame)
        assert positions == []

    @patch("motus.hand_tracking.mp.solutions.hands.Hands")
    def test_find_positions_with_hand(self, mock_mp_hands, sample_frame):
        """Test find_positions when hand is detected."""
        detector = HandDetector()

        # Create mock landmarks
        mock_landmark = MagicMock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5

        mock_hand = MagicMock()
        mock_hand.landmark = [mock_landmark] * 21

        detector.results = MagicMock()
        detector.results.multi_hand_landmarks = [mock_hand]

        positions = detector.find_positions(sample_frame)
        assert len(positions) == 21
        assert all(len(pos) == 3 for pos in positions)
        assert all(isinstance(pos[0], int) for pos in positions)

    def test_find_positions_draw_mode(self, sample_frame):
        """Test find_positions with draw enabled."""
        detector = HandDetector()

        mock_landmark = MagicMock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5

        mock_hand = MagicMock()
        mock_hand.landmark = [mock_landmark] * 21

        detector.results = MagicMock()
        detector.results.multi_hand_landmarks = [mock_hand]

        # With draw=True, circles should be drawn (we just verify no errors)
        positions = detector.find_positions(sample_frame, draw=True)
        assert len(positions) == 21
