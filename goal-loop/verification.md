# Project verification

Read this when the project has no verification, or its verification has no
check for the goal's outcome.

A project's **verification** lets the agent check its own work and keep going
until it succeeds, with no user in the loop. It is a scripted way to drive the
real app the way a user does and capture proof. It lives in the repository at
`docs/agents/verification/` (`.agents/verification/` when the repository has no
`docs/agents/`), so it changes with the code and every goal and agent on the
project reuses it. Add a pointer to it in the repository's `AGENTS.md`, beside
its other agent docs. Write it for an agent that reads it cold, mid-task.
Creating it changes the repository, so follow the repository's branch and pull
request workflow.

## Layout

- `README.md`: the Launch, Doctor, Drive, Evidence, and Cleanup sections.
- `features/README.md`: the feature map index.
- `features/<feature>.md`: one file per user-facing feature.
- `scripts/`: executable helpers, each invocation shown in `README.md`.

Create only what the goal's outcome needs; extend the rest as later goals
reach other features.

## README sections

Answer each section from the codebase; ask the user only what you cannot
observe. Prefer the repository's own commands and harnesses (dev scripts,
Playwright specs, CLI entry points, HTTP endpoints) over generic recipes.

- **Launch:** the exact command that starts the app from an empty data
  directory, including migrations and seed data, and how to tell it is usable,
  not merely answering. State whether two instances can run side by side.
- **Doctor:** one read-only check that the instance is worth driving: process
  up, right build, port owned by this run, auth valid. Run it before the first
  drive and after any surprising result.
- **Drive:** real selectors, commands, and routes from this repository. Prefer
  stable handles such as ARIA labels, data attributes, and route paths.
- **Evidence:** what to capture, saved outside the repository at
  `~/.agents/projects/<project>/goals/<goal-slug>/evidence/`. Proof exercises
  the real user path, captures the action and the resulting state, and checks
  side effects such as files, rows, and messages. Observe what a dry-run
  actually skips rather than trusting its name.
- **Cleanup:** stop only what this run started. Evidence survives cleanup.

## Feature files

Each feature file has four sections: `Sub-features`, `How to get to it (user
POV)`, `Driving it`, and `Gotchas`, and names the observable end state that
proves the feature works. When seed data lacks a precondition a journey needs,
the journey reports failure and the reason goes in `Gotchas`.

## Prove it

A check closes the loop when it runs without the user, returns a clear pass or
fail with the reason for a failure, and is cheap enough to repeat many times
per task. A step that needs the user is an open loop: record it as a human
checkpoint, not as completion evidence.

Run the verification once end to end before setting the goal: launch, doctor,
drive the feature the goal targets, capture evidence, clean up, and confirm the
evidence still exists. For new behavior, the check goes red now; it turns green
only when the outcome holds. Name the check in the goal's `Validate` field and
the verification `README.md` in `Read first`.
