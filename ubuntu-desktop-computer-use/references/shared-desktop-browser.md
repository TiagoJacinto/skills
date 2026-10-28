# One visible browser for the human and the agent

**Goal:** the human signs in privately in a visible browser on Ubuntu, locally or through Desktop Sharing, and the agent continues in the same app/profile through a fresh permitted work surface after private containers have been disposed. Current [host-verified private-handoff rules](../../computer-use-wizard/references/private-handoff.md) govern all private entry below. Human “done” or a dashboard is not release evidence; if no trusted closure adapter is ready, do not request private input. Choose normal Firefox for the demonstrated human-sign-in/native-desktop workflow, or the dedicated Chrome/CDP setup below when browser automation is needed. Profiles and login state are browser-specific; a live process/debugging port is not persistent.

**Reference validation boundary:** one tested setup launched Chrome on the physical Ubuntu desktop, disabled password saving in its dedicated profile, verified matching CDP tab IDs across calls, and visibly opened the requested provider dashboard. After a reboot closed Chrome, the agent reused that profile, refreshed the endpoint, verified matching targets, and reopened that dashboard. Authentication itself still awaited the human. Reproduce the relevant boundary on the current setup before claiming readiness.

## Choose the work surface before configuring it

Choose from the user's target invariant and required control path, not an assumption that CDP is necessary for every browser. Default to the user's existing browser/profile: extensions (including password managers), saved sessions, and authentication are part of that work surface. For human private sign-in plus permitted native desktop control, try an installed normal browser on the intended desktop first. Use the dedicated Chrome/CDP branch when browser automation is required. Check host routing before promising to continue in a normal browser that the required tool cannot control.

Before proposing a dedicated profile, explain that it starts without the user's extensions, password manager, or signed-in sessions, and that automation-enabled login may be rejected. General setup authority does not establish that this profile is a usable sign-in surface. If current Chrome restrictions prevent CDP on the normal data directory, report that limitation rather than promising to preserve its login experience through a restart. Preserve the profile and resolve the control-route mismatch without copying cookies, credentials, or extension data.

Verify the visible window and connection continuity before asking for login. A provider sign-in rejection does not authorize moving the human to another machine or bypassing its controls. Agree on an alternative that preserves the requested work surface where possible. Browser brand and automation launch mode are different variables; one successful alternative is not a general reliability ranking.

## Recover from a sign-in security rejection

Use current page meaning or the human's non-secret report to recognize a browser-security rejection or unfamiliar authentication block; provider wording and layouts can change. This is agent judgment, not an exact-message detector. Stop automated sign-in attempts while assessing the block. A wrong password, ordinary MFA request, or expired session alone is not evidence of an automation problem and does not justify a browser restart.

1. Establish what failed from safe evidence. During an active private pause, ask only for non-secret status; keep its observation barrier intact. If the cause is unclear, ask one focused question rather than repeat the attempt. Do not bypass provider controls, spoof browser identity, weaken security, clear cookies, or reset the profile.
2. If automation may be involved, inspect launch flags and automation ownership/connections read-only, outside any private pause that prohibits these tools. Avoid cookies, credentials, session contents and full authentication URLs. Identify the current browser/profile and launcher from live metadata; historical PIDs, ports and service names are not execution targets. Offer one human-operated comparison preserving the same profile and network.
3. Obtain explicit saved-work and shutdown approval before stopping the identified automation owner or closing the browser. Check the private-handoff contract first: stopping a lifecycle broker can destroy closure authority. If an active/unknown barrier or unavailable trusted adapter prevents this recovery, stop and explain the blocker; do not disable the guard or treat manual-login approval as clearance.
4. Under that approval, stop only the identified automation owner and fully quit the selected browser. Confirm exit before reopening the same profile normally without automation/debugging flags. Opening another window in the still-running process does not remove automation. A successful quit/close tool result alone is not exit evidence; if it stays open, inspect before choosing another authorized shutdown method. Preserve unrelated apps, profile data and network settings.
5. Verify the actual new process uses the preserved profile, lacks remote-debugging/Marionette launch flags, and has no relevant automation listener or connection. Disconnecting a client alone is insufficient if the endpoint remains enabled; `--no-remote` is not an automation-disable switch. Verify visible-window readiness without exposing private content. If these conditions cannot be established, report that limitation before requesting the comparison.
6. Use the applicable host-verified private-handoff route for one user-operated attempt; do not attach browser automation or observe private input during it. Ask for success/failure status, never credentials or codes. An existing-session redirect to an account dashboard is not a fresh sign-in result. Let the human initiate the intended account flow; do not sign them out or change accounts automatically.
7. Record the user-reported result separately from the verified launch conditions. A successful manual comparison supports automation involvement, not proof of the provider's internal decision signal or future reliability. Restart, elapsed time and session state may also contribute. If it fails or remains inconclusive, ask before further experiments. A result report does not clear a private barrier or authorize reattaching automation; retain the closure contract and obtain authorization for further work.

**Recorded comparison:** Google rejected sign-in in debugging-enabled Firefox with an active Pi-related broker connection. After an approved full restart using the same profile, checks found no remote-debugging/Marionette flags, no listener or connection on the former debugging port, and an inactive broker. The network was left unchanged. The human reported that the requested manual sign-in succeeded. The final sign-in result was human-reported, not independently observed; this is supporting evidence, not a universal diagnosis.

## Normal Firefox for human sign-in on Ubuntu

In one tested Ubuntu human-sign-in handoff, debugging-enabled Chrome received Google's “This browser or app may not be secure” rejection. Normal Firefox, launched without automation/debugging flags, let the human sign in to the requested provider; subsequent desktop observation found its dashboard and a non-truncated accessibility tree with named controls. This is scoped evidence, not a guarantee for other providers or browser versions.

All browser observations and actions below remain subject to host tool-routing rules. If native Computer Use is not permitted for browser content, keep sign-in human-only and pause agent inspection until an approved route is available.

This section covers preparing a fresh human sign-in handoff. For a rejection in an existing browser session, use [the recovery procedure above](#recover-from-a-sign-in-security-rejection); the historical comparison does not establish a browser-brand preference.

For an agreed normal-Firefox handoff:

1. Check Firefox is installed. Reuse/open a normal window in the actual Ubuntu graphical session; from SSH, import the same target user's graphical variables before invoking `firefox --new-window about:blank`. Do not load credential-bearing URLs before the host guard is ready. Request installation approval if missing. Do not change Firefox profiles, password storage, or launch it with automation/debugging flags merely to perform this handoff.
2. Prepare dedicated disposable source/capture containers, register them with the verified host guard and wait for successful pause before private pages/input. The human signs in via the selected Ubuntu screen or Desktop Sharing; the agent neither observes nor inputs private values. Browser installation/window readiness alone does not establish a supported guarded route.
3. Human completion permits the agent to request narrow registered-container disposal, not observation. Only authoritative host verification releases the barrier. Then create/reuse a fresh permitted work surface in the same profile, get scoped app state and verify its current window with `list_windows` / `focused_window`. Closed IDs are stale.
4. Read the target's accessibility tree. If truncated, narrow the target and raise node/depth budgets as the current Computer Use skill directs. Prefer fresh named controls when available; verify action results independently.
5. Keep that browser/session for the requested task, subject to host tool routing. Firefox here was not attached to `agent_browser`, and Chrome's CDP recipe below is not a Firefox attachment recipe. If host rules require browser automation for a later website action but the normal Firefox surface cannot be accessed through approved tools, explain the limitation and pause or use a human-assisted step rather than silently switching the user's work to another browser.

This is a normal supported-browser/manual-login handoff, not a way to evade provider anti-bot or authentication controls. Do not spoof browser fingerprints, suppress security checks, or automate Google login to get around a rejection. If the provider still rejects sign-in, stop and use its supported recovery path.

**Bounded comparison:** different browser and launch modes were used; the rejection's exact cause was not proven. Firefox's richer accessibility output helps identify controls, but it does not prove reliable click/type delivery: the first recorded post-login element click timed out without a confirmed result. Re-observe before retrying. No new Firefox profile-persistence, keyring-avoidance, or reboot test was demonstrated.

## Authorized Firefox lifecycle control, not a CDP fallback

Use this branch only when a Firefox-specific lifecycle adapter needs browser-internal disposal proof and the operator explicitly authorizes localhost automation on the existing profile. It exposes signed-in browser control/data to local software and requires starting/restarting Firefox. Consent for a native desktop service is not this authorization. Save work before an approved restart; preserve unrelated tabs/profile data and never delete profile locks, copy cookies or substitute a fresh profile.

1. Identify current Firefox processes by UID/executable and the selected existing default from profile configuration only. If already running, plan the approved restart without losing unsaved work. If profile selection is ambiguous, ask one focused question. Do not read cookies, credentials or session contents to identify the profile.
2. Import the actual user's graphical environment. Start that same profile on `about:blank` with `--remote-debugging-port PORT`; Firefox's endpoint is `ws://127.0.0.1:PORT/session`. Verify the actual socket is loopback-only and the listener-owner arguments point to that profile. To disable it, save work, fully quit this Firefox process and reopen normally without the flag. Opening another normal window while it still runs reuses the debugging-enabled process. Do not broaden allowed hosts/origins, enable Gecko system access, change password storage or disable security checks.
3. Suppress service stdout/stderr and protocol tracing before attaching to the real profile. Use only fixed metadata/lifecycle commands in the trusted adapter. `browsingContext.getTree` embeds URLs: project internally to opaque identifiers; never emit/log/persist raw responses, URLs, page text, cookies or credentials. Keep ordinary website automation separate and subject to host routing; Firefox BiDi is not Chrome CDP.
4. Verify the primitive with an owned blank window: bind browser/client/context identities and uniquely correlated fresh native surface plus listener PID; close only that context; independently confirm context/client/native absence twice. Confirm original identities remain and the shared browser process is still alive. Identity survival does not establish unchanged contents/focus/state; unique creation-delta correlation is not a general native mapping API.
5. Treat timeout as unknown, not cancellation or successful disposal. Reconcile recorded identities read-only before retrying. An unknown create can leave a remote context without a returned ID; a production adapter needs durable reconciliation. Never close whatever window happens to be active or bulk-close other contexts. Keep unavailable metadata, changed session/process/service and unexpected contexts blocked.
6. State the tested boundary. Normal blank-window disposal can pass while a Wayland window-state command times out; do not repeat equivalent minimization mutations or infer minimized/cancelled/popup support. Interface activation and a passing primitive do **not** authorize real private input until the integrated host barrier and capture containment are validated. The localhost listener stays active until Firefox exits; it is not an authentication boundary against local software.

**Observed dead ends:** Chrome/CDP cannot attach this Firefox interface. Window-state command completion was not usable evidence in the tested Wayland probe; normal disposal was verified separately. No provider sign-in, authentication, full private-handoff integration or restart persistence was established by that probe. Debugging-enabled Firefox may behave differently with a provider than the historical normal-Firefox handoff above; do not bypass rejection or promise login will succeed.

Protocol details: [Mozilla security model](https://firefox-source-docs.mozilla.org/remote/Security.html), [BiDi connection](https://developer.mozilla.org/en-US/docs/Web/WebDriver/How_to/Create_BiDi_connection), [context close](https://developer.mozilla.org/en-US/docs/Web/WebDriver/Reference/BiDi/Modules/browsingContext/close).

## 1. Create or reuse an owned desktop Chrome for CDP

Keep the personal Chrome profile and normal Login keyring unchanged. Confirm the user wants a dedicated persistent automation profile. Place its data and ownership metadata in an agreed local directory outside Git; use profile mode `0700`, metadata/preferences mode `0600`, and verify ignore status if inside a repository.

Run as the desktop user. Import the actual graphical-session environment from `systemctl --user show-environment`, selecting display/runtime/authentication variables rather than printing the whole environment. A headed browser launched from an SSH environment without that display context may not appear on the physical desktop.

When avoiding a GNOME keyring prompt is part of the requested setup, explain and obtain explicit approval for the dedicated browser's weaker credential storage. The tested, explicitly approved configuration used `--password-store=basic` and disabled password saving. This is not encrypted credential storage and is not a promise that no system prompt can ever appear. Disabling password saving does not remove sensitive cookies or other persisted login state. Protect the whole profile and its local CDP access. Do not apply it to the personal browser.

Before launching a fresh profile, create `Default/Preferences` with:

```json
{
  "credentials_enable_service": false,
  "profile": { "password_manager_enabled": false }
}
```

For an existing profile, preserve unrelated preferences and modify only agreed keys while its conclusively owned browser is stopped. Preserve the old profile if a new one is needed. Check process ownership before closing anything: UID, executable, and the exact `--user-data-dir` must match; a PID alone is insufficient.

Launch the dedicated Chrome with the chosen profile and these approved flags:

```text
--user-data-dir=/absolute/owned/profile
--password-store=basic
--remote-debugging-address=127.0.0.1
--remote-debugging-port=0
--no-first-run
--no-default-browser-check
about:blank
```

Keep Chrome's sandbox enabled. Verify the debugging listener is actually loopback-only. Do not expose CDP through a public port: it grants control of the signed-in browser.

Wait for this launch's fresh `DevToolsActivePort`; use its first line for the port. Verify the browser is still running and its visible native window belongs to that PID. Record only ownership metadata—PID, profile, port—not credentials, cookies, or login URLs. If launch outcome is ambiguous, inspect before retrying.

## 2. Attach automation to that same visible window

Use native `agent_browser` calls. One tested integration used a local connection-specific JSON config:

```json
{ "cdp": "http://127.0.0.1:CURRENT_PORT" }
```

First use the current native tool's supported attachment/session procedure and verify continuity on separate calls. Do not add a historical workaround when that path already works. If the installed integration reproduces the recorded follow-up mismatch, use the connection-specific config above: substitute the verified current port, restrict/ignore the file, and pass the same explicit `--session NAME --config /absolute/connection.json` prefix on every call, including copied follow-ups. Keep global browser defaults unchanged.

1. Verify `get url` after attachment before inspecting page content.
2. Compare `tab list` CDP target IDs with the verified endpoint's read-only `/json/list`. Do not print auth URL queries or unrelated page data. A successful `connect` or matching URL alone does not prove attachment: require a matching target ID again on a separate follow-up call. If the native window stays blank while automation reports navigation, stop handoffs and diagnose attachment; use the connection-specific config above if needed, then reverify endpoint/target continuity and the visible native window.
3. Select the intended visible tab by its stable CDP target ID; verify its URL.
4. Navigate to the requested service and verify the matching desktop window/page. Confirm the same target survives separate follow-up calls.
5. Before human login/MFA/private entry, use the host-verified private-handoff protocol with supported dedicated source/capture containers. A dashboard report never releases observation. Dispose and independently verify the registered private containers, then establish a fresh permitted work surface in the same profile. Do not reuse closed CDP target IDs or request private input when a trusted adapter is unavailable.

This lets the human and agent share browser state without simultaneous control. It does not mean the agent performs private login or that profile reuse proves authentication.

## 3. Resume after Chrome exits or the machine restarts

A profile can survive reboot while the browser process and port change. Validate the stored ownership record against the live process before reusing it. If it is gone, confirm no other process uses the profile, check approved preferences, and relaunch with the real graphical environment. Stop for a reused PID, changed ownership, symlink surprises, or a profile already in use.

Update the connection config from the new launch's fresh port, then repeat target-ID and visible-window checks. Do not reuse historical ports/PIDs or assume tabs and in-memory page state survived. Reliable Ubuntu desktop startup is a separate prerequisite; this procedure does not fix a GNOME boot failure.

## Why this configuration matters

The session's one-time CDP attachment did not remain attached on later calls; the connection-specific config did. That workaround was verified on native 0.37.0, not established as a universal requirement for all versions. Use it when the current integration needs explicit endpoint continuity, and verify rather than assume the connection.

The installed skill's [troubleshooting.md](troubleshooting.md) contains the bounded connection-mismatch diagnostic. This reference owns the successful setup, not the failed-attempt history.
