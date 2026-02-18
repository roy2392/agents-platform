"use client"
import { motion } from "framer-motion"
import { SpotlightCard } from "@/components/magicui/spotlight"
import { Badge } from "@/components/ui/badge"
import { Brain, Zap, Plug, Shield, Code2, Layers } from "lucide-react"

const features = [
  {
    icon: Brain,
    title: "Multi-Agent Orchestration",
    description: "Coordinate dozens of specialized agents working in parallel. Define goals, set constraints, and let the platform handle execution.",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    icon: Zap,
    title: "Real-Time Reasoning",
    description: "Agents analyze, plan, and adapt in milliseconds. Built on cutting-edge LLM infrastructure with sub-100ms response times.",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    icon: Plug,
    title: "Universal Integrations",
    description: "Connect to 500+ tools and services out of the box. APIs, databases, SaaS — your agents speak every protocol.",
    gradient: "from-green-500 to-emerald-500",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "SOC 2 Type II certified. End-to-end encryption, role-based access, and comprehensive audit logs for every agent action.",
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
          <Badge className="mb-4">Capabilities</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter leading-[1.05]">
            Everything you need
            <br />
            <span className="text-muted-foreground">to orchestrate intelligence.</span>
          </h2>
          <p className="mt-6 text-lg text-muted-foreground max-w-xl">
            From simple automations to complex multi-agent systems,
            Agents Platform gives you the building blocks to create anything.
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
                <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.gradient} bg-opacity-10 mb-5`}>
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </SpotlightCard>
            </motion.div>
          ))}
        </div>

        {/* Code block feature */}
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
                  <Code2 className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-2xl sm:text-3xl font-bold tracking-tight mb-4">
                  Deploy in minutes,<br />not months.
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  Define your agent&apos;s capabilities with simple, declarative code.
                  Our SDK handles the complexity — you focus on the logic.
                </p>
              </div>
              <div className="rounded-xl bg-black/60 border border-white/[0.06] p-6 font-mono text-sm leading-loose overflow-x-auto">
                <div className="text-purple-400">import</div>
                <div className="pl-4 text-blue-300">{`{ Agent, Tool }`}</div>
                <div><span className="text-purple-400">from</span> <span className="text-green-400">&apos;@agents/sdk&apos;</span></div>
                <br />
                <div><span className="text-purple-400">const</span> agent = <span className="text-purple-400">new</span> <span className="text-blue-300">Agent</span>({`{`}</div>
                <div className="pl-4">name: <span className="text-green-400">&apos;research-bot&apos;</span>,</div>
                <div className="pl-4">model: <span className="text-green-400">&apos;gpt-5-turbo&apos;</span>,</div>
                <div className="pl-4">tools: [<span className="text-blue-300">webSearch</span>, <span className="text-blue-300">analyze</span>],</div>
                <div className="pl-4">memory: <span className="text-purple-400">true</span>,</div>
                <div>{`}`})</div>
                <br />
                <div><span className="text-purple-400">await</span> agent.<span className="text-blue-300">deploy</span>()</div>
                <div className="text-muted-foreground">{"// 🚀 Live in 30 seconds"}</div>
              </div>
            </div>
          </SpotlightCard>
        </motion.div>
      </div>
    </section>
  )
}
