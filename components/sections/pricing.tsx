"use client"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { BorderBeam } from "@/components/magicui/border-beam"
import { Check } from "lucide-react"

const plans = [
  {
    name: "Builder",
    price: "Free",
    description: "Explore and prototype agent systems",
    features: [
      "3 agent deployments",
      "1,000 executions / month",
      "Basic eval metrics",
      "Community support",
      "Shared Azure resources",
    ],
    cta: "Start Building",
    popular: false,
  },
  {
    name: "Team",
    price: "$149",
    period: "/mo",
    description: "For teams shipping agents to production",
    features: [
      "Unlimited deployments",
      "50,000 executions / month",
      "Full eval framework + custom evals",
      "Cosmos DB memory (dedicated)",
      "Priority support",
      "Bring your own Azure subscription",
      "99.9% SLA",
    ],
    cta: "Start Free Trial",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "For organizations operating at scale",
    features: [
      "Everything in Team",
      "Unlimited executions",
      "Dedicated Azure resources",
      "SSO, RBAC, audit logs",
      "Custom guardrails & policies",
      "Dedicated solutions engineer",
      "On-premise deployment option",
      "SLA negotiation",
    ],
    cta: "Talk to Us",
    popular: false,
  },
]

export function Pricing() {
  return (
    <section id="pricing" className="relative py-32 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <Badge className="mb-4">Pricing</Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter">
            Start free.
            <br />
            <span className="text-muted-foreground">Scale with your agents.</span>
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <Card className={`relative p-8 h-full flex flex-col ${plan.popular ? "border-blue-500/30 bg-blue-500/[0.03]" : ""}`}>
                {plan.popular && <BorderBeam size={200} duration={10} />}
                {plan.popular && (
                  <Badge variant="default" className="absolute -top-3 left-1/2 -translate-x-1/2">
                    Most Popular
                  </Badge>
                )}
                <div className="mb-6">
                  <h3 className="text-lg font-bold mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-black tracking-tight">{plan.price}</span>
                    {plan.period && <span className="text-muted-foreground">{plan.period}</span>}
                  </div>
                  <p className="text-sm text-muted-foreground mt-2">{plan.description}</p>
                </div>
                <ul className="space-y-3 mb-8 flex-1">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-center gap-3 text-sm">
                      <Check className="h-4 w-4 text-green-400 shrink-0" />
                      <span className="text-white/80">{f}</span>
                    </li>
                  ))}
                </ul>
                <Button variant={plan.popular ? "glow" : "secondary"} className="w-full">
                  {plan.cta}
                </Button>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
