import type { DealSignal } from "@/lib/sales/types"

export function getNextBestAction(signal: DealSignal): string {
  if (signal.stage === "discovery" && signal.lastActivityHours > 48) {
    return "Schedule discovery call and send account-specific agenda."
  }

  if (signal.stage === "validation" && !signal.hasSecReview) {
    return "Kick off security review and align your SE on blockers."
  }

  if (signal.stage === "proposal" && !signal.hasExecSponsor) {
    return "Map and activate executive sponsor before commercial close."
  }

  if (signal.lastActivityHours > 72) {
    return "Re-engage account: send recap and secure next stakeholder meeting."
  }

  return "Advance current plan and log latest stakeholder update."
}
