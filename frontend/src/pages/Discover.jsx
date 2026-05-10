import { useState } from 'react'
import { motion } from 'framer-motion'
import { Network, Loader2 } from 'lucide-react'

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

export default function DiscoverPage() {
  const [selectedPaper, setSelectedPaper] = useState(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState([])

  const findRelated = () => {
    if (!selectedPaper) return
    setLoading(true)
    setTimeout(() => {
      setResults([
        { paper: mockPapers[1], score: 0.85, reasons: ['Similar abstract', 'Overlapping authors'] },
        { paper: mockPapers[2], score: 0.72, reasons: ['Related topic'] },
        { paper: mockPapers[4], score: 0.68, reasons: ['Similar methodology'] }
      ])
      setLoading(false)
    }, 1200)
  }

  return (
    <div className="discover-page">
      <header className="page-header">
        <h1>Related Papers</h1>
      </header>

      <div className="discover-select">
        <select onChange={(e) => setSelectedPaper(mockPapers.find(p => p.id === e.target.value))}>
          <option value="">Select a paper...</option>
          {mockPapers.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
        </select>
        <button className="primary-button" onClick={findRelated} disabled={!selectedPaper}>
          <Network size={18} /> Find Related
        </button>
      </div>

      {loading && <div className="loading-state"><Loader2 className="spinner" size={40} /><p>Finding related papers...</p></div>}

      {results.length > 0 && (
        <div className="related-list">
          {results.map((r, i) => (
            <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="related-card">
              <div className="similarity-score">{(r.score * 100).toFixed(0)}% match</div>
              <h3>{r.paper.title}</h3>
              <p>{r.paper.authors.join(', ')}</p>
              <div className="match-reasons">
                {r.reasons.map((reason, j) => <span key={j} className="reason-tag">{reason}</span>)}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}