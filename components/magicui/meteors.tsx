"use client"
import { cn } from "@/lib/utils"

export function Meteors({ number = 20, className }: { number?: number; className?: string }) {
  const meteors = Array.from({ length: number }, (_, i) => i)
  return (
    <div className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)}>
      {meteors.map((i) => (
        <span
          key={i}
          className="animate-meteor absolute top-1/2 left-1/2 h-0.5 w-0.5 rounded-full bg-blue-400 shadow-[0_0_0_1px_#ffffff10] rotate-[215deg]"
          style={{
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${Math.random() * 3 + 2}s`,
          }}
        >
          <div className="pointer-events-none absolute top-1/2 -z-10 h-px w-[50px] -translate-y-1/2 bg-gradient-to-r from-blue-400 to-transparent" />
        </span>
      ))}
    </div>
  )
}
