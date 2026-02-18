"use client"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BorderBeam } from "@/components/magicui/border-beam"
import { AnimatedGridPattern } from "@/components/magicui/animated-grid"
import { ArrowRight, Play, Terminal } from "lucide-react"
import { useState, useEffect } from "react"

const typewriterLines = [
  "Build a customer support agent with memory and escalation logic",
  "Create a research pipeline that crawls, summarizes, and evaluates sources",
  "Deploy a multi-agent workflow for automated code review with eval metrics",
  "Design an onboarding agent with adaptive conversation flow",
]

function useTypewriter(lines: string[], typingSpeed = 40, pauseDuration = 2000) {
  const [text, setText] = useState("")
  const [lineIndex, setLineIndex] = useState(0)
  const [charIndex, setCharIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const currentLine = lines[lineIndex]
    let timeout: NodeJS.Timeout

    if (!isDeleting && charIndex < currentLine.length) {
      timeout = setTimeout(() => {
        setText(currentLine.slice(0, charIndex + 1))
        setCharIndex(charIndex + 1)
      }, typingSpeed)
    } else if (!isDeleting && charIndex === currentLine.length) {
      timeout = setTimeout(() => setIsDeleting(true), pauseDuration)
    } else if (isDeleting && charIndex > 0) {
      timeout = setTimeout(() => {
        setText(currentLine.slice(0, charIndex - 1))
        setCharIndex(charIndex - 1)
      }, typingSpeed / 2)
    } else if (isDeleting && charIndex === 0) {
      setIsDeleting(false)
      setLineIndex((lineIndex + 1) % lines.length)
    }
    return () => clearTimeout(timeout)
  }, [charIndex, isDeleting, lineIndex, lines, typingSpeed, pauseDuration])

  return text
}

export function Hero() {
  const typed = useTypewriter(typewriterLines)

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center text-center px-6 pt-24 pb-20 overflow-hidden">
      <AnimatedGridPattern className="z-0" />
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-blue-500/15 blur-[120px] animate-pulse-slow" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-purple-500/15 blur-[120px] animate-pulse-slow [animation-delay:2s]" />

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
          Powered by Azure AI Foundry
        </Badge>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="relative z-10 text-5xl sm:text-7xl lg:text-8xl font-black tracking-tighter leading-[0.9]"
      >
        Describe it.
        <br />
        <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
          We deploy it.
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="relative z-10 mt-6 text-lg sm:text-xl text-muted-foreground max-w-2xl leading-relaxed"
      >
        Prompt what your agents should do. We handle the architecture, evaluation
        framework, memory layer, and deployment to Azure AI Foundry — in minutes, not months.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="relative z-10 flex flex-col sm:flex-row items-center gap-4 mt-10"
      >
        <Button variant="glow" size="lg" className="gap-2 group">
          Start Building
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
        </Button>
        <Button variant="secondary" size="lg" className="gap-2">
          <Play className="h-4 w-4" />
          See it in action
        </Button>
      </motion.div>

      {/* Interactive prompt preview */}
      <motion.div
        initial={{ opacity: 0, y: 60 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="relative z-10 mt-20 w-full max-w-4xl"
      >
        <div className="relative rounded-2xl border border-white/[0.08] bg-black/60 backdrop-blur-xl shadow-2xl shadow-blue-500/5">
          <BorderBeam size={250} duration={12} delay={0} />
          <div className="p-8">
            <div className="flex items-center gap-2 mb-6">
              <div className="h-3 w-3 rounded-full bg-[#ff5f57]" />
              <div className="h-3 w-3 rounded-full bg-[#febc2e]" />
              <div className="h-3 w-3 rounded-full bg-[#28c840]" />
              <span className="ml-4 text-xs text-muted-foreground font-mono">agents-platform</span>
            </div>

            <div className="flex items-start gap-3 mb-6">
              <div className="shrink-0 mt-1 h-6 w-6 rounded-md bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                <Terminal className="h-3 w-3 text-white" />
              </div>
              <div className="flex-1 min-h-[3rem]">
                <p className="text-sm text-muted-foreground mb-1">Describe what your agents should do:</p>
                <p className="text-white text-base font-mono">
                  {typed}<span className="animate-pulse text-blue-400">|</span>
                </p>
              </div>
            </div>

            <div className="border-t border-white/[0.06] pt-6">
              <p className="text-xs text-muted-foreground mb-4 uppercase tracking-wider font-medium">Generated Architecture</p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {[
                  { label: "Orchestrator", status: "Configured" },
                  { label: "Memory Layer", status: "Cosmos DB" },
                  { label: "Eval Framework", status: "3 metrics" },
                  { label: "Deployment", status: "AI Foundry" },
                ].map((item) => (
                  <div key={item.label} className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-3">
                    <div className="text-xs text-muted-foreground">{item.label}</div>
                    <div className="text-sm font-medium mt-1 text-green-400">{item.status}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  )
}
