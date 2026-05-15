export const SALES_STAGES = ["discovery", "validation", "proposal", "closed_won", "closed_lost"] as const

export type SalesStage = (typeof SALES_STAGES)[number]

export type DealSignal = {
  stage: SalesStage
  lastActivityHours: number
  hasExecSponsor: boolean
  hasSecReview: boolean
}

export type Opportunity = DealSignal & {
  id: string
  orgSlug: string
  accountName: string
  ownerUserId: string
  amountUsd: number
  healthScore: number
}

export type OpportunityWithAction = Opportunity & {
  nextAction: string
}
