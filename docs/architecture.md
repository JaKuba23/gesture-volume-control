# Motus Architecture Documentation

## System Overview

Motus is a real-time gesture recognition system built on a modular architecture that separates concerns into distinct components:

```
┌─────────────────────────────────────────────────────────┐
│                     Main Application                     │
│                   (motus/main.py)                       │
└──────────┬──────────────────────────────────────────────┘
           │
           ├─────────┐         ├─────────┐        ├────────┐
           │         │         │         │        │        │
    ┌──────▼────┐ ┌─▼─────────▼┐ ┌─────▼──────┐ ┌▼───────▼┐
    │  Config   │ │   Hand      │ │  Gestures  │ │  Volume │
    │  Manager  │ │  Tracking   │ │  Detection │ │ Control │
    └───────────┘ └─────────────┘ └────────────┘ └─────────┘
                        │                │             │
                   ┌────▼────┐     ┌────▼────┐   ┌────▼────┐
                   │MediaPipe│     │ Custom  │   │AppleScript│
                   │  Hands  │     │Algorithm│   │osascript│
                   └─────────┘     └─────────┘   └──────────┘
```

## Component Architecture

### 1. Configuration Layer (`config.py`)

**Responsibility:** Centralized configuration management

**Key Features:**
- Immutable configuration using frozen dataclasses
- Environment variable integration
- Validation of configuration values
- Type-safe configuration access

**Design Pattern:** Configuration Object Pattern

```python
@dataclass(frozen=True)
class AppConfig:
    smoothing_window: int = 5
    toggle_cooldown: float = 1.0
    # ... other settings
```

### 2. Hand Tracking Module (`hand_tracking.py`)

**Responsibility:** Real-time hand landmark detection

**Key Features:**
- MediaPipe Hands integration
- 21-point landmark detection
- Configurable confidence thresholds
- Performance optimization (non-writeable frames)

**Design Pattern:** Facade Pattern (wraps MediaPipe complexity)

**Algorithm:**
1. Convert BGR frame to RGB
2. Set frame as non-writeable (performance)
3. Process with MediaPipe
4. Extract 21 landmark positions
5. Convert to pixel coordinates

### 3. Gesture Recognition (`gestures.py`)

**Responsibility:** Interpret hand landmarks as gestures

**Key Features:**
- Finger counting algorithm
- Thumbs-up detection
- Open/closed hand detection
- Stateless gesture recognition

**Design Pattern:** Strategy Pattern (different gesture algorithms)

**Finger Counting Algorithm:**
```
For each finger:
  - Thumb: Compare tip (4) x-position with joint (3)
  - Others: Compare tip y-position with PIP joint
  
Extended finger count = volume percentage
```

### 4. Volume Control (`mac_controls.py`)

**Responsibility:** Platform-specific volume management

**Key Features:**
- AppleScript integration via subprocess
- Error handling and logging
- Platform detection
- Graceful degradation on non-macOS

**Design Pattern:** Abstract Factory (allows platform-specific implementations)

**Execution Flow:**
1. Validate platform is Darwin (macOS)
2. Check osascript availability
3. Execute AppleScript command
4. Handle errors gracefully

### 5. Main Application (`main.py`)

**Responsibility:** Application orchestration and main loop

**Key Features:**
- Camera initialization with fallback
- Frame processing pipeline
- UI rendering
- State management (control enabled/disabled)
- Smoothing history management

**Design Pattern:** Main Loop Pattern

## Data Flow

### Normal Operation Flow

```
1. Camera Capture
   ↓
2. Frame Flip (mirror image)
   ↓
3. Hand Detection (MediaPipe)
   ↓
4. Landmark Extraction
   ↓
5. Gesture Recognition
   ↓
6. Smoothing Algorithm
   ↓
7. Volume Mapping (0-5 fingers → 0-100%)
   ↓
8. Volume Control (osascript)
   ↓
9. UI Rendering
   ↓
10. Display Frame
```

### Toggle Flow

```
1. Detect Thumbs-up Gesture
   ↓
2. Check Cooldown Timer
   ↓
3. Toggle Control State
   ↓
4. Update Last Toggle Time
   ↓
5. Log State Change
```

## Performance Optimizations

### 1. Frame Processing

- **Non-writeable frames:** MediaPipe processes read-only frames faster
- **Mirroring:** Single horizontal flip operation
- **Conditional drawing:** Only draw landmarks when needed

### 2. Smoothing Algorithm

- **Moving average window:** Reduces jitter without lag
- **Circular buffer:** O(1) append/remove operations
- **NumPy operations:** Vectorized mean calculation

### 3. Volume Control

- **Subprocess caching:** Reuse subprocess module
- **Timeout protection:** Prevent hanging on osascript
- **Silent failures:** Non-macOS platforms don't block

## Error Handling Strategy

### Graceful Degradation

1. **Camera Failure:**
   - Try primary source
   - Fallback to alternative index
   - Clear error message if all fail

2. **Hand Detection Failure:**
   - Continue processing next frame
   - Show "control off" UI
   - No application crash

3. **Volume Control Failure:**
   - Log error
   - Continue gesture detection
   - Allow retry on next gesture

### Logging Levels

- **INFO:** Application state changes, initialization
- **WARNING:** Non-critical failures (e.g., wrong platform)
- **ERROR:** Critical failures requiring attention
- **DEBUG:** Detailed operational information

## Concurrency Model

**Type:** Single-threaded event loop

**Rationale:**
- Eliminates race conditions
- Simpler debugging
- Sufficient performance (30+ FPS)
- No shared mutable state

## State Management

### Application State

```python
control_enabled: bool           # Whether gesture control is active
last_thumbs_up_time: float     # Timestamp of last toggle
volume_history: List[float]    # Recent finger counts for smoothing
```

### State Transitions

```
                    ┌──────────┐
                    │ Starting │
                    └────┬─────┘
                         │
                    ┌────▼─────┐
            ┌──────►│ Disabled │◄──────┐
            │       └────┬─────┘       │
            │            │              │
    Thumbs-up      Thumbs-up     Thumbs-up
            │            │              │
            │       ┌────▼──────┐       │
            └───────┤  Enabled  ├───────┘
                    └───────────┘
```

## Testing Architecture

### Test Pyramid

```
        ┌────────────┐
        │Integration │  10% - End-to-end workflows
        │   Tests    │
        ├────────────┤
        │   Unit     │  90% - Individual components
        │   Tests    │
        └────────────┘
```

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Component tests
│   ├── test_config.py
│   ├── test_gestures.py
│   ├── test_hand_tracking.py
│   ├── test_mac_controls.py
│   └── test_main.py
└── integration/          # Integration tests
    └── test_workflow.py
```

### Mocking Strategy

- **External dependencies mocked:** MediaPipe, OpenCV, subprocess
- **Pure functions tested directly:** Gesture algorithms
- **Integration tests use minimal mocking:** Test real interactions

## Security Considerations

### 1. Input Validation

- Camera source validated (int or valid path)
- Configuration values range-checked
- Volume clamped to 0-100

### 2. Privilege Management

- No elevated privileges required
- User-level camera access only
- No system modification beyond volume

### 3. Data Privacy

- All processing local (no network)
- No frame recording or storage
- No telemetry or tracking

## Deployment Architectures

### Native macOS Deployment

```
User → Terminal → Python → Motus → Camera + Volume
```

**Advantages:**
- Full functionality
- Best performance
- Direct hardware access

### Docker Deployment

```
User → Docker → Container → Motus (headless)
```

**Limitations:**
- No camera access on macOS Docker
- No volume control in container
- Suitable for CI/testing only

