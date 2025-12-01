"""Unit tests for gestures module."""

from motus.gestures import (
    count_open_fingers,
    is_fist,
    is_open_hand,
    is_thumbs_up,
)


class TestCountOpenFingers:
    """Tests for count_open_fingers function."""

    def test_open_hand_returns_five(self, mock_hand_landmarks):
        """Test that open hand returns 5 fingers."""
        assert count_open_fingers(mock_hand_landmarks) == 5

    def test_closed_fist_returns_zero(self, mock_fist_landmarks):
        """Test that closed fist returns 0 fingers."""
        assert count_open_fingers(mock_fist_landmarks) == 0

    def test_empty_landmarks_returns_zero(self):
        """Test that empty landmark list returns 0."""
        assert count_open_fingers([]) == 0

    def test_insufficient_landmarks_returns_zero(self):
        """Test that insufficient landmarks returns 0."""
        assert count_open_fingers([[0, 100, 100]]) == 0

    def test_one_finger_extended(self):
        """Test detection of one extended finger."""
        landmarks = [
            [0, 250, 250],  # Wrist
            [1, 240, 240],
            [2, 235, 235],
            [3, 230, 230],
            [4, 225, 225],  # Thumb closed
            [5, 260, 220],
            [6, 270, 180],
            [7, 275, 140],
            [8, 280, 100],  # Index open
            [9, 280, 240],
            [10, 283, 245],
            [11, 285, 250],
            [12, 287, 255],  # Middle closed
            [13, 300, 240],
            [14, 303, 245],
            [15, 305, 250],
            [16, 307, 255],  # Ring closed
            [17, 320, 240],
            [18, 323, 245],
            [19, 325, 250],
            [20, 327, 255],  # Pinky closed
        ]
        assert count_open_fingers(landmarks) == 1


class TestIsThumbsUp:
    """Tests for is_thumbs_up function."""

    def test_thumbs_up_detected(self, mock_thumbs_up_landmarks):
        """Test that thumbs up gesture is detected."""
        assert is_thumbs_up(mock_thumbs_up_landmarks) is True

    def test_open_hand_not_thumbs_up(self, mock_hand_landmarks):
        """Test that open hand is not detected as thumbs up."""
        assert is_thumbs_up(mock_hand_landmarks) is False

    def test_fist_not_thumbs_up(self, mock_fist_landmarks):
        """Test that fist is not detected as thumbs up."""
        assert is_thumbs_up(mock_fist_landmarks) is False

    def test_empty_landmarks_returns_false(self):
        """Test that empty landmarks return False."""
        assert is_thumbs_up([]) is False

    def test_insufficient_landmarks_returns_false(self):
        """Test that insufficient landmarks return False."""
        assert is_thumbs_up([[0, 100, 100]]) is False


class TestIsFist:
    """Tests for is_fist function."""

    def test_fist_detected(self, mock_fist_landmarks):
        """Test that fist is detected correctly."""
        assert is_fist(mock_fist_landmarks) is True

    def test_open_hand_not_fist(self, mock_hand_landmarks):
        """Test that open hand is not detected as fist."""
        assert is_fist(mock_hand_landmarks) is False

    def test_empty_landmarks_is_fist(self):
        """Test that empty landmarks count as fist (no fingers)."""
        assert is_fist([]) is True


class TestIsOpenHand:
    """Tests for is_open_hand function."""

    def test_open_hand_detected(self, mock_hand_landmarks):
        """Test that open hand is detected correctly."""
        assert is_open_hand(mock_hand_landmarks) is True

    def test_fist_not_open_hand(self, mock_fist_landmarks):
        """Test that fist is not detected as open hand."""
        assert is_open_hand(mock_fist_landmarks) is False

    def test_partial_open_not_open_hand(self):
        """Test that partially open hand is not full open."""
        landmarks = [
            [0, 250, 250],
            [1, 240, 240],
            [2, 235, 235],
            [3, 230, 230],
            [4, 225, 225],
            [5, 260, 220],
            [6, 270, 180],
            [7, 275, 140],
            [8, 280, 100],
            [9, 280, 240],
            [10, 283, 245],
            [11, 285, 250],
            [12, 287, 255],
            [13, 300, 240],
            [14, 303, 245],
            [15, 305, 250],
            [16, 307, 255],
            [17, 320, 240],
            [18, 323, 245],
            [19, 325, 250],
            [20, 327, 255],
        ]
        assert is_open_hand(landmarks) is False
