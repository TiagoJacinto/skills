---
name: gherkin
description: 'Shared Gherkin scenario rules. Use when authoring or reviewing .feature scenarios, including through ATDD or a custom Gherkin profile.'
---

# Gherkin scenario structure

These rules apply to ordinary Gherkin and custom profiles. A profile defines its additional step syntax separately.

- Use ordered phases: preconditions (`Given`) → one action (`When`) → observable outcomes (`Then`). Once a phase ends, continue forward rather than returning to it.
- Write exactly one action per scenario. Split a flow that needs another action into separate scenarios.
- Use `And` and `But` to continue the current phase: additional preconditions under `Given`, or additional outcomes under `Then`.
- Distinguish state from input. State existed before the action and is independently observable; describe it under `Given`. Input is supplied for the action; describe it under `When`. Requests, commands, options, and expected values are inputs unless they were persisted before the action.

```gherkin
Scenario: Remove one stored variable
  Given APP_TOKEN is stored
  And SERVICE_KEY is stored
  When I remove APP_TOKEN
  Then APP_TOKEN is absent
  But SERVICE_KEY remains stored
```
