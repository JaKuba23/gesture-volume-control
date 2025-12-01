"""
Gesture Recognition Module.

Provides hand gesture detection algorithms for volume control.
Detects finger counting and specific gestures like thumbs-up.
"""

from typing import List


def count_open_fingers(lm_list: List[List[int]]) -> int:
    """Count how many fingers are extended (0-5).
    
    Uses hand landmark positions to determine which fingers are extended.
    Algorithm checks thumb horizontal position and other fingers' vertical position.
    
    Args:
        lm_list: List of [id, x, y] landmark positions from HandDetector.
                Must contain at least 21 landmarks.
    
    Returns:
        Number of extended fingers (0-5).
    
    Algorithm:
        - Thumb: Extended if tip (landmark 4) is right of joint (landmark 3)
        - Other fingers: Extended if tip is above PIP joint
    
    Example:
        >>> landmarks = detector.find_positions(frame)
        >>> fingers = count_open_fingers(landmarks)
        >>> print(f"Fingers extended: {fingers}")
    """
    if len(lm_list) < 21:
        return 0
    
    open_count = 0
    
    # Thumb: check horizontal position (x-axis)
    # Thumb extended if tip (4) is to the right of joint (3)
    if lm_list[4][1] > lm_list[3][1]:
        open_count += 1
    
    # Other fingers: check vertical position (y-axis)
    # Finger extended if tip is above PIP joint
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
    finger_pips = [6, 10, 14, 18]  # Corresponding PIP joints
    
    for tip, pip in zip(finger_tips, finger_pips):
        if lm_list[tip][2] < lm_list[pip][2]:
            open_count += 1
    
    return open_count


def is_thumbs_up(lm_list: List[List[int]]) -> bool:
    """Detect thumbs up gesture (only thumb extended).
    
    Thumbs up is detected when:
    - Thumb tip is above wrist (y-axis)
    - At least 3 other fingers are closed
    
    Args:
        lm_list: List of [id, x, y] landmark positions from HandDetector.
    
    Returns:
        True if thumbs up gesture detected, False otherwise.
    
    Example:
        >>> if is_thumbs_up(landmarks):
        ...     print("Thumbs up detected!")
    """
    if len(lm_list) < 21:
        return False
    
    # Thumb must be up (tip above wrist)
    thumb_up = lm_list[4][2] < lm_list[0][2]
    
    # Check other fingers are closed
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    fingers_closed = sum(
        1 for tip, pip in zip(finger_tips, finger_pips)
        if lm_list[tip][2] >= lm_list[pip][2]
    )
    
    # At least 3 fingers must be closed for thumbs up
    return thumb_up and fingers_closed >= 3


def is_fist(lm_list: List[List[int]]) -> bool:
    """Detect closed fist (all fingers closed).
    
    Args:
        lm_list: List of [id, x, y] landmark positions.
    
    Returns:
        True if fist detected, False otherwise.
    """
    return count_open_fingers(lm_list) == 0


def is_open_hand(lm_list: List[List[int]]) -> bool:
    """Detect open hand (all 5 fingers extended).
    
    Args:
        lm_list: List of [id, x, y] landmark positions.
    
    Returns:
        True if open hand detected, False otherwise.
    """
    return count_open_fingers(lm_list) == 5

