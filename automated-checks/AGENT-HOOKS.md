# Coding-agent hook layers

Consult this reference when an automated check could run inside Pi, Claude Code, Codex, or another coding agent. Inspect the installed agent's documentation and existing configuration before implementation: event names, payloads, blocking semantics, trust, and scope change between versions.

Agent hooks provide earlier feedback than Git hooks, but only for work performed through that agent. Pair checks that protect shared history with a repository-owned Git or CI layer.

## Select by lifecycle boundary

| Boundary | Use for | Blocking policy | Pi | Claude Code | Codex |
| --- | --- | --- | --- | --- | --- |
| Project/session setup | Validate prerequisites, load policy, start watchers, initialize a worktree | Block only when continuing would be unsafe or invalid | `project_trust`, `session_start`, `resources_discover` | `Setup`, `SessionStart`, `InstructionsLoaded`, `WorktreeCreate` | `SessionStart` |
| User input | Detect secrets or prohibited input; attach project-specific guidance | Block a clear policy violation; otherwise add context | `input`, `before_agent_start` | `UserPromptSubmit`, `UserPromptExpansion` | `UserPromptSubmit` |
| Before tool execution | Deny destructive commands, protected-path writes, unsafe network access, or policy violations | Fail closed for high-confidence safety rules; provide an actionable reason | `tool_call` | `PreToolUse`, `PermissionRequest`, `PermissionDenied` | `PreToolUse`, `PermissionRequest` |
| After one tool | Format a changed file, run narrow lint/type checks, inspect command output, record provenance | A fixer may modify files only when explicitly intended; report validation failures immediately | `tool_result`, `tool_execution_end` | `PostToolUse`, `PostToolUseFailure`, `FileChanged` | `PostToolUse` |
| After a tool batch or turn | Deduplicate per-file work and run checks that need the complete batch | Block continuation only when the agent can repair the failure | `turn_end` | `PostToolBatch`, `Stop`, `StopFailure` | `Stop` |
| Subagent/task completion | Validate delegated output before accepting it into the parent task | Return the failure to the responsible agent with a reproduction command | Use the subagent runner's completion contract; `agent_end` is session-agent lifecycle, not a dedicated child hook | `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle` | `SubagentStart`, `SubagentStop` |
| Agent settled | Run repository-scope checks once no automatic continuation remains | Prefer feedback or a repair turn; keep authoritative enforcement in Git/CI | `agent_settled` | `Stop` | `Stop` |
| Environment/config change | Revalidate when instructions, config, cwd, roots, or watched files change | Block only when the new state violates an invariant | `resources_discover`; use an explicit watcher started at `session_start` for files | `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged` | No general equivalent; use tool hooks or session checks |
| Context compaction | Preserve or restore check policy and required context | Add context; this is not a code-quality gate | `session_before_compact`, `session_compact` | `PreCompact`, `PostCompact` | `PreCompact`, `PostCompact`; compact also re-fires `SessionStart` |
| Session/worktree teardown | Flush audit data, stop watchers, clean temporary state | Keep cleanup bounded; surface failures without trapping exit | `session_shutdown` | `SessionEnd`, `WorktreeRemove` | `SessionEnd` |
| Notification/observability | Emit metrics, desktop notices, audit records, or status | Non-blocking | message/tool lifecycle events | `Notification`, `MessageDisplay` | Use hook output or external notification integration |

## Agent-specific rules

### Pi

- Extensions live in project-local `.pi/extensions/` or global `~/.pi/agent/extensions/`. Ask before choosing global scope.
- `tool_call` can mutate input or return `{ block: true, reason, terminate? }`. Handler errors block the tool, so catch internal failures when the policy should fail open.
- `tool_result` can patch the result but cannot undo side effects. Use `tool_execution_end` for observation and `tool_result` when the result itself must change.
- File-change checks require observing `write`/`edit` tool calls or starting a filesystem watcher at `session_start`; Pi has no native `FileChanged` event.
- Use `agent_settled`, rather than `agent_end`, for a once-after-completion check because retries, compaction, or queued follow-ups may still run after `agent_end`.
- Close watchers, subprocesses, and sockets in an idempotent `session_shutdown` handler.

### Claude Code

- Hooks may be commands, HTTP handlers, prompts, agents, or MCP tools. Choose commands for deterministic checks and reserve model handlers for judgments that cannot be expressed deterministically.
- Tool hooks can match the tool and arguments. Use `PreToolUse` for prevention, `PermissionRequest` for approval policy, `PostToolUse` for successful execution, and `PostToolUseFailure` for failures.
- `FileChanged` is the tightest native file watcher. `PostToolBatch` avoids repeating a repository check after each parallel tool.
- `Stop` means a response completed; guard against a stop-hook loop when requesting another repair turn.
- Hooks defined in settings, managed policy, plugins, skills, and subagents have different scopes and trust behavior. Preserve existing entries and use project scope for repository policy unless the user chooses global scope.

### Codex

- Hooks live in `hooks.json` or inline `config.toml` tables at active configuration layers. Non-managed command hooks require review and trust; changing a hook definition invalidates its prior trust.
- `PreToolUse` covers Bash, `apply_patch`, MCP tools, and most local function tools, but hosted tools and specialized paths may bypass it. Treat it as a guardrail rather than a security boundary.
- Matching command hooks launch concurrently. Keep independent hooks independent; combine checks that require ordering into one handler.
- Use `PermissionRequest` only for operations that already need approval. Use `PreToolUse` for policy that applies regardless of approval mode.
- `PostToolUse` cannot undo side effects. `Stop` can request another repair turn, but must detect that it already ran to avoid a loop.
- Codex currently lacks general file/config/cwd-change events; approximate them through `PostToolUse`, `Stop`, or a watcher managed by `SessionStart`/`SessionEnd`.

## Reliability rules

1. Put the check implementation in a canonical repository command or script; keep agent adapters thin.
2. Scope per-file hooks to the files actually changed. Coalesce parallel tool calls before repository-wide work.
3. Give each failure a reason and a command the agent or developer can run to reproduce it.
4. Set explicit timeouts. Keep pre-tool checks deterministic and fast; move expensive work to turn-end, Git, or CI.
5. Choose fail-closed only for high-confidence safety or integrity rules. Fail open with a visible warning for optional feedback and infrastructure faults.
6. Test allow, deny/failure, malformed input, timeout, concurrent invocation, subagent behavior, and teardown.

## Primary references

- Pi: `@earendil-works/pi-coding-agent/docs/extensions.md`
- Claude Code: <https://docs.anthropic.com/en/docs/claude-code/hooks>
- Codex: <https://developers.openai.com/codex/hooks>
