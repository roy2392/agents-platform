import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Agents Platform — The Future of AI Agents",
  description: "Build, deploy, and orchestrate autonomous AI agents at scale. The platform that powers the next generation of intelligent automation.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background font-sans overflow-x-hidden">
        {children}
      </body>
    </html>
  )
}
