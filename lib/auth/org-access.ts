import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"

type OrgAccess = {
  userId: string
  orgSlug: string
  canManageTeam: boolean
}

export async function requireOrgAccess(expectedSlug: string): Promise<OrgAccess> {
  const { userId, orgSlug, has } = await auth()

  if (!userId) {
    redirect("/sign-in")
  }

  if (!orgSlug) {
    redirect("/")
  }

  if (orgSlug !== expectedSlug) {
    redirect(`/orgs/${orgSlug}/dashboard`)
  }

  return {
    userId,
    orgSlug,
    canManageTeam: has({ role: "org:admin" }),
  }
}
