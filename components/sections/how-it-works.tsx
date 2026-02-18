"use client"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { DotPattern } from "@/components/magicui/dot-pattern"

const steps = [
  {
    number: "01",
    title: "Define",
    description: "Describe your agent's purpose, tools, and constraints using our intuitive SDK or visual builder. No PhD required.",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    number: "02",
    title: "Deploy",
    description: "One command to production. Auto-scaling infrastructure handles millions of requests. Zero DevOps needed.",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    number: "03",
    title: "Evolve",
    description: "Agents learn from every interaction. Built-in analytics, A/B testing, and continuous improvement loops.",
    gradient: "from-green-500 to-emerald-500",
  },
]

export function HowItWorks() {
  return (
    <section id="how" className="relative py-32 px-6 overflow-hidden">
      <DotPattern className="z-0" />
      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <Badge className="mb-4">How It Works</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter">
            Three steps to
            <br />
            <span className="text-muted-foreground">autonomous intelligence.</span>
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="relative"
            >
              <div className={`text-[100px] font-black leading-none tracking-tighter bg-gradient-to-b ${step.gradient} bg-clip-text text-transparent opacity-20`}>
                {step.number}
              </div>
              <h3 className="text-2xl font-bold mt-2 mb-3">{step.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{step.description}</p>
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 -right-6 w-12 h-px bg-gradient-to-r from-white/20 to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
