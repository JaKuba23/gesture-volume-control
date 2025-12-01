# Motus Deployment Guide

## Deployment Options

Motus can be deployed in multiple configurations depending on your requirements.

## Native macOS Deployment (Recommended)

### Prerequisites

- macOS 11.0 (Big Sur) or higher
- Python 3.10, 3.11, or 3.12
- Webcam with permissions enabled
- 4GB RAM minimum

### Production Deployment Steps

#### 1. System Preparation

```bash
# Update system
sudo softwareupdate --install --all

# Install Python (if not present)
brew install python@3.12

# Verify Python version
python3 --version  # Should be 3.10+
```

#### 2. Application Installation

```bash
# Create application directory
sudo mkdir -p /opt/motus
cd /opt/motus

# Clone repository
git clone https://github.com/JaKuba23/motus.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configuration

```bash
# Set environment variables
cat > /opt/motus/.env << EOF
CAMERA_SOURCE=0
HEADLESS=0
EOF
```

#### 4. Permissions

```bash
# Grant camera permissions
# Go to: System Settings → Privacy & Security → Camera
# Enable for Terminal or your application launcher
```

#### 5. Launch Application

```bash
# Manual launch
/opt/motus/venv/bin/python -m motus

# Or use helper script
chmod +x /opt/motus/run.sh
/opt/motus/run.sh
```

### LaunchAgent (Auto-start on Login)

Create `~/Library/LaunchAgents/com.jakuba23.motus.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jakuba23.motus</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/motus/venv/bin/python</string>
        <string>-m</string>
        <string>motus</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/opt/motus</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/motus.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/motus.error.log</string>
</dict>
</plist>
```

Load the agent:

```bash
launchctl load ~/Library/LaunchAgents/com.jakuba23.motus.plist
```

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

### Multi-architecture Build

```bash
# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/jakuba23/motus:latest \
  --push \
  .
```

## Kubernetes Deployment (Not Recommended)

Motus is not designed for Kubernetes deployment due to:
- Hardware requirements (webcam access)
- Desktop application nature
- Real-time processing constraints

If deploying to Kubernetes for testing:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: motus-test
spec:
  containers:
  - name: motus
    image: ghcr.io/jakuba23/motus:latest
    env:
    - name: HEADLESS
      value: "1"
    - name: CAMERA_SOURCE
      value: "/app/test-video.mp4"
```

## CI/CD Deployment

### GitHub Actions Integration

Motus includes comprehensive CI/CD:

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
# View logs (if using LaunchAgent)
tail -f /tmp/motus.log
tail -f /tmp/motus.error.log

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
```

#### 4. Performance Issues

```bash
# Close resource-heavy applications
# Check CPU usage
top -o cpu

# Reduce target FPS in config
# Edit src/motus/config.py: target_fps = 15
```

## Backup and Recovery

### Configuration Backup

```bash
# Backup configuration
tar -czf motus-config-backup.tar.gz \
  /opt/motus/.env \
  /opt/motus/src/motus/config.py
```

### Full Application Backup

```bash
# Backup entire installation
tar -czf motus-full-backup.tar.gz \
  --exclude='venv' \
  --exclude='__pycache__' \
  /opt/motus/
```

### Recovery

```bash
# Restore from backup
cd /opt/
tar -xzf motus-full-backup.tar.gz

# Recreate virtual environment
cd motus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Security Hardening

### File Permissions

```bash
# Set appropriate permissions
sudo chown -R $(whoami):staff /opt/motus
chmod 755 /opt/motus
chmod 644 /opt/motus/src/motus/*.py
chmod 755 /opt/motus/run.sh
```

### Network Isolation

Motus does not require network access:

```bash
# Block network access (optional)
sudo pfctl -e
sudo pfctl -f /etc/pf.conf
```

### Dependency Verification

```bash
# Verify package integrity
pip check

# Scan for vulnerabilities
safety check

# Check for security issues
bandit -r src/motus
```

## Scaling Considerations

Motus is designed for single-user deployment. For multiple users:

### Option 1: Multiple Instances

- Deploy separate instance per user
- Use different camera sources
- Isolate configurations

### Option 2: Multi-user Server (Future)

- Would require architectural changes
- WebSocket for remote control
- Centralized gesture processing
- Not currently supported

## Support and Maintenance

### Update Procedure

```bash
# Pull latest changes
cd /opt/motus
git pull origin main

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Run tests
make test

# Restart application
# (kill existing process and relaunch)
```

### Rollback Procedure

```bash
# Rollback to previous version
git log --oneline -10  # Find commit hash
git checkout <commit-hash>

# Reinstall dependencies
pip install -r requirements.txt

# Restart application
```

---

For additional support, see [CONTRIBUTING.md](../CONTRIBUTING.md) or contact @JaKuba23.

