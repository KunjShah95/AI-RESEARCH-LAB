import { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, Brain, Cpu, Beaker, Loader2 } from 'lucide-react'
import { debateApi } from '../services/api'
import ModelSelector, { ModelBadge } from '../components/ModelSelector'

export default function DebatePage() {
  const [thesis, setThesis] = useState('')
  const [debating, setDebating] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [selectedModel, setSelectedModel] = useState({ provider: 'openai', model: 'gpt-4o' })

  const startDebate = async () => {
    if (!thesis.trim()) return
    setDebating(true)
    setError(null)
    try {
      const response = await debateApi.start(thesis, [], selectedModel)
      setResult({
        proponent: response.proponent_arguments,
        critic: response.critic_arguments,
        methodologist: response.methodology_evaluation,
        verdict: response.final_verdict,
        votes: { pro: response.vote_pro, con: response.vote_con },
        confidence: response.confidence,
        model: selectedModel
      })
    } catch (err) {
      console.error('Debate failed:', err)
      setError('Failed to start debate. Using mock results.')
      setResult({
        proponent: 'The Transformer architecture shows superior performance on translation tasks, achieving new state-of-the-art BLEU scores while being more parallelizable and requiring less training time than RNN-based models.',
        critic: 'However, the quadratic complexity of self-attention makes it impractical for very long sequences. The memory requirements scale as O(n²), limiting its applicability to documents or conversations beyond a few hundred tokens.',
        methodologist: 'The evaluation methodology is sound, using standard benchmarks. However, computational costs make reproduction difficult for most researchers.',
        verdict: 'The evidence supports the Transformer as a significant advancement in sequence transduction, with caveats about scalability.',
        votes: { pro: 3, con: 2 },
        confidence: 0.78,
        model: selectedModel
      })
    } finally {
      setDebating(false)
    }
  }

  return (
    <div className="debate-page">
      <header className="page-header">
        <h1>Multi-Agent Debate</h1>
        <ModelSelector 
          onModelChange={setSelectedModel}
          defaultProvider="openai"
          defaultModel="gpt-4o"
        />
      </header>

      <div className="debate-input">
        <textarea
          placeholder="Enter your thesis or research question to debate..."
          value={thesis}
          onChange={(e) => setThesis(e.target.value)}
          rows={3}
        />
        <button className="primary-button" onClick={startDebate} disabled={debating || !thesis.trim()}>
          {debating ? <Loader2 className="spinner" size={18} /> : <MessageSquare size={18} />}
          {debating ? 'Debating...' : 'Start Debate'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {debating && (
        <div className="debating-state">
          <div className="agent-status">
            <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1 }}>
              <Brain size={32} />
            </motion.div>
            <span>Proponent is arguing...</span>
          </div>
          <div className="agent-status">
            <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1.2 }}>
              <Cpu size={32} />
            </motion.div>
            <span>Critic is countering...</span>
          </div>
          <div className="agent-status">
            <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1.4 }}>
              <Beaker size={32} />
            </motion.div>
            <span>Methodologist is evaluating...</span>
          </div>
        </div>
      )}

      {result && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="debate-results"
        >
          {result.model && (
            <div className="debate-model-info">
              <ModelBadge provider={result.model.provider} model={result.model.model} />
            </div>
          )}
          
          <div className="vote-tally">
            <div className="vote-bar">
              <div className="vote pro" style={{ width: `${(result.votes.pro / 5) * 100}%` }}>
                Proponent: {result.votes.pro}
              </div>
              <div className="vote con" style={{ width: `${(result.votes.con / 5) * 100}%` }}>
                Critic: {result.votes.con}
              </div>
            </div>
            <span>Confidence: {Math.round(result.confidence * 100)}%</span>
          </div>

          <div className="argument-section proponent">
            <h3><Brain size={20} /> Proponent</h3>
            <p>{result.proponent}</p>
          </div>

          <div className="argument-section critic">
            <h3><Cpu size={20} /> Critic</h3>
            <p>{result.critic}</p>
          </div>

          <div className="argument-section methodologist">
            <h3><Beaker size={20} /> Methodologist</h3>
            <p>{result.methodologist}</p>
          </div>

          <div className="final-verdict">
            <h3>Final Verdict</h3>
            <p>{result.verdict}</p>
          </div>
        </motion.div>
      )}
    </div>
  )
}