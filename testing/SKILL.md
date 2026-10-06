---
name: testing
description: 'Testing taxonomy: test purposes, levels, verification modes, and doubles. Use when choosing the kind of test, its boundary, or how to observe its subject.'
---

# Testing model

Use this model to choose the subject, verification style, and test doubles for each test. A level describes how the test views its subject, so the same component can take different roles at different test boundaries.

## Test purposes

A temporary developer test helps explore or implement something and may be deleted afterward. A retained behavior-verifying test protects a specified behavior. Acceptance tests implement concrete acceptance examples. Purpose and level are separate: the level describes the subject boundary, not whether a test should be retained or what makes it valuable.

## Test levels

### Level 1 — Stateless Input-Output

A typical unit test exercises a direct Input-Output System and uses result verification. The subject retains no state: input enters one of its operations and a direct output returns. A policy object is Level 1 when the test exercises a function such as `policy.isAllowed(input)` and observes its returned decision.

### Level 2 — Stateful

A typical unit test exercises a Stateful System and uses state verification. The subject retains information across interactions, so the test performs an action and then inquires about the resulting state. Aggregates, entities, and stateful adapters can be Level 2 subjects.

### Level 3 — Application

An application test verifies a Service, Use Case, or Application Layer API directly. A **high-value unit test** is an application-boundary unit test implementing a concrete acceptance example.

An application test can use result, state, or communication verification according to whether the observed behavior is a direct output, a state transition, or an indirect input/output interaction.

A use case is a *Controller* in the Responsibility-Driven Design sense: it controls and directs collaborators, makes application-level decisions, delegates lower-level work, and makes collaborators interact. Controller describes a responsibility carried by a behavior-bearing module, component, aggregate, function, or class.

Application tests exercise those application-level decisions and coordination. Typical unit tests exercise lower-level responsibilities assigned to collaborators, including responsibilities reused across features. Those responsibilities may also execute transitively in application tests; that overlap is valid because the tests operate at different levels.

When selecting high-value acceptance tests as the approach: Call the Skill tool with "high-value-testing" for its specialized requirements.

## Subject verification

The test level determines the available verification modes:

| Test level | System view | Verification |
| --- | --- | --- |
| Level 1 | Stateless direct Input-Output System | Result only |
| Level 2 | Stateful System | State only |
| Level 3 | Application System | Result, state, or communication |

### Result verification

Result verification applies to Level 1 and Level 3. Treat the observed operation as a direct Input-Output System: provide input and observe its direct output.

At Level 1, a typical unit test observes the result of a stateless operation:

```ts
// result verification
expect(isANumber(7)).toBe(true)
```

At Level 3, an application test observes the application's direct response:

```ts
const createUserResponse = await application.users.createUser(createUserInput)

// result verification
expect(createUserResponse.email).toEqual(createUserInput.email)
expect(createUserResponse.firstName).toEqual(createUserInput.firstName)
```

### State verification

State verification applies to Level 2 and Level 3. Perform an action against a Stateful System, then inquire about the state it retained.

At Level 2, a typical unit test inquires through the stateful subject:

```ts
game.pause()

// state verification
expect(game.getCurrentStatus()).toBe("Paused")
```

At Level 3, an application test performs an application action and inquires about the resulting state through the application API:

```ts
await application.users.createUser(createUserInput)

// state verification
const getUserResponse = await application.users.getUserByEmail(createUserInput.email)
expect(getUserResponse.email).toEqual(createUserInput.email)
```

### Communication verification

Communication verification applies only to Level 3. Treat a collaborator as an Indirect Input & Output System: preload its indirect inputs, execute the application subject, then inspect its recorded indirect outputs to verify attempted state changes.

An application test observes the outgoing adapter spy after the application action:

```ts
await application.users.createUser(createUserInput)

// communication verification
expect(contactListAPISpy.getTimesMethodCalled("addEmailToList")).toEqual(1)
```

An adapter can have different views at different test boundaries. As a Level 2 subject, a stateful adapter is verified through the state it retains. As a Level 3 collaborator, an outgoing adapter is an Indirect Input & Output System used to verify the application's communication with it rather than the adapter's correctness.

A repository is one example: at Level 2, verify the state it retains; at Level 3, its queries supply indirect input and its recorded saves expose indirect output.

## Adapter test doubles

### Outgoing adapters

For repositories, gateways, notification senders, and other outgoing adapters, prefer a hand-written in-memory spy. It implements the production interface, supplies controlled indirect input, and records outgoing calls for later inspection.

A spy may take this shape:

```ts
export class InMemoryUserRepositorySpy
  extends Spy<UsersRepository>
  implements UsersRepository
```

### Incoming adapters

For request handlers, HTTP controllers, and other incoming adapters, prefer the unit-test runner's native mocking facilities for their collaborators: `jest.fn()` under Jest, `vi.fn()` under Vitest, or the ecosystem equivalent. Use the runner already present in the project.
