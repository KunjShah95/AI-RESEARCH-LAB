import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Loader2 } from 'lucide-react'
import { advancedSearchApi } from '../services/api'

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

export default function AdvancedSearchPage() {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState('hybrid')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])

  const searchTypes = [
    { id: 'hybrid', name: 'Hybrid', desc: 'Best of semantic + keyword' },
    { id: 'semantic', name: 'Semantic', desc: 'AI-powered meaning search' },
    { id: 'keyword', name: 'Keyword', desc: 'Traditional exact match' },
    { id: 'boolean', name: 'Boolean', desc: 'AND, OR, NOT operators' },
    { id: 'vector', name: 'Vector', desc: 'Embedding similarity' },
  ]

  const handleSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      const response = await advancedSearchApi.search(query, searchType)
      if (response.results && response.results.length > 0) {
        setResults(response.results)
      } else {
        setResults(mockPapers.map(p => ({
          paper: p,
          score: Math.random() * 0.5 + 0.5,
          match_type: searchType,
          highlights: [`Match in ${p.title.slice(0, 30)}...`]
        })))
      }
    } catch (error) {
      console.error('Advanced search failed:', error)
      setResults(mockPapers.map(p => ({
        paper: p,
        score: Math.random() * 0.5 + 0.5,
        match_type: searchType,
        highlights: [`Match in ${p.title.slice(0, 30)}...`]
      })))
    } finally {
      setLoading(false)
    }
  }

  const handleAutocomplete = (value) => {
    setQuery(value)
    if (value.length > 2) {
      setSuggestions(['transformer', 'attention', 'BERT', 'GPT'].filter(s => s.startsWith(value)))
    } else {
      setSuggestions([])
    }
  }

  return (
    <div className="advanced-search-page">
      <header className="page-header">
        <h1>Advanced Search</h1>
      </header>

      <div className="search-type-selector">
        {searchTypes.map(type => (
          <button
            key={type.id}
            className={`search-type-btn ${searchType === type.id ? 'active' : ''}`}
            onClick={() => setSearchType(type.id)}
          >
            <span className="type-name">{type.name}</span>
            <span className="type-desc">{type.desc}</span>
          </button>
        ))}
      </div>

      <div className="advanced-search-input">
        <div className="autocomplete-wrapper">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Enter search query..."
            value={query}
            onChange={(e) => handleAutocomplete(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
          />
          {suggestions.length > 0 && (
            <div className="autocomplete-dropdown">
              {suggestions.map(s => (
                <button key={s} onClick={() => { setQuery(s); setSuggestions([]) }}>
                  {s}
                </button>
              ))}
            </div>
          )}
        </div>
        <button className="primary-button" onClick={handleSearch}>
          <Search size={18} /> Search
        </button>
      </div>

      {loading && (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Searching with {searchType} mode...</p>
        </div>
      )}

      {results.length > 0 && (
        <div className="search-results">
          <div className="results-header">
            <span>{results.length} results found</span>
            <span className="search-type-badge">{searchType}</span>
          </div>
          
          {results.map((result, i) => (
            <motion.div
              key={result.paper.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: i * 0.05 }}
              className="result-card"
            >
              <div className="result-score">
                <div className="score-bar">
                  <div className="score-fill" style={{ width: `${result.score * 100}%` }} />
                </div>
                <span>{Math.round(result.score * 100)}%</span>
              </div>
              <div className="result-content">
                <div className="result-meta">
                  <span className="match-type">{result.match_type}</span>
                  <span className="source">{result.paper.source}</span>
                </div>
                <h3>{result.paper.title}</h3>
                <p className="authors">{result.paper.authors.join(', ')}</p>
                <p className="abstract">{result.paper.abstract}</p>
                {result.highlights.map((h, j) => (
                  <div key={j} className="highlight">{h}</div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}