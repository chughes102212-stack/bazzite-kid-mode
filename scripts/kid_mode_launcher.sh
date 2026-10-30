#!/usr/bin/env bash

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
CONFIG_PATH="$SCRIPT_DIR/../config.yaml"

python3 "$SCRIPT_DIR/../kid_mode.py" --monitor --config "$CONFIG_PATH"
