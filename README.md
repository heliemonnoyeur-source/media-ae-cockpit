# media-ae-cockpit

Clerk-powered smart sales workflow starter for account executives.

## What is included

- Next.js App Router + TypeScript scaffold
- Clerk authentication with sign-in/sign-up routes
- Organization-aware dashboard route at `orgs/[slug]/dashboard`
- Protected sales API route at `api/sales/opportunities`
- Public Clerk webhook endpoint at `api/webhooks`
- Demo next-best-action rules engine for opportunities

## Quickstart

1. Install dependencies:

   ```bash
   npm install
   ```

2. Create env file:

   ```bash
   cp .env.example .env.local
   ```

   - Keyless mode can work without explicit keys for local startup.
   - For dashboard-managed apps, fill in `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY`.
   - Set `CLERK_WEBHOOK_SIGNING_SECRET` to verify webhook requests from Clerk.

3. Start the app:

   ```bash
   npm run dev
   ```

4. Open `http://localhost:3000`.
5. Sign in, select an organization, and navigate to `orgs/<org-slug>/dashboard`.

## Clerk setup notes

- Enable **Organizations** in Clerk dashboard.
- Add a webhook endpoint to `/api/webhooks`.
- Configure org roles (`org:admin`, `org:member`, plus optional custom roles).

## Documentation

- [Smart Sales Workflow for a Snowflake-Style Team](docs/smart-sales-workflow-clerk.md)
