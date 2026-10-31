---
name: idiot-boss
description: Run the idiot-boss orchestration approach when a cheaper coordinator handles logistics and light QA while stronger models own planning, design, and technical judgment.
---

# Idiot-boss orchestration

The coordinator owns glue and light QA. Strong models own the decisions and do the substantive work directly. In design, the desired taste lives in the designer's weights: preserve its room to interpret the brief.

## Establish the plan

Use the existing plan supplied by the user or invoking workflow, including its model assignments, input boundaries, and completion criteria. For ambitious work without a plan, give a strong model the original request and source artifacts. Ask it to produce the steps, dependencies, and observable completion criteria the coordinator needs to follow the plan.

Give the coordinator explicit operational instructions: which step to dispatch next, its inputs, how completion is checked, and when to return to the planner. A complex plan or hard-to-test product warrants a more capable coordinator; use the selected orchestration configuration.

## Dispatch the work

For each ready step, send its strong worker:

- The user's original brief and relevant source artifacts, including target screenshots or specs.
- The step's objective, dependencies, and constraints from the user or plan.
- The expected artifact and evidence of completion.

Frame the problem and desired outcome. Leave design and technical solutions to the worker. Preserve user requirements verbatim where paraphrasing could change them; give the worker direct access to the sources instead of a chain of summaries.

The coordinator follows the plan, dispatches ready work, tracks dependencies and artifacts, and runs the prescribed checks. Questions requiring design, architecture, technical tradeoffs, or changes to the plan go to the responsible strong model with the relevant evidence. The coordinator relays its decision and continues.

## Check and repair

Use observable evidence for light QA: prescribed commands and their results, missing artifacts, broken interactions, or visible overlap. Send failures and screenshots back as observations against the brief. The strong worker chooses the repair. Subjective design quality and subtle correctness questions go to a strong evaluator.

Before retrying a disappointing result, inspect the prompt the worker actually received. Remove solutions invented by the coordinator and restore missing source material. Keep decisions and updated artifacts available directly to subsequent workers so the goal survives handoffs.

If the same failure returns after a repair, route the evidence to a strong model for diagnosis or replanning. Report a concrete unresolved blocker when progress requires unavailable input or capability.

Before reporting on a worker, confirm its state from the host's lifecycle evidence. When a worker stops without a recap, such as after an error or usage limit, report what happened.

Finish when the plan's completion criteria are met. Report the artifacts and verification evidence, including any evaluation that remains unresolved.
