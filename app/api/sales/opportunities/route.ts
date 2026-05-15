import { auth } from "@clerk/nextjs/server"
import { listOpportunitiesForOrg } from "@/lib/sales/data"
import { NextResponse } from "next/server"

export async function GET() {
  const { userId, orgSlug } = await auth()

  if (!userId) {
    return NextResponse.json({ error: "Authentication required." }, { status: 401 })
  }

  if (!orgSlug) {
    return NextResponse.json({ error: "Select an organization first." }, { status: 403 })
  }

  const opportunities = listOpportunitiesForOrg(orgSlug)
  return NextResponse.json({ orgSlug, opportunities })
}
