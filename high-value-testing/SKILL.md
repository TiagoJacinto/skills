---
name: high-value-testing
description: 'High-value testing: requirements and scenario bindings for application-boundary acceptance tests. Use when designing, implementing, or reviewing high-value tests, whether or not the work uses TDD.'
---

# High-value testing

Use these requirements for high-value acceptance tests. They describe the selected testing approach, independently of the implementation workflow.

## Application coverage

Use the acceptance-test runner for the concrete acceptance examples.

Cover successes and failures in extreme detail, including every meaningful edge case in scope. A use case normally earns many high-value unit tests.

## Collaborators

Exercise the agreed public seams with real collaborators. Use no mocks.

## Verification-mode annotation

Each test contains exactly one simple comment that names its verification mode: `// result verification`, `// state verification`, or `// communication verification`.

## Scenario bindings and verification

For bindings and acceptance verification of existing or approved `.feature` scenarios, read [Scenario execution](scenario-execution.md).
