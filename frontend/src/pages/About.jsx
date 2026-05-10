import { motion } from 'framer-motion'
import { Beaker, Brain, BookOpen, Sparkles, Shield } from 'lucide-react'
import Navbar from '../components/Navbar'

export default function About() {
  const features = [
    { icon: Brain, title: 'AI-Powered Analysis', desc: 'Multi-agent AI for research synthesis' },
    { icon: BookOpen, title: 'Multi-Source Search', desc: 'arXiv, Semantic Scholar, PubMed, CrossRef' },
    { icon: Sparkles, title: 'Paper Generation', desc: 'Write complete research papers automatically' },
    { icon: Shield, title: 'Citation Tracking', desc: 'Track citations and research gaps' },
  ]

  return (
    <div className="about-page">
      <Navbar />
      <section className="about-hero">
        <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          About Research Lab
        </motion.h1>
        <p className="tagline">AI-powered literature analysis for the modern researcher</p>
      </section>

      <section className="about-mission">
        <h2>Our Mission</h2>
        <p>
          Research Lab automates the tedious aspects of academic research. 
          From discovering relevant papers to generating literature reviews, 
          our AI assistants help you focus on what matters — your research.
        </p>
      </section>

      <section className="about-features">
        <h2>Key Features</h2>
        <div className="features-grid">
          {features.map((f, i) => (
            <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.1 }} className="feature-item">
              <f.icon size={32} />
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="about-team">
        <h2>Built With</h2>
        <div className="tech-stack">
          <span>FastAPI</span>
          <span>CrewAI</span>
          <span>LangGraph</span>
          <span>React</span>
          <span>PostgreSQL</span>
        </div>
      </section>
    </div>
  )
}