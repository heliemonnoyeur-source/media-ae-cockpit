# Smart Sales Workflow for a Snowflake-Style Team (with Clerk)

This guide gives you an implementation-ready workflow for an enterprise sales org using Clerk as the identity layer.

## 1) What "smart workflow" means for sales

For an account executive workflow, "smart" usually means:

- The right rep sees the right account at the right time.
- Access is role-aware (AE, SE, manager, ops) and territory-aware.
- Next steps are automatically suggested from deal stage + activity signals.
- Team/account changes instantly update permissions and assignments.

Clerk is a strong fit because it gives you:

- Authentication (SSO/social/passwordless if needed)
- Multi-tenant Organizations (great for account teams/workspaces)
- Role and permission controls
- Webhooks for real-time identity and membership sync

---

## 2) Recommended architecture

Use Clerk for identity and an app database/CRM layer for sales data.

```text
Rep login -> Clerk auth -> org + role context -> app dashboard
                                      |
                                      v
                            Deal + activity engine
                                      |
                                      v
                          Next best action suggestions
```

### Core entities

- **User**: salesperson, manager, SE, sales ops
- **Organization** (Clerk): a team/workspace (region, segment, or business unit)
- **Lead / Account / Opportunity** (your DB or CRM mirror)
- **CadenceTask**: next action items (call, email, technical validation, exec alignment)

### Role model (example)

- `org:admin` -> regional manager / sales ops
- `org:member` -> AE/SE
- Optional custom roles:
  - `org:ae`
  - `org:se`
  - `org:manager`

Use Clerk role checks to gate sensitive actions like reassignment and forecast edits.

---

## 3) Workflow design (MVP)

### Stage A: Sign-in and org routing

1. User signs in with Clerk.
2. User lands in the org-specific workspace (`/orgs/[slug]/dashboard`).
3. App verifies membership and role before loading data.

### Stage B: Lead/account intake and assignment

1. New lead/account enters from form/API/import.
2. Scoring function ranks priority using:
   - Segment fit
   - Engagement recency
   - Existing product usage signal
3. Assignment chooses owner based on:
   - Territory rules
   - Current load
   - Role specialization (AE vs SE pairing)

### Stage C: Next-best-action generation

At every dashboard refresh (or scheduled run), create recommended tasks:

- **No discovery call booked within 48h** -> create "book discovery" task.
- **POC active but no technical checkpoint** -> assign SE follow-up.
- **Late stage with no exec sponsor** -> create "exec alignment" task.

### Stage D: Identity-driven automation

When identity/org changes happen in Clerk:

- New user added to org -> provision workspace defaults.
- Role upgraded -> unlock forecasting/reassignment actions.
- User removed -> reassign open opportunities and tasks.

Use Clerk webhooks to keep this automatic and auditable.

---

## 4) Next.js + Clerk implementation skeleton

## 4.1 Middleware: protect app routes, keep webhooks public

```ts
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher([
  '/orgs/(.*)',
  '/dashboard(.*)',
  '/api/sales/(.*)',
])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect()
})

export const config = {
  matcher: [
    '/((?!_next|.*\\..*).*)',
    '/api/(.*)',
  ],
}
```

> Keep `/api/webhooks` public so Clerk can deliver signed events.

## 4.2 Role and org checks in server components/routes

```ts
import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'

export async function assertOrgAccess(expectedSlug: string) {
  const { orgSlug, has } = await auth()

  if (!orgSlug || orgSlug !== expectedSlug) {
    redirect('/select-org')
  }

  return {
    canManage: has({ role: 'org:admin' }),
  }
}
```

## 4.3 Webhook endpoint for sync and reassignment triggers

```ts
// app/api/webhooks/route.ts
import { verifyWebhook } from '@clerk/nextjs/webhooks'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const evt = await verifyWebhook(req)

  switch (evt.type) {
    case 'organizationMembership.created':
      // Provision new member defaults (views, queue, starter tasks)
      break
    case 'organizationMembership.deleted':
      // Reassign open deals/tasks from removed member
      break
    case 'user.updated':
      // Sync name/title/metadata changes into CRM mirror
      break
    default:
      break
  }

  return NextResponse.json({ received: true })
}
```

## 4.4 Next-best-action function (simplified)

```ts
type DealSignal = {
  stage: 'discovery' | 'validation' | 'proposal' | 'closed_won' | 'closed_lost'
  lastActivityHours: number
  hasExecSponsor: boolean
  hasSecReview: boolean
}

export function getNextBestAction(signal: DealSignal): string {
  if (signal.stage === 'discovery' && signal.lastActivityHours > 48) {
    return 'Schedule discovery call and send agenda'
  }
  if (signal.stage === 'validation' && !signal.hasSecReview) {
    return 'Launch security review with customer IT'
  }
  if (signal.stage === 'proposal' && !signal.hasExecSponsor) {
    return 'Align executive sponsor before commercial negotiation'
  }
  return 'Advance current plan and log stakeholder update'
}
```

---

## 5) Data contract suggestions

Store only sales app data in your DB; keep identity in Clerk as source-of-truth.

### `sales_user_profile`

- `clerk_user_id` (unique)
- `org_id`
- `role`
- `territory`
- `segment`

### `opportunity`

- `id`
- `org_id`
- `owner_clerk_user_id`
- `stage`
- `health_score`
- `next_action`
- `next_action_due_at`

### `cadence_task`

- `id`
- `opportunity_id`
- `assignee_clerk_user_id`
- `task_type`
- `status`
- `due_at`

---

## 6) Clerk configuration checklist

1. Enable Organizations in Clerk Dashboard.
2. Configure organization roles and permissions.
3. Add environment variables:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`
   - `CLERK_WEBHOOK_SIGNING_SECRET`
4. Add webhook endpoint in Clerk Dashboard (`/api/webhooks`).
5. Verify webhook events are processed and idempotent.

---

## 7) High-leverage enhancements after MVP

- **AI assistant for reps**: summarize account state + draft follow-up email.
- **Forecast risk detector**: alert managers when deal activity drops.
- **Auto reassignment rules**: holiday/leave coverage using org role + capacity.
- **Playbook personalization**: next actions vary by segment (ENT/MM/SMB).

---

## 8) Practical first sprint scope

If you want to ship quickly:

1. Clerk auth + Organizations + role checks.
2. Opportunity dashboard with health score + next action.
3. Webhook sync for membership create/delete + user updates.
4. Simple assignment engine (territory + load).

That gives immediate value while staying implementation-light.
