---
name: compile-instruction
description: Compile one written instruction into the smallest executable command, code, configuration rule, or automated check. Use when asked to make prose directly runnable or mechanically enforced rather than leave it as documentation.
---

# Compile instruction

Turn the instruction into an **executable** artifact and run or wire it where the user expects.

## 1. Fix the contract

Identify:

- the input or trigger;
- the observable result;
- the constraints stated in the instruction; and
- the environment that will execute it.

Inspect the target environment for its existing language, commands, configuration, and enforcement surfaces. Ask one question only when different unresolved interpretations would produce materially different behavior.

**Done when:** one concrete input-to-result contract preserves the instruction without adding requirements.

## 2. Choose the native form

Use the smallest form the target environment executes directly:

- a command for an immediate action;
- code for behavior used by a program;
- native configuration for a tool-owned rule; or
- an automated check when a violation must be rejected.

Prefer an existing project command, standard-library primitive, or native configuration over a new dependency or abstraction. If the instruction names no destination, return a self-contained command in the environment already in use. If there is no target environment, choose the most portable available form and name its runtime.

For repository enforcement, invoke the `automated-checks` skill rather than duplicating hook or CI policy here.

## 3. Compile

Implement the contract as the chosen artifact. Make parameters explicit where the instruction leaves values variable. Preserve its latitude: do not strengthen words such as “long,” “random,” or “valid” into unstated lengths, algorithms, character sets, or quality gates. When execution requires such a value, expose it as a parameter or ask for it.

Keep one source of truth. Replace superseded prose with the executable artifact or a pointer to its canonical invocation when the prose exists only to make the action happen.

## 4. Prove

Execute the command or the narrowest relevant test. Exercise one compliant example and, for a rule, one violating example. Confirm the observed result matches the contract.

Return:

1. the executable artifact or its path;
2. the exact invocation;
3. the observed verification result; and
4. any input the user must still supply.
