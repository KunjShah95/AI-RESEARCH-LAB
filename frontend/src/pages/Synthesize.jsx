import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Loader2 } from 'lucide-react'
import { synthesizeApi } from '../services/api'

const mockPapers = [
  { id: '1', title: 'Attention Is All You Need', year: 2017, citations: 95000 },
  { id: '2', title: 'BERT: Pre-training', year: 2018, citations: 85000 },
  { id: '3', title: 'GPT-4 Technical Report', year: 2023, citations: 5000 },
]

export default function SynthesizePage() {
  const [synthesizing, setSynthesizing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const synthesize = async () => {
    setSynthesizing(true)
    setError(null)
    try {
      const response = await synthesizeApi.synthesize('LLM architectures transformer', mockPapers)
      setResults({
        summary: response.summary,
        insights: response.insights,
        gaps: response.gaps,
        recommendations: response.recommendations
      })
    } catch (err) {
      console.error('Synthesis failed:', err)
      setError('Failed to synthesize. Using mock results.')
      setResults({
        summary: 'Analysis of 15 papers on LLM architectures reveals significant progress in transformer-based models, with emerging trends in efficient attention mechanisms and multimodal capabilities.',
        insights: [
          { type: 'trend', title: 'Increasing efficiency focus', description: 'More papers addressing attention complexity', confidence: 0.92 },
          { type: 'finding', title: 'Multimodal success', description: 'Vision-language models showing strong results', confidence: 0.88 },
          { type: 'gap', title: 'Reasoning benchmarks', description: 'Limited progress on complex reasoning tasks', confidence: 0.85 },
        ],
        gaps: [
          { priority: 'high', description: 'Long-context efficiency', direction: 'Develop sparse attention mechanisms' },
          { priority: 'medium', description: 'Cultural bias in training', direction: 'Improve dataset diversification' },
        ],
        recommendations: [
          'Priority: Address long-context efficiency gap with sparse attention',
          'Explore multimodal architectures for vision-language tasks',
          'Develop better evaluation for complex reasoning',
        ]
      })
    } finally {
      setSynthesizing(false)
    }
  }

  return (
    <div className="synthesize-page">
      <header className="page-header">
        <h1>Insight Synthesis</h1>
      </header>

      <button className="primary-button" onClick={synthesize} disabled={synthesizing}>
        {synthesizing ? <Loader2 className="spinner" size={18} /> : <Sparkles size={18} />}
        {synthesizing ? 'Synthesizing...' : 'Generate Synthesis'}
      </button>

      {error && <div className="error-message">{error}</div>}

      {synthesizing && (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Analyzing literature for insights and gaps...</p>
        </div>
      )}

      {results && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="synthesis-results"
        >
          <div className="summary-section">
            <h2>Literature Summary</h2>
            <p>{results.summary}</p>
          </div>

          <div className="insights-grid">
            <h2>Key Insights</h2>
            {results.insights.map((insight, i) => (
              <div key={i} className={`insight-card ${insight.type}`}>
                <span className="insight-type">{insight.type}</span>
                <h3>{insight.title}</h3>
                <p>{insight.description}</p>
                <span className="confidence">{Math.round(insight.confidence * 100)}% confidence</span>
              </div>
            ))}
          </div>

          <div className="gaps-section">
            <h2>Research Gaps</h2>
            {results.gaps.map((gap, i) => (
              <div key={i} className={`gap-card ${gap.priority}`}>
                <span className="priority">{gap.priority}</span>
                <h3>{gap.description}</h3>
                <p>Suggested: {gap.direction}</p>
              </div>
            ))}
          </div>

          <div className="recommendations-section">
            <h2>Recommendations</h2>
            <ul>
              {results.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  )
}