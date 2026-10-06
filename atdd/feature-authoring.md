# Feature authoring

Use this reference when deciding scenario coverage or writing Gherkin.

Before authoring or reviewing scenarios, call the Skill tool with "gherkin" for shared scenario structure and state-versus-input rules.

## Scenario coverage

Update scenarios when the task explicitly changes scenarios; adds, removes, or changes observable product behavior or an actor-facing outcome; changes a user flow, acceptance criterion, validation rule, permission, or visible error; or fixes behavior missing from or inaccurately represented by existing scenarios. Each requested behavior change should map to a scenario change or be covered accurately by an existing scenario.

Keep existing scenarios unchanged for implementation-only refactors, documentation, formatting, tooling, test infrastructure, presentation-only adjustments without changed interaction or meaning, and behavior already specified accurately and completely. If the need for a scenario update remains genuinely ambiguous, ask: **"Is a BDD scenario update needed for this change?"**

## Feature conventions and domain wording

Inspect feature-file locations and naming, relevant scenarios, and existing step wording to find domain phrases that can be reused. Consult project configuration when needed to identify the feature location or which step wording applies to the feature area. Follow the nearest relevant feature-file conventions. Ask the user only when multiple authoring conventions remain equally plausible after inspection.

## Scenario rules

Apply these by default; follow explicit user direction when it differs for the affected scenarios.

- Specify a complete actor-facing flow ending in a meaningful observable outcome, using the fewest scenarios that completely cover the requested behavior.
- Reuse project domain terms and existing step wording where meanings match. Prefer business-aware steps over UI mechanics or generic, heavily parameterized steps.
- Consolidate repeated values of one kind into a data table when that makes the behavior clearer.
- Add a one- or two-sentence feature description immediately below each `Feature:` line, using concrete domain language. Append new scenarios after existing ones unless the user requests another location.
- Keep framework APIs, drivers, selectors, fixtures, and implementation details out of Gherkin.
- In `playwright-bdd`, let interactions establish availability: when a scenario clicks, fills, selects, or otherwise uses an element, add a separate visibility, existence, or enabled assertion only if availability itself is a meaningful precondition or outcome.

Example:

```gherkin
Feature: Shopping cart
  Customers can collect products they intend to buy and review the current cart contents.

  Scenario: Add an available product to the cart
    Given the product "banana" is available
    And the customer's cart is empty
    When the customer adds "banana" to the cart
    Then the cart contains "banana"
    And the cart contains 1 product
```

## Approval and test path

Show the exact proposed Gherkin before implementing changed scenarios: name each target feature-file path, show edits to existing content as a unified diff, and show entirely new content in a `gherkin` block. Ask **"Approve the proposed feature-file changes?"** Revise and re-present until the user explicitly approves the exact Gherkin for each target path. For a requested plan, scenario approval precedes the implementation plan. Approved scenarios are the implementation source of truth.

After approval, write the approved feature-file changes. When invoked through `atdd`, return to ATDD without asking whether to use high-value tests. Otherwise ask **"Do you want high-value tests for these scenarios? I recommend using the `hvtdd` skill. (Yes/no; you can choose a different approach.)"**

- Yes without another approach: Call the Skill tool with "hvtdd".
- A specified alternative takes precedence.
- No proceeds without high-value tests.
