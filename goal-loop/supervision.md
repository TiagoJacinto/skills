# Supervision

Read this when drafting, setting, or updating a goal that has a supervisor.

The **supervisor** is a separate session that runs goal-supervise against the
goal session. It keeps the goal agent working until `Complete when` holds and
resolves its blockers itself, so the run reaches the user only when nothing
within the supervisor's authority can unblock it. It is a coordinator: it
delegates fixes to the workers its rows in `Coordination` name.

## Before start

- Write the full contract to its file, as in Length limit step 1, even when the
  goal text fits inline. The goal agent and the supervisor share it, and the
  supervisor logs its interventions there. Save the final goal text there
  under `Goal text`; the supervisor sets the goal from it.
- The supervisor must read the goal session and send it messages. Check that
  the chosen harnesses allow both, such as T3 threads through `t3_thread_read`
  and `t3_thread_send`. Where the supervisor can only read, each message
  becomes a relay through the user, which is a human checkpoint; prefer placing
  both sessions where it can message (see Capabilities).

## Supervisor goal

The supervisor runs as its own goal loop in its execution harness, so it keeps
going across turns and compactions. Apply that harness's goal rules, such as
the blocked-exit clause in [`claude-code-goal.md`](claude-code-goal.md) for
Claude Code `/goal`.

```text
Objective: Start the goal loop in <goal session reference>, then keep it working until its goal is complete, resolving its blockers yourself.
Supervise: Call the Skill tool with "goal-supervise" before acting and after every resume, and follow it for <goal session reference>.
Contract: <absolute contract path>. Read it in full before acting and after every resume. Its Supervisor field defines your authority and coordination; its Never and Hard stop bind you too.
Complete when: you have run the contract's Validate checks yourself and they show its Complete when holds.
```

## Start

This session starts only the supervisor; the supervisor starts the goal loop,
so it is watching from the loop's first turn.

1. **Create the goal session** with the harness, model, and effort the
   contract names, without starting its goal. Use this authoring session
   instead only when it holds state the contract cannot carry, such as a login
   made inside it.
2. **Start the supervisor** with the harness, model, and effort its
   `Supervisor` field names, and its goal as the first message through that
   harness's goal start, such as `/goal <supervisor goal text>` for Claude
   Code. Use a tool that starts a session there, such as `t3_thread_launch`.
   When no tool here can start it, give the user the exact launch command and
   goal text to run in a new session.
3. **Confirm** the supervisor's goal is active. Record its session reference in
   the `Supervisor` field. When this session is the goal session, end this
   turn; the supervisor sets the goal here once the turn ends.

## Updates

When the contract changes, send the supervisor a message naming the change; it
rereads the contract. The supervisor ends when the goal completes.
