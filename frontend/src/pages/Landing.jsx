import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, BookOpen, GitCompare, MessageSquare, Sparkles, FileText, Beaker, ArrowRight } from 'lucide-react'

export default function LandingPage() {
  const features = [
    { icon: Search, title: 'Semantic Search', desc: 'Search across arXiv, Semantic Scholar, PubMed with deep understanding', color: '#d4a853' },
    { icon: BookOpen, title: 'Smart Summaries', desc: 'Multi-granularity summaries with confidence scores & citations', color: '#c9956c' },
    { icon: GitCompare, title: 'Method Comparison', desc: 'Side-by-side analysis of datasets, metrics & architectures', color: '#a38742' },
    { icon: MessageSquare, title: 'AI Debates', desc: 'Multi-agent debates with Proponent, Critic & Methodologist', color: '#d4a853' },
    { icon: Sparkles, title: 'Insight Synthesis', desc: 'Identify research gaps & generate actionable recommendations', color: '#c9956c' },
    { icon: FileText, title: 'Paper Writing', desc: 'Generate literature reviews with source-grounded citations', color: '#a38742' },
  ]
  
  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-nav">
          <div className="logo">
            <Beaker className="logo-icon" />
            <span className="logo-text">Research Lab</span>
          </div>
          <div className="nav-links">
            <Link to="/features" className="nav-link">Features</Link>
            <Link to="/about" className="nav-link">About</Link>
            <Link to="/login" className="nav-link">Sign In</Link>
            <Link to="/signup" className="btn-primary">Get Started</Link>
          </div>
        </div>
      </header>
      
      <section className="hero-section">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="hero-content"
        >
          <span className="badge">AI-Powered Research Assistant</span>
          <h1>Accelerate Your <em>Literature Review</em></h1>
          <p className="hero-desc">
            Discover, summarize, compare, and synthesize academic papers with source-grounded citations. 
            Let AI agents debate research claims to uncover deeper insights.
          </p>
          <div className="hero-actions">
            <Link to="/signup" className="btn-hero-primary">
              Start Free Research <ArrowRight size={20} />
            </Link>
            <Link to="/login" className="btn-hero-secondary">
              View Demo
            </Link>
          </div>
          
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">50K+</span>
              <span className="stat-label">Papers Indexed</span>
            </div>
            <div className="stat">
              <span className="stat-number">10×</span>
              <span className="stat-label">Faster Review</span>
            </div>
            <div className="stat">
              <span className="stat-number">99%</span>
              <span className="stat-label">Citation Accuracy</span>
            </div>
          </div>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="hero-visual"
        >
          <div className="dashboard-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span></span><span></span><span></span>
              </div>
              <span className="preview-title">Research Lab Dashboard</span>
            </div>
            <div className="preview-content">
              <div className="preview-search">
                <Search size={18} />
                <span>Search papers, topics, or ask a research question...</span>
              </div>
              <div className="preview-features">
                <div className="preview-card">
                  <BookOpen size={16} />
                  <span>Smart Summaries</span>
                </div>
                <div className="preview-card">
                  <GitCompare size={16} />
                  <span>Compare Methods</span>
                </div>
                <div className="preview-card">
                  <MessageSquare size={16} />
                  <span>AI Debates</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>
      
      <section className="features-section">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="section-header"
        >
          <h2>Everything You Need for Research</h2>
          <p>Powerful AI tools to accelerate your academic workflow — from discovery to synthesis</p>
        </motion.div>
        
        <div className="features-grid-landing">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="feature-card-landing"
            >
              <div className="feature-icon-landing" style={{ background: feature.color }}>
                <feature.icon size={24} />
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
            </motion.div>
          ))}
        </div>
        
        <div className="section-divider">
          <span>Where knowledge meets innovation</span>
        </div>
      </section>
      
      <section className="cta-section">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="cta-box"
        >
          <h2>Ready to Transform Your Research?</h2>
          <p>Join thousands of researchers who have discovered a faster, smarter way to explore academic literature</p>
          <Link to="/signup" className="btn-hero-primary">
            Begin Your Journey <ArrowRight size={20} />
          </Link>
        </motion.div>
      </section>
      
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="logo">
            <Beaker className="logo-icon" />
            <span className="logo-text">Research Lab</span>
          </div>
          <p>© 2026 Research Lab. AI-powered literature analysis.</p>
        </div>
      </footer>
    </div>
  )
}