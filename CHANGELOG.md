# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-01

### Added
- Initial release
- Real-time hand tracking using MediaPipe Hands (21-point landmark detection)
- Gesture-based volume control with 5-level precision (0-100%)
- Thumbs-up toggle activation system
- Smoothing over recent frames to reduce jitter
- Unit and integration test suite (pytest)
- Type annotations checked with mypy
- CI pipeline with GitHub Actions (lint, type check, tests, Docker build)
- Docker image for headless/CI use
- README, CONTRIBUTING, SECURITY docs (English + Polish)
- Security scanning with Bandit and Safety
- Automated dependency updates via Dependabot
- Pre-commit hooks
- EditorConfig for consistent code style

### Technical
- Python 3.10+ support
- Apple Silicon (M1/M2) optimization
- OpenCV 4.8.1 integration
- MediaPipe 0.10.13 integration
- NumPy 1.26.4 for numerical operations
- Pytest-based testing framework
- Black code formatting
- isort import sorting
- flake8 linting
- mypy type checking

### Documentation
- README with usage, architecture and dev setup
- Contributing guidelines
- Security policy
- Architecture documentation
- Deployment guide
- Polish translation

[Unreleased]: https://github.com/JaKuba23/gesture-volume-control/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/JaKuba23/gesture-volume-control/releases/tag/v1.0.0

