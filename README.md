# 🎛️ Gesture Volume Control

Control your Mac's system volume using simple hand gestures. No keyboard or mouse required!

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🖐️ **Hand-based volume control** - Open and close your hand to adjust volume
- 👍 **Thumbs up toggle** - Enable/disable control with a simple gesture
- 📊 **Smooth transitions** - Uses moving average for fluid volume changes
- 🎥 **Real-time feedback** - Live camera view with hand tracking visualization
- ⚡ **Optimized performance** - Runs smoothly with minimal CPU usage

## 🎬 Demo

| Gesture | Volume | Description |
|---------|--------|-------------|
| ✊ Fist | 0% | Closed fist = silence |
| 🤏 1 finger | 20% | One finger extended |
| ✌️ 2 fingers | 40% | Two fingers extended |
| 🤟 3 fingers | 60% | Three fingers extended |
| 🖖 4 fingers | 80% | Four fingers extended |
| ✋ Open hand | 100% | All fingers extended = max volume |
| 👍 Thumbs up | Toggle | Enable/disable control |

## 📋 Requirements

- macOS (tested on macOS 14+)
- Python 3.12+
- Webcam
- Camera permissions for Python/Terminal

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/gesture-volume-control.git
cd gesture-volume-control
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Grant camera permissions:**
   - Go to **System Settings > Privacy & Security > Camera**
   - Enable access for Terminal or Python

## 🎮 Usage

1. **Start the application:**
```bash
python main.py
```

2. **Controls:**
   - Show **👍 thumbs up** to toggle control ON/OFF
   - **Open your hand** gradually to increase volume
   - **Close your fist** to decrease volume
   - Press **Q** to quit

3. **Tips:**
   - Keep your hand 30-60cm from the camera
   - Ensure good lighting for better detection
   - Move your hand smoothly for fluid volume changes

## 🏗️ Project Structure

```
gesture-volume-control/
├── main.py                  # Main application
├── handTrackingModule.py    # MediaPipe hand detection
├── mac_controls.py          # macOS volume control
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
└── .gitignore              # Git ignore rules
```

## 🔧 How It Works

### Hand Detection
Uses [MediaPipe](https://google.github.io/mediapipe/) to detect 21 hand landmarks in real-time:

```
Landmarks used:
- 0: Wrist (reference point)
- 3-4: Thumb joints
- 6,8: Index finger joints
- 10,12: Middle finger joints
- 14,16: Ring finger joints
- 18,20: Pinky finger joints
```

### Volume Mapping
```python
fingers_extended = count_open_fingers(hand)  # 0-5
volume = (fingers_extended / 5.0) * 100      # 0-100%
```

### Smoothing Algorithm
Uses a moving average window (5 frames) to prevent jittery volume changes:
```python
smooth_value = mean(last_5_measurements)
```

## 🛠️ Technical Details

| Component | Technology |
|-----------|------------|
| Hand Tracking | MediaPipe Hands |
| Computer Vision | OpenCV |
| Volume Control | AppleScript (osascript) |
| Smoothing | NumPy moving average |

### Configuration

Edit these values in `main.py` to customize behavior:

```python
smoothing_window = 5        # Frames to average (higher = smoother)
toggle_cooldown = 1.0       # Seconds between toggles
min_detection_confidence = 0.7  # Detection threshold (0.0-1.0)
```

## 🐛 Troubleshooting

**Camera not opening:**
- Check if another app is using the camera (Zoom, FaceTime, etc.)
- Verify camera permissions in System Settings
- Try restarting your computer

**Hand not detected:**
- Ensure good lighting
- Keep hand fully visible in frame
- Try different hand positions

**Volume changes too fast/slow:**
- Increase `smoothing_window` for slower, smoother changes
- Decrease `smoothing_window` for faster response

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking
- [OpenCV](https://opencv.org/) for computer vision
- Inspired by gesture control systems in modern vehicles

## 👨‍💻 Author

Created by [JaKuba23]

---

**⭐ If you find this project useful, please give it a star!**

---

### Start command (for deployment forms)

If a platform asks for the start/run command, use:

```
python3 main.py
```

If you are using a local virtual environment created at `./venv`, use:

```
./venv/bin/python main.py
```
