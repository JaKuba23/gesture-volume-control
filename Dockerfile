# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim as base

# Metadata
LABEL org.opencontainers.image.title="Motus"
LABEL org.opencontainers.image.description="Gesture-based volume control for macOS"
LABEL org.opencontainers.image.authors="JaKuba23"
LABEL org.opencontainers.image.source="https://github.com/JaKuba23/gesture-volume-control"
LABEL org.opencontainers.image.licenses="MIT"

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Default to headless mode in container
ENV HEADLESS=1
ENV CAMERA_SOURCE=0

WORKDIR /app

# System libraries needed by OpenCV in runtime (headless)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy application source
COPY src/ src/
COPY LICENSE ./

# Add src to PYTHONPATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Switch to non-privileged user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "from motus import __version__; print(__version__)" || exit 1

# Run application
CMD ["python", "-m", "motus"]
