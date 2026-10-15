# HTML5 drag starts but never drops

Use when native desktop dragging starts a browser HTML5 drag but the target never receives `drop`. This is distinct from the cold first-pointer-click failure in [first-pointer-click.md](first-pointer-click.md).

## Verified boundary

On Ubuntu GNOME 50.1 Wayland, the Computer Use 0.7.13 portal drag implementation pressed left, waited 35ms, jumped directly to the endpoint, waited 35ms, and released. Native Firefox and Chrome both failed a minimal text/plain HTML5 source/target fixture.

A temporary matched-source build retained the installed click-only workaround and added 19 intermediate absolute motions, 20ms apart, before the final endpoint motion. Four warm Firefox trials and one warm Chrome trial each recorded exactly one actual target drop. Switching that same build back to the original sequence failed again in Chrome. This establishes the missing continuing motion as the repair at the tested application boundary; it does not establish the exact internal Mutter mechanism or a minimum step count.

A follow-up candidate also settled source focus: after the initial source motion, wait 50ms and reassert the same coordinate before pressing, then perform the stepped drag. Three fresh-helper Firefox trials and one fresh-helper Chrome trial each delivered exactly one actual drop as their first input, without a warm-up click. A new helper was started for each trial using the existing saved permission. The build and 34 remote_desktop tests passed.

After user approval, a clean release helper was installed at `~/.local/lib/computer-use-linux-desktop-input/computer-use-linux`. It retains the click fix, source settling, and stepped drag, without diagnostic switches. The existing persistence wrapper now selects it. Installed fresh-helper first-drag trials passed in Firefox and Chrome, and the installed first GTK click also passed. The same 34 library tests passed. Cross-monitor dragging and combined-repair persistence through another reboot remain unverified.

Read the installed `build-info.json` and `desktop-input.patch` before rebuilding; inspect the actual running helper path/hash. The retired click-only helper directory is archived under the private diagnosis workspace, not selected by a runtime fallback.

## Reproduce and compare

1. Inspect the actual Pi-owned helper executable, its parent, version/provenance, and launcher. Preserve the existing click fix and persistence export. Keep saved portal grants private.
2. Use an owned local HTML fixture with a draggable source, `dataTransfer.setData('text/plain', marker)`, a target that prevents default on `dragover`, and a `drop` handler that checks the marker. Record only its own pointer/drag events and drop count. Separate trial IDs prevent old evidence from passing a new trial.
3. Verify the browser window and screenshot coordinates through native Computer Use. Require source `pointerdown` with button held and `dragstart` before interpreting a no-drop result. A cold-helper trial containing only target `pointerup` is an input-startup failure, not evidence about the drag trajectory. For trajectory comparisons, warm the pointer on an owned blank area and reset the fixture. For cold-start verification, prepare the page with the previous helper, stop only that helper, start the candidate, observe/focus the intended window through read-only tools, and make drag its first input. Require one actual drop; a warm retry cannot validate cold delivery.
4. Use browser-controlled dragging as a fixture positive control, not as proof of desktop input. Both smooth and single-jump browser-controlled gestures passed this fixture.
5. With authorization, build a temporary helper from the matching upstream tag, retaining approved local patches. Change the drag trajectory, compare against an equal-duration wait without intermediate motion, and switch the same build back to the original sequence. Stop only the verified helper owned by this Pi when replacing it; restore the exact launcher and normal executable after the experiment.
6. Gate success on application evidence: actual source press/start, exactly one target `drop`, counter 1, and drag end. A native tool's `ok: true` is submission only. Repeat successful trials and test both browser implementations before generalizing.
7. Close only owned windows/server/profile. Verify restored executable provenance and unchanged installed binary. Keep experimental source and nonsecret event evidence in a private, clearly marked diagnosis workspace when needed for follow-up.

The recorded workspace is `~/.cache/pi-drag-diagnosis/`: `diagnosis.json`, `experimental-drag.patch` (trajectory experiment), `cold-drag.patch` (trajectory plus source settling), warm/cold trial JSON files, `check-trial.py`, fixture server, and matched source. The historical experimental patches contain diagnostic modes for controlled comparison; the current clean source and installed `desktop-input.patch` contain none. A private Rust 1.99.0 toolchain was assembled from checksum-verified official rustc/cargo/rust-std component archives because the earlier Ubuntu compiler could not build this source. Both diagnostic builds and `cargo build --locked --release --bin computer-use-linux` succeeded; `cargo test --locked --lib remote_desktop::` passed 34 tests.

## What did not work

- Adding 500ms after the endpoint motion before release: Chrome still had no drop.
- Adding 380ms before the single endpoint jump, matching the stepped trajectory's added duration: Firefox still had no drop.
- Adding only one 12px intermediate movement: Firefox still had no drop.
- Treating Chrome native drag-over `buttons=0` as proof of lost button state: successful stepped native Chrome trials also reported zero there.
- Treating stepped motion as a cold-start fix: the first restored-session drag still lacked its press event. Keep cold startup and trajectory failures separate.
