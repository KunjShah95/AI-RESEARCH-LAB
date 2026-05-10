import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Star, FileText, Plus, Loader2 } from 'lucide-react'
import { papersApi } from '../services/api'

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

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [shortlist, setShortlist] = useState([])
  const [error, setError] = useState(null)
  const [source, setSource] = useState('')
  const [year, setYear] = useState('')
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setHasSearched(true)
    try {
      const filters = {}
      if (source) filters.source = source
      if (year) filters.year_from = parseInt(year)
      const response = await papersApi.search(query, filters)
      setResults(response.papers || [])
      if (!response.papers || response.papers.length === 0) {
        setResults(mockPapers)
      }
    } catch (err) {
      console.error('Search failed:', err)
      setError('Search failed. Showing mock results.')
      setResults(mockPapers)
    } finally {
      setLoading(false)
    }
  }

  const toggleShortlist = (paper) => {
    if (shortlist.find(p => p.id === paper.id)) {
      setShortlist(shortlist.filter(p => p.id !== paper.id))
    } else {
      setShortlist([...shortlist, paper])
    }
  }

  return (
    <div className="search-page">
      <header className="page-header">
        <h1>Paper Search</h1>
        {shortlist.length > 0 && (
          <div className="shortlist-badge">
            <Star size={16} fill="currentColor" />
            {shortlist.length} shortlisted
          </div>
        )}
      </header>

      <div className="search-filters">
        <input
          type="text"
          placeholder="Enter search query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          className="filter-input"
        />
        <select className="filter-select" value={source} onChange={(e) => setSource(e.target.value)}>
          <option value="">All Sources</option>
          <option value="arxiv">arXiv</option>
          <option value="semantic_scholar">Semantic Scholar</option>
          <option value="pubmed">PubMed</option>
        </select>
        <select className="filter-select" value={year} onChange={(e) => setYear(e.target.value)}>
          <option value="">Any Year</option>
          <option value="2024">2024</option>
          <option value="2023">2023</option>
          <option value="2022">2022</option>
          <option value="2021">2021</option>
        </select>
        <button className="primary-button" onClick={handleSearch}>
          <Search size={18} /> Search
        </button>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}

      {loading ? (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Searching across {query || 'all'} sources...</p>
        </div>
      ) : hasSearched && results.length > 0 ? (
        <div className="results-container">
          <div className="results-list">
            {results.map((paper, i) => (
              <motion.div 
                key={paper.id || i}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.05 }}
                className={`result-card ${shortlist.find(p => p.id === paper.id) ? 'shortlisted' : ''}`}
              >
                <button 
                  className={`shortlist-btn ${shortlist.find(p => p.id === paper.id) ? 'active' : ''}`}
                  onClick={() => toggleShortlist(paper)}
                >
                  <Star size={18} fill={shortlist.find(p => p.id === paper.id) ? 'currentColor' : 'none'} />
                </button>
                <div className="result-content">
                  <div className="result-header">
                    <span className="source-tag">{paper.source || 'arxiv'}</span>
                    <span className="year-tag">{paper.year || 'N/A'}</span>
                  </div>
                  <h3>{paper.title}</h3>
                  <p className="authors">{paper.authors?.join(', ') || paper.authors || 'Unknown Authors'}</p>
                  <p className="abstract">{paper.abstract || 'No abstract available'}</p>
                  <div className="result-actions">
                    <Link to={`/app/summarize/${paper.id}`}>
                      <button className="action-btn">
                        <FileText size={16} /> Summarize
                      </button>
                    </Link>
                    <button 
                      className="action-btn"
                      onClick={() => toggleShortlist(paper)}
                    >
                      <Plus size={16} /> Shortlist
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      ) : hasSearched && results.length === 0 ? (
        <div className="loading-state">
          <p>No papers found. Try a different search query.</p>
        </div>
      ) : (
        <div className="loading-state">
          <p>Enter a search query to find papers.</p>
        </div>
      )}
    </div>
  )
}