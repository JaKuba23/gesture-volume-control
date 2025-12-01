"""
Hand Tracking Module using MediaPipe.

Detects hand landmarks in real-time using webcam feed with MediaPipe Hands.
"""

from typing import List, Optional

import cv2 as cv
import mediapipe as mp


class HandDetector:
    """Hand detection and landmark tracking using MediaPipe Hands.

    Provides real-time hand landmark detection with configurable parameters
    for detection confidence, tracking confidence, and model complexity.

    Attributes:
        static_image_mode: Whether to treat input as static images.
        max_num_hands: Maximum number of hands to detect.
        min_detection_confidence: Minimum confidence for hand detection.
        min_tracking_confidence: Minimum confidence for hand tracking.
        model_complexity: Complexity of the hand landmark model (0, 1, or 2).

    Example:
        >>> detector = HandDetector(max_num_hands=1, min_detection_confidence=0.7)
        >>> frame = cv.imread('hand.jpg')
        >>> frame = detector.find_hands(frame, draw=True)
        >>> positions = detector.find_positions(frame)
    """

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.6,
        min_tracking_confidence: float = 0.5,
        model_complexity: int = 0,
    ) -> None:
        """Initialize the hand detector with MediaPipe Hands.

        Args:
            static_image_mode: If True, treats each image independently.
                             If False, uses tracking for better performance.
            max_num_hands: Maximum number of hands to detect (1-2).
            min_detection_confidence: Minimum confidence value (0.0-1.0) for
                                    hand detection to be considered successful.
            min_tracking_confidence: Minimum confidence value (0.0-1.0) for
                                   hand tracking to be considered successful.
            model_complexity: Complexity of hand landmark model: 0 (lite), 1 (full).
        """
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            model_complexity=self.model_complexity,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results: Optional[mp.solutions.hands.Hands] = None

    def find_hands(self, frame: cv.Mat, draw: bool = True) -> cv.Mat:
        """Detect hands and optionally draw landmarks on the frame.

        Args:
            frame: Input BGR image from camera or file.
            draw: If True, draws hand landmarks and connections on the frame.

        Returns:
            The input frame with landmarks drawn (if draw=True).

        Example:
            >>> detector = HandDetector()
            >>> frame = cv.imread('hand.jpg')
            >>> frame_with_landmarks = detector.find_hands(frame, draw=True)
        """
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img.flags.writeable = False
        self.results = self.hands.process(img)
        img.flags.writeable = True

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        frame, handlms, self.mpHands.HAND_CONNECTIONS
                    )
        return frame

    def find_positions(
        self, frame: cv.Mat, hand_no: int = 0, draw: bool = False
    ) -> List[List[int]]:
        """Get list of hand landmark positions.

        Extracts the (x, y) pixel coordinates of all 21 hand landmarks
        from the most recent detection result.

        Args:
            frame: Input BGR image (used to convert normalized coordinates).
            hand_no: Index of the hand to extract positions from (0 or 1).
            draw: If True, draws circles at each landmark position.

        Returns:
            List of [id, x, y] for each landmark (21 points total).
            Empty list if no hands detected.

            Landmark IDs:
                0: Wrist
                1-4: Thumb (base to tip)
                5-8: Index finger
                9-12: Middle finger
                13-16: Ring finger
                17-20: Pinky

        Example:
            >>> positions = detector.find_positions(frame)
            >>> if len(positions) > 0:
            ...     wrist_x, wrist_y = positions[0][1], positions[0][2]
        """
        lm_list: List[List[int]] = []
        if self.results and self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]

            for id_num, landmark in enumerate(my_hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lm_list.append([id_num, cx, cy])

                if draw:
                    cv.circle(frame, (cx, cy), 5, (0, 178, 240), cv.FILLED)

        return lm_list
