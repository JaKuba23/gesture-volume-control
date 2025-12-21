"""
Main Application Module.

Entry point for the Motus gesture-based volume control application.
Handles camera initialization, frame processing, and UI rendering.
"""

import logging
import os
import time
from collections import deque
from typing import Any, Deque, List, Tuple, Union, cast

import cv2 as cv
import numpy as np

from motus.config import AppConfig, DEFAULT_CONFIG
from motus.gestures import count_open_fingers, is_thumbs_up
from motus.hand_tracking import HandDetector
from motus.mac_controls import set_volume


def _to_deque(history: Union[List[int], Deque[int]], maxlen: int) -> Deque[int]:
    """Convert list or deque to deque with specified maxlen."""
    if isinstance(history, deque):
        # Create new deque with correct maxlen
        result = deque(history, maxlen=maxlen)
    else:
        result = deque(history, maxlen=maxlen)
    return result


logger = logging.getLogger(__name__)


def get_camera_source() -> Union[int, str]:
    """Get camera source from environment variable.

    Returns:
        Camera index (int) or video file path (str).
        Defaults to 0 if CAMERA_SOURCE is not set.

    Example:
        >>> source = get_camera_source()  # Returns 0 by default
        >>> os.environ["CAMERA_SOURCE"] = "1"
        >>> source = get_camera_source()  # Returns 1
    """
    source = os.getenv("CAMERA_SOURCE", "0")
    try:
        return int(source)
    except ValueError:
        return source


def get_config_from_env() -> AppConfig:
    """Create AppConfig from environment variables.

    Reads CAMERA_SOURCE and HEADLESS from environment and creates
    a configuration object with those values.

    Returns:
        AppConfig instance with values from environment or defaults.

    Example:
        >>> os.environ["HEADLESS"] = "1"
        >>> config = get_config_from_env()
        >>> assert config.headless is True
    """
    camera_source = get_camera_source()
    headless = os.getenv("HEADLESS", "0").lower() in ("1", "true", "yes")

    return AppConfig(camera_source=camera_source, headless=headless)


def initialize_camera(source: Union[int, str]) -> cv.VideoCapture:
    """Initialize camera or video file capture.

    Attempts to open the specified camera source. If the first attempt
    fails, tries fallback sources (0, 1) before raising an error.

    Args:
        source: Camera index (int) or video file path (str).

    Returns:
        OpenCV VideoCapture object.

    Raises:
        RuntimeError: If camera cannot be opened after trying fallbacks.

    Example:
        >>> cap = initialize_camera(0)
        >>> assert cap.isOpened()
    """
    cap = cv.VideoCapture(source)
    if cap.isOpened():
        return cap

    # Try fallback sources if initial source fails
    if isinstance(source, int):
        logger.warning("Camera source %d failed, trying fallback sources", source)
        for fallback in [0, 1]:
            if fallback != source:
                cap = cv.VideoCapture(fallback)
                if cap.isOpened():
                    logger.info("Using fallback camera source %d", fallback)
                    return cap

    raise RuntimeError("No camera found. Please check camera connection.")


def draw_ui(
    frame: cv.Mat,
    control_enabled: bool,
    volume: int = 0,
    fingers: int = 0,
) -> None:
    """Draw UI overlay on video frame.

    Displays control status, volume level, and finger count on the frame.

    Args:
        frame: Video frame to draw on.
        control_enabled: Whether volume control is currently active.
        volume: Current volume level (0-100).
        fingers: Number of extended fingers detected.

    Example:
        >>> frame = cv.imread('test.jpg')
        >>> draw_ui(frame, control_enabled=True, volume=50, fingers=3)
    """
    height, width = frame.shape[:2]

    # Status text
    status_text = "CONTROL: ON" if control_enabled else "CONTROL: OFF"
    status_color = (0, 255, 0) if control_enabled else (0, 0, 255)
    cv.putText(
        frame,
        status_text,
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        status_color,
        2,
    )

    # Volume and finger count
    if control_enabled:
        info_text = f"Volume: {volume}% | Fingers: {fingers}"
        cv.putText(
            frame,
            info_text,
            (10, 60),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    # Instructions
    instruction_text = "Press 'Q' to quit"
    cv.putText(
        frame,
        instruction_text,
        (10, height - 20),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5,
        (200, 200, 200),
        1,
    )


def process_frame(
    detector: HandDetector,
    frame: cv.Mat,
    history: Union[List[int], Deque[int]],
    config: AppConfig,
    control_enabled: bool,
    last_toggle_time: float,
) -> Tuple[bool, float, List[int]]:
    """Process a single video frame for gesture detection and volume control.

    Detects hand gestures, updates volume based on finger count, and handles
    toggle gestures (thumbs up).

    Args:
        detector: HandDetector instance for landmark detection.
        frame: Current video frame.
        history: List or deque of recent volume values for smoothing.
        config: Application configuration.
        control_enabled: Whether volume control is currently active.
        last_toggle_time: Timestamp of last toggle gesture.

    Returns:
        Tuple of (control_enabled, last_toggle_time, updated_history as list).

    Example:
        >>> detector = HandDetector()
        >>> frame = cv.imread('test.jpg')
        >>> history = []
        >>> enabled, time, hist = process_frame(detector, frame, history, config, False, 0.0)
    """
    # Convert history to deque for processing
    history_deque = _to_deque(history, config.smoothing_window)

    # Detect hands and get landmarks
    frame = detector.find_hands(frame, draw=not config.headless)
    landmarks = detector.find_positions(frame)

    if not landmarks:
        return control_enabled, last_toggle_time, list(history_deque)

    # Check for toggle gesture (thumbs up)
    current_time = time.time()
    if is_thumbs_up(landmarks):
        if current_time - last_toggle_time >= config.toggle_cooldown:
            control_enabled = not control_enabled
            last_toggle_time = current_time
            logger.info("Control toggled: %s", "ON" if control_enabled else "OFF")

    # Process volume control if enabled
    if control_enabled:
        fingers = count_open_fingers(landmarks)
        volume = int((fingers / 5) * 100)

        # Smooth volume changes using moving average
        history_deque.append(volume)
        if len(history_deque) >= config.smoothing_window:
            smoothed_volume = int(sum(history_deque) / len(history_deque))
            set_volume(smoothed_volume)
            logger.debug("Volume set to %d%% (fingers: %d)", smoothed_volume, fingers)

    return control_enabled, last_toggle_time, list(history_deque)


def main() -> None:
    """Main application entry point.

    Initializes camera, hand detector, and runs the main processing loop.
    Handles keyboard input and cleanup.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    config = get_config_from_env()
    camera_source = get_camera_source()

    logger.info("Starting Motus - Gesture Volume Control")
    logger.info("Camera source: %s", camera_source)
    logger.info("Headless mode: %s", config.headless)

    # Initialize camera
    try:
        cap = initialize_camera(camera_source)
    except RuntimeError as e:
        logger.error("Failed to initialize camera: %s", e)
        return

    # Initialize hand detector
    detector = HandDetector(
        max_num_hands=config.max_num_hands,
        min_detection_confidence=config.min_detection_confidence,
        min_tracking_confidence=config.min_tracking_confidence,
    )

    # Initialize state
    control_enabled = False
    last_toggle_time = 0.0
    history: Union[List[int], Deque[int]] = []

    # Main processing loop
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to read frame")
                break

            # Cast frame to cv.Mat for type checking
            frame_mat = cast(cv.Mat, frame)

            # Process frame
            control_enabled, last_toggle_time, history = process_frame(
                detector,
                frame_mat,
                history,
                config,
                control_enabled,
                last_toggle_time,
            )

            # Draw UI if not in headless mode
            if not config.headless:
                fingers = (
                    count_open_fingers(detector.find_positions(frame_mat))
                    if detector.find_positions(frame_mat)
                    else 0
                )
                current_volume = int(sum(history) / len(history)) if history else 0
                draw_ui(frame_mat, control_enabled, current_volume, fingers)
                cv.imshow("Motus - Gesture Volume Control", frame_mat)

                # Check for quit key
                if cv.waitKey(1) & 0xFF == ord("q"):
                    logger.info("Quit key pressed")
                    break

            # Frame rate limiting
            time.sleep(1.0 / config.target_fps)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        cap.release()
        if not config.headless:
            cv.destroyAllWindows()
        logger.info("Application stopped")
