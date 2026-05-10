import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Network, Download, Loader2, X, BarChart3, Users, Activity, FileText, GitCompare } from 'lucide-react'
import { graphApi } from '../services/api'

const mockPapers = [
  {
    id: '1',
    title: 'Attention Is All You Need',
    authors: ['Ashish Vaswani'],
    year: 2017,
    source: 'arxiv',
    citations: 95000,
  },
  {
    id: '2',
    title: 'BERT: Pre-training',
    authors: ['Jacob Devlin'],
    year: 2018,
    source: 'arxiv',
    citations: 85000,
  },
  {
    id: '3',
    title: 'GPT-4 Technical Report',
    authors: ['OpenAI'],
    year: 2023,
    source: 'arxiv',
    citations: 5000,
  },
  {
    id: '4',
    title: 'Llama 2',
    authors: ['Hugo Touvron'],
    year: 2023,
    source: 'arxiv',
    citations: 3000,
  },
  {
    id: '5',
    title: 'Chain-of-Thought',
    authors: ['Jason Wei'],
    year: 2022,
    source: 'arxiv',
    citations: 8000,
  },
]

const mockGraphData = {
  nodes: [
    { id: '1', label: 'Attention Is All You Need', citations: 95000 },
    { id: '2', label: 'BERT: Pre-training', citations: 85000 },
    { id: '3', label: 'GPT-4 Technical Report', citations: 5000 },
    { id: '4', label: 'Llama 2', citations: 3000 },
    { id: '5', label: 'Chain-of-Thought', citations: 8000 },
  ],
  links: [
    { source: '1', target: '2' },
    { source: '1', target: '3' },
    { source: '1', target: '4' },
    { source: '2', target: '3' },
    { source: '5', target: '3' },
  ]
}

export default function GraphPage() {
  const [selectedNode, setSelectedNode] = useState(null)
  const [graphData, setGraphData] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('visualization')
  const [recommendations, setRecommendations] = useState([])
  const [analysis, setAnalysis] = useState(null)

  const loadGraphData = async () => {
    setLoading(true)
    try {
      const papers = mockPapers.map(p => ({
        id: p.id,
        title: p.title,
        year: p.year,
        citations: p.citations || 0,
        references: []
      }))
      await graphApi.buildGraph(papers)
      const metricsData = await graphApi.getMetrics()
      setMetrics(metricsData)
      
      const vizData = await graphApi.getD3Visualization()
      if (vizData && !vizData.error) {
        setGraphData(vizData)
      } else {
        setGraphData(mockGraphData)
      }
    } catch (error) {
      console.error('Failed to load graph:', error)
      setGraphData(mockGraphData)
    }
    setLoading(false)
  }

  const handleNodeClick = (node) => {
    setSelectedNode(node)
    loadRecommendations(node.id)
    loadAnalysis(node.id)
  }

  const loadRecommendations = async (paperId) => {
    try {
      const recs = await graphApi.getRecommendations(paperId, 5, 'combined')
      setRecommendations(recs.recommendations || [])
    } catch (error) {
      console.error('Failed to load recommendations:', error)
    }
  }

  const loadAnalysis = async (paperId) => {
    try {
      const data = await graphApi.getAnalysis(paperId)
      setAnalysis(data)
    } catch (error) {
      console.error('Failed to load analysis:', error)
    }
  }

  return (
    <div className="graph-page">
      <header className="page-header">
        <h1>Citation Graph</h1>
        <div className="graph-controls">
          <button className="action-btn" onClick={loadGraphData} disabled={loading}>
            <Network size={16} /> Refresh
          </button>
          <button className="action-btn"><Download size={16} /> Export</button>
        </div>
      </header>

      {metrics && (
        <div className="graph-metrics">
          <div className="metric-item">
            <span className="metric-value">{metrics.total_nodes}</span>
            <span className="metric-label">Nodes</span>
          </div>
          <div className="metric-item">
            <span className="metric-value">{metrics.total_edges}</span>
            <span className="metric-label">Edges</span>
          </div>
          <div className="metric-item">
            <span className="metric-value">{metrics.density}</span>
            <span className="metric-label">Density</span>
          </div>
          <div className="metric-item">
            <span className="metric-value">{metrics.connected_components}</span>
            <span className="metric-label">Components</span>
          </div>
        </div>
      )}

      <div className="graph-tabs">
        <button className={activeTab === 'visualization' ? 'active' : ''} onClick={() => setActiveTab('visualization')}>
          <Network size={16} /> Visualization
        </button>
        <button className={activeTab === 'influential' ? 'active' : ''} onClick={() => setActiveTab('influential')}>
          <BarChart3 size={16} /> Influential Papers
        </button>
        <button className={activeTab === 'bridges' ? 'active' : ''} onClick={() => setActiveTab('bridges')}>
          <Users size={16} /> Citation Bridges
        </button>
        <button className={activeTab === 'cycles' ? 'active' : ''} onClick={() => setActiveTab('cycles')}>
          <Activity size={16} /> Citation Cycles
        </button>
      </div>

      <div className="graph-content">
        {loading ? (
          <div className="loading-state">
            <Loader2 className="spinner" size={40} />
            <p>Building citation graph...</p>
          </div>
        ) : activeTab === 'visualization' && (
          <div className="graph-container">
            <div className="graph-visualization">
              <svg width="100%" height="500" viewBox="0 0 800 500">
                {graphData?.links?.map((edge, i) => (
                  <line 
                    key={i} 
                    x1="150" y1="100" x2="650" y2="300" 
                    stroke="var(--border)" 
                    strokeWidth="2" 
                    opacity="0.5"
                  />
                ))}
                {graphData?.nodes?.map((node, i) => (
                  <g 
                    key={node.id} 
                    onClick={() => handleNodeClick(node)}
                    style={{ cursor: 'pointer' }}
                  >
                    <circle 
                      cx={150 + (i % 4) * 180} 
                      cy={100 + Math.floor(i / 4) * 150} 
                      r={Math.max(node.radius || 10, 15)} 
                      fill="var(--accent)" 
                      opacity="0.8"
                    />
                    <text 
                      x={150 + (i % 4) * 180} 
                      y={145 + Math.floor(i / 4) * 150} 
                      textAnchor="middle" 
                      fill="var(--text-primary)" 
                      fontSize="9"
                    >
                      {node.label?.slice(0, 18)}...
                    </text>
                  </g>
                ))}
              </svg>
            </div>

            {selectedNode && (
              <div className="graph-sidebar">
                <div className="sidebar-header">
                  <h3>{selectedNode.label}</h3>
                  <button className="action-btn" onClick={() => setSelectedNode(null)}>
                    <X size={16} />
                  </button>
                </div>
                
                <div className="sidebar-stats">
                  <div className="stat">
                    <span className="stat-label">Citations</span>
                    <span className="stat-value">{selectedNode.citations || 0}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Year</span>
                    <span className="stat-value">{selectedNode.year}</span>
                  </div>
                </div>

                {recommendations.length > 0 && (
                  <div className="sidebar-section">
                    <h4>Similar Papers</h4>
                    {recommendations.map(rec => (
                      <div key={rec.paper_id} className="recommendation-item">
                        <span className="rec-title">{rec.title}</span>
                        <span className="rec-score">{rec.score}</span>
                      </div>
                    ))}
                  </div>
                )}

                {analysis && (
                  <div className="sidebar-section">
                    <h4>Analysis</h4>
                    <div className="analysis-stats">
                      <span>H-index: {analysis.h_index}</span>
                      <span>i10-index: {analysis.i10_index}</span>
                      <span>Avg Citation Age: {analysis.avg_citation_age} years</span>
                    </div>
                  </div>
                )}

                <div className="sidebar-actions">
                  <Link to={`/app/summarize/${selectedNode.id}`}>
                    <button className="action-btn"><FileText size={16} /> Summarize</button>
                  </Link>
                  <button className="action-btn"><GitCompare size={16} /> Compare</button>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'influential' && (
          <div className="influential-section">
            <h3>Most Influential Papers (PageRank)</h3>
            <div className="influential-list">
              {graphData?.nodes?.slice(0, 10).map((node, i) => (
                <motion.div 
                  key={node.id} 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="influential-item"
                  onClick={() => handleNodeClick(node)}
                >
                  <span className="rank">#{i + 1}</span>
                  <span className="title">{node.label}</span>
                  <span className="score">{node.citations} citations</span>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'bridges' && (
          <div className="bridges-section">
            <h3>Citation Bridges - Papers Connecting Research Areas</h3>
            <p className="section-desc">These papers are referenced by multiple different research clusters</p>
            <div className="bridges-list">
              {graphData?.nodes?.slice(0, 8).map((node, i) => (
                <div key={node.id} className="bridge-card">
                  <Network size={20} />
                  <h4>{node.label}</h4>
                  <p>{node.citations} citations across research areas</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'cycles' && (
          <div className="cycles-section">
            <h3>Citation Cycles</h3>
            <p className="section-desc">Circular citation patterns where papers reference each other</p>
            <div className="cycles-list">
              <div className="cycle-item">
                <span className="cycle-label">No cycles detected</span>
                <span className="cycle-desc">Build the graph with more papers to detect citation cycles</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="graph-legend">
        <h3>Legend</h3>
        <div className="legend-items">
          <span><div className="legend-dot large"></div> High influence</span>
          <span><div className="legend-dot medium"></div> Medium influence</span>
          <span><div className="legend-dot small"></div> Low influence</span>
        </div>
      </div>
    </div>
  )
}