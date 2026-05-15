import { getNextBestAction } from "@/lib/sales/next-best-action"
import type { Opportunity, OpportunityWithAction } from "@/lib/sales/types"

const opportunities: Opportunity[] = [
  {
    id: "opp_001",
    orgSlug: "amer-enterprise",
    accountName: "Acme Media Group",
    ownerUserId: "user_ae_1",
    stage: "discovery",
    lastActivityHours: 56,
    hasExecSponsor: false,
    hasSecReview: false,
    amountUsd: 250000,
    healthScore: 61,
  },
  {
    id: "opp_002",
    orgSlug: "amer-enterprise",
    accountName: "Northstar Retail",
    ownerUserId: "user_ae_2",
    stage: "validation",
    lastActivityHours: 22,
    hasExecSponsor: true,
    hasSecReview: false,
    amountUsd: 420000,
    healthScore: 77,
  },
  {
    id: "opp_003",
    orgSlug: "emea-strategic",
    accountName: "Vantage Insurance",
    ownerUserId: "user_ae_3",
    stage: "proposal",
    lastActivityHours: 31,
    hasExecSponsor: false,
    hasSecReview: true,
    amountUsd: 610000,
    healthScore: 70,
  },
]

export function listOpportunitiesForOrg(orgSlug: string): OpportunityWithAction[] {
  return opportunities
    .filter((opportunity) => opportunity.orgSlug === orgSlug)
    .map((opportunity) => ({
      ...opportunity,
      nextAction: getNextBestAction(opportunity),
    }))
}
