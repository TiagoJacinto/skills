---
name: ubuntu-desktop-computer-use
description: Set up, diagnose, and verify Pi Computer Use on Ubuntu GNOME. Use for desktop readiness, a shared visible browser, Desktop Sharing handoffs, repeated permission/unlock prompts, or control that fails after a helper restart or reboot. Also use for browser-security sign-in rejections or unfamiliar authentication blocks during a desktop handoff. Covers session access, accessibility, targeting, capture, portal input, keyrings, locking, and idle sleep.
---

# Ubuntu desktop computer use

Install and configure Computer Use against the existing logged-in desktop, then verify readiness with a harmless application test. Do not replace it with a virtual desktop merely because Pi runs over SSH.

Scope ends at Computer Use readiness and the machine settings needed to keep its desktop accessible. This includes explicitly authorized screen-lock configuration and agreed idle/AC-suspend settings when locking or sleep blocks the intended Computer Use workflow. It also covers a dedicated visible browser and Desktop Sharing access needed for human login/approval handoffs, including explicitly approved credential-storage changes. Automatic-login configuration, manual power operations, and Wake-on-LAN remain separate machine configuration.

**Failure pattern:** an installed package and successful tool calls can coexist with an inaccessible desktop, disabled GNOME extension, denied screenshot permission, or undelivered input.

## Setup once, verify reuse

Before setup or recovery, read [references/readiness-and-reuse.md](references/readiness-and-reuse.md). Establish the target invariant and requested lifecycle, reuse existing approved setup, and keep the original task pending while repairing its prerequisite. That reference owns layered readiness, bounded diagnosis, timed consent, and persistence proof.

Report **configuration saved**, **effective in the actual Pi helper**, **grant saved**, and **reuse verified** separately. Gate completion on actual target-specific probes, not tool readiness flags. “Works now” does not complete a requested restart/reboot requirement.

## Reuse common helper code

Read [templates/README.md](templates/README.md) for the disposable native [pointer probe](templates/pointer-probe.py) and child-side [persistence launcher template](templates/helper-launcher.template.sh). Reuse these instead of rebuilding event loggers or wrappers during each task. They do not replace capability probes, consent, or lifecycle verification; preserve working installed assets unless an authorized change is needed.

## 1. Establish the target and authority

Call the Skill tool with "computer-use-linux" for the current tool procedures. For a new staged conversational setup, call the Skill tool with "computer-use-wizard"; it owns human handoffs, secret handling, and stage approvals. If that wizard called this skill to resolve a blocker, retain its current stage and return there after readiness is verified; do not start another wizard.

Inspect before modifying. Discover the desktop user and target application through available tools; ask only for missing or ambiguous information. Minimize human Ubuntu UI interaction: perform routine setup/diagnostics within the request, collect missing non-secret details in chat, and hand over only the smallest genuinely human-only step. Confirm human screen access when an unlock or portal prompt is actually needed; SSH/Herdr alone does not show that prompt.

Keep one desktop controller active. Respect read-only requests. Let the human unlock the screen and approve security prompts. Do not remove profile locks, log out, or reboot without the relevant explicit authorization. Never ask for passwords or tokens in chat.

## 2. Identify the real graphical session

Use `id`, `loginctl list-sessions`, and `loginctl show-session SESSION_ID -p Name -p Type -p State -p LockedHint`. Select the target user's graphical session; do not reuse historical session IDs.

`DISPLAY=:0` is not proof of native X11: it can identify Xwayland while the graphical session is Wayland. Do not switch display systems to resolve that ambiguity.

From SSH, local GNOME diagnostics may need the target user's runtime directory and session bus. For the same current user:

```bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
```

Discover graphical values from the user's session, not invented defaults. If the bus or display is absent, stop and resolve session access. Do not run Pi as root to bypass it.

Keep the selected user's normal Pi settings and host workflow. If an approved per-user launcher already imports graphical-session variables from `systemctl --user show-environment`, inspect and reuse it rather than inventing defaults or changing the user's usual command. A launcher's existence is not proof of live desktop access; do not install a transparent replacement for `pi`.

## 3. Probe each capability separately

In Pi, enable `get_app_state`, `list_windows`, `focused_window`, and `doctor` using `computer_use_linux_tools`. Start observation with scoped `get_app_state`, initially without a screenshot when accessibility data is sufficient. Use `doctor` for unresolved readiness details.

If missing, install the native package with authorization:

```bash
pi install npm:@agent-sh/computer-use-linux
```

Reload/restart Pi as needed. Native tools do not require an MCP adapter or a separately installed CLI. Do not treat package installation as successful desktop setup.

Track distinct results:

- Accessibility tree available (and whether it contains useful controls).
- Window list/focus identifies the intended application.
- Screenshot contains the real desktop, not a black image.
- Mouse/keyboard events reach the intended application.

Read [references/troubleshooting.md](references/troubleshooting.md) for window `AccessDenied`, inactive extensions, failed/black capture, locked-screen disagreement, portal prompts, stale Chrome locks, or browser automation controlling a different Chrome instance.

For repeated control prompts or remembered permission, read [references/remembered-control.md](references/remembered-control.md). It covers effective native-helper configuration, the version-specific environment-filtering workaround, timed initial human consent, private grants, and reuse tests after helper replacement and reboot. The recorded reboot passed keyboard delivery and pointer-session reconnection. For restored permission with a lost first click, read [references/first-pointer-click.md](references/first-pointer-click.md): a later local helper patch passed cold-session GTK and Firefox targeting checks; another reboot of that patch remains untested.

If locking prevents the intended Computer Use workflow, read [references/screen-lock.md](references/screen-lock.md). Diagnose the current lock separately from automatic-lock policy; obtain explicit security approval before changing the policy.

If screen blanking, dimming, or inactivity sleep blocks desktop availability, read [references/keep-desktop-awake.md](references/keep-desktop-awake.md). Configure only the agreed availability settings; preserve unrelated keys and obtain explicit security approval if changing idle delay could reduce automatic-lock protection, even when the lock key itself stays unchanged.

A readiness boolean or active extension is not a substitute for an actual window-list/focus check; the recorded continuation had successful capture but a failed window list.

### Set up a shared work surface when the journey needs one

For a browser-security sign-in rejection, an unfamiliar authentication block, or private sign-in followed by agent work in the same visible browser, read [references/shared-desktop-browser.md](references/shared-desktop-browser.md). Its recovery branch uses current evidence rather than fixed provider wording; a wrong password alone is not a browser-restart trigger. It covers normal Firefox for the demonstrated human sign-in handoff and richer desktop accessibility, alongside dedicated Chrome/CDP setup for browser automation. Select by workflow and host tool routing; do not assume all browsers or launch modes behave alike.

If the human needs Windows access to the existing Ubuntu desktop for these handoffs, read [references/desktop-sharing-keyring.md](references/desktop-sharing-keyring.md). Preserve the requested Desktop Sharing + Remote Control mode. Its approved passwordless-default-keyring setup requires separate security authorization; loading this skill does not authorize it. Reliable graphical startup after reboot remains a separate prerequisite.

## 4. Verify input without disturbing real work

For a requested setup/diagnosis that includes functional verification, perform harmless disposable interaction tests without a separate permission question. Confine them to owned local test surfaces: no real messages, purchases, production writes, persistent permission changes, or other external effects. Honor read-only requests and obtain any required platform consent. Then:

1. Obtain fresh scoped app state and verify window identity with `list_windows` or `focused_window` before input.
2. Open an owned disposable surface yourself using the real graphical environment, and preserve original windows/tabs. For pointer delivery, prefer the reusable [native pointer fixture](templates/README.md#pointer-delivery-fixture); use other owned disposable surfaces for click/text/scroll checks. Use `agent_browser` for ordinary website tasks, not native desktop input tests.
3. Test a click and require an observable application change. If verifying a replacement helper, test its first click and require exactly one activation; a warm retry does not prove cold-start delivery.
4. Enter a harmless exact string; verify it. Select and clear it; verify the field is empty. Do not submit an omnibox test string to a search engine.
5. Scroll and verify position or a counter changed.
6. Close only the test surface and remove only the temporary files created for it. Verify original work remains.

Re-observe after changes. Prefer semantic targets; if Chrome exposes only a shallow accessibility tree, use a fresh screenshot and its coordinate dimensions, scale, and crop origin. Never reuse historical window IDs or coordinates.

If an input action opens a **Remote Desktop** permission dialog, stop for the human to enable **Allow Remote Interaction** and click **Share**. Re-observe afterward. Ubuntu **Remote Login** is a different setting and is not a substitute for portal consent.

Tool `ok: true` proves submission, not delivery. For dragging, require an actual drop/event result. When HTML5 drag starts but never drops, read [references/html5-drag-motion.md](references/html5-drag-motion.md): the installed private helper combines source settling and stepped portal motion, verified with cold first-drag drops in Firefox and Chrome. Cross-monitor dragging and another reboot remain unverified.

## 5. Complete the setup

Report installed/configured components separately from demonstrated readiness, using **capability · evidence · tested boundary · remaining limit**. List pending human approvals and unresolved blockers. Other apps, dragging, and untested lifecycle changes remain unverified. If this skill repaired a prerequisite for another task, return to that task's saved stage and approval boundaries; do not strand the user at a readiness summary or expand into unrelated configuration.

## What did not work

- Treating SSH as inherently incompatible with desktop access: the existing GNOME session was reachable; permissions and state were the blockers.
- Inferring X11 from `DISPLAY`: led toward the wrong backend; inspect the graphical session type.
- Repeating extension enable/reboot attempts: the global `disable-user-extensions` setting and lock state still needed diagnosis.
- Installing `gnome-screenshot` alone: its fallback timed out; portal permission and screen state needed separate attention.
- Believing accepted keyboard/drag calls: a shortcut initially made no visible change and drag registered no drops.
