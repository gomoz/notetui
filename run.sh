#!/bin/bash
# Simple launcher for NoteTUI

# Change to the notetui directory
cd "$(dirname "$0")"

# Run with uv (which manages the venv)
uv run python -m notetui.app
