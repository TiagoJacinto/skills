# Scenario execution

Use this reference to bind and verify existing or approved `.feature` scenarios.

## Binding and runner discovery

Inspect the specified scenarios and registered step definitions to identify the bindings that match each step. Inspect binding scope, fixtures, framework configuration, and existing generation, validation, and test commands to determine how those scenarios execute. Follow repository scripts, configuration, and the nearest relevant step-definition patterns. Ask the user only when multiple binding or runner conventions remain equally plausible after inspection. For `playwright-bdd`, read [Playwright BDD](playwright-bdd.md). For `@amiceli/vitest-cucumber`, read [Vitest Cucumber](vitest-cucumber.md).

## Bindings and verification

Implement the approved behavior according to project guidelines. Before editing bindings, read [Scenario bindings](bindings.md) and the applicable framework reference. If choosing `@amiceli/vitest-cucumber` for a project without an acceptance-spec runner, follow its [bootstrap guidance](vitest-cucumber.md#bootstrap-a-missing-runner). Bind every approved step using the project's framework, language, naming, fixtures, and scoping conventions. Reuse a step when its domain meaning matches exactly; otherwise create a focused step. The implementation should exercise every approved scenario.

Run the repository's BDD generation or validation command when required by its framework, then the narrowest test command executing all changed scenarios. Run the broader BDD suite when shared bindings or infrastructure changed. Report commands and results. Work remains incomplete while any changed scenario fails through the configured BDD runner or generation or binding errors remain.
