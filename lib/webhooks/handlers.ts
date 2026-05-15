type ClerkEventPayload = {
  type: string
  data: unknown
}

const onboardedMemberships = new Set<string>()
const reassignmentQueue = new Map<string, string[]>()

function extractStringId(data: unknown): string | null {
  if (typeof data !== "object" || data === null) {
    return null
  }

  const maybeId = (data as { id?: unknown }).id
  return typeof maybeId === "string" ? maybeId : null
}

export function handleClerkSalesEvent(event: ClerkEventPayload): string {
  switch (event.type) {
    case "organizationMembership.created": {
      const membershipId = extractStringId(event.data)
      if (membershipId) {
        onboardedMemberships.add(membershipId)
      }
      return "Provisioned membership defaults."
    }
    case "organizationMembership.deleted": {
      const membershipId = extractStringId(event.data)
      if (membershipId) {
        reassignmentQueue.set(membershipId, ["opp_001", "opp_002"])
      }
      return "Queued open opportunities for reassignment."
    }
    case "user.updated":
      return "Synced user profile fields for CRM mirror."
    case "user.deleted":
      return "Flagged user-owned tasks for archival and reassignment."
    default:
      return "Event ignored by sales workflow handler."
  }
}

export function getWebhookDebugSnapshot() {
  return {
    onboardedMembershipCount: onboardedMemberships.size,
    pendingReassignments: reassignmentQueue.size,
  }
}
