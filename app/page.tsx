import { OrganizationSwitcher, SignInButton, SignUpButton } from "@clerk/nextjs"
import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"

export default async function HomePage() {
  const { userId, orgSlug } = await auth()

  if (userId && orgSlug) {
    redirect(`/orgs/${orgSlug}/dashboard`)
  }

  return (
    <main className="container grid">
      <section className="card">
        <h1>Smart sales workflow starter</h1>
        <p className="muted">
          This starter app combines Clerk auth, organization-aware routing, and a demo next-best-action
          workflow for account executives.
        </p>
        {!userId ? (
          <div className="nav-actions">
            <SignInButton mode="modal">
              <button className="button" type="button">
                Sign in
              </button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="button primary" type="button">
                Sign up
              </button>
            </SignUpButton>
          </div>
        ) : (
          <p className="muted">Select your organization from the switcher and open your workspace dashboard.</p>
        )}
      </section>

      {userId ? (
        <section className="card">
          <h2>Choose an organization</h2>
          <p className="muted">
            Organizations should represent your region, segment, or sales unit so permissions and deal access are
            scoped correctly.
          </p>
          <OrganizationSwitcher hidePersonal />
          <p>
            After selecting an org, open{" "}
            <code>/orgs/&lt;org-slug&gt;/dashboard</code> to see opportunities and next actions.
          </p>
        </section>
      ) : null}

      <section className="card">
        <h2>Included workflow components</h2>
        <ul>
          <li>Protected org routes via Clerk middleware.</li>
          <li>Role-aware dashboard pages with org slug validation.</li>
          <li>Sales opportunity API with next-best-action recommendations.</li>
          <li>Webhook endpoint for user/org membership synchronization hooks.</li>
        </ul>
        <p className="muted">
          Architecture reference is available in the repository docs at{" "}
          <code>docs/smart-sales-workflow-clerk.md</code>.
        </p>
      </section>
    </main>
  )
}
