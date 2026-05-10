import { motion } from 'framer-motion'

export default function AnalyticsPage() {
  const stats = [
    { label: 'Total Searches', value: '1,247', change: '+12%' },
    { label: 'Papers Analyzed', value: '89', change: '+8%' },
    { label: 'Collections Created', value: '12', change: '+2' },
    { label: 'Citations Exported', value: '456', change: '+23%' },
  ]
  
  return (
    <div className="analytics-page">
      <header className="page-header"><h1>Research Analytics</h1></header>
      <div className="analytics-stats">
        {stats.map((stat, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="stat-card">
            <span className="stat-label">{stat.label}</span>
            <span className="stat-value">{stat.value}</span>
            <span className="stat-change positive">{stat.change}</span>
          </motion.div>
        ))}
      </div>
    </div>
  )
}