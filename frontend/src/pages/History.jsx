import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search } from 'lucide-react'

export default function HistoryPage() {
  const historyItems = [
    { id: 1, query: 'transformer attention mechanisms', type: 'semantic', date: '2 hours ago', results: 156 },
    { id: 2, query: 'BERT pretraining language models', type: 'keyword', date: '5 hours ago', results: 89 },
    { id: 3, query: 'neural network optimization', type: 'citation', date: '1 day ago', results: 234 },
    { id: 4, query: 'GPT models scaling laws', type: 'semantic', date: '2 days ago', results: 67 },
    { id: 5, query: 'reinforcement learning from human feedback', type: 'boolean', date: '3 days ago', results: 123 },
  ]
  
  return (
    <div className="history-page">
      <header className="page-header">
        <h1>Search History</h1>
        <button className="primary-button">Clear All</button>
      </header>
      <div className="history-list">
        {historyItems.map((item) => (
          <motion.div key={item.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="history-item">
            <div className="history-icon"><Search size={20} /></div>
            <div className="history-content">
              <h3>{item.query}</h3>
              <div className="history-meta">
                <span className="history-type">{item.type}</span>
                <span>{item.date}</span>
                <span>{item.results} results</span>
              </div>
            </div>
            <Link to={`/app/search?q=${encodeURIComponent(item.query)}`}><button className="action-btn">Re-run</button></Link>
          </motion.div>
        ))}
      </div>
    </div>
  )
}