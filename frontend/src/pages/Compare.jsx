import { useState } from 'react'
import { motion } from 'framer-motion'
import { GitCompare, Loader2 } from 'lucide-react'
import { papersApi, compareApi } from '../services/api'

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

export default function ComparePage() {
  const [selectedPapers, setSelectedPapers] = useState(mockPapers.slice(0, 3))
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const generateComparison = async () => {
    setLoading(true)
    setError(null)
    try {
      if (selectedPapers.length >= 2) {
        const result = await compareApi.compare(
          selectedPapers.map(p => p.id),
          selectedPapers[0].source || 'arxiv'
        )
        setComparison({
          datasets: result.comparisons?.map(c => c.datasets?.join(', ') || 'N/A') || ['N/A', 'N/A', 'N/A'],
          metrics: result.comparisons?.[0]?.metrics || [
            { name: 'Citations', values: selectedPapers.map(p => p.citations?.toString() || 'N/A') },
          ],
          architectures: result.comparisons?.map(c => c.architecture || 'N/A') || selectedPapers.map(p => 'Transformer'),
          training: result.comparisons?.map(c => c.training || 'N/A') || selectedPapers.map(p => 'N/A'),
        })
      }
    } catch (err) {
      console.error('Compare failed:', err)
      setError('Failed to compare papers. Using mock data.')
      setComparison({
        datasets: ['WMT 2014 EN-DE', 'WMT 2014 EN-FR', 'BooksCorpus', 'Wikipedia'],
        metrics: [
          { name: 'BLEU (EN-DE)', values: ['28.4', '26.4', '25.3'] },
          { name: 'BLEU (EN-FR)', values: ['41.0', '39.2', '38.1'] },
        ],
        architectures: ['Transformer (6 layers)', 'Transformer (6 layers)', 'Transformer (6 layers)'],
        training: ['8x V100 3.5 days', '8x V100 3.5 days', '8x V100 3.5 days'],
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="compare-page">
      <header className="page-header">
        <h1>Compare Papers</h1>
      </header>

      <div className="compare-selector">
        <h3>Select Papers to Compare</h3>
        <div className="paper-chips">
          {mockPapers.map(paper => (
            <button
              key={paper.id}
              className={`chip ${selectedPapers.find(p => p.id === paper.id) ? 'selected' : ''}`}
              onClick={() => {
                if (selectedPapers.find(p => p.id === paper.id)) {
                  setSelectedPapers(selectedPapers.filter(p => p.id !== paper.id))
                } else if (selectedPapers.length < 4) {
                  setSelectedPapers([...selectedPapers, paper])
                }
              }}
            >
              {paper.title.slice(0, 30)}...
            </button>
          ))}
        </div>
      </div>

      <button className="primary-button" onClick={generateComparison} disabled={loading}>
        <GitCompare size={18} /> {loading ? 'Loading...' : 'Generate Comparison'}
      </button>

      {error && <div className="error-message">{error}</div>}

      {comparison && (
        <div className="comparison-table">
          <table>
            <thead>
              <tr>
                <th>Attribute</th>
                {selectedPapers.map(p => (
                  <th key={p.id}>{p.title.slice(0, 20)}...</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Datasets</td>
                {comparison.datasets.map((v, i) => (
                  <td key={i}>{v}</td>
                ))}
              </tr>
              {comparison.metrics.map((metric, i) => (
                <tr key={i}>
                  <td>{metric.name}</td>
                  {metric.values.map((v, j) => (
                    <td key={j}>{v}</td>
                  ))}
                </tr>
              ))}
              <tr>
                <td>Architecture</td>
                {comparison.architectures.map((v, i) => (
                  <td key={i}>{v}</td>
                ))}
              </tr>
              <tr>
                <td>Training Cost</td>
                {comparison.training.map((v, i) => (
                  <td key={i}>{v}</td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}