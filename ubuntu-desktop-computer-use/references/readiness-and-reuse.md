# Prove the requested control path

Read before setup or recovery when the goal includes a shared desktop, repeated use, or surviving a lifecycle change. This reference owns the verification contract; branch references own the fixes.

## 1. Preserve the target

Record a short **target invariant**: machine → desktop user/session → visible application/profile → human access mode → agent control route. Discover current IDs and endpoints separately; they are not durable identity.

For example: “Use the existing Ubuntu desktop, shared with the human through Desktop Sharing + Remote Control; preserve the signed-in work surface.” A blocker does not authorize substituting Remote Login, a virtual desktop, another machine, or a fresh browser profile. Explain any necessary change and obtain agreement. Follow host tool routing; if the requested route conflicts with it, state the limitation rather than silently substituting.

Clarify the requested lifecycle: same helper, replacement helper, new Pi session, app restart, logout/login, reboot, or an idle interval. Test only the relevant boundaries. “Not again” means reduce recurring human setup, not bypass consent or promise indefinite availability.

Keep the original task/stage pending while repairing its prerequisite. Record the next task action so a successful readiness repair returns to useful work instead of another open-ended setup discussion.

## 2. Separate the layers

A similar-looking prompt can belong to a different control path. Identify the owner before changing settings:

- **Graphical session:** startup/login, current lock, display blanking, and suspend are separate states. SSH reachability proves none of them.
- **Window targeting:** extension installed/enabled/active, actual window listing, and actual focus are separate checks.
- **Capture:** API success must yield a usable picture of the intended desktop. A black picture is not verified capture.
- **Pi input:** GNOME portal consent and the native helper's pointer/keyboard grants. These are not the Windows RDP switches or credentials.
- **Human remote access:** Desktop Sharing service, Remote Control enabled, credentials available, network reachability, and a successful client connection/control check.
- **Browser:** visible process, correct profile, endpoint/tab continuity, and authentication. A stored profile does not keep a process, debugging port, or unsaved form alive.
- **Credential storage:** a browser's password-store option affects that browser, not GNOME Remote Desktop's keyring lookup. An unlocked keyring now does not prove its stored protection changed.

Use the observed error to choose the branch. `Credentials are not set` is not automatically a missing-password diagnosis; a locked collection can prevent lookup. A restored portal session plus a lost click is not automatically a revoked-grant diagnosis.

## 3. Probe before reinstalling or restarting

Reuse existing approved setup. Inspect the installed version, current configuration and actual helper first. Perform routine diagnostics, launch/open/focus work surfaces, and run harmless disposable tests under the requested setup or diagnosis without repeated permission questions. Preserve read-only/stop boundaries and host tool rules; changes to security policy, disruptive restarts, and other sensitive actions still need their specific authorization.

Keep the human in the conversation, not operating Ubuntu. Ask for missing non-secret details in chat and enter them yourself. Before a UI handoff, establish the concrete reason it is necessary: private authentication/input, platform consent, or unavailable control after bounded diagnosis. Prepare everything else first, ask for the smallest human action, then resume agent control. An ordinary contact email is not a secret; its use for account recovery/permissions may make the action sensitive.

Verify only the capabilities needed by the task:

1. Fresh scoped app state and real window list/focus identify the target. On error, report targeting unavailable; an empty failed query is not proof that no apps exist.
2. Capture shows that target when visual control is needed.
3. A harmless click produces an application change, not just `ok: true`, cursor movement, or portal Start success.
4. Exact harmless text reaches the intended field; clearing leaves it empty. Do not submit the test string.
5. Scroll/drag passes only with its own observed result when needed; a successful click does not prove drag-and-drop.
6. Cleanup preserves original applications and work.

Probe through the actual Pi-owned helper/control route. A standalone binary test does not establish how the live integration is configured. If readiness flags and actual probes disagree, report the discrepancy and use the probe result as the gate.

For cold-helper reuse, exercise the **first** intended action on a disposable target and require exactly one effect. A warm-session retry can hide a lost first click. Keep separate results for permission restoration, event delivery, and target accuracy. Never double-click a real application merely to make a failed first click disappear.

## 4. Diagnose with a bounded experiment

For each attempt, state: **observed failure → hypothesis → smallest discriminating probe/change → expected result**. Save its result before choosing the next action.

After two materially equivalent failures or two actions with no measurable progress, stop that branch. Inspect the responsible layer and consult available diagnostic guidance/Advisor before another equivalent attempt. Repeated extension toggles, reinstallations, broad service restarts, and larger sleeps are not new evidence. Separate the symptom's proven cause from a proposed mitigation.

Prefer read-only discrimination, then one authorized scoped change. Reset only the identified Pi-owned helper if warranted; preserve GNOME, the browser, RDP, and grants. A reboot is a test boundary or justified repair, not a default diagnostic step.

For timed consent, confirm the human can see the target and is ready **before** issuing the request. Explain the prompt and deadline first. A timeout does not mean the prompt never appeared; inspect pending/expired state before retrying. Human approval during a reuse test invalidates a claim of prompt-free reuse. If consent is required, pause that test and obtain it normally; record that approval-free reuse was not demonstrated rather than bypassing permission.

When an earlier fix returns, investigate who overwrote it, a different config/collection, or an ineffective launch setting before asking the human to repeat the same steps. Reproduce update/login transitions with dummy data when testing credential storage. Do not experiment on real secrets or replay ambiguous submissions.

## 5. Prove persistence, not just storage

For the relevant subsystem, report these outcomes separately:

- **Saved:** the intended non-secret setting/config or grant metadata is present at the intended durable location.
- **Effective:** the actual live helper/service uses it, with the correct owner, executable and launch environment.
- **Authorized:** required grants/credentials are available through the intended private route. File presence alone does not prove validity.
- **Reused:** a genuinely new process/session after the agreed boundary performs the required action without renewed setup/approval.

Machine-wide reusable launchers/config belong in user-level locations, not solely inside one project's worktree. Project credentials stay project-scoped. Do not move existing files without authorization. Record custom helper version/provenance and revalidate compatibility after upgrades.

Before disruptive tests, obtain approval, save work and a non-secret checkpoint, and establish a recovery path. Confirm the specific requested boundary really occurred (new helper/process, new session, changed boot ID). A helper replacement proves neither logout/login nor reboot persistence. After it, revalidate identity, effective configuration, and actual application effects. Label human-confirmed RDP connection separately from agent-observed service readiness.

Use a compact result record: **capability · evidence · tested boundary · remaining limit**. Completion requires the requested path, not every possible capability. “Configured, reuse untested” is an incomplete persistence requirement, not a green check. If the user enters a password or grants consent during the test, record the confound and leave unattended reuse unverified.

One successful reboot does not prove every future boot; an unexplained earlier startup failure stays a reliability risk. After a later patch, earlier reboot evidence proves only the earlier build. Do not upgrade it to a reboot-tested fix.

## 6. Resume or identify the exact blocker

Once the required probes pass, return to the recorded task/stage under its existing approval boundaries. By default, perform the next authorized routine action without another generic “continue?” gate; ask for stage approval only if the user requested that cadence. Pause only for a material decision, private input, platform consent, sensitive-action authorization, or an unresolved outcome. Continue independent authorized work when one operation is blocked. The wizard skill owns detailed submission/acknowledgement classification; a routine Save/Continue control is not itself a reason to ask permission.

If blocked, name the missing capability, the evidence, and one exact human action needed. Distinguish work completed from what remains unverified; report only results the current evidence supports.
