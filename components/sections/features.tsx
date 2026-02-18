"use client"
import { motion } from "framer-motion"
import { SpotlightCard } from "@/components/magicui/spotlight"
import { Badge } from "@/components/ui/badge"
import { Layers, BarChart3, Database, GitBranch, Shield, Workflow } from "lucide-react"

const features = [
  {
    icon: Workflow,
    title: "Multi-Agent Orchestration",
    description: "Define complex agent workflows with routing, handoffs, and parallel execution. The platform decomposes your prompt into the right agent topology automatically.",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    icon: BarChart3,
    title: "Built-in Evaluation",
    description: "Every deployed agent ships with evaluation metrics — groundedness, relevance, coherence, and custom domain-specific evals. No afterthought, it's part of the architecture.",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    icon: Database,
    title: "Persistent Memory",
    description: "Conversation memory, semantic search over past interactions, and long-term knowledge storage backed by Cosmos DB. Agents that actually remember context.",
    gradient: "from-green-500 to-emerald-500",
  },
  {
    icon: Shield,
    title: "Responsible AI Guardrails",
    description: "Content safety filters, PII detection, jailbreak protection, and custom policy enforcement built into every deployment. Enterprise-grade from day one.",
    gradient: "from-orange-500 to-red-500",
  },
]

export function Features() {
  return (
    <section id="features" className="relative py-32 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <Badge className="mb-4">Agent Design System</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter leading-[1.05]">
            Not just agents.
            <br />
            <span className="text-muted-foreground">Production-grade agent systems.</span>
          </h2>
          <p className="mt-6 text-lg text-muted-foreground max-w-xl">
            Every deployment includes the full stack — orchestration, memory, evaluation,
            and guardrails. The things most teams bolt on later, we build in from the start.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <SpotlightCard className="h-full">
                <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.gradient} mb-5`}>
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </SpotlightCard>
            </motion.div>
          ))}
        </div>

        {/* Architecture diagram card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-6"
        >
          <SpotlightCard className="overflow-hidden">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="inline-flex p-3 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 mb-5">
                  <Layers className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-2xl sm:text-3xl font-bold tracking-tight mb-4">
                  From prompt to production<br />in a single command.
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  You describe the task. The platform generates the agent graph,
                  configures memory and eval, provisions Azure resources, and deploys —
                  complete with monitoring and an API endpoint.
                </p>
              </div>
              <div className="rounded-xl bg-black/60 border border-white/[0.06] p-6 font-mono text-sm leading-loose overflow-x-auto">
                <div className="text-muted-foreground"># Define your agent system</div>
                <div><span className="text-purple-400">agents</span> deploy \</div>
                <div className="pl-4">--prompt <span className="text-green-400">&quot;Customer support agent</span></div>
                <div className="pl-4"><span className="text-green-400">  with order lookup, refund processing,</span></div>
                <div className="pl-4"><span className="text-green-400">  and escalation to human agents&quot;</span> \</div>
                <div className="pl-4">--memory <span className="text-blue-300">cosmos-db</span> \</div>
                <div className="pl-4">--eval <span className="text-blue-300">groundedness,relevance,coherence</span> \</div>
                <div className="pl-4">--target <span className="text-blue-300">azure-ai-foundry</span></div>
                <br />
                <div className="text-muted-foreground"># Output:</div>
                <div className="text-green-400">Deployed 3 agents to AI Foundry</div>
                <div className="text-green-400">Endpoint: https://your-project.inference.ai.azure.com</div>
                <div className="text-green-400">Eval dashboard: https://ai.azure.com/evals/run-42</div>
              </div>
            </div>
          </SpotlightCard>
        </motion.div>
      </div>
    </section>
  )
}
