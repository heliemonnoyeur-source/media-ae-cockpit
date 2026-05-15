import type { Metadata } from "next"
import { ClerkProvider, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs"
import { auth } from "@clerk/nextjs/server"
import "./globals.css"

export const metadata: Metadata = {
  title: "Media AE Cockpit",
  description: "Clerk-powered smart sales workflow starter",
}

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const { userId } = await auth()

  return (
    <html lang="en">
      <body>
        <ClerkProvider>
          <div className="page-shell">
            <header className="top-nav">
              <a className="brand" href="/">
                Media AE Cockpit
              </a>
              <div className="nav-actions">
                {userId ? (
                  <UserButton />
                ) : (
                  <>
                    <SignInButton mode="modal">
                      <button className="button" type="button">
                        Sign in
                      </button>
                    </SignInButton>
                    <SignUpButton mode="modal">
                      <button className="button primary" type="button">
                        Create account
                      </button>
                    </SignUpButton>
                  </>
                )}
              </div>
            </header>
            {children}
          </div>
        </ClerkProvider>
      </body>
    </html>
  )
}
