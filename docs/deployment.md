# Motus Deployment Guide

## Deployment Options

Motus runs natively on macOS, or in Docker for CI and testing.

## Native macOS Deployment (Recommended)

### Prerequisites

- macOS 11.0 (Big Sur) or higher
- Python 3.10, 3.11, or 3.12
- Webcam with permissions enabled
- 4GB RAM minimum

### Setup

Follow the [Quick Start](../README.md#quick-start) in the main README to install and run Motus. To
launch without retyping the commands, use `./run.sh` or `make run-venv`.

## Docker Deployment

### Limitations

- **macOS:** Docker Desktop on macOS cannot access host camera
- **Volume Control:** Containers cannot modify host system volume
- **Use Case:** CI/CD testing, development only

### Build and Run

```bash
# Build image
docker compose build

# Run in headless mode
docker compose up

# Run with video file
docker run --rm \
  -e HEADLESS=1 \
  -e CAMERA_SOURCE=/app/video.mp4 \
  -v $(pwd)/sample.mp4:/app/video.mp4 \
  motus:latest
```

## CI/CD Deployment

### GitHub Actions Integration

Motus has a CI pipeline (lint, type check, tests, Docker build):

```yaml
# .github/workflows/ci.yml is pre-configured
# Runs automatically on push/PR to main
```

### Manual CI/CD Setup

```bash
# Run full CI pipeline locally
make quality

# Individual steps
make lint
make type-check
make test
make security-scan
```

## Production Checklist

### Before Deployment

- [ ] Python 3.10+ installed and verified
- [ ] All dependencies installed from requirements.txt
- [ ] Camera permissions granted
- [ ] Virtual environment created and activated
- [ ] Environment variables configured
- [ ] Tests passing (`make test`)
- [ ] Security scan clean (`make security-scan`)

### Post-Deployment

- [ ] Application starts without errors
- [ ] Camera initializes successfully
- [ ] Hand detection works
- [ ] Volume control functions
- [ ] Logging configured
- [ ] Monitoring in place (if applicable)

## Monitoring and Logging

### Application Logs

```bash
# Configure log level
export LOG_LEVEL=DEBUG
python -m motus
```

### Health Checks

```bash
# Check if application is running
ps aux | grep motus

# Check resource usage
top -pid $(pgrep -f "python.*motus")
```

### Performance Monitoring

```python
# Add to main.py for FPS monitoring
import time
frame_count = 0
start_time = time.time()

while True:
    frame_count += 1
    if frame_count % 30 == 0:
        fps = 30 / (time.time() - start_time)
        logger.info(f"FPS: {fps:.1f}")
        start_time = time.time()
```

## Troubleshooting Deployment

### Common Issues

#### 1. Camera Not Accessible

```bash
# Check camera permissions
sudo sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db \
  "SELECT * FROM access WHERE service='kTCCServiceCamera';"

# Reset permissions
tccutil reset Camera
```

#### 2. Python Version Issues

```bash
# Verify Python version
python3 --version

# Use pyenv for version management
brew install pyenv
pyenv install 3.12
pyenv global 3.12
```

#### 3. Dependency Conflicts

```bash
# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### 4. Performance Issues

```bash
# Close resource-heavy applications
# Check CPU usage
top -o cpu

# Reduce target FPS in config
# Edit src/motus/config.py: target_fps = 15
```

## Dependency Verification

```bash
# Verify package integrity
pip check

# Scan for vulnerabilities
safety check

# Check for security issues
bandit -r src/motus
```

## Support and Maintenance

### Update Procedure

```bash
# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt
pip install -e .

# Run tests
make test
```

### Rollback Procedure

```bash
# Rollback to previous version
git log --oneline -10  # Find commit hash
git checkout <commit-hash>

# Reinstall dependencies
pip install -r requirements.txt
pip install -e .
```

---

For additional support, see [CONTRIBUTING.md](../CONTRIBUTING.md) or contact @JaKuba23.
