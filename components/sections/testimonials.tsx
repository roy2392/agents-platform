"use client"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Star } from "lucide-react"

const testimonials = [
  {
    text: "We replaced 12 microservices with 3 agents. Deployment time went from weeks to minutes. This is the future of backend architecture.",
    name: "Sarah Chen",
    role: "CTO, DataFlow",
    avatar: "S",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    text: "The multi-agent orchestration is mind-blowing. Our customer support agents resolve 89% of tickets autonomously now.",
    name: "Marcus Rivera",
    role: "VP Engineering, Nexus AI",
    avatar: "M",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    text: "Best developer experience I've seen in the AI space. The SDK is beautifully designed and the docs are incredible.",
    name: "Aisha Patel",
    role: "Staff Engineer, CloudScale",
    avatar: "A",
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
          <Badge className="mb-4">What People Say</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter">
            Loved by engineers
            <br />
            <span className="text-muted-foreground">and teams worldwide.</span>
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
                <div className="flex gap-1 mb-4">
                  {Array.from({ length: 5 }).map((_, j) => (
                    <Star key={j} className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                  ))}
                </div>
                <p className="text-[15px] leading-relaxed text-white/80 mb-8">&ldquo;{t.text}&rdquo;</p>
                <div className="flex items-center gap-3 mt-auto">
                  <div className={`h-10 w-10 rounded-full bg-gradient-to-br ${t.gradient} flex items-center justify-center text-sm font-bold`}>
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
