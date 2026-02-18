"use client"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BorderBeam } from "@/components/magicui/border-beam"
import { AnimatedGridPattern } from "@/components/magicui/animated-grid"
import { ArrowRight, Play, Sparkles } from "lucide-react"

export function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center text-center px-6 pt-24 pb-20 overflow-hidden">
      {/* Background effects */}
      <AnimatedGridPattern className="z-0" />
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-blue-500/20 blur-[120px] animate-pulse-slow" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-purple-500/20 blur-[120px] animate-pulse-slow [animation-delay:2s]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-green-500/10 blur-[150px] animate-pulse-slow [animation-delay:4s]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10"
      >
        <Badge className="mb-6 gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
          </span>
          Now in Public Beta
        </Badge>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="relative z-10 text-5xl sm:text-7xl lg:text-8xl font-black tracking-tighter leading-[0.9]"
      >
        Build the future
        <br />
        <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
          with AI Agents
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="relative z-10 mt-6 text-lg sm:text-xl text-muted-foreground max-w-2xl leading-relaxed"
      >
        Deploy autonomous agents that think, reason, and execute.
        The platform that powers the next generation of intelligent automation.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="relative z-10 flex flex-col sm:flex-row items-center gap-4 mt-10"
      >
        <Button variant="glow" size="lg" className="gap-2 group">
          <Sparkles className="h-4 w-4" />
          Start Building — Free
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
        </Button>
        <Button variant="secondary" size="lg" className="gap-2">
          <Play className="h-4 w-4" />
          Watch Demo
        </Button>
      </motion.div>

      {/* Agent Dashboard Preview */}
      <motion.div
        initial={{ opacity: 0, y: 60 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="relative z-10 mt-20 w-full max-w-5xl"
      >
        <div className="relative rounded-2xl border border-white/[0.08] bg-black/50 backdrop-blur-xl p-1 shadow-2xl shadow-blue-500/5">
          <BorderBeam size={250} duration={12} delay={0} />
          <div className="rounded-xl bg-gradient-to-b from-white/[0.04] to-transparent p-8">
            {/* Fake dashboard */}
            <div className="flex items-center gap-2 mb-6">
              <div className="h-3 w-3 rounded-full bg-red-500/80" />
              <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
              <div className="h-3 w-3 rounded-full bg-green-500/80" />
              <span className="ml-4 text-xs text-muted-foreground font-mono">agents-platform — dashboard</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                { icon: "🧠", name: "Research Agent", status: "Active", progress: 87, color: "from-blue-500 to-cyan-500" },
                { icon: "📊", name: "Analytics Agent", status: "Processing", progress: 62, color: "from-purple-500 to-pink-500" },
                { icon: "🔗", name: "Integration Agent", status: "Connected", progress: 95, color: "from-green-500 to-emerald-500" },
                { icon: "💬", name: "Communication Agent", status: "Listening", progress: 78, color: "from-orange-500 to-red-500" },
                { icon: "🛡️", name: "Security Agent", status: "Monitoring", progress: 100, color: "from-blue-500 to-purple-500" },
                { icon: "⚙️", name: "Orchestrator", status: "Running", progress: 91, color: "from-pink-500 to-purple-500" },
              ].map((agent) => (
                <div key={agent.name} className="group rounded-xl border border-white/[0.06] bg-white/[0.02] p-5 hover:border-blue-500/20 hover:bg-blue-500/[0.03] transition-all duration-500">
                  <div className="text-2xl mb-3">{agent.icon}</div>
                  <div className="text-sm font-semibold mb-1">{agent.name}</div>
                  <div className="flex items-center gap-1.5 text-xs text-green-400 mb-3">
                    <span className="h-1.5 w-1.5 rounded-full bg-green-400" />
                    {agent.status}
                  </div>
                  <div className="h-1 rounded-full bg-white/[0.06] overflow-hidden">
                    <div
                      className={`h-full rounded-full bg-gradient-to-r ${agent.color} transition-all duration-1000`}
                      style={{ width: `${agent.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  )
}
