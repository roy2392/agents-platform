"use client"

const words = [
  "Azure AI Foundry",
  "Cosmos DB",
  "Semantic Kernel",
  "Prompt Flow",
  "Content Safety",
  "AI Evaluation",
  "Multi-Agent Systems",
  "Responsible AI",
]

export function LogoCloud() {
  return (
    <section className="relative border-y border-white/[0.06] py-16 overflow-hidden">
      <div className="flex gap-12 animate-marquee whitespace-nowrap">
        {[...words, ...words, ...words].map((word, i) => (
          <span
            key={i}
            className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tighter text-white/[0.04] hover:text-white/[0.1] transition-colors duration-300 select-none"
          >
            {word}
            <span className="text-blue-500/60 mx-6">/</span>
          </span>
        ))}
      </div>
    </section>
  )
}
