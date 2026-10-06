---
name: atdd
description: 'ATDD: author or revise .feature scenarios, obtain approval, and hand off implementation to hvtdd. Use when acceptance behavior needs feature-file changes.'
---

# Acceptance-Test-Driven Development

1. Read [Feature authoring](feature-authoring.md) to decide scenario coverage and follow the project's feature-file conventions. If existing scenarios already specify the requested behavior accurately, continue to step 3 without changing them.
2. For new or changed scenarios: Call the Skill tool with "behavior-specification". Propose the exact `.feature` changes and obtain approval as specified by Feature authoring. Write the approved feature files.
3. Hand off bindings, implementation, and acceptance verification: Call the Skill tool with "hvtdd".
