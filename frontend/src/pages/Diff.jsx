import { useState } from 'react'
import { motion } from 'framer-motion'
import { GitCompare } from 'lucide-react'

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

export default function DiffPage() {
  const [selectedPapers, setSelectedPapers] = useState(mockPapers.slice(0, 2))
  const [diffMode, setDiffMode] = useState('side-by-side')
  const [showDiff, setShowDiff] = useState(false)

  const generateDiff = () => {
    setShowDiff(true)
  }

  return (
    <div className="diff-page">
      <header className="page-header">
        <h1>Paper Diff View</h1>
      </header>

      <div className="diff-controls">
        <div className="paper-selector">
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
                {paper.title.slice(0, 25)}...
              </button>
            ))}
          </div>
        </div>

        <div className="diff-modes">
          <button 
            className={diffMode === 'side-by-side' ? 'active' : ''}
            onClick={() => setDiffMode('side-by-side')}
          >
            Side by Side
          </button>
          <button 
            className={diffMode === 'unified' ? 'active' : ''}
            onClick={() => setDiffMode('unified')}
          >
            Unified Diff
          </button>
          <button 
            className={diffMode === 'changes' ? 'active' : ''}
            onClick={() => setDiffMode('changes')}
          >
            Changes Only
          </button>
        </div>

        <button className="primary-button" onClick={generateDiff} disabled={selectedPapers.length < 2}>
          <GitCompare size={18} /> Generate Diff
        </button>
      </div>

      {showDiff && selectedPapers.length >= 2 && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="diff-results"
        >
          <div className="diff-similarity">
            <span>Overall Similarity: </span>
            <span className="similarity-score">{(Math.random() * 0.4 + 0.6).toFixed(1)}%</span>
          </div>

          {diffMode === 'side-by-side' && (
            <div className="side-by-side-diff">
              {selectedPapers.slice(0, 2).map((paper, i) => (
                <div key={paper.id} className={`diff-column ${i === 0 ? 'left' : 'right'}`}>
                  <div className="diff-header">
                    <h3>{paper.title}</h3>
                    <span className="paper-meta">{paper.year} | {paper.authors.slice(0, 2).join(', ')}</span>
                  </div>
                  <div className="diff-content">
                    <div className="diff-section">
                      <h4>Abstract</h4>
                      <p className={i === 0 ? 'original' : 'modified'}>{paper.abstract}</p>
                    </div>
                    <div className="diff-section">
                      <h4>Methods</h4>
                      <p>{paper.methods || 'Standard research methodology'}</p>
                    </div>
                    <div className="diff-section">
                      <h4>Results</h4>
                      <p>{paper.results || 'Significant findings in the domain'}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {diffMode === 'unified' && (
            <div className="unified-diff">
              <pre className="diff-output">
{`--- a/${selectedPapers[0].title.slice(0, 30)}
+++ b/${selectedPapers[1].title.slice(0, 30)}
@@ -1,5 +1,5 @@
-Original: ${selectedPapers[0].abstract.slice(0, 100)}
+Modified: ${selectedPapers[1].abstract.slice(0, 100)}
@@ -10,3 +10,5 @@
 Methods comparison shows:
-${selectedPapers[0].methods || 'standard approach'}
+${selectedPapers[1].methods || 'enhanced approach'}
+Additional findings: significant improvement`}
              </pre>
            </div>
          )}

          {diffMode === 'changes' && (
            <div className="changes-list">
              <h3>Key Differences</h3>
              <div className="change-item added">
                <span className="change-type">+</span>
                <span>Added: New methodology section in paper 2</span>
              </div>
              <div className="change-item removed">
                <span className="change-type">-</span>
                <span>Removed: Preliminary experiments section</span>
              </div>
              <div className="change-item modified">
                <span className="change-type">~</span>
                <span>Modified: Updated results with more data points</span>
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}