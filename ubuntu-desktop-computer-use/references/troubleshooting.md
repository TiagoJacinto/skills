# Diagnose the blocked capability

Use the current `computer-use-linux` skill for tool schemas and targeting. The commands below are GNOME diagnostics from the recorded workflow, not unconditional setup steps. Run them as the target desktop user with the correct session bus. Inspect current state before retrying an ambiguous mutation.

## Window targeting denied or extension inactive

Enable/call native `setup_accessibility` or `setup_window_targeting` only for the reported missing capability and with setup authorization. Newly installed GNOME Wayland extensions may require a graphical logout/login. Ask the user to save work; reconnecting SSH does not reload GNOME. Do not initiate logout/reboot automatically.

For the extension used in the source session:

```bash
gsettings get org.gnome.shell disable-user-extensions
gsettings get org.gnome.shell enabled-extensions
timeout 5 gnome-extensions info computer-use-linux@avifenesh.dev
```

Inspect the installed extension's actual identifier if it differs. `enabled-extensions` membership alone did not mean it was active. When the CLI hung, the session used:

```bash
timeout 5 gdbus call --session --dest org.gnome.Shell \
  --object-path /org/gnome/Shell \
  --method org.gnome.Shell.Extensions.GetExtensionInfo \
  computer-use-linux@avifenesh.dev
```

In the recorded GNOME version, state `1` plus a successful native window list confirmed activity. Do not infer current readiness from the numeric state alone.

If `disable-user-extensions` is `true`, explain that enabling user extensions affects more than this extension. After explicit approval:

```bash
gsettings set org.gnome.shell disable-user-extensions false
gsettings get org.gnome.shell disable-user-extensions
```

Verify with a fresh native `list_windows`, not just a saved setting. If two equivalent enable/reload attempts make no progress, stop repeating them and investigate session/extension errors.

## Capture denied, timed out, or black

First distinguish API success from a usable picture. In one tested GNOME setup, an initial check returned a completely black capture without proving its cause. The human then woke the connected monitor with Shift and the next portal capture succeeded. If keyboard activity is needed to show an image, read [keep-desktop-awake.md](keep-desktop-awake.md) for recovery and agreed idle settings. Do not generalize this sequence into a universal black-screen or headless diagnosis.

Check both login-session lock state and GNOME's screen shield:

```bash
loginctl show-session SESSION_ID -p Type -p State -p LockedHint
gdbus call --session --dest org.gnome.ScreenSaver \
  --object-path /org/gnome/ScreenSaver \
  --method org.gnome.ScreenSaver.GetActive
```

They disagreed in the recorded session. Report the disagreement and ask what the user sees rather than asserting certainty from one check. Request manual unlock if needed. If automatic locking prevents the intended Computer Use workflow, read [screen-lock.md](screen-lock.md) for the explicitly authorized setup branch; do not change policy merely to dismiss a current lock.

For a portal failure, inspect:

```bash
journalctl --user -b -u xdg-desktop-portal.service \
  -u xdg-desktop-portal-gnome.service --no-pager -n 60
gdbus call --session --dest org.freedesktop.impl.portal.PermissionStore \
  --object-path /org/freedesktop/impl/portal/PermissionStore \
  --method org.freedesktop.impl.portal.PermissionStore.Lookup \
  screenshot screenshot
```

The recorded permission map contained `{'': ['no']}`: a saved screenshot denial for the empty application-ID bucket. A native portal request failed immediately, consistent with that denial. GNOME also rejected direct screenshot calls from untrusted applications. Installing the documented `gnome-screenshot` fallback did not solve it.

Only if that denial is present and relevant, explain that removing it affects unidentified local applications, not only Pi. Obtain explicit permission immediately before resetting it. Remove only the denied entry, preserving other entries:

```bash
gdbus call --session --dest org.freedesktop.impl.portal.PermissionStore \
  --object-path /org/freedesktop/impl/portal/PermissionStore \
  --method org.freedesktop.impl.portal.PermissionStore.DeletePermission \
  screenshot screenshot ''
```

Read back the map. This removes a decision; it does not grant access. Retry scoped capture only after the human is ready to handle a permission prompt. Pause observation/input while private credentials are entered. Do not write blanket `yes` permissions or disable GNOME security.

Historical completion required an unlocked desktop and human consent: `get_app_state` then returned `screenshot_capture_status: verified`, `can_capture_screenshots: true`, and a visible Chrome screenshot through `xdg-desktop-portal`. The permission reset alone still timed out; it was not the whole solution.

## Input accepted but no visible effect

A new remote-control request may show the **Remote Desktop → Allow Remote Interaction → Share** dialog. Have the human approve it on the Ubuntu desktop, not in SSH. Re-observe and confirm the application result. A sharing indicator or successful tool response is insufficient.

For repeated consent prompts, read [remembered-control.md](remembered-control.md). Saved grants and keyboard input after helper replacement and one actual reboot were subsequently verified. For a lost first pointer click despite restored permission and correct cursor coordinates, read [first-pointer-click.md](first-pointer-click.md). A local 0.7.13 patch passed three cold-helper GTK trials and a Firefox address-bar test. Suspend behavior and another reboot of the new patch remain untested.

## Test application blocked by a moved-drive Chrome lock

Prefer another harmless local application for readiness testing rather than altering an existing browser profile. Use this branch only if Chrome is required for the agreed test and cannot open. It is not a general profile-maintenance step.

One tested machine inherited a Chrome profile whose `SingletonLock` named its previous host. Chrome was installed; reinstalling was not the necessary fix.

1. Inspect the actual profile directory, its `SingletonLock`, `SingletonCookie`, and `SingletonSocket` symlink targets, the current hostname, filesystem mount, and live browser processes. A defunct process is not a live profile owner.
2. Ask whether the old machine still uses this profile, or whether its drive/profile was moved. Stop if ownership is uncertain or shared storage is in use.
3. With explicit cleanup authorization, recheck there is no live Chrome/Chromium owner and that the lock targets have not changed. Remove only those three stale symlinks. Stop for unexpected regular files; never delete the profile or its login data.
4. Launch Chrome with the correct graphical environment; verify a new live process and its visible window. Do not equate launching with verified screenshots or input.

The historical cleanup checked `/proc/*/exe`, refused if a live browser was found, verified the exact observed old-host lock target, unlinked only the three symlinks, and preserved the existing profile. Do not reuse its PID, host target, or coordinates.

## Browser automation controls a different Chrome instance

**Failure pattern:** an initial native CDP attachment reports the desktop browser's tab IDs, but a same-session follow-up reports new IDs while the visible window remains unchanged.

**Verified workaround:** on native 0.37.0 with ambient `AGENT_BROWSER_ARGS=--no-sandbox`, a connection-specific native config retained the owned desktop tab across initial and repeated follow-up calls. Navigating the selected original tab then visibly opened the requested provider dashboard on the selected Ubuntu monitor. The ambient-default interaction was not isolated as the sole root cause.

1. Verify the owned browser's UID, executable, profile and loopback-only debugging listener. Derive the current port from that profile's `DevToolsActivePort`; use only its first line. Never reuse a historical port or inspect stored credentials.
2. Compare `agent_browser tab list` target IDs with that endpoint's read-only `/json/list`. Strip URL queries from diagnostic output. Test the initial attachment and a separate same-session follow-up before allowing authentication.
3. If the initial match is lost on follow-up, create a permission-restricted, Git-ignored connection config with the native `cdp` field pointing to the verified current endpoint. Pass the same `--session NAME --config /absolute/config/path` prefix on every call, including helpers and copied `nextActions`. Keep global defaults unchanged.
4. Select the original visible tab by its stable CDP target ID. Verify its URL, navigate to the requested service, and require a matching native desktop screenshot. Repeat the target-ID comparison on two later calls.
5. Refresh the config and repeat ownership checks after browser restart because its debugging port can change. Close only conclusively owned diagnostic sessions; preserve the working desktop browser. Pause observation for private sign-in.

**What did not work:** a one-time `connect PORT`, or one-time `--cdp ENDPOINT` followed by calls omitting the connection configuration. Both returned successful commands while follow-ups controlled a separate browser. Merely pinning a tab did not preserve the correct browser connection. A headed launch from SSH without graphical environment variables also opened off the physical desktop.
