#!/usr/bin/env python3
"""An owned GTK pointer target with atomic, non-secret event evidence.

Launch with --output NEW_FILE in an owned directory. Use native Computer Use
against this fixture, not real application buttons. --verify-file reads only
this fixture's event file; it never injects input or changes permissions.
"""

import argparse
import contextlib
import importlib
import json
import math
import os
import stat
import sys
import uuid
from pathlib import Path


class ProbeError(Exception):
    pass


class ProbeLog:
    """Record this fixture's events only; replace its own JSON atomically."""

    def __init__(self, output: Path):
        if not output.is_absolute():
            raise ProbeError("Use an absolute output path.")
        self.output = output
        self.events: list[dict] = []
        self.activations = 0
        self.session = uuid.uuid4().hex
        self._parent = os.open(output.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            parent = os.fstat(self._parent)
            if parent.st_uid != os.getuid() or parent.st_mode & 0o022:
                raise ProbeError("Use an owned directory without shared write access.")
            fd = os.open(output.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self._parent)
            try:
                os.fchmod(fd, 0o600)
                initial = os.fstat(fd)
                self._identity = (initial.st_dev, initial.st_ino)
            finally:
                os.close(fd)
            self._publish()
        except Exception:
            os.close(self._parent)
            self._parent = -1
            raise

    def snapshot(self) -> dict:
        return {
            "schema": 1, "pid": os.getpid(), "session": self.session,
            "activations": self.activations, "events": list(self.events),
        }

    def record(self, kind: str, x: float, y: float, button: int, target: bool) -> None:
        if kind not in {"motion", "press", "release", "activate"}:
            raise ProbeError("Unknown event kind.")
        if not math.isfinite(x) or not math.isfinite(y) or button not in {0, 1, 2, 3}:
            raise ProbeError("Invalid event coordinates or button.")
        if len(self.events) >= 1000:
            raise ProbeError("Event limit reached; start a new fixture.")
        self.events.append({"kind": kind, "x": x, "y": y, "button": button, "target": target})
        if kind == "activate":
            self.activations += 1
        self._publish()

    def _publish(self) -> None:
        try:
            current = os.stat(self.output.name, dir_fd=self._parent, follow_symlinks=False)
        except OSError:
            raise ProbeError("The output is unavailable; refusing to replace it.") from None
        if not stat.S_ISREG(current.st_mode) or (current.st_dev, current.st_ino) != self._identity:
            raise ProbeError("The output changed ownership; refusing to replace it.")
        temporary = ".pointer-probe-" + uuid.uuid4().hex
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self._parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(self.snapshot(), stream, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.output.name, src_dir_fd=self._parent, dst_dir_fd=self._parent)
            info = os.stat(self.output.name, dir_fd=self._parent, follow_symlinks=False)
            self._identity = (info.st_dev, info.st_ino)
        finally:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(temporary, dir_fd=self._parent)

    def close(self) -> None:
        if self._parent >= 0:
            os.close(self._parent)
            self._parent = -1


def verify_snapshot(snapshot: dict, expected: int, session: str) -> bool:
    """Require the requested session and exact left-button event sequence."""
    if expected < 1 or not session or snapshot.get("schema") != 1 or snapshot.get("session") != session:
        return False
    events = snapshot.get("events")
    if not isinstance(events, list) or snapshot.get("activations") != expected:
        return False
    sequence = []
    for event in events:
        if not isinstance(event, dict) or event.get("kind") not in {"motion", "press", "release", "activate"}:
            return False
        if event["kind"] == "motion":
            continue
        if event.get("target") is not True or event.get("button") != 1:
            return False
        sequence.append(event["kind"])
    return sequence == ["press", "release", "activate"] * expected


def open_probe(output: Path) -> int:
    import gi
    gi.require_version("Gtk", "3.0")
    Gtk = importlib.import_module("gi.repository.Gtk")
    Gdk = importlib.import_module("gi.repository.Gdk")
    if not Gtk.init_check()[0]:
        raise ProbeError("No graphical session is available.")
    log = ProbeLog(output)
    window = Gtk.Window(title="Pointer delivery probe")
    window.set_default_size(640, 400)
    area = Gtk.EventBox()
    area.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK)
    layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    layout.set_border_width(24)
    layout.pack_start(Gtk.Label(label="Click the green target exactly once."), False, False, 0)
    target = Gtk.Label(label="Target")
    target.set_size_request(160, 100)
    target.set_halign(Gtk.Align.CENTER)
    target.set_valign(Gtk.Align.CENTER)
    target.get_style_context().add_class("pointer-target")
    layout.pack_start(target, True, True, 0)
    counter = Gtk.Label(label=f"Activations: 0   PID: {os.getpid()}")
    layout.pack_start(counter, False, False, 0)
    area.add(layout)
    style = Gtk.CssProvider()
    style.load_from_data(b".pointer-target { background-color: #198c4d; color: white; }")
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    armed = False
    failed = False

    def hit(event):
        position = target.translate_coordinates(area, 0, 0)
        if position is None:
            return False
        x, y = position
        return x <= event.x < x + target.get_allocated_width() and y <= event.y < y + target.get_allocated_height()

    def record(kind, event, button):
        nonlocal failed
        try:
            log.record(kind, float(event.x), float(event.y), button, hit(event))
        except Exception:
            failed = True
            window.destroy()

    def motion(_area, event):
        record("motion", event, 0)
        return True

    def press(_area, event):
        nonlocal armed
        if event.type == Gdk.EventType.BUTTON_PRESS:
            armed = event.button == 1 and hit(event)
            record("press", event, event.button)
        return True

    def release(_area, event):
        nonlocal armed
        record("release", event, event.button)
        if not failed and armed and event.button == 1 and hit(event):
            record("activate", event, 1)
        armed = False
        counter.set_text(f"Activations: {log.activations}   PID: {os.getpid()}")
        return True

    area.connect("motion-notify-event", motion)
    area.connect("button-press-event", press)
    area.connect("button-release-event", release)
    window.connect("destroy", lambda _window: Gtk.main_quit())
    window.add(area)
    try:
        window.show_all()
        print(json.dumps({"status": "ready", "pid": os.getpid(), "session": log.session}), flush=True)
        Gtk.main()
    finally:
        log.close()
    return 2 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path, help="New event file for a native GTK window")
    mode.add_argument("--verify-file", type=Path, help="Read this fixture's non-secret event file")
    parser.add_argument("--session", help="Session ID returned by this fixture's launch")
    parser.add_argument("--expected", type=int, default=1)
    args = parser.parse_args()
    try:
        if args.verify_file:
            snapshot = json.loads(args.verify_file.read_text(encoding="utf-8"))
            passed = verify_snapshot(snapshot, args.expected, args.session or "")
            print(json.dumps({"status": "pass" if passed else "fail"}))
            return 0 if passed else 1
        return open_probe(args.output)
    except Exception:
        print(json.dumps({"status": "probe-unavailable"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
