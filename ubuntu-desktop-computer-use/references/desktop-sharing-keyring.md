# Desktop Sharing without a separate keyring unlock

**Goal:** the human connects from Windows to the existing Ubuntu desktop using **Desktop Sharing + Remote Control**, uses the same visible apps as the agent, and does not separately unlock Login to make RDP credentials available. Keep this mode; Remote Login starts a different kind of session and is not a substitute for the requested shared desktop.

**Reference validation boundary:** in one tested GNOME setup, the agent moved only the existing Desktop Sharing credential into a separate passwordless default keyring, preserved the password and unrelated Login entries, and verified enabled/control-enabled sharing on port 3389. The human retried Windows `mstsc` with existing credentials and replied “works.” End-to-end access in that session is human-confirmed; reliable startup and access after a fresh boot remain unverified.

## 1. Confirm the intended access and current state

Inspect the target user's active graphical session and Desktop Sharing service, the actual configured port, and private-network reachability. The recorded connection used Tailscale; discover the current address instead of copying the historical one.

Use `grdctl status` without credential-display options. Verify enabled sharing, non-view-only control, and the user service/listener. Displayed hidden credentials are not proof of successful authentication. Keep firewall policy, authentication, personal browser state, and unrelated keyring entries unchanged.

If credentials depend on the protected Login keyring, ask whether the user wants the below storage trade-off. A human can privately unlock Login once for an approved migration; pause screenshots, accessibility reads, and other observation during private input. Never request the keyring password in chat.

## Failed fixes to distinguish before asking for more human work

In the recorded GNOME configuration, an empty-password **Login** keyring was not a durable remedy: an isolated password-login plus later credential-save sequence encrypted it again. The human had already performed the requested change. Repeating those UI steps would not explain or prevent the reset. Inspect the actual backing collection and relevant login/update path; never equate “unlocked now” with “stored passwordless.”

A separate **nondefault** passwordless collection also failed the update test: fresh lookup worked, but a normal RDP credential update created a second item in Login and cold lookup returned the old password. Initial lookup alone was therefore an inadequate acceptance check. This is version-specific evidence, not a claim that every GNOME setup behaves identically.

If an earlier fix returns, reproduce the responsible transition with dummy data before proposing another real change. Preserve the user's access mode and current working connection during diagnosis.

## 2. Obtain explicit approval for the actual security change

The successful arrangement is a separate **passwordless keyring made the default**, not merely a second nondefault collection.

Explain both consequences before proceeding:

- The migrated RDP credential is stored without keyring encryption.
- Other applications using the new default may store future secrets unencrypted too. Existing unrelated Login entries stay where they were.

File permissions `0600` restrict access; they do not provide encryption. Approval must cover credential migration and the global default change. Prior session approval does not authorize applying it to another machine or credential. Do not reset the RDP password or disable Windows authentication merely to avoid local unlock prompts.

## 3. Validate the migration for the installed GNOME version

The recorded helper used libsecret/Secret Service to transfer the existing value privately in memory. It used GNOME's internal `CreateWithMasterPassword` interface to create the empty-password collection, so it is version-dependent—not a portable stock command. Inspect and test the exact implementation before touching real credentials; stop if the interface is unsupported.

Historical helper source paths belong in external audit records, not reusable execution instructions. Discover and inspect any current approved implementation before reuse; do not assume helpers exist or remain unchanged. Read source code only; do not read real keyring bodies or credential values through agent tools.

Before applying an equivalent migration, test with dummy values in disposable HOME/XDG directories and a private D-Bus session. Verify the secret daemon really uses that disposable storage. Require these results:

- Lookup with Login still locked after a fresh daemon start.
- A later password login leaves the separate collection passwordless.
- RDP credential updates through the installed `grdctl` use one current item; a later fresh lookup returns the updated dummy password.
- Unrelated dummy credentials survive.
- An injected failure before deleting the source preserves the original item and restores the previous default.

## 4. Apply only the approved credential migration

Preflight the target user, keyring storage paths, original default, unique Desktop Sharing item, unlocked source, absent destination, and restricted ignored metadata path. Stop on duplicates, a changed default, or evidence of a prior partial migration; do not rerun blindly.

The verified sequence was:

1. Create a distinct passwordless collection (`Unattended Desktop Sharing` in the session).
2. Copy the exact existing RDP secret, attributes, and content type without returning them to the model or logs.
3. Privately compare the copy against the source. Verify persistent backing format and permissions without printing its contents.
4. Save metadata-only recovery information, then make that collection default and verify the alias.
5. Only after verified copy/default selection, delete the exact original RDP item. Preserve every unrelated Login item.
6. Require one matching RDP item in the new default, no old RDP item in Login, unrelated item preservation, and service readback.

Retain the verified destination on any post-deletion failure. Recovery after deletion requires copying back from that retained credential; metadata alone cannot restore secret bytes. Do not delete keyrings or restart/lock the real secret daemon as an automatic cleanup step.

The actual helper recorded non-secret migration metadata in `.tools/desktop-sharing-keyring-migration.json`, mode `0600`. Do not embed passwords in shell arguments, transcripts, patches, logs, or skill files.

## 5. Verify from Windows and state the remaining prerequisite

Have the human run Windows `mstsc` against the verified private address/port using their existing Desktop Sharing credentials. Pause observation during private authentication; ask for connection/control confirmation. A running service is not an end-to-end test.

This mode requires a working logged-in Ubuntu desktop. The session found a separate GNOME cold-start timeout that prevented automatic login on one boot. No timeout change or reliable-startup fix was applied. Record that as unresolved; do not replace Desktop Sharing with Remote Login, silently change GDM, or promise access “always.” A fresh-boot test requires separate authorization, saved work, and recovery arrangements.

## Design rationale, not troubleshooting history

Making the separate passwordless collection default kept RDP updates in one place in the isolated tests. A nondefault arrangement did not reliably preserve update behavior. The successful setup kept unrelated Login secrets protected while accepting the broader future-default-storage trade-off explicitly described above.
