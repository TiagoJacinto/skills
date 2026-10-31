# Execution harness: Claude Code `/goal`

Read this when the loop will run through Claude Code `/goal`, regardless of
which harness authors the goal. See the
[Claude Code goal documentation](https://code.claude.com/docs/en/goal).

## Start

After the contract is finalized and saved, start the loop in a fresh Claude
Code session with `/goal <final goal text>`. In a reused session, run
`/compact` first.

## Blocked exit

Include this clause in the goal condition. Keep it inline even when the full
contract moves to a file: the evaluator reads the condition and conversation,
not the contract file independently.

```text
Blocked exit: if every remaining step needs a user action, approval, or input and no authorized independent work remains, post one final message starting with BLOCKED: that names each required action, then stop. That message satisfies this condition.
```

Treat this as an alternative terminal condition alongside `Complete when`.
Before taking it, finish useful authorized independent work and resolve running
workers that can still advance the goal. Save verified progress and the required
user actions in the durable contract when one exists. Begin the final response
with `BLOCKED:` and state the unresolved actions without claiming the objective
is complete.

This is a model-evaluated mitigation, not a guaranteed pause. When it works, the
evaluator clears the goal and records it as achieved even though the task
remains incomplete. After the dependency is resolved, the user re-sets `/goal`
with the same condition and current contract. If repetition continues, the user
interrupts the run and uses `/goal clear` to remove it.

This clause applies only to Claude Code `/goal`. It does not authorize marking
an unfinished objective complete through another runtime's goal tools; use that
runtime's actual blocked or pause control when available.
