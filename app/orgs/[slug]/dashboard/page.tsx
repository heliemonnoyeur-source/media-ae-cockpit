import { OrganizationSwitcher } from "@clerk/nextjs"
import { listOpportunitiesForOrg } from "@/lib/sales/data"
import { requireOrgAccess } from "@/lib/auth/org-access"

type DashboardPageProps = {
  params: Promise<{ slug: string }>
}

function formatUsd(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(amount)
}

export default async function DashboardPage({ params }: DashboardPageProps) {
  const { slug } = await params
  const { userId, canManageTeam } = await requireOrgAccess(slug)
  const opportunities = listOpportunitiesForOrg(slug)

  return (
    <main className="container grid">
      <section className="card">
        <h1>{slug} sales workspace</h1>
        <p className="muted">
          Signed in as <strong>{userId}</strong>. {canManageTeam ? "Manager privileges enabled." : "Member view."}
        </p>
        <OrganizationSwitcher hidePersonal />
      </section>

      <section className="card">
        <h2>Open opportunities</h2>
        <ul className="opportunity-list">
          {opportunities.map((opportunity) => (
            <li className="opportunity-item" key={opportunity.id}>
              <h3>{opportunity.accountName}</h3>
              <p className="muted">
                Stage: <span className="pill">{opportunity.stage}</span> · Amount:{" "}
                <strong>{formatUsd(opportunity.amountUsd)}</strong> · Health score: {opportunity.healthScore}
              </p>
              <p>
                <strong>Next best action:</strong> {opportunity.nextAction}
              </p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
