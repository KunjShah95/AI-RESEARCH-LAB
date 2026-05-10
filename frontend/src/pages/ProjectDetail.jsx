import { useState } from 'react'
import { Search, Trash2 } from 'lucide-react'

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
]

export default function ProjectDetailPage() {
  const [selectedPapers, setSelectedPapers] = useState(mockPapers.slice(0, 3))

  return (
    <div className="project-detail-page">
      <header className="page-header">
        <div>
          <h1>Project Details</h1>
          <p className="project-subtitle">Manage papers in this project</p>
        </div>
      </header>

      <div className="project-papers">
        <h2>Papers in Project</h2>
        <div className="papers-list">
          {selectedPapers.map(paper => (
            <div key={paper.id} className="result-card">
              <div className="result-content">
                <div className="result-header">
                  <span className="source-tag">{paper.source}</span>
                  <span className="year-tag">{paper.year}</span>
                </div>
                <h3>{paper.title}</h3>
                <p className="authors">{paper.authors.join(', ')}</p>
                <button className="action-btn remove-btn" onClick={() => setSelectedPapers(selectedPapers.filter(p => p.id !== paper.id))}>
                  <Trash2 size={16} /> Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="add-papers">
        <h2>Add Papers</h2>
        <div className="filter-input-wrapper">
          <input type="text" placeholder="Search papers to add..." className="filter-input" />
          <button className="primary-button"><Search size={18} /> Search</button>
        </div>
      </div>
    </div>
  )
}