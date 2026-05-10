import { useState } from 'react'
import { motion } from 'framer-motion'

const mockTimelinePapers = [
  { id: '1', title: 'Attention Is All You Need', year: 2017, source: 'arxiv' },
  { id: '2', title: 'BERT: Pre-training', year: 2018, source: 'arxiv' },
  { id: '3', title: 'GPT-3', year: 2020, source: 'arxiv' },
  { id: '4', title: 'Llama 2', year: 2023, source: 'arxiv' },
  { id: '5', title: 'GPT-4 Technical Report', year: 2023, source: 'arxiv' },
  { id: '6', title: 'Chain-of-Thought', year: 2022, source: 'arxiv' },
]

export default function TimelinePage() {
  const [filter, setFilter] = useState('all')
  const years = [...new Set(mockTimelinePapers.map(p => p.year))].sort()

  return (
    <div className="timeline-page">
      <header className="page-header">
        <h1>Research Timeline</h1>
        <select className="filter-select" value={filter} onChange={e => setFilter(e.target.value)}>
          <option value="all">All Sources</option>
          <option value="arxiv">arXiv</option>
          <option value="semantic_scholar">Semantic Scholar</option>
        </select>
      </header>

      <div className="timeline-container">
        <div className="timeline-line"></div>
        {years.map(year => (
          <div key={year} className="timeline-year">
            <div className="year-marker">{year}</div>
            <div className="year-papers">
              {mockTimelinePapers.filter(p => p.year === year).map(paper => (
                <motion.div
                  key={paper.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="timeline-paper"
                >
                  <div className="paper-source">{paper.source}</div>
                  <h3>{paper.title}</h3>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}