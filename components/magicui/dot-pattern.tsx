"use client"
import { cn } from "@/lib/utils"

export function DotPattern({ className }: { className?: string }) {
  return (
    <svg
      className={cn(
        "pointer-events-none absolute inset-0 h-full w-full fill-white/[0.03] [mask-image:radial-gradient(400px_circle_at_center,white,transparent)]",
        className
      )}
      aria-hidden="true"
    >
      <defs>
        <pattern id="dot-pattern" x="0" y="0" width="16" height="16" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="1" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#dot-pattern)" />
    </svg>
  )
}
