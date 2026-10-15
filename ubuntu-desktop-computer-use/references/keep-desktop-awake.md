# Keep the desktop awake for Computer Use

Use this branch when screen blanking, dimming, or automatic suspend prevents the intended Computer Use workflow from seeing or reaching the desktop. Screen sleep is distinct from screen locking and from the whole machine suspending.

**Failure pattern:** disabling screen locking alone can leave the display blank or the machine unavailable after inactivity.

**Reference validation boundary:** in one tested GNOME setup, the human pressed Shift and reported a visible desktop with no lock screen; the next portal screenshot succeeded. GNOME settings were subsequently read back as idle delay `uint32 0`, dimming `false`, and AC idle action `'nothing'`. No full idle period or reboot was tested.

## 1. Recover and distinguish the current state

If a connected monitor shows no image until keyboard activity, ask the human to wake it with Shift and report whether a lock screen appears. Pause observation during any private unlock input. Re-observe through scoped `get_app_state` with a screenshot after the human returns.

A usable screenshot after waking is evidence of recovery, not proof of every black-screen cause. It also does not prove window targeting or input: check the intended application's window separately.

## 2. Inspect the target user's idle policy

Run as the target desktop user with the correct graphical-session bus. Inspect key availability on the installed GNOME version before relying on this recipe:

```bash
gsettings list-keys org.gnome.desktop.session
gsettings list-keys org.gnome.settings-daemon.plugins.power
gsettings get org.gnome.desktop.session idle-delay
gsettings get org.gnome.settings-daemon.plugins.power idle-dim
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type
gsettings range org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type
gsettings get org.gnome.desktop.screensaver lock-enabled
```

The recorded machine had a 300-second idle delay, dimming enabled, AC idle action `'suspend'` with timeout `0`, and locking already disabled. A saved action of `'suspend'` with timeout `0` alone does not establish that automatic suspension actually occurred.

## 3. Apply the agreed Computer Use availability settings

Confirm that the intended workflow requires the desktop to remain awake while plugged in. Explain increased energy use and an illuminated/unattended screen; agree on the change before applying it. Setting `idle-delay=0` can also affect automatic locking because GNOME's idle blanking and lock activation are coupled. An unchanged `lock-enabled` key does not guarantee unchanged protection. If automatic locking is enabled, obtain explicit approval for this potential reduction before changing idle delay; otherwise leave it unchanged. Direct lock-key changes use the separately approved branch in [screen-lock.md](screen-lock.md).

For the supported GNOME keys, the recorded successful configuration was:

```bash
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.settings-daemon.plugins.power idle-dim false
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
```

The AC idle-action change is AC-specific. Idle delay and dimming are user settings, not AC-only settings. Leave the battery idle-action key, existing lock key, and unrelated power settings unchanged. Account for the idle-delay/locking coupling above rather than promising unchanged locking behavior. This recipe does not perform a suspend, reboot, shutdown, or display-manager restart.

## 4. Read back and bound the claim

```bash
gsettings get org.gnome.desktop.session idle-delay
gsettings get org.gnome.settings-daemon.plugins.power idle-dim
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type
gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type
gsettings get org.gnome.desktop.screensaver lock-enabled
```

Require `uint32 0`, `false`, and `'nothing'` for the three authorized changes, with the battery-action and lock keys unchanged. This verifies those saved keys, not identical locking behavior after changing idle delay. Report saved policy separately from an observed full idle interval. These are saved per-user settings; restart behavior and actual idle availability remain untested until checked.

Resume the main skill's independent screenshot, window-targeting, and input tests. If the user wants an idle-period test, arrange it explicitly; do not claim it happened from immediate readbacks.

## What did not establish readiness

- Disabled screen locking: it did not prevent the monitor from needing a keyboard wake.
- A readiness block saying window access was available: the next actual window-list call failed. An active extension/service was not proof that an application window could be targeted.
- Immediate settings readback: it verified configuration, not a complete idle interval or reboot behavior.
