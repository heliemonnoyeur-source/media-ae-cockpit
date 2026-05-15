import { verifyWebhook } from "@clerk/nextjs/webhooks"
import { handleClerkSalesEvent, getWebhookDebugSnapshot } from "@/lib/webhooks/handlers"
import { NextResponse } from "next/server"

const processedWebhookIds = new Set<string>()

export async function POST(req: Request) {
  const webhookId = req.headers.get("svix-id")
  if (!webhookId) {
    return NextResponse.json({ error: "Missing svix-id header." }, { status: 400 })
  }

  if (processedWebhookIds.has(webhookId)) {
    return NextResponse.json({ received: true, duplicate: true }, { status: 200 })
  }

  try {
    const event = await verifyWebhook(req)
    const action = handleClerkSalesEvent(event)
    processedWebhookIds.add(webhookId)

    return NextResponse.json(
      {
        received: true,
        action,
        ...getWebhookDebugSnapshot(),
      },
      { status: 200 },
    )
  } catch {
    return NextResponse.json({ error: "Webhook verification failed." }, { status: 400 })
  }
}
