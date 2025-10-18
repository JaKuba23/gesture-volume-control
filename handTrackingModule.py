"""
Hand Tracking Module using MediaPipe
Detects hand landmarks in real-time using webcam feed.
"""

import cv2 as cv
import mediapipe as mp


class handDetector:
    """Hand detection and landmark tracking using MediaPipe Hands."""
    
    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
        model_complexity=0,
    ):
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
    
    def findHands(self, frame, draw=True):   
        # Convert to RGB and mark non-writeable for performance
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        """Detect hands and optionally draw landmarks on the frame."""
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
    
    def findPositions(self, frame, handNo=0, draw=False):
        """
        Get list of hand landmark positions.
        
        Returns:
            List of [id, x, y] for each landmark (21 points)
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            for id, landmark in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lmList.append([id, cx, cy])
                
                if draw:
                    cv.circle(frame, (cx, cy), 5, (0, 178, 240), cv.FILLED)
        
        return lmList
