#!/usr/bin/env python3
"""Capture dummy input into the trusted broker; persist only an opaque receipt.

Python 3.10+. The GUI requires PyGObject and GTK 3. No clipboard reads,
remote network, autosave, recovery files, or dotenv editing. Masking is not proof
that accessibility, recording, clipboard synchronization, or telemetry is safe.
"""

import argparse
import importlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, '/opt/pi-secret-broker')
broker_module = importlib.import_module('broker')
CaptureReceiptError = broker_module.CaptureReceiptError
confirmed_capture = broker_module.confirmed_capture
save_capture = broker_module.save_capture
request = importlib.import_module('client').request


class CaptureError(Exception):
    """A deliberately value-free error safe to display in the capture window."""


def make_receipt(output: Path, handoff_id: str, status: str) -> dict:
    """Value-free failure/cancel receipt; successful saves use the broker receipt."""
    return {"schema": 3, "handoff_id": handoff_id, "destination": str(output), "status": status}


def storage_confirmed(receipt: object, handoff_id: str, output: Path, exit_code: int | None) -> bool:
    """Confirm broker storage metadata only; source closure remains the host guard's job."""
    try:
        return confirmed_capture(receipt, handoff_id, output, exit_code, request)
    except Exception:
        return False


def load_receipt(path: Path, max_bytes: int = 4096) -> object:
    """Read only a bounded owner-only metadata receipt; never echo bad input."""
    try:
        with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), "r", encoding="utf-8") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                return None
            if info.st_size > max_bytes:
                return None
            data = stream.read(max_bytes + 1)
            if len(data.encode('utf-8')) > max_bytes:
                return None
            return json.loads(data)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def activation_valid(path: Path, capture_id: str) -> bool:
    """Input readiness only: require this process in the current host binding."""
    try:
        ready = load_receipt(path)
        if not isinstance(ready, dict) or set(ready) != {'capture_id', 'handoff_id', 'barrier'} or ready['capture_id'] != capture_id:
            return False
        handoff = ready['handoff_id']
        if not isinstance(handoff, str) or len(handoff) != 32 or any(c not in '0123456789abcdef' for c in handoff):
            return False
        root = Path(ready['barrier'])
        info = root.lstat()
        if not root.is_absolute() or not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            return False
        fd = os.open(root / 'active', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            active = os.fstat(fd)
            if not stat.S_ISREG(active.st_mode) or active.st_uid != os.getuid() or active.st_mode & 0o077 or os.read(fd, 33).decode() != handoff:
                return False
        finally:
            os.close(fd)
        binding = load_receipt(root / 'binding', 131072)
        return bool(isinstance(binding, dict) and binding.get('handoff_id') == handoff
                    and binding.get('binding', {}).get('schema') == 3
                    and any(p.get('kind') == 'capture' and p.get('scope', {}).get('id') == capture_id
                            and p.get('scope', {}).get('worker_pid') == os.getpid()
                            for p in binding.get('binding', {}).get('proofs', [])))
    except Exception:
        return False


def open_capture(output: Path, handoff_id: str, activation_path: Path, json_fields: tuple[str, ...] = (), json_root: str | None = None) -> int:
    """Save privately and close the capture; the host separately verifies source closure."""
    import gi
    gi.require_version("Gtk", "3.0")
    Gtk = importlib.import_module("gi.repository.Gtk")
    GLib = importlib.import_module("gi.repository.GLib")

    if not Gtk.init_check()[0]:
        raise CaptureError("No graphical session is available.")
    saved_receipt = None
    window = Gtk.Window(title="Private value capture")
    window.set_default_size(520, 300)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    box.set_border_width(18)
    box.pack_start(Gtk.Label(label="Dummy-only validation. Enter only NONSECRET-DUMMY. Do not enter real private input."), False, False, 0)
    entries = {}
    for field in json_fields or ("value",):
        entry = Gtk.Entry()
        entry.set_visibility(False)
        entry.set_sensitive(False)
        entry.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        entry.set_max_length(16384)
        entry.set_placeholder_text(field)
        if json_fields:
            box.pack_start(Gtk.Label(label=field), False, False, 0)
        box.pack_start(entry, False, False, 0)
        entries[field] = entry
    status = Gtk.Label(label="Waiting for the host privacy guard. Do not enter private values yet.")
    status.set_line_wrap(True)
    button = Gtk.Button(label="Save privately")
    button.set_sensitive(False)
    ready_before = False

    def refresh():
        nonlocal ready_before
        ready = activation_valid(activation_path, handoff_id)
        if ready != ready_before:
            for entry in entries.values():
                entry.set_sensitive(ready)
            button.set_sensitive(ready)
            status.set_text("Dummy input ready. Agent observation is paused. No real private input." if ready else "Privacy guard unavailable. Input is disabled.")
            ready_before = ready
        return True

    watcher = GLib.timeout_add(100, refresh)
    for widget in (button, status):
        box.pack_start(widget, False, False, 0)

    def save(_button):
        nonlocal saved_receipt
        if not activation_valid(activation_path, handoff_id):
            refresh()
            return
        try:
            values = {field: entry.get_text() for field, entry in entries.items()}
            saved_receipt = save_capture(output, handoff_id, values, request, json_root)
        except (CaptureError, CaptureReceiptError) as error:
            status.set_text(str(error))
            return
        except Exception:
            status.set_text("Not saved. Capture is unavailable.")
            return
        for entry in entries.values():
            entry.set_text("")
            entry.set_sensitive(False)
        button.set_sensitive(False)
        window.destroy()

    def close(_window):
        GLib.source_remove(watcher)
        for entry in entries.values():
            entry.set_text("")
        Gtk.main_quit()

    button.connect("clicked", save)
    window.connect("destroy", close)
    window.add(box)
    window.show_all()
    next(iter(entries.values())).grab_focus()
    Gtk.main()
    if saved_receipt is None:
        print(json.dumps(make_receipt(output, handoff_id, "cancelled")))
        return 1
    print(json.dumps(saved_receipt))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Agreed owner-only metadata receipt destination")
    parser.add_argument("--handoff-id", required=True, help="Fresh UUID hex identifier for this private handoff")
    parser.add_argument("--activation-path", type=Path, help="Owned guardian readiness metadata; never human confirmation")
    parser.add_argument("--json-field", action="append", default=[], help="Non-secret string-field name; repeat for a JSON bundle")
    parser.add_argument("--json-root", help="Optional non-secret root key for the JSON bundle")
    parser.add_argument("--check-saved-receipt", type=Path, help="Verify storage metadata only; never release the host observation guard")
    parser.add_argument("--process-exit-code", type=int, help="Verified capture process exit code, for receipt checking")
    args = parser.parse_args()
    if len(args.handoff_id) != 32 or any(c not in "0123456789abcdef" for c in args.handoff_id):
        parser.error("Use a fresh lowercase UUID hex handoff identifier.")
    if not args.output.is_absolute():
        parser.error("Use an absolute destination path.")
    if len(args.json_field) > 16 or len(set(args.json_field)) != len(args.json_field) or any(not key.isidentifier() for key in args.json_field):
        parser.error("Use distinct non-secret JSON field identifiers.")
    if args.json_root and (not args.json_field or not args.json_root.isidentifier()):
        parser.error("A JSON root requires named JSON fields.")
    if args.check_saved_receipt:
        stored = storage_confirmed(load_receipt(args.check_saved_receipt), args.handoff_id, args.output, args.process_exit_code)
        print(json.dumps({"status": "stored" if stored else "storage-unverified"}))
        return 0 if stored else 1
    if args.activation_path is None or not args.activation_path.is_absolute():
        parser.error("Use the owned capture launcher with an absolute activation path.")
    try:
        return open_capture(args.output, args.handoff_id, args.activation_path, tuple(args.json_field), args.json_root)
    except Exception:
        # Never include exception objects, input, clipboard, or file contents.
        print(json.dumps(make_receipt(args.output, args.handoff_id, "capture-unavailable")), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
