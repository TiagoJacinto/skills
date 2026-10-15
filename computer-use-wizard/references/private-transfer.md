# Private local transfer when the user asks the agent to do it

Use only for an explicitly requested transfer of an authorized secret to an agreed destination without returning the value to the model. Human private entry remains the default for login, MFA, CAPTCHA, passwords, and recovery codes. This procedure does not authorize generating, revealing, rotating, or revoking credentials.

## Choose the route before exposing a value

Read [private-handoff.md](private-handoff.md) before reveal or private entry. It owns the active observation barrier and its current-handoff source-closure clearance; storage success is not clearance.

Confirm the exact source, destination, owner/project/environment, variable name, and authorization. Prefer a local non-echoing file/CLI transfer if the value already exists privately. Preserve existing working credentials; inspect name/scope metadata before provisioning again.

For a one-time UI reveal, agree on capture **before** generation. If the user already lost the value, do not claim it can be recovered; obtain the required authorization for a replacement. Keep revocation a separate action.

A route is eligible only if secret bytes stay out of model-visible tool inputs/results, observations, clipboard reads, DOM/accessibility extraction, screenshots/recordings, shell arguments, logs, and retained diagnostics. Check automatic post-action captures, clipboard history/RDP synchronization, and temporary retention as well as explicit reads. Inspect relevant local capture/tool behavior. If telemetry or clipboard behavior is unknown, say so and use human entry; dummy testing proves mechanics, not confidentiality. This branch never overrides host freshness/observation rules: if satisfying them would expose a secret, use human transfer.

## Verify the destination and mechanics with dummy data

Use the reusable [private-capture.py](../templates/private-capture.py) and [capture instructions](../templates/README.md) when a masked local capture window is the agreed route. Keep its common code unchanged; supply a new non-secret destination, fresh handoff UUID and expected raw/bundle field names. It returns metadata only and refuses overwrites. This helper does not establish route confidentiality or authorize agent clipboard transfer.

Use a disposable nonsecret sample through the same route. Confirm:

- The destination has owner-only access and is outside Git or actually ignored, with the exact agreed key/scope; unrelated content is preserved. Ignore rules prevent accidental commits, not local access.
- Capture writes the exact sample and reports status only. Masking the GUI is not sufficient if the value is returned by accessibility or logging.
- A GUI capture tool does not create recovery files, swap files, backups, or retained history containing input. A general-purpose text editor with autosave/recovery is not a verified private sink.
- Window identity/focus and save behavior are reliable; cleanup touches only owned temporary artifacts.

For local programs, consume secret bytes privately from a protected file/stdin or local memory; emit only boolean/status results. Never interpolate real values into command arguments or diagnostic messages. Do not claim a dummy pass establishes an application's real credential-generation result.

## Perform the approved transfer without observation

Enter `PRIVATE_HANDOFF_ACTIVE` and pause all observation of the secret surface and any recording before reveal or private entry. For GUI copy/paste, use only a confirmed local Copy → masked capture → Save route whose tools do not read/echo the clipboard or secret. Keep target identity known; if a rerender or focus change makes blind input unsafe, stop for the human instead of inspecting the revealed value.

Submit a credential-creation operation only with its required specific authorization, and only once. If the outcome is uncertain, inspect safe name/status metadata or ask the human for error/loading status; do not resubmit or observe the secret display merely to resolve uncertainty.

After saving, retain the private barrier until the guard closes the pre-registered dedicated windows and independently verifies absence under [private-handoff.md](private-handoff.md). Human attestation cannot release it. A bare “done,” closed capture window, saved status or failed helper is not permission to resume observation. Agree on clearing transient clipboard/capture state without reading it; verify cleanup by status, not contents. Do not delete user-owned source files automatically.

## Verify storage and use separately

Check permissions, ignore status, key/name presence, and destination scope without printing values. Then, if authorized, perform a non-echoing read-only integration check against the exact intended resource. Sanitize errors as well as success output. A saved file is not proof that the credential works; an existing remote key name is not proof that its value is saved locally.

If either check fails, retain the task as incomplete and identify the exact missing step. Record the route used, destination and scope, storage check, integration result, and any confidentiality limitation—never the value. During a conversation wizard, keep this record internal; communicate only the necessary action, authorization or blocker.
