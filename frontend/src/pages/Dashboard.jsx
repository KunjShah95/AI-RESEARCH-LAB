import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Search, BookOpen, GitCompare, MessageSquare, 
  Sparkles, Brain, Network, Zap, Loader2
} from 'lucide-react'
import { papersApi } from '../services/api'

const categories = [
  { id: 'cs.AI', name: 'Artificial Intelligence' },
  { id: 'cs.LG', name: 'Machine Learning' },
  { id: 'cs.CL', name: 'Computation & Language' },
  { id: 'cs.CV', name: 'Computer Vision' },
  { id: 'cs.NE', name: 'Neural & Evolutionary' },
  { id: 'stat.ML', name: 'Machine Learning (Stats)' },
]

const mockPapers = [
  {
    id: '1',
    title: 'Attention Is All You Need',
    authors: ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar'],
    year: 2017,
    source: 'arxiv',
    abstract: 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder.',
    citations: 95000,
    openAccess: true,
  },
  {
    id: '2',
    title: 'BERT: Pre-training of Deep Bidirectional Transformers',
    authors: ['Jacob Devlin', 'Ming-Wei Chang', 'Kenton Lee'],
    year: 2018,
    source: 'arxiv',
    abstract: 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.',
    citations: 85000,
    openAccess: true,
  },
  {
    id: '3',
    title: 'GPT-4 Technical Report',
    authors: ['OpenAI'],
    year: 2023,
    source: 'arxiv',
    abstract: 'We report the development of GPT-4, a large-scale, multimodal model which can accept image and text inputs and produce text outputs.',
    citations: 5000,
    openAccess: false,
  },
  {
    id: '4',
    title: 'Llama 2: Open Foundation and Chat Models',
    authors: ['Hugo Touvron', 'Louis Martin', 'Kevin Stone'],
    year: 2023,
    source: 'arxiv',
    abstract: 'We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters.',
    citations: 3000,
    openAccess: true,
  },
  {
    id: '5',
    title: 'Chain-of-Thought Prompting Elicits Reasoning',
    authors: ['Jason Wei', 'Xuezhi Wang', 'Dale Schuurmans'],
    year: 2022,
    source: 'arxiv',
    abstract: 'We explore how chain of thought prompting can improve the reasoning abilities of large language models.',
    citations: 8000,
    openAccess: true,
  },
]

function FeatureCard({ icon: Icon, title, description, to, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="feature-card"
    >
      <Link to={to}>
        <div className="feature-icon">
          <Icon size={24} />
        </div>
        <h3>{title}</h3>
        <p>{description}</p>
      </Link>
    </motion.div>
  )
}

export default function Dashboard() {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState('semantic')
  const [recentPapers, setRecentPapers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRecentPapers = async () => {
      try {
        const result = await papersApi.search('transformer', { max_results: 5 })
        if (result.papers && result.papers.length > 0) {
          setRecentPapers(result.papers)
        } else {
          setRecentPapers(mockPapers.slice(0, 3))
        }
      } catch (error) {
        console.log('Using mock papers - API not available')
        setRecentPapers(mockPapers.slice(0, 3))
      } finally {
        setLoading(false)
      }
    }
    fetchRecentPapers()
  }, [])

  return (
    <div className="dashboard">
      <header className="hero">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="hero-content"
        >
          <h1>Research Lab</h1>
          <p className="tagline">AI-powered literature analysis with source-grounded citations</p>
        </motion.div>
      </header>

      <section className="search-section">
        <div className="search-container">
          <div className="search-type-tabs">
            <button 
              className={searchType === 'semantic' ? 'active' : ''}
              onClick={() => setSearchType('semantic')}
            >
              <Brain size={16} /> Semantic
            </button>
            <button 
              className={searchType === 'keyword' ? 'active' : ''}
              onClick={() => setSearchType('keyword')}
            >
              <Search size={16} /> Keyword
            </button>
            <button 
              className={searchType === 'boolean' ? 'active' : ''}
              onClick={() => setSearchType('boolean')}
            >
              <Zap size={16} /> Boolean
            </button>
            <button 
              className={searchType === 'citation' ? 'active' : ''}
              onClick={() => setSearchType('citation')}
            >
              <Network size={16} /> Citation
            </button>
          </div>
          
          <div className="search-input-wrapper">
            <input
              type="text"
              placeholder="Search papers, topics, or ask a research question..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="search-input"
            />
            <Link to={`/app/search?q=${encodeURIComponent(query)}`}>
              <button className="search-button">
                <Search size={20} />
              </button>
            </Link>
          </div>
          
          <div className="quick-categories">
            {categories.slice(0, 4).map(cat => (
              <button 
                key={cat.id} 
                className="category-pill"
                onClick={() => setQuery(cat.id)}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="features-grid">
        <FeatureCard
          icon={BookOpen}
          title="Smart Summaries"
          description="Generate multi-granularity summaries with confidence scores"
          to="/app/search"
          delay={0.1}
        />
        <FeatureCard
          icon={GitCompare}
          title="Method Comparison"
          description="Side-by-side comparison of datasets, metrics, and approaches"
          to="/app/compare"
          delay={0.2}
        />
        <FeatureCard
          icon={MessageSquare}
          title="AI Debates"
          description="Multi-agent debates with Proponent, Critic, and Methodologist"
          to="/app/debate"
          delay={0.3}
        />
        <FeatureCard
          icon={Sparkles}
          title="Insight Synthesis"
          description="Identify research gaps and generate recommendations"
          to="/app/synthesize"
          delay={0.4}
        />
      </section>

<section className="recent-activity">
        <h2>Recent Papers</h2>
        <div className="papers-list">
          {loading ? (
            <div className="loading-state">
              <Loader2 className="spinner" size={32} />
              <p>Loading papers...</p>
            </div>
          ) : (
            recentPapers.map((paper, i) => (
              <motion.div 
                key={paper.id || i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.1 }}
                className="paper-card"
              >
                <div className="paper-badge">{paper.source || 'arxiv'}</div>
                <h3>{paper.title}</h3>
                <p className="paper-authors">{paper.authors?.join(', ') || 'Unknown Authors'}</p>
                <div className="paper-meta">
                  <span>{paper.year || 'N/A'}</span>
                  <span>{(paper.citations || 0).toLocaleString()} citations</span>
                  <span className={paper.openAccess ? 'open-access' : 'paywalled'}>
                    {paper.openAccess ? 'Open Access' : 'Paywalled'}
                  </span>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </section>
    </div>
  )
}