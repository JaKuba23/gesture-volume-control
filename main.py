"""
Gesture Volume Control - macOS
Control system volume by opening and closing your hand.
Thumbs up gesture toggles control on/off.
"""

import cv2
import time
import numpy as np
import os

try:
    from handTrackingModule import handDetector
except ImportError:
    print("ERROR: 'handTrackingModule.py' not found.")
    print("Please ensure it's in the same directory.")
    exit(1)

try:
    from mac_controls import set_volume
except ImportError:
    print("ERROR: 'mac_controls.py' not found.")
    print("This script requires macOS volume control module.")
    exit(1)


def count_open_fingers(lmlist):
    """Count how many fingers are extended (0-5)."""
    open_count = 0
    
    if lmlist[4][1] > lmlist[3][1]:
        open_count += 1
    
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    for tip, pip in zip(finger_tips, finger_pips):
        if lmlist[tip][2] < lmlist[pip][2]:
            open_count += 1
    
    return open_count


def is_thumbs_up(lmlist):
    """Detect thumbs up gesture (only thumb extended)."""
    thumb_up = lmlist[4][2] < lmlist[0][2]
    
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    fingers_closed = sum(1 for tip, pip in zip(finger_tips, finger_pips) 
                         if lmlist[tip][2] >= lmlist[pip][2])
    
    return thumb_up and fingers_closed >= 3


def _get_camera_source():
    """Read CAMERA_SOURCE env: int index (e.g., "0") or a file path."""
    src = os.getenv("CAMERA_SOURCE", "0").strip()
    try:
        return int(src)
    except ValueError:
        return src


def main():
    """Main application loop."""
    print("Starting Gesture Volume Control...")
    
    cam_src = _get_camera_source()
    cap = cv2.VideoCapture(cam_src)
    if not cap.isOpened():
        # Fallback to another index for multi-camera setups
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("ERROR: No camera found.")
            return
    
    print("Camera ready.")
    
    detector = handDetector(min_detection_confidence=0.7, max_num_hands=1)
    
    volume_history = []
    smoothing_window = 5
    control_enabled = False
    last_thumbs_up_time = 0
    toggle_cooldown = 1.0
    
    print("Controls:")
    print("  👍 Thumbs up = Toggle control ON/OFF")
    print("  ✊ Fist = 0% volume")
    print("  ✋ Open hand = 100% volume")
    print("  Q = Quit")
    
    headless = os.getenv("HEADLESS", "0") == "1"

    while True:
        success, img = cap.read()
        if not success:
            time.sleep(0.1)
            continue
        
        img = cv2.flip(img, 1)
        img = detector.findHands(img, draw=True)
        lmlist = detector.findPositions(img, draw=False)
        
        if len(lmlist) > 0:
            if is_thumbs_up(lmlist):
                current_time = time.time()
                if current_time - last_thumbs_up_time > toggle_cooldown:
                    control_enabled = not control_enabled
                    last_thumbs_up_time = current_time
                    status = "ON" if control_enabled else "OFF"
                    print(f"Control: {status}")
            
            if control_enabled:
                open_fingers = count_open_fingers(lmlist)
                volume_history.append(open_fingers)
                
                if len(volume_history) > smoothing_window:
                    volume_history.pop(0)
                
                smooth_fingers = np.mean(volume_history)
                vol = np.clip((smooth_fingers / 5.0) * 100, 0, 100)
                
                set_volume(int(vol))
                
                cv2.putText(img, f'Volume: {int(vol)}%', (30, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, f'Fingers: {open_fingers}/5', (30, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            else:
                cv2.putText(img, 'CONTROL: OFF', (30, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(img, 'Thumbs up to enable', (30, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if not headless:
            cv2.imshow('Gesture Volume Control', img)
        
        if not headless:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Headless: small sleep to avoid busy loop
            time.sleep(0.01)
    
    cap.release()
    if not headless:
        cv2.destroyAllWindows()
    print("Stopped.")


if __name__ == "__main__":
    main()