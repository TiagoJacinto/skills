---
name: automated-checks
description: turn a requested validation into the right file-change agent hook, Git hook, or CI gate. Use when asked to automate a check, enforce a validation, add a hook, or make a command run before commit, push, or merge.
---

# Automated checks

Make the requested check a **tight loop**: the earliest reliable feedback that fits its cost, plus authoritative CI enforcement where the check protects shared history. Implement it; do not merely recommend a location.

## 1. Discover

Inspect the target repository before selecting or changing a mechanism:

- existing commands, package manager, task runner, formatter/linter/test configuration, and generated-file workflow;
- existing editor/file watchers, agent hooks, Git-hook framework, CI workflows, merge protection, deployment gates, production checks, and contributor documentation;
- whether the requested command is deterministic, its affected scope, its measured or expected runtime, required services/network/secrets, and whether it modifies files;
- the host's supported hook mechanisms and their documented configuration format.

Reuse established project mechanisms and commands. If a command does not exist, identify the smallest reliable implementation.

When an agent hook is a candidate, read [`AGENT-HOOKS.md`](AGENT-HOOKS.md) and verify the installed agent's current event contract before choosing an event.

Ask the user before either branch:

1. The change would configure a developer-global agent hook rather than repository-owned automation. State the target and the effect.
2. The check needs new tooling. Offer the smallest maintained third-party option and a small project-local implementation, with trade-offs. Wait for the choice.

If the repository cannot support a requested layer, choose the next viable layer and state why in the final result. Ask only when no safe viable layer remains.

## 2. Create one check

Create a canonical, repository-owned command or script for the check before wiring surfaces. Give it a clear verb and a scope appropriate to the request, such as `format:check`, `lint`, `test:unit`, or `check:secrets`.

Every surface invokes that command (or a documented scoped form of it). Keep the check's policy and implementation in its native configuration; hooks and CI are runners, not duplicate implementations.

Use validation-only commands by default. Allow a file-changing command only in a file-change agent hook or when the user explicitly requests fixing. A commit/push hook and CI must leave tracked files unchanged.

## 3. Route the tight loop

Choose the earliest mechanism that supplies useful, reliable feedback. The layers below are common possibilities, not a closed set or mandatory stages. A repository or platform may offer a different layer that is the best fit; select it using the same cost, scope, reliability, and authority criteria.

| Layer | Use when | Behaviour |
| --- | --- | --- |
| Editor/save/file watcher | Per-file, deterministic checks that should help every developer immediately | Format, organise imports, or report narrow diagnostics. Treat this as feedback, not shared enforcement. |
| Coding-agent lifecycle hook | The check should run around prompts, tool calls, file changes, turns, subagents, sessions, or worktrees | Prevent unsafe actions before a tool; fix or validate after a file/tool; aggregate at batch, turn, or settled boundaries. Pair shared policy with Git or CI. |
| Pre-commit | Fast, local, dependency-ready checks that protect commit contents | Run staged/scoped formatting, linting, secret/large-file detection, generated-file freshness, or fast tests. Block a bad commit. |
| Commit-message hook | Commit metadata itself is governed | Validate Conventional Commits, issue references, signatures, or required trailers. |
| Pre-push | Medium-cost repository-wide checks valuable before sharing | Run full lint/type checks, builds, or a reliable test suite. Block a bad push. |
| CI on push | Every pushed branch needs centralized validation or an artifact | Run repository-wide checks, builds, scans, or branch previews independent of local setup. |
| CI on pull request | A proposed integration needs reviewable, authoritative status checks | Run full tests, coverage policy, security checks, migrations, and platform matrices. Report actionable annotations and fail violations. |
| Protected branch / merge queue | The exact candidate entering the main branch must be valid with concurrent changes | Require authoritative statuses and retest the queued merge result when the platform supports it. |
| Deployment/release gate | Safety depends on an artifact, target environment, or release metadata | Verify artifact provenance, vulnerabilities, configuration, migration safety, smoke tests, and rollout prerequisites. Block promotion on failure. |
| Post-deployment/runtime check | Correctness can only be observed in the running system | Run health and synthetic checks, canary analysis, SLO/error-budget gates, and rollback triggers. |

Place one check in multiple layers when each layer has a distinct purpose: early feedback, shared-history enforcement, integration safety, and production validation are complementary. Avoid duplicate local runs that add latency without catching a different failure class.

Use these defaults when the check characteristics leave the choice open:

- **Tight:** prefer editor/file-change, a post-file agent event, or pre-commit for checks that finish in seconds and have stable local dependencies.
- **Preventive:** use a pre-tool agent event for dangerous actions and a pre-commit security check for dangerous content; neither replaces CI or platform security controls.
- **Medium:** prefer pre-push or an agent turn/settled event when a repository-wide run has predictable, acceptable cost.
- **Heavy:** use blocking CI for long, networked, service-backed, or platform-matrix work; quarantine known-flaky checks from required gates until reliability is restored.
- **Integration:** require pull-request CI and, when concurrent merges can invalidate results, a protected branch or merge queue.
- **Release:** put artifact- and environment-specific checks at deployment, then use post-deployment evidence for canary continuation or rollback.
- **Security:** run a maintained secret scan in CI and, when available, pre-commit. Treat Gitleaks as the baseline scanner; use a broader scanner only when its added coverage justifies its cost and setup.

Respect a repository's existing time budgets and hook framework over the table. Measure an unfamiliar command once when practical rather than guessing its tier.

## 4. Wire and document

Configure only the selected surfaces. Preserve existing hook entries and CI jobs; extend their native configuration instead of replacing it. Pin or lock added dependencies according to the repository's package-manager practice.

For each installed layer, make failures actionable: name the command that failed and the command that reproduces it locally. Keep bypasses limited to the native mechanism and document them only when the repository exposes one.

Update contributor documentation only when contributors need a new installation, enablement, or recovery step. Do not restate commands already discoverable from the project configuration.

## 5. Prove the loop

Run the canonical command and every affected local runner. Validate agent-hook payload and decision behavior, Git hooks, CI syntax, merge rules, and deployment configuration with the repository's available tools; when feasible, exercise each workflow or its equivalent command. Confirm that:

- the intended violation fails at every selected enforcement layer;
- a compliant input succeeds;
- validation-only runners leave the worktree unchanged; and
- no unrelated hook, job, or platform configuration was replaced.

Report the canonical command, each selected layer and its purpose, user decisions obtained, files changed, and verification evidence. Name any layer intentionally omitted and the observed constraint.
