---
name: behavior-specification
description: 'Behavior specification: decide and describe the behavior to test through context, action, observable outcome, concrete examples, and behavior names. Use when authoring or revising scenarios or test descriptions.'
---

# Behavior specification

Use this reference to specify what behavior should be tested. A `.feature` scenario or a test description can express that specification; executable setup, invocation, and assertions are a separate concern.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language.

- Frame the work as behavior rather than as tests: behavior names what the system should do; tests check whether it does.
- Evolve the design by probing for the next important behavior. Use concrete examples to make the expected behavior precise.
- Describe the relevant context, action, and observable outcome in the domain's language. Specify what should happen, leaving internal realization open.
- Describe one coherent behavior through a public interface.
- Name tests with sentences about their behavior. Prefer a simple sentence format to keep each test focused; an expressive name communicates the broken expectation when it fails.
- Make acceptance criteria executable when specifying acceptance behavior, so the examples can verify whether the agreed behavior exists.
