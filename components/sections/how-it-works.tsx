"use client"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { DotPattern } from "@/components/magicui/dot-pattern"

const steps = [
  {
    number: "01",
    title: "Prompt",
    description: "Describe the task or workflow in plain language. What should the agent do? What tools does it need? What are the success criteria?",
    gradient: "from-blue-500 to-cyan-500",
    detail: "Natural language in, agent architecture out.",
  },
  {
    number: "02",
    title: "Generate",
    description: "The platform decomposes your prompt into an agent graph — orchestrator, sub-agents, tool bindings, memory config, and evaluation framework. Review and adjust before deploying.",
    gradient: "from-purple-500 to-pink-500",
    detail: "Full architecture generated in seconds.",
  },
  {
    number: "03",
    title: "Deploy",
    description: "One click to Azure AI Foundry. Agents are provisioned with Cosmos DB memory, content safety filters, eval pipelines, and a production-ready API endpoint with monitoring.",
    gradient: "from-green-500 to-emerald-500",
    detail: "Production-ready from the first deployment.",
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
            Prompt. Generate. Deploy.
          </h2>
          <p className="mt-4 text-lg text-muted-foreground max-w-xl mx-auto">
            Go from idea to deployed agent system on Azure AI Foundry in three steps.
          </p>
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
              <p className="text-muted-foreground leading-relaxed mb-4">{step.description}</p>
              <p className="text-sm text-white/40 font-medium italic">{step.detail}</p>
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-16 -right-6 w-12 h-px bg-gradient-to-r from-white/20 to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
