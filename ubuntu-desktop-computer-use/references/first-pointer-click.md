# First portal click is lost after helper startup

Use this branch when saved pointer permission restores, the compositor cursor reaches the expected coordinate, but the first click never reaches the application. Do not reset grants or ask the human to approve remote interaction again merely for this symptom.

## Verified pattern and limits

On Ubuntu 26.04 / GNOME 50.1 Wayland with Computer Use 0.7.13, a fresh helper's first coordinate click produced no GTK motion/press/release. A subsequent click worked. Numeric-only D-Bus tracing showed the correct monitor coordinate and evdev left-button press/release; the extension's `GetIndicatorState` confirmed the actual cursor coordinate. The internal Mutter failure mechanism was not proven.

A matched-source local patch passed three cold-helper GTK tests, each with exactly one target activation. An unmodified build using the same compiler failed its cold control test. A fresh patched helper's first Firefox address-bar click focused the intended editable control; harmless exact text was read back, never submitted, then cleared. The upstream `remote_desktop::` library tests passed: 34 tests. The new patch has not been tested through another reboot.

## Installed workaround

- `~/.local/lib/computer-use-linux-desktop-input/computer-use-linux`: private release helper, upstream tag `v0.7.13` plus click settling and the combined drag repair.
- `desktop-input.patch` and `build-info.json` in that directory: exact patch and nonsecret provenance/check summary. The installed release passed a fresh-helper GTK click with exactly one press/release/activation.
- `~/.local/bin/pi-computer-use-linux`: retains the persistence export, then execs this helper with unchanged arguments.
- The existing global `desktop-control-persistence.ts` extension still selects that wrapper. Installed npm package files and GNOME settings were not modified.

The patch in `src/remote_desktop.rs::click` sends:

1. Absolute motion to the requested target.
2. A 50ms pause.
3. Absolute motion to the **same** requested target.
4. The existing single press/release sequence, unchanged.

The click component does not replay a click, add button events, move to a second location, or request another permission. The combined helper also repairs portal dragging; read [html5-drag-motion.md](html5-drag-motion.md) when drag starts but never drops. Scroll is unchanged. This is a version-pinned local workaround, not an upstream fix. Recheck native integration compatibility after package upgrades; prefer an upstream fix when one is verified.

## Reproduce before changing anything

1. Inspect the wrapper, private helper and provenance. Check the actual Pi-owned process executable and artifact hash, not only a binary's existence. Keep pointer/keyboard grants private.
2. Reuse [pointer-probe.py](../templates/pointer-probe.py) with its [instructions](../templates/README.md#pointer-delivery-fixture) on the real desktop instead of writing another GTK event logger. Use a new owned output file per trial; the fixture atomically records only its own motion/press/release and target activation. Preserve Firefox, Windows Desktop Sharing and other user applications.
3. Obtain fresh window bounds and screenshot coordinate dimensions. Verify coordinates independently: compositor cursor readback and numeric-only portal/Mutter arguments. Never dump full portal response bodies or restore tokens.
4. Replace only the identified same-user native helper directly owned by the current Pi. Re-observe the fixture, then issue exactly one click. Poll its event log for up to two seconds; require exactly one activation and no off-target button events. Do not repeat unknown-outcome clicks in real applications.
5. Test three fresh helpers and an unmodified same-toolchain control. Only then verify one harmless real-app target. Check actual focus/value, clear test input and close only the disposable fixture.

Keep operational event evidence, numeric traces and verification records in an owned private location outside skill directories, chosen for the current task. Summary JSON is not independent evidence; use event records and observed tool readback too. Historical PIDs, window IDs and coordinates must not be reused.

## Rebuild or roll back

For an authorized rebuild, obtain the matching upstream tag, inspect/apply the stored patch, and build with `cargo build --locked --release --bin computer-use-linux`. The verified build used Rust 1.99.0; the Ubuntu 1.93 compiler failed on upstream `atomic_try_update`. Run `cargo test --locked --lib remote_desktop::`—the binary test target contains zero matching tests. Confirm successful build exit, artifact hash and actual launched executable. Stop the precisely identified helper before replacing its executable; preserve grants and persistence configuration.

To roll back only this workaround, edit the wrapper's `exec` target back to the installed matching bundled binary, then replace only the current Pi-owned helper. Do not remove the persistence export/global extension or delete saved grants. Revalidate input because the old first-click failure can return.

## What did not work

- 100ms between a single motion and button-down: the cold click still produced no fixture events.
- 300ms after portal startup before a single motion: same failure; do not keep increasing sleeps without evidence.
- Treating correct cursor location or successful D-Bus calls as delivered input.
- Reading the fixture JSON during its truncate/write interval: transient decoding failure, not a failed click. The reusable fixture writes atomically; distinguish missing/startup errors from failed delivery and poll verification without repeating the click.
- Assuming the Bash process always exists between Python and Pi: Bash can exec its final command. Locate and verify the owning Pi ancestor before selecting its child helper.
- Using Tab to dismiss a cleared Firefox omnibox: it can select private history suggestions. Use Ctrl+L, Backspace, Escape, and verify only an empty/about:blank result. Suppress incidental private focus/history feedback in diagnostic output.
