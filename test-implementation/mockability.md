# Designing external adapters for testability

At a system boundary, make the adapter interface easy to replace with the double chosen by the testing model.

## Inject external dependencies

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to replace at the boundary
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Tied to a concrete external client
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

## Prefer specific operations over generic fetchers

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// Each operation has a distinct shape
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// A double must branch on the endpoint
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

Specific operations let each double return one shape without conditional test setup and make the exercised operation visible.
