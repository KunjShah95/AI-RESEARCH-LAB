import { useState, useEffect } from 'react'
import { Copy, Loader2 } from 'lucide-react'
import { clipboardApi } from '../services/api'

const mockPapers = [
  {
    id: '1',
    title: 'Attention Is All You Need',
    authors: ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar'],
    year: 2017,
    source: 'arxiv',
    abstract: 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.',
    citations: 95000,
    openAccess: true,
  },
  {
    id: '2',
    title: 'BERT: Pre-training of Deep Bidirectional Transformers',
    authors: ['Jacob Devlin', 'Ming-Wei Chang', 'Kenton Lee'],
    year: 2018,
    source: 'arxiv',
    abstract: 'We introduce a new language representation model called BERT.',
    citations: 85000,
    openAccess: true,
  },
  {
    id: '3',
    title: 'GPT-4 Technical Report',
    authors: ['OpenAI'],
    year: 2023,
    source: 'arxiv',
    abstract: 'We report the development of GPT-4, a large-scale, multimodal model.',
    citations: 5000,
    openAccess: false,
  },
  {
    id: '4',
    title: 'Llama 2: Open Foundation and Chat Models',
    authors: ['Hugo Touvron', 'Louis Martin', 'Kevin Stone'],
    year: 2023,
    source: 'arxiv',
    abstract: 'We introduce LLaMA, a collection of foundation language models.',
    citations: 3000,
    openAccess: true,
  },
  {
    id: '5',
    title: 'Chain-of-Thought Prompting Elicits Reasoning',
    authors: ['Jason Wei', 'Xuezhi Wang', 'Dale Schuurmans'],
    year: 2022,
    source: 'arxiv',
    abstract: 'We explore how chain of thought prompting can improve reasoning abilities.',
    citations: 8000,
    openAccess: true,
  },
]

export default function ClipboardPage() {
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedPapers, setSelectedPapers] = useState([])
  const [citationStyle, setCitationStyle] = useState('apa')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    const fetchClipboard = async () => {
      try {
        const response = await clipboardApi.getAll()
        if (response && response.length > 0) {
          setPapers(response)
        } else {
          setPapers(mockPapers)
        }
      } catch (error) {
        console.log('Using mock papers - API not available')
        setPapers(mockPapers)
      } finally {
        setLoading(false)
      }
    }
    fetchClipboard()
  }, [])

  const styles = [
    { id: 'apa', name: 'APA' },
    { id: 'mla', name: 'MLA' },
    { id: 'chicago', name: 'Chicago' },
    { id: 'ieee', name: 'IEEE' }
  ]

  const copyCitation = (paper) => {
    setSelectedPapers([paper])
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const generateCitation = (paper) => {
    const authors = paper.authors.join(', ')
    switch (citationStyle) {
      case 'apa': return `${authors} (${paper.year}). ${paper.title}.`
      case 'mla': return `${authors}. "${paper.title}." ${paper.year}.`
      case 'chicago': return `${authors}. "${paper.title}." ${paper.year}.`
      case 'ieee': return `${authors}, "${paper.title}," ${paper.year}.`
      default: return `${authors} (${paper.year}). ${paper.title}.`
    }
  }

  return (
    <div className="clipboard-page">
      <header className="page-header">
        <h1>Citation Clipboard</h1>
      </header>

      <div className="citation-style-selector">
        {styles.map(style => (
          <button key={style.id} className={citationStyle === style.id ? 'active' : ''} onClick={() => setCitationStyle(style.id)}>
            {style.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Loading citations...</p>
        </div>
      ) : (
        <div className="citation-papers">
          {papers.map(paper => (
            <div key={paper.id} className="citation-item">
              <h3>{paper.title}</h3>
              <p className="citation-preview">{generateCitation(paper)}</p>
              <button className="action-btn" onClick={() => copyCitation(paper)}>
                <Copy size={16} /> Copy
              </button>
            </div>
          ))}
        </div>
      )}

      {copied && <div className="toast">Citation copied to clipboard!</div>}
    </div>
  )
}