---
name: tdd
description: 'TDD: drive implementation through the red → green loop. Use when building features or fixing bugs test-first, or when another workflow supplies behavior to implement through failing tests.'
---

# Test-Driven Development

Use an existing accurate behavior specification directly, including approved `.feature` scenarios. If the behavior still needs specification or revision: Call the Skill tool with "behavior-specification". An existing accurate specification needs neither re-authoring nor another invocation of that reference skill.

Call the Skill tool with "test-implementation" for executable setup, invocation, and assertions. Respect ADRs in the area you're touching.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Vertical slices.** One test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you. Writing all tests first, then all implementation verifies imagined behavior rather than user-facing behavior and commits to test structure before understanding the implementation.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
