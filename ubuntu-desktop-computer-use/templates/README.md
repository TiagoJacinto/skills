# Reusable desktop-control helpers

Run these helpers unchanged with task-specific non-secret arguments. Only the launcher's marked `HELPER` assignment is configuration. They support the agent's conversation workflow; they do not introduce a human-operated Bash wizard or authorize security changes. Use the existing desktop/session/profile. Do not install helpers, modify grants, reload Pi, or change machine settings just to validate the templates.

## Pointer delivery fixture

[pointer-probe.py](pointer-probe.py) creates a disposable native GTK target. It records **only its own** motion/press/release/activation events, not global input, keyboard text, application data, clipboard, portal tokens or recordings. The JSON is replaced atomically with mode `0600`. An existing output file/link or shared-writable/non-owned parent is refused at startup. Use a dedicated private workspace, unique filename and one writer; the replacement-inode check is not an atomic defense against concurrent same-user pathname substitution. Python 3.10+, PyGObject and GTK 3 are required; help and event verification work without GTK. No Python Cairo dependency is needed.

1. Select the actual graphical-session environment, and an owned private directory (mode `0700`) outside Git. Launch through the host's supervised process mechanism:

   ```bash
   python3 /absolute/skill/templates/pointer-probe.py \
     --output /absolute/owned/probe/events.json
   ```

2. Retain the non-secret `pid` and `session` from the `ready` status. They identify this fixture, not a helper grant. Before clicking, verify the file has that launch session, zero activations and no button/activation events; allow motion only. If the baseline is not fresh, start a new fixture. Do not derive the expected session from the log under verification. Keep one desktop controller active and avoid human input during the trial. Confirm the actual **Pointer delivery probe** window through fresh native Computer Use app state and window/focus queries. The window displays its PID and activation count. Derive the green target's coordinate from a fresh screenshot; do not reuse coordinates.
3. For cold first-click diagnosis, follow [first-pointer-click.md](../references/first-pointer-click.md). Use a fresh fixture/event file per helper trial and replace only the verified Pi-owned helper when that test is authorized. Issue exactly **one** native coordinate click inside the green target. The fixture deliberately does not offer an accessibility activation that could bypass pointer delivery.
4. Poll this fixture's non-secret event file for up to two seconds; retry verification, **not the click**:

   ```bash
   python3 /absolute/skill/templates/pointer-probe.py \
     --verify-file /absolute/owned/probe/events.json \
     --session FIXTURE_SESSION --expected 1
   ```

   Exit `0`/`pass` requires the matching session, exactly one activation, and exactly one in-target left-button press → release → activation sequence. Extra/off-target button events, incomplete delivery, stale sessions and duplicate activations fail. Motion alone, accepted tool input, or an activation counter without the event sequence do not pass. Exit `1` means the criterion is unmet; exit `2` means startup/read/recording was unavailable. A `ready` message proves startup only, not desktop-control capability.
5. Verify both native tool readback and the event evidence. Close only this fixture and remove only its temporary event file. Preserve the original desktop/apps/grants. This probe verifies pointer clicks only; use separate disposable tests for keyboard, scroll, drag and real-app focus. Headless signal tests do not establish Wayland portal delivery or reboot reuse.

## Child-side persistence launcher

[helper-launcher.template.sh](helper-launcher.template.sh) supplies `COMPUTER_USE_LINUX_PERSIST_REMOTE_DESKTOP=1` **inside the launched child**, even when a host filters the parent environment. Read [remembered-control.md](../references/remembered-control.md) first. Reuse an existing working approved launcher; do not replace it merely to adopt this template.

When configuration is needed and authorized:

1. Discover the matching installed/private helper and supported host launch override. Inspect actual executable/provenance and current configuration; do not guess a bundled path or silently replace a pointer fix.
2. Copy the template to a new owned per-user launcher outside installed dependencies. Change the marked `HELPER` assignment to the discovered absolute executable path, quoting it correctly for POSIX shell. Set the copied launcher's mode to `0700`. The unchanged template fails closed; it never installs or patches anything.
3. Configure the supported absolute `COMPUTER_USE_LINUX_BIN` override to that launcher through the host's current configuration mechanism. Follow the reference's approved helper-replacement procedure; preserve other sessions and saved grants.
4. Verify the actual Pi-owned helper inherited persistence and arguments, then independently check private grant metadata and input/reuse through the requested lifecycle. The launcher forwards arguments unchanged using `exec` and preserves the helper's exit status. It does not grant consent, create tokens, prove first-click delivery, or verify a new-session/logout/reboot boundary.

For shell-only checking, `sh -n helper-launcher.template.sh` checks syntax and running the unchanged template must exit `2`. Test argument forwarding/export with a dummy executable in a temporary sandbox, not the installed helper. Do not treat these checks as live persistence evidence.
