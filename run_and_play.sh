#!/usr/bin/env bash
set -e
# Usage: ./run_and_play.sh "Text to speak"
cd "$(dirname "$0")"
TEXT="${1:-Hello from the Empathy Engine}"
# activate venv if present
if [ -f venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi
export PYTHONPATH=./src
python3 -m src.main "$TEXT"
# Open the resulting audio on macOS
if command -v open >/dev/null 2>&1; then
  open output.wav
else
  echo "Please open output.wav with your preferred audio player"
fi
