import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import { 
  Search, BookOpen, GitCompare, MessageSquare, 
  Sparkles, Settings, Star,
  FileText, Download,
  Beaker, Network, LogOut, User, FolderOpen, Clock, BarChart3, Copy
} from 'lucide-react'
import './App.css'
import { AuthProvider, useAuth } from './context/AuthContext'
import { 
  Dashboard, Search as SearchPage, Summarize as SummarizePage, Compare as ComparePage, 
  Debate as DebatePage, Synthesize as SynthesizePage, WritePaper as WritePaperPage, 
  Projects as ProjectsPage, ProjectDetail as ProjectDetailPage, Graph as GraphPage, 
  Timeline as TimelinePage, Admin as AdminPage, Diff as DiffPage, QA as QAPage, 
  Discover as DiscoverPage, Clipboard as ClipboardPage, Collections as CollectionsPage, 
  AdvancedSearch as AdvancedSearchPage, About, Features, Landing, Login, Signup,
  History, Export, Analytics, Settings as SettingsPage
} from './pages'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" />
  return children
}

function Sidebar() {
  const location = useLocation()
  const { user, logout } = useAuth()
  
  const navItems = [
    { path: '/app', icon: Search, label: 'Dashboard' },
    { path: '/app/search', icon: BookOpen, label: 'Papers' },
    { path: '/app/advanced-search', icon: Search, label: 'Advanced Search' },
    { path: '/app/compare', icon: GitCompare, label: 'Compare' },
    { path: '/app/diff', icon: GitCompare, label: 'Diff View' },
    { path: '/app/qa', icon: MessageSquare, label: 'Q&A Chat' },
    { path: '/app/discover', icon: Network, label: 'Related Papers' },
    { path: '/app/debate', icon: MessageSquare, label: 'Debate' },
    { path: '/app/synthesize', icon: Sparkles, label: 'Synthesize' },
    { path: '/app/write', icon: FileText, label: 'Write' },
    { path: '/app/collections', icon: Star, label: 'Collections' },
    { path: '/app/history', icon: Clock, label: 'History' },
    { path: '/app/export', icon: Download, label: 'Export' },
    { path: '/app/clipboard', icon: Copy, label: 'Clipboard' },
    { path: '/app/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/app/projects', icon: FolderOpen, label: 'Projects' },
    { path: '/app/graph', icon: Network, label: 'Graph' },
    { path: '/app/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <Link to="/app" className="logo">
          <Beaker className="logo-icon" />
          <span className="logo-text">Research Lab</span>
        </Link>
      </div>
      
      <nav className="nav-menu">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link 
              key={item.path} 
              to={item.path} 
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        {user && (
          <div className="user-menu">
            <div className="user-avatar">
              <User size={18} />
            </div>
            <div className="user-info">
              <span className="user-name">{user.name}</span>
              <span className="user-email">{user.email}</span>
            </div>
            <button className="logout-btn" onClick={logout} title="Sign out">
              <LogOut size={18} />
            </button>
          </div>
        )}
        <div className="status-indicator">
          <div className="status-dot"></div>
          <span>API Connected</span>
        </div>
      </div>
    </aside>
  )
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/about" element={<About />} />
          <Route path="/features" element={<Features />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/app" element={
            <ProtectedRoute>
              <div className="app">
                <Sidebar />
                <main className="main-content">
                  <Routes>
                    <Route path="/app" element={<Dashboard />} />
                    <Route path="/app/search" element={<SearchPage />} />
                    <Route path="/app/advanced-search" element={<AdvancedSearchPage />} />
                    <Route path="/app/summarize/:id" element={<SummarizePage />} />
                    <Route path="/app/compare" element={<ComparePage />} />
                    <Route path="/app/diff" element={<DiffPage />} />
                    <Route path="/app/qa" element={<QAPage />} />
                    <Route path="/app/discover" element={<DiscoverPage />} />
                    <Route path="/app/debate" element={<DebatePage />} />
                    <Route path="/app/synthesize" element={<SynthesizePage />} />
                    <Route path="/app/write" element={<WritePaperPage />} />
                    <Route path="/app/history" element={<History />} />
                    <Route path="/app/collections" element={<CollectionsPage />} />
                    <Route path="/app/export" element={<Export />} />
                    <Route path="/app/clipboard" element={<ClipboardPage />} />
                    <Route path="/app/analytics" element={<Analytics />} />
                    <Route path="/app/settings" element={<SettingsPage />} />
                    <Route path="/app/projects" element={<ProjectsPage />} />
                    <Route path="/app/projects/:id" element={<ProjectDetailPage />} />
                    <Route path="/app/graph" element={<GraphPage />} />
                    <Route path="/app/timeline" element={<TimelinePage />} />
                  </Routes>
                </main>
              </div>
            </ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App