# Reusable private capture

Use [private-capture.py](private-capture.py) through the direct host guard, not an untracked shell launch. The GUI sends input only to the trusted broker and persists an opaque schema-3 receipt; receipt metadata never authorizes observation. **Current route is dummy-only. Enter only `NONSECRET-DUMMY`; real input is prohibited until restricted-session migration, integrated handoff validation and reload pass.**

## Prepare and launch

1. Read [private handoff](../references/private-handoff.md) and [private transfer](../references/private-transfer.md). Preserve the current graphical session/profile and obtain authorization for the exact newly created disposable sources.
2. Use existing Python/PyGObject/GTK dependencies. Choose a new absolute metadata-receipt destination in an owned directory, preferably `0700`, outside Git or verified ignored. The helper refuses overwrite and direct parent/destination links; this is not a hostile-filesystem sandbox.
3. Call the direct host tool with `action:prepare`, `disposable_sources:true` and `capture:{output:ABSOLUTE_NEW_PATH}`. Include `firefox:true` when a dedicated source browser is needed. Optional capture `fields` and `root` name fields and a broker namespace. No input values belong in arguments, chat, logs or model-visible environment reads.
4. The guardian generates its capture ID, retains its original cgroup and supplies the mandatory activation path. The host pauses before launch, registers every scope and then activates the disabled form. Wait for `ready:true`; pending/failed preparation never permits private input. Readiness does not supply missing task/disposal authorization.
5. For validation, enter only `NONSECRET-DUMMY` and click **Save privately** inside the registered scope. The broker rejects other values. The helper clears and closes after save. There is no source-closure checkbox or Finish button.
6. Use the direct guard `close` action with its host handoff ID. Only verified containment disposal resumes ordinary tools. Do not inspect a failed save/private UI through a generic tool.

The GUI CLI requires `--activation-path`, but this is a guardian-owned protocol file, not a user-supplied unlock file. Standalone UUID/activation-file fabrication is not a supported handoff. Arrays/multiline or unsupported download formats need a separately assessed protected import route.

## Storage receipt is not release evidence

Schema-3 saved receipts contain capture UUID, destination, status and an opaque broker reference; no captured values are written to the destination. The host guardian confirms the reference through the broker and checks worker exit separately. Cancellation exits `1`; startup failure exits `2`. Save errors remain in the masked window with value-free messages. No receipt field claims source closure or observation readiness.

After verified host release, check owner-only receipt metadata, never credential contents:

```bash
python3 /home/tiago/.agents/skills/computer-use-wizard/templates/private-capture.py \
  --check-saved-receipt /absolute/owned/private/capture-receipt.json \
  --output /absolute/owned/private/new-value --handoff-id CAPTURE_32_HEX_ID \
  --process-exit-code ACTUAL_CAPTURE_EXIT_CODE
```

Use the capture identity and exit status obtained independently from its original guardian, not the host handoff ID or an assumed zero. The check emits only `stored` or `storage-unverified`; malformed/legacy/unsafe metadata and unknown/nonzero exit fail verification. Neither result changes the barrier.

## Broker storage and limits

The broker accepts 1–16 named fields only when every value is exactly `NONSECRET-DUMMY`. It stores those dummy values under a broker-owned `0700` directory as `0600` files and returns a random reference. Agent status/use operations return booleans, not values. The restricted agent cannot read the broker records. This proves neither universal confidentiality nor safety from the trusted capture UID, system administrator, external recording, clipboard/history or kernel compromise.

No clipboard read, editor recovery, overwrite or automatic credential testing is performed. Clearing Python/GTK entries is not secure memory erasure. Masking and dummy checks do not establish telemetry/clipboard safety or end-to-end secrecy. Register every secret-bearing container before exposure; disposal cannot discover private bytes moved into unrelated windows.
