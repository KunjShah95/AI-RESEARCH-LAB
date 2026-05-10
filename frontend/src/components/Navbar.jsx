import { Link } from 'react-router-dom'
import { Beaker, ArrowRight } from 'lucide-react'

export default function Navbar() {
  return (
    <header className="landing-header">
      <div className="landing-nav">
        <Link to="/" className="logo">
          <Beaker className="logo-icon" />
          <span className="logo-text">Research Lab</span>
        </Link>
        <div className="nav-links">
          <Link to="/features" className="nav-link">Features</Link>
          <Link to="/about" className="nav-link">About</Link>
          <Link to="/login" className="nav-link">Sign In</Link>
          <Link to="/signup" className="btn-primary">
            Get Started <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </header>
  )
}