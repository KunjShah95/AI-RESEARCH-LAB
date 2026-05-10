import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Plus, Star, Loader2 } from 'lucide-react'
import { collectionsApi } from '../services/api'

export default function CollectionsPage() {
  const [collections, setCollections] = useState([])
  const [loading, setLoading] = useState(true)

  const mockCollections = [
    { id: 1, name: 'Transformers Research', papers: 24, color: '#d4a853' },
    { id: 2, name: 'LLM Alignment', papers: 18, color: '#c9956c' },
    { id: 3, name: 'Computer Vision', papers: 31, color: '#a38742' },
    { id: 4, name: 'NLP Benchmarks', papers: 12, color: '#d4a853' },
  ]

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const response = await collectionsApi.list()
        if (response && response.length > 0) {
          setCollections(response)
        } else {
          setCollections(mockCollections)
        }
      } catch (error) {
        console.log('Using mock collections - API not available')
        setCollections(mockCollections)
      } finally {
        setLoading(false)
      }
    }
    fetchCollections()
  }, [])
  
  return (
    <div className="collections-page">
      <header className="page-header">
        <h1>Collections</h1>
        <button className="primary-button">
          <Plus size={18} /> New Collection
        </button>
      </header>
      
      {loading ? (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Loading collections...</p>
        </div>
      ) : (
      <div className="collections-grid">
        {collections.map((collection) => (
          <motion.div 
            key={collection.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="collection-card"
            style={{ borderColor: collection.color }}
          >
            <div className="collection-header" style={{ background: collection.color }}>
              <Star size={24} />
            </div>
            <h3>{collection.name}</h3>
            <p>{collection.papers} papers</p>
          </motion.div>
        ))}
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="collection-card add-new"
        >
          <Plus size={32} />
          <p>Create New</p>
        </motion.div>
      </div>
      )}
    </div>
  )
}