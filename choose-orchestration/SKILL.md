---
name: choose-orchestration
description: Choose who plans, coordinates, implements, and reviews when deciding whether to use subagents or how to divide work across models.
---

# Choose orchestration

Allocate judgment first, then reduce the cost of the remaining work. Treat model size as a routing heuristic; use demonstrated capability for the task, especially design taste. Preserve the user's model choices and any workflow they already selected.

## Decide

Use the request and available context to answer these questions. Ask the user only when an unresolved priority would change the choice.

1. **Quality or correctness above all else?** Use a strong model for planning, coordination, implementation, and review. Delegate only where separation adds value.
2. **Too little work to justify handoffs?** Have one capable model finish it directly.
3. **Ambitious work with multiple steps?** Give a strong model the original request and source artifacts to create the plan. A cheaper coordinator can execute that plan and dispatch strong models to implement its steps. Planning changes return to the strong model.
4. **Complex plan or hard-to-test result?** Use a coordinator one or two capability tiers above the smallest model. If evaluating success itself requires expert judgment, assign that evaluation to a strong model.
5. **Otherwise, clear steps with observable outcomes?** A small coordinator can handle dispatch, bookkeeping, and light QA; strong workers own work requiring judgment.

For design, assign the actual design work to the model whose taste the user wants. Save tokens by moving logistics off its plate. A coordinator's detailed aesthetic instructions cannot substitute for the designer's judgment.

## Make the choice concrete

Give a short recommendation naming who plans, coordinates, implements, and evaluates, with the reason for the split. One model may fill several roles. Separate the model choice from effort: low effort can suit a rough creative take; more demanding planning, execution, or verification may warrant more effort without changing whose taste is wanted.

When naming models for a run, discover the host's available models and supported effort settings. Use the user's preferences and task evidence to assign roles. Report an unavailable requested model rather than silently substituting another. This skill chooses a configuration; the host's orchestration instructions own dispatch mechanics.

When recommending a configuration only, stop after the recommendation. When execution is also requested, apply the choice within the existing authorization. For a cheaper coordinator with strong workers, call the Skill tool with "idiot-boss"; if the host has no Skill tool, read [its instructions](../idiot-boss/SKILL.md).

A role assignment does not change the current agent's model. Use the host's supported handoff mechanism if the lead must change; otherwise state which role remains on the current model.

## Reconsider from evidence

When a delegated task fails with a rate-limit or quota error, send that provider no more work in this run. Tell the user which tasks stopped, and offer to reassign them to an available model.

If results degrade, inspect the actual worker briefs first. Restore the original request and artifacts, and remove coordinator-invented solutions. If plan following or objective checking still fails, strengthen the coordinator. If design, implementation, or expert evaluation fails, revisit the model owning that judgment.
