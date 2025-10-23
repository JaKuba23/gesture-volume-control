#!/usr/bin/env zsh
# Small helper to run the Gesture Volume Control app with the right interpreter.
set -euo pipefail

if [[ -x "./venv/bin/python" ]]; then
  ./venv/bin/python main.py
else
  python3 main.py
fi
