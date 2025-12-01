"""
Pytest configuration and shared fixtures.
"""

from typing import List
from unittest.mock import MagicMock, Mock

import cv2
import numpy as np
import pytest


@pytest.fixture
def mock_camera() -> Mock:
    """Mock cv2.VideoCapture for testing."""
    mock = Mock(spec=cv2.VideoCapture)
    mock.isOpened.return_value = True
    mock.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    mock.release.return_value = None
    return mock


@pytest.fixture
def mock_hand_landmarks() -> List[List[int]]:
    """Sample hand landmarks for testing.

    Returns 21 landmarks representing an open hand.
    """
    return [
        [0, 250, 250],  # Wrist
        [1, 240, 230],
        [2, 230, 210],
        [3, 220, 190],
        [4, 210, 170],  # Thumb
        [5, 260, 220],
        [6, 270, 180],
        [7, 275, 140],
        [8, 280, 100],  # Index
        [9, 280, 230],
        [10, 285, 180],
        [11, 287, 140],
        [12, 290, 100],  # Middle
        [13, 300, 235],
        [14, 305, 185],
        [15, 307, 145],
        [16, 310, 105],  # Ring
        [17, 320, 240],
        [18, 325, 190],
        [19, 327, 150],
        [20, 330, 110],  # Pinky
    ]


@pytest.fixture
def mock_fist_landmarks() -> List[List[int]]:
    """Sample hand landmarks representing a closed fist."""
    return [
        [0, 250, 250],  # Wrist
        [1, 240, 240],
        [2, 235, 235],
        [3, 230, 230],
        [4, 225, 225],  # Thumb closed
        [5, 260, 240],
        [6, 265, 245],
        [7, 267, 250],
        [8, 270, 255],  # Index closed
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


@pytest.fixture
def mock_thumbs_up_landmarks() -> List[List[int]]:
    """Sample hand landmarks representing thumbs up gesture."""
    return [
        [0, 250, 250],  # Wrist
        [1, 240, 230],
        [2, 230, 210],
        [3, 220, 190],
        [4, 210, 170],  # Thumb up
        [5, 260, 240],
        [6, 265, 245],
        [7, 267, 250],
        [8, 270, 255],  # Index closed
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


@pytest.fixture
def mock_mediapipe_hands() -> MagicMock:
    """Mock MediaPipe Hands solution."""
    mock = MagicMock()
    mock.process.return_value.multi_hand_landmarks = None
    return mock


@pytest.fixture
def sample_frame() -> np.ndarray:
    """Create a sample video frame for testing."""
    return np.zeros((480, 640, 3), dtype=np.uint8)


@pytest.fixture
def mock_subprocess_run(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Mock subprocess.run for volume control testing."""
    mock = Mock()
    mock.return_value.returncode = 0
    mock.return_value.stdout = "50"
    mock.return_value.stderr = ""
    monkeypatch.setattr("subprocess.run", mock)
    return mock


@pytest.fixture
def mock_platform_darwin(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock platform.system to return Darwin (macOS)."""
    monkeypatch.setattr("platform.system", lambda: "Darwin")


@pytest.fixture
def mock_platform_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock platform.system to return Linux."""
    monkeypatch.setattr("platform.system", lambda: "Linux")
