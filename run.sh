#!/usr/bin/env zsh
# Motus launcher script
# Automatically selects the best Python interpreter

set -euo pipefail

echo "Starting Motus - Gesture Volume Control"

# Check Python version
check_python_version() {
    local python_cmd=$1
    local version=$($python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' 2>/dev/null || echo "0.0")
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)
    
    if [[ $major -ge 3 ]] && [[ $minor -ge 10 ]]; then
        return 0
    else
        return 1
    fi
}

# Try virtual environment first
if [[ -x "./venv/bin/python" ]]; then
    if check_python_version "./venv/bin/python"; then
        echo "Using virtual environment Python"
        ./venv/bin/python -c "import motus" 2>/dev/null || ./venv/bin/python -m pip install -e . --quiet
        exec ./venv/bin/python -m motus
    else
        echo "Warning: Virtual environment Python version too old (need 3.10+)"
    fi
fi

# Fall back to system Python
for python_cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$python_cmd" &> /dev/null; then
        if check_python_version "$python_cmd"; then
            echo "Using system Python: $python_cmd"
            "$python_cmd" -c "import motus" 2>/dev/null || "$python_cmd" -m pip install -e . --quiet
            exec "$python_cmd" -m motus
        fi
    fi
done

echo "Error: No suitable Python interpreter found (need Python 3.10+)"
echo "Please install Python 3.10 or higher"
exit 1
