import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, FolderOpen, BookOpen, Clock, Loader2 } from 'lucide-react'
import { projectsApi } from '../services/api'

const mockProjects = [
  { id: '1', name: 'Transformers Research', description: 'Comprehensive study of transformer architectures', paperCount: 24, createdAt: '2024-01-15' },
  { id: '2', name: 'LLM Benchmarking', description: 'Evaluation of large language models on various tasks', paperCount: 18, createdAt: '2024-02-20' },
  { id: '3', name: 'Vision-Language Models', description: 'Survey of VLM architectures and capabilities', paperCount: 12, createdAt: '2024-03-10' },
]

export default function ProjectsPage() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [newProject, setNewProject] = useState({ name: '', description: '' })

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await projectsApi.list()
        if (response && response.length > 0) {
          setProjects(response)
        } else {
          setProjects(mockProjects)
        }
      } catch (error) {
        console.log('Using mock projects - API not available')
        setProjects(mockProjects)
      } finally {
        setLoading(false)
      }
    }
    fetchProjects()
  }, [])

  return (
    <div className="projects-page">
      <header className="page-header">
        <h1>My Projects</h1>
        <button className="primary-button" onClick={() => setShowModal(true)}>
          <Plus size={18} /> New Project
        </button>
      </header>

      {loading ? (
        <div className="loading-state">
          <Loader2 className="spinner" size={40} />
          <p>Loading projects...</p>
        </div>
      ) : (
      <div className="projects-grid">
        {projects.map(project => (
          <Link key={project.id} to={`/projects/${project.id}`} className="project-card">
            <div className="project-header">
              <FolderOpen size={24} />
              <h3>{project.name}</h3>
            </div>
            <p>{project.description}</p>
            <div className="project-meta">
              <span><BookOpen size={14} /> {project.paperCount} papers</span>
              <span><Clock size={14} /> {project.createdAt}</span>
            </div>
          </Link>
        ))}
      </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>Create New Project</h2>
            <input
              type="text"
              placeholder="Project name"
              value={newProject.name}
              onChange={e => setNewProject({...newProject, name: e.target.value})}
              className="filter-input"
            />
            <textarea
              placeholder="Description"
              value={newProject.description}
              onChange={e => setNewProject({...newProject, description: e.target.value})}
              rows={3}
            />
            <div className="modal-actions">
              <button className="action-btn" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="primary-button" onClick={() => {
                setProjects([...projects, { id: String(projects.length + 1), ...newProject, paperCount: 0, createdAt: new Date().toISOString().split('T')[0] }])
                setShowModal(false)
              }}>Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}