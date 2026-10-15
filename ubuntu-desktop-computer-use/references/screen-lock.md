# Screen-lock configuration for Computer Use

Use this branch when screen locking prevents the intended Computer Use workflow from keeping the desktop accessible. It is machine preparation for Computer Use, not unrelated host maintenance.

## Diagnose before changing policy

Check the target graphical session's `LockedHint` and GNOME `org.gnome.ScreenSaver.GetActive` as described in [troubleshooting.md](troubleshooting.md). They can disagree. Ask what the human sees instead of declaring the screen unlocked from one result.

A currently locked screen needs a manual unlock. Disabling automatic locking does not unlock it. For supervised Computer Use, manual unlock may be all that is needed.

## Configure continued desktop availability

When the intended workflow needs automatic/suspend locking disabled, explain that anyone with physical access can use the logged-in accounts. Obtain explicit action-specific approval before changing these security settings. Do not infer approval from a general request to install Computer Use.

Run as the target desktop user with the correct session bus. Inspect key availability and saved values:

```bash
gsettings list-keys org.gnome.desktop.screensaver
gsettings get org.gnome.desktop.screensaver lock-enabled
gsettings get org.gnome.desktop.screensaver ubuntu-lock-on-suspend
```

On the recorded Ubuntu GNOME version, after approval:

```bash
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver ubuntu-lock-on-suspend false
gsettings get org.gnome.desktop.screensaver lock-enabled
gsettings get org.gnome.desktop.screensaver ubuntu-lock-on-suspend
```

Set only supported keys covered by the approval. Preserve unrelated settings. For separately agreed idle/AC-suspend changes needed for Computer Use, use [keep-desktop-awake.md](keep-desktop-awake.md). Lock-policy changes alone do not authorize that branch or automatic-login configuration.

## Verify the setup

Require readback of the authorized values. These settings take effect without reboot, but do not prevent manual locking. If the screen is already locked, have the human unlock it once; then recheck current lock state and verify actual Computer Use capture/input separately.

Historical readback changed both values from `true` to `false`. Later the desktop was unlocked and portal screenshot capture worked. This establishes saved policy and that session's availability, not a tested reboot/suspend cycle or guaranteed unattended access.

**Dead end to avoid:** repeatedly restarting or changing lock policy to dismiss an existing lock. Neither replaces the needed manual unlock.
