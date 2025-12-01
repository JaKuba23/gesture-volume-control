# MOTUS

```
 ███╗   ███╗ ██████╗ ████████╗██╗   ██╗███████╗
 ████╗ ████║██╔═══██╗╚══██╔══╝██║   ██║██╔════╝
 ██╔████╔██║██║   ██║   ██║   ██║   ██║███████╗
 ██║╚██╔╝██║██║   ██║   ██║   ██║   ██║╚════██║
 ██║ ╚═╝ ██║╚██████╔╝   ██║   ╚██████╔╝███████║
 ╚═╝     ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝
```

**Professional gesture-based volume control system for macOS using machine learning**

[![CI Status](https://github.com/JaKuba23/motus/workflows/CI/badge.svg)](https://github.com/JaKuba23/motus/actions)
[![codecov](https://codecov.io/gh/JaKuba23/motus/branch/main/graph/badge.svg)](https://codecov.io/gh/JaKuba23/motus)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)

---

## Overview

Motus is a production-grade application that enables touchless system volume control through intuitive hand gestures. Built with MediaPipe hand tracking and OpenCV computer vision, it demonstrates advanced machine learning integration for human-computer interaction on macOS platforms.

## Key Features

- Real-time hand landmark detection using MediaPipe Hands (21-point tracking)
- Gesture-based volume control with 5-level precision (0-100%)
- Toggle activation system via thumbs-up gesture
- Adaptive smoothing algorithm for jitter reduction
- Optimized for Apple Silicon (M1/M2) processors
- Comprehensive test suite with 80%+ code coverage
- Docker support for cross-platform development
- Type-safe implementation with full mypy strict compliance

## Quick Start

### Prerequisites

- macOS 11.0 or higher
- Python 3.10, 3.11, or 3.12
- Webcam with camera permissions enabled
- 4GB RAM minimum (8GB recommended for optimal performance)

### Installation

```bash
# Clone repository
git clone https://github.com/JaKuba23/motus.git
cd motus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application

```bash
# Standard execution
python -m motus

# Alternative
python src/motus/main.py
```

### Camera Permissions

Enable camera access in System Settings:

```
System Settings → Privacy & Security → Camera → Enable for Terminal/Python
```

## Usage

### Basic Controls

| Gesture | Volume Level | Description |
|---------|--------------|-------------|
| Closed fist | 0% | Mute |
| 1 finger extended | 20% | Low volume |
| 2 fingers extended | 40% | Medium-low volume |
| 3 fingers extended | 60% | Medium volume |
| 4 fingers extended | 80% | Medium-high volume |
| Open hand (5 fingers) | 100% | Maximum volume |
| Thumbs up | Toggle | Enable/disable control |

### Keyboard Commands

- `Q` - Quit application

### Optimal Performance Tips

- Position hand 30-60cm from camera
- Ensure adequate lighting (>300 lux recommended)
- Keep hand fully visible within frame
- Use smooth movements for fluid volume transitions

## Architecture

```
motus/
├── src/motus/              # Source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration management
│   ├── hand_tracking.py    # MediaPipe integration
│   ├── gestures.py         # Gesture recognition algorithms
│   └── mac_controls.py     # macOS volume control via AppleScript
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Extended documentation
├── .github/                # CI/CD workflows
└── pyproject.toml          # Project configuration
```

### Technical Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Hand Tracking | MediaPipe Hands | 0.10.13 |
| Computer Vision | OpenCV | 4.8.1 |
| Numerical Computing | NumPy | 1.26.4 |
| Volume Control | AppleScript (osascript) | Native |
| Testing | pytest | 7.4+ |
| Type Checking | mypy | 1.5+ |

## Configuration

Configure via environment variables:

```bash
# Camera source (index or video file path)
export CAMERA_SOURCE=0

# Headless mode (no GUI)
export HEADLESS=1
```

Edit configuration in `src/motus/config.py`:

```python
@dataclass(frozen=True)
class AppConfig:
    smoothing_window: int = 5           # Frames for moving average
    toggle_cooldown: float = 1.0        # Seconds between toggles
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    target_fps: int = 30
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests with coverage
pytest --cov=motus --cov-report=term-missing

# Run specific test suite
pytest tests/unit/
pytest tests/integration/

# Run with markers
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/motus --strict

# Security scan
bandit -r src/motus
safety check
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker compose build

# Run in headless mode
docker compose up

# Run with video file
docker compose run --rm -e CAMERA_SOURCE=/app/video.mp4 app
```

### Limitations

Docker deployment on macOS has constraints:
- Host camera cannot be accessed from container
- System volume control unavailable in container
- Suitable for testing/CI pipelines only

For production use on macOS, run natively outside Docker.

## Performance

Benchmarks on Apple M1 MacBook Pro (16GB RAM):

| Metric | Value |
|--------|-------|
| Frame Rate | 30-60 FPS |
| CPU Usage | 8-15% (single core) |
| Memory Usage | ~250MB |
| Detection Latency | <33ms (30 FPS) |
| Gesture Response Time | 100-200ms |

## Troubleshooting

### Camera Not Opening

- Close applications using camera (Zoom, FaceTime, etc.)
- Verify camera permissions in System Settings
- Check camera is not hardware-disabled
- Restart Terminal/IDE

### Hand Detection Issues

- Improve lighting conditions
- Ensure hand is fully in frame
- Adjust `min_detection_confidence` in config
- Clean camera lens

### Performance Issues

- Close resource-intensive applications
- Reduce `target_fps` in configuration
- Disable hand landmark drawing (`draw=False`)
- Use lower camera resolution via `CAMERA_SOURCE`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Coding standards
- Testing requirements
- Pull request process

## Security

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).

Do not open public issues for security concerns.

## Documentation

- [Architecture Documentation](docs/architecture.md)
- [API Reference](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Polish Documentation](docs/pl/README.pl.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) by Google for hand tracking framework
- [OpenCV](https://opencv.org/) for computer vision library
- Inspired by automotive gesture control systems

## Author

**Created by JaKuba23**

- GitHub: [@JaKuba23](https://github.com/JaKuba23)
- Portfolio: [jakuba23.dev](https://jakuba23.dev)

---

**Professional AI/ML Portfolio Project**

Demonstrates: Computer Vision | Machine Learning | Real-time Processing | System Integration | Professional Software Engineering

---

## Project Status

**Production Ready** - Fully tested, documented, and deployable

- CI/CD pipeline with GitHub Actions
- 80%+ test coverage
- Type-safe with mypy strict mode
- Security scanned with Bandit
- Automated dependency updates via Dependabot

---

If you find this project useful, please consider giving it a star ⭐
