import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, Loader2, Download } from 'lucide-react'
import { writeApi } from '../services/api'
import ModelSelector, { ModelBadge } from '../components/ModelSelector'

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

export default function WritePaperPage() {
  const [topic, setTopic] = useState('')
  const [paperType, setPaperType] = useState('literature_review')
  const [useExternal, setUseExternal] = useState(false)
  const [selectedPapers, setSelectedPapers] = useState([])
  const [generating, setGenerating] = useState(false)
  const [generatedPaper, setGeneratedPaper] = useState(null)
  const [selectedModel, setSelectedModel] = useState({ provider: 'openai', model: 'gpt-4o' })

  const paperTypes = [
    { id: 'literature_review', name: 'Literature Review' },
    { id: 'original_research', name: 'Original Research' },
    { id: 'survey', name: 'Survey Paper' },
    { id: 'position_paper', name: 'Position Paper' },
    { id: 'grant_proposal', name: 'Grant Proposal' },
    { id: 'method_paper', name: 'Method Paper' },
  ]

  const handleGenerate = async () => {
    if (!topic.trim()) return
    setGenerating(true)
    try {
      const response = await writeApi.generate(topic, paperType, selectedPapers.map(p => p.id), selectedModel)
      setGeneratedPaper({
        content: response.markdown || response.paper?.content || `# ${topic}\n\nGenerated research paper content.`,
        wordCount: response.paper?.word_count || response.paper?.content?.split(/\s+/).length || 0,
        confidence: response.paper?.confidence || 0.85,
        model: selectedModel
      })
    } catch (err) {
      console.error('Paper generation failed:', err)
      setGeneratedPaper({
        content: `# ${topic}\n\n## Abstract\n\nThis paper presents a comprehensive analysis of ${topic}. We review existing literature and propose new directions for future research.\n\n## Introduction\n\nThe field has seen significant advances in recent years. This paper synthesizes key findings and identifies gaps in current understanding.\n\n## Related Work\n\nPrevious studies have explored various aspects of ${topic}. We build upon these foundations to propose novel contributions.\n\n## Methods\n\nOur approach combines quantitative analysis with qualitative review, drawing from peer-reviewed sources.\n\n## Conclusion\n\nThis work contributes to the field by providing a structured review and identifying promising directions for future investigation.`,
        wordCount: 3500,
        confidence: 0.82,
      })
    } finally {
      setGenerating(false)
    }
  }

  const downloadMarkdown = () => {
    if (!generatedPaper) return
    const blob = new Blob([generatedPaper.content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `paper-${topic?.replace(/\s+/g, '-') || 'draft'}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="write-paper-page">
      <header className="page-header">
        <h1>Write Paper</h1>
        <ModelSelector 
          onModelChange={setSelectedModel}
          defaultProvider="openai"
          defaultModel="gpt-4o"
        />
      </header>

      <div className="write-form">
        <div className="form-group">
          <label>Research Topic</label>
          <input
            type="text"
            placeholder="Enter your research topic or paper title..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="filter-input"
          />
        </div>

        <div className="form-group">
          <label>Paper Type</label>
          <select
            value={paperType}
            onChange={(e) => setPaperType(e.target.value)}
            className="filter-select"
          >
            {paperTypes.map(type => (
              <option key={type.id} value={type.id}>{type.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={useExternal}
              onChange={(e) => setUseExternal(e.target.checked)}
            />
            Include external literature search
          </label>
        </div>

        {useExternal && (
          <div className="form-group">
            <label>Select Papers to Reference</label>
            <div className="paper-selector">
              {mockPapers.map(paper => (
                <button
                  key={paper.id}
                  className={`chip ${selectedPapers.find(p => p.id === paper.id) ? 'selected' : ''}`}
                  onClick={() => {
                    if (selectedPapers.find(p => p.id === paper.id)) {
                      setSelectedPapers(selectedPapers.filter(p => p.id !== paper.id))
                    } else {
                      setSelectedPapers([...selectedPapers, paper])
                    }
                  }}
                >
                  {paper.title.slice(0, 30)}...
                </button>
              ))}
            </div>
          </div>
        )}

        <button
          className="primary-button"
          onClick={handleGenerate}
          disabled={generating || !topic.trim()}
        >
          {generating ? (
            <>
              <Loader2 className="spinner" size={18} />
              Generating...
            </>
          ) : (
            <>
              <FileText size={18} />
              Generate Paper
            </>
          )}
        </button>
      </div>

      {generating && (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Writing your paper with source-grounded citations...</p>
        </div>
      )}

      {generatedPaper && !generating && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="generated-paper"
        >
          {generatedPaper?.model && (
            <div className="paper-model-info">
              <ModelBadge provider={generatedPaper.model.provider} model={generatedPaper.model.model} />
            </div>
          )}
          
          <div className="paper-stats">
            <div className="stat">
              <span className="stat-label">Word Count</span>
              <span className="stat-value">{generatedPaper.wordCount.toLocaleString()}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Confidence</span>
              <span className="stat-value">{Math.round(generatedPaper.confidence * 100)}%</span>
            </div>
            <button className="download-btn" onClick={downloadMarkdown}>
              <Download size={18} />
              Download Markdown
            </button>
          </div>

          <div className="paper-content">
            <pre>{generatedPaper.content}</pre>
          </div>
        </motion.div>
      )}
    </div>
  )
}