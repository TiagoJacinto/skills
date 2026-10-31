---
name: goal-loop
description: >-
  Create or revise a long-running agent goal: agree on the outcome, execution
  authority, and human dependencies before starting or changing the loop. Use
  when the user asks to create a goal, update an existing goal, or draft a goal
  prompt for `/goal` or a persistent autonomous run.
---

# Goal authoring

A goal is an execution contract, not just a finish line. Agree on what the agent
may decide and do, then carry that agreement in the durable goal so execution
can continue without relying on this skill remaining in context.

Each loop has a **supervisor**: a second session that keeps the goal agent
working and resolves its blockers, so the run reaches the user only when
nothing else can unblock it. Aim for a run with no human checkpoints.

Use the creation branch for a new goal and the update branch for an existing
one. Drafting a goal is not authorization to start it.

The **execution harness** is the harness that will run and coordinate the loop.
It may differ from the harness authoring the goal. Base the goal text, model
selection, commands, lifecycle rules, and handoff instructions on the execution
harness. Identify it from the request and established context, or recommend
one from the capabilities the work needs (see Capabilities); if still unclear,
ask which harness will run the loop before finalizing the output.

## Create a goal

1. **Inspect.** Read the task, relevant project instructions, and enough of the
   environment to identify the completion evidence and likely dependencies.
   Reuse decisions and approvals already established in the conversation.
   Inspect any current goal before proposing a replacement. Identify the
   execution harness and its supported goal controls. Read the project's
   verification, which its project instructions point to; `<project>` in goal
   paths is the repository name.
2. **Show the span.** Present the proposed goal using the scope review below
   before finalizing its authority. Ask about sizing when the boundary is
   unsettled; preserve a boundary the user has already chosen.
3. **Resolve material uncertainty.** Ask focused questions directly in the
   conversation, one decision at a time. Ask only where the answer changes the
   execution contract; use the decision areas below, not a fixed questionnaire.
   Name the concrete action or trade-off, its limits, and your recommendation
   when useful. Wait for the answer before treating that decision as settled.
   Settle now what the run would otherwise stop to ask.
4. **Check feasibility.** Identify a plausible path within the agreed authority
   and the fewest human checkpoints it needs. Establish verification readiness
   now: locate and run the outcome check; if it is missing or does not cover the
   outcome, read [`verification.md`](verification.md) and follow it before
   proceeding. Record the exact command, observed result, and evidence path.
   For new behavior, establish an expected failure that demonstrates the missing
   behavior; distinguish it from a broken test setup. A plan for the future loop
   to create verification does not satisfy this gate. Distinguish missing
   permission from unavailable evidence, access, or capability; a capability
   another available harness provides is a harness choice, not a blocker. If a
   prerequisite cannot be met, leave the goal unstarted and label any saved
   contract **Draft — not ready to start**, naming the unmet prerequisite.
   Present the actual choice: supply it or explicitly revise the scope or
   approach.
   Give start instructions only after this gate passes. Permission alone cannot
   manufacture evidence.
5. **Confirm the agreement.** Summarize the outcome, the three authority tiers,
   the execution harness, the coordination approach and per-concern
   assignments for the lead and the supervisor, the capability each harness
   choice meets, the `Ask first` entries the supervisor may grant, any model
   selection command the user must run there first, human checkpoints, and
   material limits. Request confirmation only for
   proposed choices not already approved. This step is done when those
   decisions are settled and remaining human dependencies are explicit—not
   when every possible detail is specified.
6. **Draft and set.** Use the contract below, then apply its length limit. When
   the execution harness is Claude Code `/goal`, read
   [`claude-code-goal.md`](claude-code-goal.md) before drafting: it adds a
   required clause and the start commands. When the goal has a supervisor,
   read [`supervision.md`](supervision.md) before drafting: it adds the
   contract file and the supervisor's goal, and the supervisor, not this
   session, starts the loop. If the user requested only a draft, return the
   goal text without a `/goal` prefix. If they requested creation, use an
   available tool that creates the goal in the execution harness after
   resolving the agreement. If that harness cannot be controlled here, give
   the user its exact start instructions. Replace an unfinished goal only when
   replacement was requested or approved.

   The loop starts in a fresh session, seeded only by the goal text and its
   contract, with the harness, model, and effort the contract names. The
   contract carries every decision the loop needs, so a fresh start also tests
   that it is complete. Reuse this authoring session only when it holds state
   the contract cannot carry, such as a login made inside it, and then compact
   it with the execution harness's command before the goal starts. Compact
   rather than clear: in Claude Code, `/clear` starts a new session ID, which a
   supervisor watching the old one loses, and a T3 thread resumes the old,
   uncleared session after its process restarts.

### Scope review

Show the **goal span** first: its starting state or assumed prerequisites, the
work included within its boundaries, and the observable finish. Name relevant
exclusions when needed to clarify the boundary. Make the included work concrete
enough for the user to judge its size without prescribing implementation detail.

Add a **surrounding span** only where it helps explain that boundary. Label
surrounding work as already agreed, a prerequisite, or a possible follow-up.
Suggestions remain suggestions; preserve the established scope and label
uncertainty rather than inventing a larger project or complete roadmap. An
inferred prerequisite remains unconfirmed; identifying it neither includes it
in the goal nor authorizes work on it. Resolve material dependencies during
feasibility review.

Recommend whether to keep, merge, split, or use an ordinary task instead of a
loop. Keep checkpoints together when they advance one coherent outcome within
the same authority. Split at distinct outcome or execution boundaries, not
merely at context-window boundaries. An unresolved decision may be a human
checkpoint within one goal rather than a reason to split it.
When splitting agreed work, make clear which part this goal completes and what
remains of the overall request. Ask: “Does this span feel right, or should we
make it smaller or larger?” when a sizing decision is needed.

### Decision areas

- **Outcome:** What result and evidence establish completion? The goal needs
  a closed loop: a check the agent runs without the user, with a clear pass or
  fail, cheap enough to repeat. Base the evidence on the project's
  verification and apply the verification-readiness gate in step 4.
  When completion is a measured number, agree on the baseline, the measurement
  command, and how a result is shown to come from the change rather than noise
  or setup.
- **Reach:** Which stages are included: implementation, deployment, live
  validation, or a narrower endpoint?
- **Authority:** Sort every material action and decision into three tiers:
  what the agent **can do** independently, what it **can do after asking**
  (each time, or once for a named target), and what it **must never do**, even
  when it seems needed. Bind each entry to its targets and limits. Name any hard
  stop: a condition that halts the dependent work until the user responds.
  Place reversible actions within the span in **can do** by default; reserve
  **can do after asking** for irreversible or outward-facing actions,
  credentials, and choices of taste the user has not delegated. For each
  `Ask first` entry, recommend whether the supervisor may grant it, so the run
  reaches the user only for the entries the user keeps.
- **Coordination:** The loop has two coordinators: the goal's lead and its
  supervisor. List the concerns each will handle: for the lead, derived from
  the span, the kinds of work it will do; for the supervisor, derived from the
  blockers that work is likely to meet. Discover the harnesses, models, and
  thinking-effort settings available, and the named agents each harness
  defines, such as Claude Code subagents. For each coordinator, call the Skill
  tool with "choose-orchestration" to pick the approach; recommend one named
  approach, such as a single lead, or "idiot-boss" for a cheaper coordinator
  with strong workers, and give its reason. Then show a table with one row per
  concern, grouped by coordinator: the recommended harness, model or named
  agent, and effort, each passing Capabilities. Ask the user to confirm or
  change each row; their choices override the recommendation. Also settle what
  may run in parallel or in an isolated worktree, and how delegated results
  are checked and integrated.
- **Capabilities:** For each coordinator and concern, match what the work
  needs against what its harness, model, and effort together provide: tools
  and MCP servers, network reach, sandbox and permissions, the data it can
  handle safely, goal and session controls, and context size. Discover the
  harnesses installed here and read their own documentation; a launcher or
  wrapper can change what a base harness provides. When the authoring harness
  lacks a need that another available harness meets, recommend that harness
  and name the need it meets. A need no available harness meets is a
  capability dependency for step 4.
- **Supervision:** Settle the supervisor's harness, lead model, and effort,
  its coordination, the `Ask first` entries it may grant, and how it reads and
  messages the goal session. Recommend supervision for every loop; omit it
  only when the user declines.
- **Lead model:** Select the model for the execution harness's coordinating
  session, the coordination concern's row, independently of the model
  authoring the goal. A goal cannot change
  the model of the session that runs it.
  When the chosen approach needs a different lead model, give the user the exact
  command supported by that harness to run before setting the goal, and record
  it in the contract. Wait for the user to run it before setting the goal.
- **Human dependencies:** Which inputs, access, or actions must the user supply?
  For each, prefer in order: the user supplies it before the start; a harness,
  tool, or authority grant removes the need (see Capabilities); the supervisor
  resolves it during the run. Keep a human checkpoint only where none of these
  can. What independent work can advance while each remaining one is pending?
- **Discretion:** Which alternative approaches and trade-offs may the agent
  choose if its first approach fails? Which choices should return to the user?
- **Limits:** Which cost, time, scope, and risk limits matter to this task?

Preserve higher-priority safety requirements regardless of the execution
agreement.

## Update a goal

1. **Read current state.** Inspect the objective, status, completion evidence,
   approvals, and blocker. Separate verified progress from earlier claims.
2. **Identify the delta.** Determine whether the request changes the outcome,
   authority, constraints, or only progress. Ask about newly unresolved decisions
   using the creation branch's decision areas. Preserve valid approvals and
   completed work; recheck them when a changed target or condition affects them.
   If the boundary changes, show the revised span using the scope review above.
3. **Resolve feasibility changes.** If the revised path needs unavailable
   evidence or capability, present that dependency rather than repeatedly asking
   for an approval that cannot resolve it.
4. **Persist the agreed delta.** Use the exposed tools or supported commands.
   A progress update need not replace the objective. When replacement is needed,
   carry forward applicable requirements, approvals, and evidence pointers.
   Setting or resuming a goal grants no additional execution authority. When
   the goal has a supervisor, send it a message naming the change.

## Durable contract

Keep the goal compact. Name each document that already defines part of the
task under `Read first`, with when to read it, and refer to it instead of
restating it. The goal carries only what those documents lack: authority,
coordination, and completion evidence. Keep permissions and execution policy
explicit in the goal, or in the contract file when the length limit applies.
Use exact paths and validation commands discovered from its environment rather
than guessed commands.

```text
Objective: <one concrete outcome and included stages>
Execution harness: <harness that will run and coordinate this loop>
Span: <starting state, included work, and relevant exclusions>
Read first: <task sources and relevant instructions>
Can do: <actions and decisions taken without asking, with targets, limits,
  and alternatives the agent may choose>
Ask first: <actions allowed only after approval, whether approval is per use
  or once per target, and whether the supervisor may grant it>
Never: <actions prohibited even when they seem needed>
Hard stop: <conditions that halt dependent work until the user responds>
Coordination: <approach and reason; per concern, the harness, model or named
  agent, and effort the user confirmed; parallel or isolated work; and how
  delegated results are verified>
Supervisor: <session reference once started; harness, model, and effort; its
  approach and per-concern rows; how it reads and messages the goal session>
Lead model: <model the coordinating session must run, and its harness's model
  selection command when a change is needed there>
Constraints: <task-specific invariants and exclusions>
Human checkpoints: <required decisions, inputs, or actions and when needed>
Validate: <commands and other evidence required for progress and completion>
Document: Write concise, targeted documentation for changes.
Progress: <verified completed work and evidence pointers, when applicable>
Execution policy: Continue meaningful work within the approved scope. Take a
  reversible action the contract does not list when it serves the objective
  within the span, and report it with progress. When one dependency is
  blocked, advance independent work that is safe under the current state. An
  Ask first action waits only for its own approval; other authorized work
  continues. Messages beginning SUPERVISOR: carry the authority the
  Supervisor field and Ask first give the supervisor, no more. Keep progress
  and approvals current. Before blocking, check
  for useful authorized work that remains. If none remains, identify whether
  the dependency is permission, human action, evidence, access, or capability;
  ask one specific question directly in the conversation when an answer can
  resolve it. State the required action when a question cannot resolve it.
  Record answers within their approved scope and follow the runtime's actual
  resumption requirements.
Complete when: <observable end state, with each requirement backed by evidence>
```

Adapt the contract to the task; omit empty fields. Carry its execution policy
into each goal rather than relying on a past skill load. State any hard safety
boundary that requires an immediate stop, including cases where independent
work is also prohibited. Keep routine progress reports brief; they do not
require a reply.

Completion evidence must cover the requested outcome, not merely passing unit
tests. Do not delete, skip, weaken, or narrow tests to make the goal pass. Scope
or acceptance changes require the user's agreement. New ADRs require explicit
approval.

### Length limit

The goal text you set or return is at most 4000 characters, whatever the
runtime allows. Measure the final text, for example with `wc -m`.

When the full contract is longer:

1. Write the full contract to a Markdown file at a durable path that every
   session pursuing the goal can read. Default:
   `~/.agents/projects/<project>/goals/<goal-slug>.md`. Ask the user for a
   location when the goal may run where that path is unavailable, such as a
   cloud session or another machine.
2. Set a short goal that keeps `Objective`, a pointer line, `Never`,
   `Hard stop`, and `Complete when` inline, plus the blocked-exit clause when
   the execution harness is Claude Code `/goal`. Pointer line:
   `Contract: Read <absolute path> in full before acting and after every resume.
   It defines Can do, Ask first, Coordination, Supervisor, and checkpoints.
   Act only within it.`
3. Measure the short goal again. If it still exceeds 4000 characters, shorten
   the inline fields; the file stays complete.
4. Give the user the file path. Keep later progress and approval updates in the
   file; replace the short goal only when its inline fields change.

## Runtime controls

Use the execution harness's supported tools and documentation for creation,
updates, budgets, pause, and resume. Authentication, headless support, objective
limits, and lifecycle behavior differ between agents; do not infer them from
another agent's `/goal` feature.

Approval and resumption are distinct. If the runtime requires an explicit resume
command after a blocker is resolved, give the user that exact command together
with the approval question. A conversational answer does not automatically
reactivate a blocked goal unless the runtime implements that behavior. Provider
limits and aborted turns can stop pursuit regardless of task permissions.
