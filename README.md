# Motus

**Touchless macOS volume control using hand gestures, built with MediaPipe and OpenCV.**

[![CI](https://github.com/JaKuba23/gesture-volume-control/workflows/CI/badge.svg)](https://github.com/JaKuba23/gesture-volume-control/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Overview

Motus reads hand landmarks from a webcam feed with MediaPipe Hands and maps finger-count gestures to macOS system volume. It is a personal project built to work hands-on with real-time computer vision and gesture recognition, not a commercial product.

## Features

- Real-time hand landmark detection (MediaPipe Hands, 21-point tracking)
- Gesture-to-volume mapping with 5 discrete levels (0-100%)
- Thumbs-up gesture toggles control on/off
- Smoothing over recent frames to reduce jitter
- Optimized for Apple Silicon
- Unit and integration test suite (pytest)
- Docker image for headless/CI use

## Quick Start

### Prerequisites

- macOS 11.0 or higher
- Python 3.10, 3.11, or 3.12
- Webcam with camera permission enabled

### Installation

```bash
git clone https://github.com/JaKuba23/gesture-volume-control.git
cd gesture-volume-control

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Running

```bash
python -m motus
# or
python src/motus/main.py
```

### Camera Permissions

```
System Settings → Privacy & Security → Camera → Enable for Terminal/Python
```

## Usage

| Gesture | Volume Level |
|---------|--------------|
| Closed fist | 0% (mute) |
| 1 finger extended | 20% |
| 2 fingers extended | 40% |
| 3 fingers extended | 60% |
| 4 fingers extended | 80% |
| Open hand (5 fingers) | 100% |
| Thumbs up | Toggle control on/off |

Press `Q` to quit.

Tips: keep your hand 30-60cm from the camera, in good lighting, fully inside the frame.

## Architecture

```
motus/
├── src/motus/              # Source code
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration
│   ├── hand_tracking.py    # MediaPipe integration
│   ├── gestures.py         # Gesture recognition
│   └── mac_controls.py     # macOS volume control via AppleScript
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
└── .github/                # CI workflows
```

### Stack

| Component | Technology |
|-----------|------------|
| Hand tracking | MediaPipe Hands |
| Computer vision | OpenCV |
| Numerical computing | NumPy |
| Volume control | AppleScript (osascript) |
| Testing | pytest |
| Type checking | mypy |

## Configuration

```bash
export CAMERA_SOURCE=0   # camera index or video file path
export HEADLESS=1        # no GUI window
```

```python
@dataclass(frozen=True)
class AppConfig:
    smoothing_window: int = 5
    toggle_cooldown: float = 1.0
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    target_fps: int = 30
```

## Development

```bash
pip install -r requirements-dev.txt
pre-commit install
```

```bash
# Tests
pytest --cov=motus --cov-report=term-missing

# Formatting and linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# Type checking
mypy src/motus --strict

# Security scan
bandit -r src/motus
safety check
```

## Docker

```bash
docker compose build
docker compose up   # headless mode
```

Camera access and system volume control are not available inside a container — Docker here is for CI/testing, not for running the app day-to-day. Run natively on macOS for actual use.

## Troubleshooting

**Camera won't open** — close other apps using the camera (Zoom, FaceTime), check camera permission in System Settings, restart the terminal/IDE.

**Hand not detected** — improve lighting, keep the hand fully in frame, adjust `min_detection_confidence` in `config.py`.

**Performance** — close other resource-heavy apps, lower `target_fps`, or disable landmark drawing.

## Documentation

- [Architecture](docs/architecture.md)
- [Deployment](docs/deployment.md)
- [Polish README](docs/pl/README.pl.md)

## License

MIT — see [LICENSE](LICENSE).

## Author

**JaKuba23** — [github.com/JaKuba23](https://github.com/JaKuba23)
