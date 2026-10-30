#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml


def load_config(config_path: str):
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a YAML dictionary.")

    return data


def parse_time(value: str):
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise ValueError(f"Invalid time value: {value!r}. Expected HH:MM") from exc


def current_time_ok(windows):
    if not windows:
        return True

    now = datetime.now().time()
    for entry in windows:
        start = parse_time(entry["start"])
        end = parse_time(entry["end"])
        if start <= end:
            if start <= now <= end:
                return True
        else:
            if now >= start or now <= end:
                return True
    return False


def run_command(command: str):
    if not command:
        return
    subprocess.Popen(command, shell=True)


def kill_processes(patterns):
    if not patterns:
        return

    for pattern in patterns:
        subprocess.run(["bash", "-lc", f"pkill -f -- '{pattern}' || true"], check=False)


def is_allowed_app(app_name: str, allowed_apps):
    if not allowed_apps:
        return False
    return app_name in allowed_apps or app_name.split("/")[-1] in allowed_apps


def launch_allowed_app(app_name: str, config: dict):
    allowed = config.get("allowed_apps", [])
    if not is_allowed_app(app_name, allowed):
        print(f"App not allowed: {app_name}")
        return 1

    if not current_time_ok(config.get("allowed_time_windows", [])):
        print(config.get("messages", {}).get("time_limit", "This app is not available right now."))
        return 2

    run_command(app_name)
    return 0


def monitor(config: dict):
    blocked = config.get("blocked_processes", [])
    windows = config.get("allowed_time_windows", [])
    message = config.get("messages", {}).get("time_limit", "Access is restricted right now.")

    print("Kid Mode monitor started. Press Ctrl+C to exit.")
    try:
        while True:
            if not current_time_ok(windows):
                kill_processes(blocked)
                print(message)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


def status(config: dict):
    windows = config.get("allowed_time_windows", [])
    print(f"Allowed time: {windows}")
    print(f"Current time allowed: {current_time_ok(windows)}")
    print(f"Allowed apps: {config.get('allowed_apps', [])}")
    print(f"Blocked processes: {config.get('blocked_processes', [])}")


def main():
    parser = argparse.ArgumentParser(description="Parent-managed Kid Mode launcher for Bazzite/KDE")
    parser.add_argument("--config", default="config.yaml", help="Path to the YAML config file")
    parser.add_argument("--launch", help="Launch a single app if it is in the config allow list")
    parser.add_argument("--monitor", action="store_true", help="Run the enforcement monitor")
    parser.add_argument("--status", action="store_true", help="Print the current configuration status")
    parser.add_argument("--block", action="store_true", help="Kill all blocked processes right now")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    if args.block:
        kill_processes(config.get("blocked_processes", []))
        print("Blocked processes terminated.")
        return 0

    if args.status:
        status(config)
        return 0

    if args.launch:
        return launch_allowed_app(args.launch, config)

    if args.monitor:
        monitor(config)
        return 0

    print("No action requested. Use --launch, --monitor, or --status.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
