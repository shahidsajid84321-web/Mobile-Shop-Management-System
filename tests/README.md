# Frontend Test Suite

Install dependencies and run:

```bash
npm install
npm test
```

Watch mode:

```bash
npm run test:watch
```

Run one feature independently:

```bash
npx vitest run tests/features/catalogApi.test.ts
npx vitest run tests/features/authApi.test.ts
```

## What is covered

- `lib/auth` token storage
- `lib/api` authorization headers, JSON handling, API errors, refresh-on-401 and media URLs
- Auth API: login, refresh, logout, registration, email verification and password reset
- Catalog API: categories, products and image upload
- Customers
- Dashboard
- Inventory
- Payments
- Purchases
- Reports
- Roles and permissions
- Sales
- Online store management orders/returns
- Suppliers
- Users

The feature tests mock HTTP calls so they can run without starting the backend. UI/page behavior can be added later with React Testing Library if desired.
