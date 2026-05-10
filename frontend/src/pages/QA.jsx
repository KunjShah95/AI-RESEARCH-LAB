import { useState } from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

export default function QAPage() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [chatHistory, setChatHistory] = useState([])

  const askQuestion = () => {
    if (!question.trim()) return
    setLoading(true)
    setTimeout(() => {
      const answer = {
        answer: `Based on the papers analyzed, ${question.toLowerCase().includes('method') ? 'the methodology uses multi-head attention mechanisms with positional encoding.' : 'significant findings relate to transformer architecture improvements over traditional RNNs.'}`,
        confidence: 0.85,
        sources: ['Attention Is All You Need', 'BERT: Pre-training']
      }
      setChatHistory([...chatHistory, { role: 'user', content: question }, { role: 'assistant', content: answer.answer }])
      setResult(answer)
      setLoading(false)
      setQuestion('')
    }, 1500)
  }

  return (
    <div className="qa-page">
      <header className="page-header">
        <h1>AI Q&A Chat</h1>
      </header>

      <div className="qa-messages">
        {chatHistory.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`qa-message ${msg.role}`}
          >
            <p>{msg.content}</p>
          </motion.div>
        ))}
      </div>

      <div className="qa-input">
        <textarea
          placeholder="Ask a question about the papers..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && e.ctrlKey && askQuestion()}
          rows={2}
        />
        <button className="primary-button" onClick={askQuestion} disabled={loading || !question.trim()}>
          {loading ? <Loader2 className="spinner" size={18} /> : 'Ask'}
        </button>
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="qa-result"
        >
          <div className="confidence-meter">
            <span>Confidence</span>
            <div className="confidence-bar">
              <div className="confidence-fill" style={{ width: `${result.confidence * 100}%` }} />
            </div>
            <span>{Math.round(result.confidence * 100)}%</span>
          </div>
          <div className="sources">
            <h4>Sources</h4>
            {result.sources.map((s, i) => <span key={i} className="source-tag">{s}</span>)}
          </div>
        </motion.div>
      )}
    </div>
  )
}