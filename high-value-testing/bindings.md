# Scenario bindings

Use these rules when implementing approved scenarios, alongside the project's framework guidance. Apply every applicable rule. A binding is complete only when every applicable item in the completion check passes.

## Public seams

Keep scenarios domain-level. Put interface-specific setup, invocation, and assertions in high value test bindings. Bind each action and observation through the seams agreed for the scenario.

Apply the collaborator requirements in [High-value testing](SKILL.md#collaborators).

## Bind the example values

Treat each scenario as an executable example. Capture each value written in a step. Use it to arrange state, invoke the action, or derive the expected observation. A wildcard such as `{any}` that swallows structured values without using them does not bind the example. Hard-coded fixtures or assertions that repeat the feature values also do not bind the example.

For a structured domain value, capture its primitive fields with typed expressions or define one typed domain parameter. A binding is value-faithful when a change to a feature value changes what the high value test arranges, invokes, or expects, with no matching callback edit.

## Completion check

A binding is complete when:

- one reusable expression matches the scenario step;
- each example value is captured with its intended type;
- each captured value controls setup, invocation, or an expected observation;
- changing a feature value requires no matching hard-coded callback edit;
- the action enters through the agreed action seam;
- assertions observe only through the agreed observation seams;
- the specialized collaborator requirements are met; and
- execution reaches domain behavior instead of failing in test plumbing.
