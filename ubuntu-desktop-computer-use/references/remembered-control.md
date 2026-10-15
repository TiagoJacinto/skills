# Remember Pi desktop-control permission

**Goal:** approve desktop control during setup, then let later Pi helpers reuse the authorization without routine manual permission toggles. Use for repeated GNOME Remote Desktop consent prompts from Pi's Computer Use helper. This is separate from Windows Desktop Sharing and its RDP credentials.

Keep the goal and evidence separate: installing the persistence configuration, seeing the flag in the actual helper, saving the grants, and demonstrating reuse are four different steps. Inspect existing grants before requesting another initial approval. A valid saved grant is a capability, not permission to expand the user's task.

**Failure pattern:** a manual Allow Remote Interaction approval works only in the current helper; the helper did not request persistence. Native Pi integration 0.7.13 also omits `COMPUTER_USE_LINUX_PERSIST_REMOTE_DESKTOP` from its environment allowlist, so exporting the variable in Pi alone does not reach the helper.

**Verified:** the configured actual Pi helper inherited persistence=1 and saved nonempty pointer and keyboard token files with mode0600 in a0700 directory. A replacement helper and a later new Pi/helper after an actual computer reboot typed an exact harmless string into Firefox without renewed approval. No test text was submitted; it was restored or cleared. Pointer sessions returned Start response0 without human approval after both helper replacement and reboot. The reboot click test did not focus the address bar. A later diagnosis isolated a lost first portal click; the local helper patch in [first-pointer-click.md](first-pointer-click.md) subsequently passed cold-session GTK and Firefox targeting checks. That new patch has not been tested through another reboot. Automatic GNOME login succeeded on that reboot; Windows Desktop Sharing end-to-end reconnection had not yet been confirmed by the human. Keep operational audit records outside skill directories, in an owned private location chosen for the task; do not embed project paths or grant contents in reusable instructions.

## Procedure

1. Obtain explicit approval for remembered control. Explain that same-user processes able to read the private saved grant can reuse it; GNOME can revoke permission. Preserve browser and Windows Desktop Sharing sessions.
2. Inspect existing approved configuration and grants first. Check the installed integration's environment allowlist and the actual live Pi helper; a parent-shell export or standalone probe is not evidence of native inheritance. If the integration passes `COMPUTER_USE_LINUX_PERSIST_REMOTE_DESKTOP`, configure it as `1` through the existing supported launch route. If the installed version demonstrably drops it, use the per-user wrapper rather than patching dependencies:
   - Reuse [helper-launcher.template.sh](../templates/helper-launcher.template.sh) and its [instructions](../templates/README.md#child-side-persistence-launcher) instead of rebuilding the wrapper. An owned per-user launcher (for example, `~/.local/bin/pi-computer-use-linux`) exports the variable inside the child, then execs the selected matching helper with unchanged arguments. The current target is the private pointer-fix build documented in [first-pointer-click.md](first-pointer-click.md); the installed npm binary remains unchanged.
   - `~/.pi/agent/extensions/desktop-control-persistence.ts` sets the supported absolute `COMPUTER_USE_LINUX_BIN` override to that wrapper in its factory.
   Inspect these files before reuse; the bundled binary path is installation-specific. The verified modes were0700 and0600 respectively.
3. Run `/reload` in Pi after adding the global extension. Pi emits session_shutdown, closes the cached MCP client, reloads extension factories, then emits session_start. This replaces the helper, not GNOME or the browser. Check the actual helper's executable, owner, Pi parent, and persistence flag; a standalone probe does not prove native configuration.
4. Reuse valid existing grants. Only if initial remembered consent is actually missing, have the human watching and ready before the timed request. They review the Remote Desktop prompt, keep the remember option selected, enable Allow Remote Interaction, select a monitor if requested, and click Share. Pointer and keyboard have separate stored grants; say that before the first request so “one final approval” does not conceal a second capability. Preserve human approval; do not operate the consent controls for them.
5. Inspect grant metadata only under `$XDG_STATE_HOME/computer-use-linux/` or `~/.local/state/computer-use-linux/`. Expected token names are `remote-desktop-pointer.token` and `remote-desktop-keyboard.token`; require nonempty, same-owner files, mode0600. The zero-byte `.lock` files are not grants. Never print or copy token contents.
6. Stop only the precisely verified Pi-owned helper, preserving its grant files. Let a native observation spawn its replacement, then perform harmless pointer/keyboard checks without human approval. Verify actual UI effects. A pointer session Start success is not proof of accurate click targeting; report these separately.
7. Reuse the saved grants instead of resetting them. These are single-use restore tokens refreshed by the helper. Do not equate their presence with permanent permission or claim future reboot behavior without testing it.

## Verification across the requested lifecycle

For helper replacement, test with a genuinely new Pi-owned helper; success in the original helper only proves temporary access. For reboot, obtain authorization, preserve a non-secret checkpoint and recovery plan, and have the human save work. Verify a changed boot and actual desktop readiness before testing. Ask the human not to approve new prompts during the reuse test; if one appears, stop and report reuse as unverified rather than making the test pass with new consent.

The latest recorded reboot had matching-owner nonempty private pointer/keyboard grants and a persistence-enabled native Pi helper. Exact keyboard test text was read back in Firefox without submitting it. Pointer portal startup also succeeded without new approval, but the intended address-bar click did not focus the field. Thus permission reuse and keyboard delivery passed for that reboot. The lost-first-click symptom was mitigated afterward in the tested cold-helper GTK and Firefox scenarios using [first-pointer-click.md](first-pointer-click.md), not through another reboot. Windows Desktop Sharing reconnection without keyring unlock was awaiting human confirmation. Do not repeat security setup merely to fix pointer targeting.

## Consent timing

The native integration's default request timeout was60 seconds. The consent frame existed in the portal backend's accessibility tree while Start was pending, but was absent in later observations. Asking the human to look only after a timeout missed the approval window. An in-flight read-only probe distinguished this from a missing or crashed dialog.

On an ambiguous timeout, inspect before another attempt; cancellation is not proof that all delayed work ended. Scope the consent accessibility tree to `xdg-desktop-portal-gnome`, not only GNOME Shell. A SHOWING frame is not proof it is foregrounded on the human's screen.

## What did not work

- Manual approval without persistence: control worked, but no reusable token existed.
- Setting the persistence variable only in Pi's environment: native0.7.13 filtered it out. The supported binary override plus child-side export passed the flag without dependency edits.
- Restarting only the old helper: it did not make unanswered consent succeed or add missing persistence configuration.
- Treating accepted pointer events or saved token files as an accurate click test: Firefox's account menu did not visibly open. Preserve this as a separate targeting diagnosis.
