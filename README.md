# Bazzite Kid Mode

A simple, safe, parent-managed launcher for Bazzite/KDE child accounts. It is designed to run as a standard user and enforce a limited desktop environment without requiring the child to know an admin password.

This project is intentionally limited to legitimate parental-control behavior:
- allow only a small set of approved apps
- block known game/online launchers during restricted hours
- enforce a daily usage window
- keep the browser limited to a safe, controlled experience

It does not bypass admin protections or defeat system security. It is meant to help parents provide a managed child experience on a home Linux workstation.

## Features
- Approved app launcher list
- Daily time window enforcement
- Browser-safe wrapper for restricted web access
- Process blocking for games and social apps during restricted windows
- KDE autostart support for login-time enforcement

## Files
- `kid_mode.py` — main monitoring and launcher logic
- `config.yaml` — sample child-safe configuration
- `kde/autostart/kid-mode.desktop` — KDE autostart entry
- `scripts/kid_mode_launcher.sh` — launcher wrapper for login
- `requirements.txt` — Python dependencies

## Quick start

1. Clone the repo
2. Install Python deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Review and edit `config.yaml`
4. Start the monitor:
   ```bash
   python3 kid_mode.py --monitor --config config.yaml
   ```
5. To launch only a safe app:
   ```bash
   python3 kid_mode.py --launch "firefox"
   ```

## KDE autostart

Copy the example file into your user startup folder:

```bash
mkdir -p ~/.config/autostart
cp kde/autostart/kid-mode.desktop ~/.config/autostart/
```

Then edit the path in the desktop file to point to your local checkout.

## Important safety notes
- Use this as a parent-managed, account-level launcher.
- Keep the child on a Standard user account, not an admin account.
- The parent should maintain the configuration and review it regularly.
- This is not designed to bypass system permissions or admin controls.

## Example configuration

The included `config.yaml` is a template. You can tailor it for your home setup:
- `allowed_apps` = programs the child may use
- `blocked_processes` = apps to stop during restricted time
- `allowed_time_windows` = allowed login periods
- `safe_browser_url` = a safe landing page for browsing

## Suggested use on Bazzite/KDE
- Create a separate Standard child account
- Put this launcher in KDE autostart
- Restrict ~/.config/autostart for the child account
- Keep the browser limited by a safe landing page or dedicated browser wrapper
- Use the parent login to edit config and grant time windows

## License
MIT
