# Vitest Cucumber

Use this reference for `@amiceli/vitest-cucumber` bindings and when choosing it to bootstrap a missing acceptance-spec runner.

## Bootstrap a missing runner

Use the project's package manager to add `vitest` and `@amiceli/vitest-cucumber` as development dependencies. Add the smallest configuration and script that discovers the acceptance specs. Identify the exact command for the selected scenario.

Bootstrap is complete when that command discovers and executes the selected scenario. Binding or domain failures can remain for the red phase.

## Prefer step expressions

Use a step expression when a step contains variable values. Prefer one typed expression to concrete-string bindings or repeated parsing logic.

`@amiceli/vitest-cucumber` supports parameter types such as `{int}`, `{number}`, `{string}`, `{word}`, and `{list}`. Captured values follow the test context in the binding callback and are transformed to the corresponding type.

Use a regular expression when step-expression syntax cannot express the match clearly. For recurring domain-specific values, define one custom parameter expression instead of duplicate parsing logic.

Consult the [Cucumber expression guidance](https://cucumber.io/docs/cucumber/step-definitions/#expressions) and the [`vitest-cucumber` step-expression reference](https://vitest-cucumber.miceli.click/features/step-expression/) when built-in expression behavior or custom parameter syntax needs clarification.
