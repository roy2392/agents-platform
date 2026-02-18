"use client"
import { cn } from "@/lib/utils"

export function AnimatedGridPattern({ className }: { className?: string }) {
  return (
    <div className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)}>
      <div className="absolute inset-0 [mask-image:radial-gradient(500px_circle_at_center,white,transparent)]">
        <div
          className="absolute inset-0 animate-grid"
          style={{
            backgroundImage: `linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)`,
            backgroundSize: "60px 60px",
          }}
        />
      </div>
    </div>
  )
}
