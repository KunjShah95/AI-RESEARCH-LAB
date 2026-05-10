import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles, Loader2 } from 'lucide-react'
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
]

export default function SummarizePage() {
  const { id } = useParams()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [granularity, setGranularity] = useState('structured')
  const [error, setError] = useState(null)

  const paper = mockPapers.find(p => p.id === id) || mockPapers[0]

  const handleSummarize = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await papersApi.summarize(id || paper.id, granularity)
      setSummary(response.summary || response)
    } catch (err) {
      console.error('Summarize failed:', err)
      setError('Summary generation failed. Using mock data.')
      setSummary({
        problem: 'The paper addresses the limitation of existing sequence transduction models that use RNNs or CNNs, proposing a simpler architecture based solely on attention mechanisms.',
        methods: 'The Transformer uses multi-head self-attention and positional encoding, with encoder-decoder architecture. Training uses parallel computation for efficiency.',
        results: 'The Transformer achieves state-of-the-art results on WMT 2014 English-German and French translation tasks, training in less time than previous models.',
        limitations: 'The quadratic complexity of self-attention limits its application to very long sequences. Memory requirements scale with sequence length.',
        confidence: 0.92
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="summarize-page">
      <header className="page-header">
        <h1>Paper Summary</h1>
      </header>

      <div className="paper-info-card">
        <h2>{paper.title}</h2>
        <p>{paper.authors?.join(', ') || paper.authors} ({paper.year})</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="summary-controls">
        <div className="granularity-selector">
          <button 
            className={granularity === 'sentence' ? 'active' : ''}
            onClick={() => setGranularity('sentence')}
          >
            One Sentence
          </button>
          <button 
            className={granularity === 'abstract' ? 'active' : ''}
            onClick={() => setGranularity('abstract')}
          >
            Abstract
          </button>
          <button 
            className={granularity === 'structured' ? 'active' : ''}
            onClick={() => setGranularity('structured')}
          >
            Structured
          </button>
        </div>
        <button className="primary-button" onClick={handleSummarize}>
          <Sparkles size={18} /> Generate Summary
        </button>
      </div>

      {loading ? (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Analyzing paper and generating summary...</p>
        </div>
      ) : summary ? (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="summary-content"
        >
          <div className="confidence-meter">
            <span>Confidence Score</span>
            <div className="confidence-bar">
              <div 
                className="confidence-fill" 
                style={{ width: `${summary.confidence * 100}%` }}
              />
            </div>
            <span className="confidence-value">{Math.round(summary.confidence * 100)}%</span>
          </div>

          <div className="summary-section">
            <h3>Problem</h3>
            <p>{summary.problem}</p>
            <span className="citation">[Source: {paper.title}]</span>
          </div>

          <div className="summary-section">
            <h3>Methods</h3>
            <p>{summary.methods}</p>
            <span className="citation">[Source: {paper.title}]</span>
          </div>

          <div className="summary-section">
            <h3>Results</h3>
            <p>{summary.results}</p>
            <span className="citation">[Source: {paper.title}]</span>
          </div>

          <div className="summary-section">
            <h3>Limitations</h3>
            <p>{summary.limitations}</p>
            <span className="citation">[Source: {paper.title}]</span>
          </div>
        </motion.div>
      ) : null}
    </div>
  )
}