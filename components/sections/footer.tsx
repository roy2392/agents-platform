"use client"
import { Zap } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t border-white/[0.06] py-12 px-6">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="h-6 w-6 rounded-md bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
            <Zap className="h-3 w-3 text-white" />
          </div>
          <span className="text-sm text-muted-foreground">© 2026 Agents Platform. All rights reserved.</span>
        </div>
        <div className="flex items-center gap-6">
          {["Privacy", "Terms", "Docs", "GitHub", "Twitter"].map((link) => (
            <a key={link} href="#" className="text-sm text-muted-foreground hover:text-white transition-colors">
              {link}
            </a>
          ))}
        </div>
      </div>
    </footer>
  )
}
