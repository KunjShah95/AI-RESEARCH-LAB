import { motion } from 'framer-motion'
import { 
  Search, BookOpen, GitCompare, MessageSquare, Sparkles, FileText,
  Network, Clock, Shield, Beaker, Zap, Brain, FolderOpen, Clipboard
} from 'lucide-react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'

export default function Features() {
  const features = [
    { icon: Search, title: 'Smart Search', desc: 'Semantic, keyword, boolean, and hybrid search', path: '/app/search' },
    { icon: BookOpen, title: 'Paper Summaries', desc: 'Multi-granularity summaries with confidence scores', path: '/app/summarize' },
    { icon: GitCompare, title: 'Paper Comparison', desc: 'Side-by-side comparison of methods and results', path: '/app/compare' },
    { icon: MessageSquare, title: 'AI Debates', desc: 'Multi-agent debates with Proponent, Critic, Methodologist', path: '/app/debate' },
    { icon: Sparkles, title: 'Insight Synthesis', desc: 'Identify research gaps and generate recommendations', path: '/app/synthesize' },
    { icon: FileText, title: 'Paper Writer', desc: 'Generate complete research papers in multiple formats', path: '/app/write' },
    { icon: Network, title: 'Citation Graph', desc: 'Visual citation network analysis', path: '/app/graph' },
    { icon: Clock, title: 'Research Timeline', desc: 'Timeline of papers by year and topic', path: '/app/timeline' },
    { icon: FolderOpen, title: 'Projects', desc: 'Organize papers into projects with notes', path: '/app/projects' },
    { icon: Clipboard, title: 'Citation Clipboard', desc: 'One-click citation in 7 formats', path: '/app/clipboard' },
    { icon: Brain, title: 'Q&A Chat', desc: 'Ask questions about papers and get AI answers', path: '/app/qa' },
    { icon: Zap, title: 'Advanced Search', desc: 'Semantic, hybrid, boolean, and vector search', path: '/app/advanced-search' },
  ]

  return (
    <div className="features-page">
      <Navbar />
      <header className="features-header">
        <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          Features
        </motion.h1>
        <p>Everything you need for academic research</p>
      </header>

      <div className="features-grid">
        {features.map((f, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Link to={f.path} className="feature-card">
              <f.icon size={28} />
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  )
}