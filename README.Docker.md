## Docker usage

This project is a desktop-style app (camera + macOS volume control). Running in Docker is supported in a limited, headless way for demo/build purposes. On macOS, a container cannot access the host camera or change host volume.

### Build and run (headless)

```
docker compose up --build
```

The container sets `HEADLESS=1` and `CAMERA_SOURCE=0` by default. No GUI window will be shown.

### Feeding a video file (macOS/Linux)

Copy your video into the image or mount it, then run:

```
docker compose run --rm -e CAMERA_SOURCE=/app/sample.mp4 app
```

### Linux: use a physical camera (experimental)

```
docker compose run --rm \
	--device /dev/video0:/dev/video0 \
	-e CAMERA_SOURCE=0 \
	app
```

### Environment variables
- HEADLESS: `1` disables GUI windows (default in container)
- CAMERA_SOURCE: camera index (e.g., `0`) or path to a video file inside the container

### Recommended: run locally (non-Docker)

```
python3 -u main.py
# or
./venv/bin/python main.py
```
This is the recommended way on macOS to actually use camera and control system volume.