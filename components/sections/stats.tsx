"use client"
import { motion } from "framer-motion"
import { NumberTicker } from "@/components/magicui/number-ticker"

const stats = [
  { value: 12000, suffix: "+", label: "Agents Deployed" },
  { value: 99, suffix: ".9%", label: "Uptime SLA" },
  { value: 340, suffix: "+", label: "Enterprise Teams" },
  { value: 47, suffix: "ms", label: "Avg. Latency" },
]

export function Stats() {
  return (
    <section className="relative border-y border-white/[0.06] py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="text-center"
            >
              <div className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent">
                <NumberTicker value={stat.value} suffix={stat.suffix} />
              </div>
              <div className="mt-2 text-sm text-muted-foreground font-medium">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
