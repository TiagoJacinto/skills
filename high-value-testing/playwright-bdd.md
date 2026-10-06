# Playwright BDD

Use this reference when the project uses `playwright-bdd`.

## Discover configuration and steps

- Inspect `defineBddConfig(...)` in `playwright.config.ts` or `playwright.config.js` for the feature location, step-definition globs, and generated test directory (`testDir`). If there are multiple configurations, choose the one matching the feature area; ask only if the choice remains ambiguous.
- Inspect relevant feature files and registered step definitions before writing new steps. `npx bddgen export` can list registered steps.
- Follow the project's existing fixtures, naming, and step-definition patterns. Prefer `@`-prefixed feature directories for domain-scoped steps when appropriate; steps in `features/@homepage/steps.ts`, for example, are scoped to features in that directory without explicit `{ tags: '@homepage' }`. See [scoped steps](https://vitalets.github.io/playwright-bdd/#/writing-steps/scoped?id=tags-from-path).

## Verify

Generate the Playwright tests, then run the generated specs for the changed features using the configured `testDir`:

```sh
npx bddgen && npx playwright test <generated-feature-spec-path>
```

For example, if `testDir` is `.features-gen` and the changed feature generates that spec:

```sh
npx bddgen && npx playwright test .features-gen/@homepage/homepage.feature.spec.js
```
