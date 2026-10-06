---
name: test-implementation
description: 'Test implementation: turn specified behavior into executable setup, invocation, and assertions. Use when implementing or reviewing behavior-verifying tests, agreeing public seams, or avoiding implementation-coupled assertions.'
---

# Test implementation

Use this reference to implement a check for specified behavior. These rules apply to tests intended to verify behavior, not automatically to temporary developer tests used to explore or implement something.

Before choosing test levels, verification modes, or test doubles: Call the Skill tool with "testing".

When shaping an external interface for a test double, read [Designing external adapters for testability](mockability.md).

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose): Call the Skill tool with "codebase-design". Use the module, interface, depth, seam, adapter, leverage, and locality vocabulary.

## Observable behavior

Observe what a caller can see; several assertions may establish one behavior. Use an expectation independent of the implementation, such as a known value or an agreed example.

```typescript
// Verifies the specified checkout outcome
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

## Implementation coupling

A test that checks an internal collaborator, private method, or its call order can fail after a refactor even when behavior has not changed. Communication at an agreed external boundary can itself be observable behavior; choosing that verification mode belongs to the [testing model](../testing/SKILL.md).

```typescript
// Checks an internal call instead of the specified checkout outcome
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Observe through the public interface rather than bypassing it to inspect internal storage:

```typescript
// Bypasses the interface
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// Observes the specified behavior through the interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

## Tautological expectations

A test that recomputes the expected value like the implementation can pass by construction. Derive the expectation independently:

```typescript
// Recomputes the expected value
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// Uses a known value
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
