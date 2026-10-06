# Skills

A personal collection of agent skills for behavior-driven development, test-driven development, testing, codebase design, and code review.

## Install

Install the complete collection from your project's root directory:

```sh
npx skills add TiagoJacinto/skills --skill '*'
```

The CLI prompts you to choose your coding agents and installation method. To install all skills globally for a specific agent, for example Pi:

```sh
npx skills add TiagoJacinto/skills --skill '*' --agent pi --global
```

List available skills without installing:

```sh
npx skills add TiagoJacinto/skills --list
```

Install the whole collection by default: skills reference one another, and the installer does not automatically resolve those dependencies. Individual skills can be selected with `--skill <name>`, but their referenced skills must also be available.

Browse the collection on [skills.sh](https://skills.sh/tiagojacinto/skills).

## Included skills

- [bdd](bdd/SKILL.md): behavior-driven development and routing to specification, authoring, and execution.
- [atdd](atdd/SKILL.md): acceptance-test-driven development, including scenario approval.
- [hvtdd](hvtdd/SKILL.md): implement approved scenarios through high-value tests and TDD.
- [tdd](tdd/SKILL.md): the red–green implementation loop.
- [behavior-specification](behavior-specification/SKILL.md): describe observable behavior and concrete examples.
- [gherkin](gherkin/SKILL.md): shared scenario structure and state-versus-input rules.
- [high-value-testing](high-value-testing/SKILL.md): application-boundary acceptance testing and scenario bindings.
- [test-implementation](test-implementation/SKILL.md): executable setup, invocation, assertions, and public test seams.
- [testing](testing/SKILL.md): test purposes, levels, verification modes, and doubles.
- [codebase-design](codebase-design/SKILL.md): deep modules, interfaces, and responsibility allocation.
- [code-review](code-review/SKILL.md): separate standards and specification reviews.
- [setup-engineering-skills](setup-engineering-skills/SKILL.md): configure a project's issue tracker, triage labels, and domain documentation.

Supporting documents and agent metadata are included with each skill. The Playwright BDD and Vitest Cucumber references under `high-value-testing` are documents, not separate skills in this collection.

## Runtime requirements

These are instructions for agents that support `SKILL.md`, not executable test runners. The skill text retains its existing `Skill` tool invocation wording. Your agent must support named skill loading or its equivalent. Workflows that request subagents need an agent runtime with that capability.

Use your project's test runner and dependencies. The collection does not install application testing frameworks. `code-review` expects issue-tracker configuration; if it is missing, run `/setup-engineering-skills` in the project being reviewed.

The setup templates also mention optional engineering workflows outside this collection. Those references do not mean those skills are included here.

## Maintain this collection

This repository is the source of truth. Its checkout is also the maintainer's local skills directory. `.gitignore` allowlists the published skills and repository files; other local skills remain in place and are not published.

To add a skill to the public collection, explicitly add its directory to the allowlist before staging it. Review `git diff --cached` before committing. Do not use `git add --force` to bypass the allowlist.

Issues and contributions are welcome. This is a personal collection with no promised support response time or release schedule.

## License

[MIT](LICENSE).
