"use client"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Star } from "lucide-react"

const testimonials = [
  {
    text: "We went from a three-month agent development cycle to deploying production-ready systems in an afternoon. The eval framework alone saved us weeks of custom tooling.",
    name: "Sarah Chen",
    role: "CTO, DataFlow",
    avatar: "SC",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    text: "The multi-agent orchestration is the real deal. We described our support workflow in plain English and got a deployed system with memory, routing, and human escalation — all wired up.",
    name: "Marcus Rivera",
    role: "VP Engineering, Nexus AI",
    avatar: "MR",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    text: "Finally, an agent platform that treats evaluation as a first-class citizen. Groundedness and coherence metrics out of the box, plus custom evals for our domain. This is how it should work.",
    name: "Aisha Patel",
    role: "Staff Engineer, CloudScale",
    avatar: "AP",
    gradient: "from-green-500 to-emerald-500",
  },
]

export function Testimonials() {
  return (
    <section id="testimonials" className="relative py-32 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <Badge className="mb-4">From the field</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter">
            Trusted by teams
            <br />
            <span className="text-muted-foreground">shipping agents to production.</span>
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <Card className="p-8 h-full hover:border-white/[0.15] transition-all duration-500 hover:-translate-y-1">
                <div className="flex gap-1 mb-5">
                  {Array.from({ length: 5 }).map((_, j) => (
                    <Star key={j} className="h-4 w-4 fill-amber-400 text-amber-400" />
                  ))}
                </div>
                <p className="text-[15px] leading-relaxed text-white/80 mb-8">&ldquo;{t.text}&rdquo;</p>
                <div className="flex items-center gap-3 mt-auto">
                  <div className={`h-10 w-10 rounded-full bg-gradient-to-br ${t.gradient} flex items-center justify-center text-xs font-bold`}>
                    {t.avatar}
                  </div>
                  <div>
                    <div className="text-sm font-semibold">{t.name}</div>
                    <div className="text-xs text-muted-foreground">{t.role}</div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
