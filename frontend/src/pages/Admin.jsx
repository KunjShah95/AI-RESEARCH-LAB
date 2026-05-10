import { useState } from 'react'
import { Activity, BookOpen, Users, BarChart3, Settings } from 'lucide-react'

const mockUsers = [
  { id: '1', name: 'Dr. Jane Smith', email: 'jane@university.edu', role: 'admin', papers: 156, apiCalls: 2340 },
  { id: '2', name: 'Prof. John Doe', email: 'john@university.edu', role: 'researcher', papers: 89, apiCalls: 1200 },
  { id: '3', name: 'Alice Chen', email: 'alice@university.edu', role: 'researcher', papers: 45, apiCalls: 800 },
  { id: '4', name: 'Bob Wilson', email: 'bob@university.edu', role: 'viewer', papers: 12, apiCalls: 200 },
]

export default function AdminPage() {
  const [users, setUsers] = useState(mockUsers)
  const systemStats = { totalPapers: 1247, totalApiCalls: 45200, cacheSize: '2.3 GB', activeUsers: 12 }

  return (
    <div className="admin-page">
      <header className="page-header">
        <h1>Admin Dashboard</h1>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <Activity size={24} />
          <div>
            <span className="stat-number">{systemStats.totalApiCalls.toLocaleString()}</span>
            <span className="stat-label">API Calls Today</span>
          </div>
        </div>
        <div className="stat-card">
          <BookOpen size={24} />
          <div>
            <span className="stat-number">{systemStats.totalPapers.toLocaleString()}</span>
            <span className="stat-label">Papers Indexed</span>
          </div>
        </div>
        <div className="stat-card">
          <Users size={24} />
          <div>
            <span className="stat-number">{systemStats.activeUsers}</span>
            <span className="stat-label">Active Users</span>
          </div>
        </div>
        <div className="stat-card">
          <BarChart3 size={24} />
          <div>
            <span className="stat-number">{systemStats.cacheSize}</span>
            <span className="stat-label">Cache Size</span>
          </div>
        </div>
      </div>

      <div className="users-section">
        <h2>User Management</h2>
        <div className="users-table">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Papers</th>
                <th>API Calls</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>
                    <select
                      value={user.role}
                      onChange={e => setUsers(users.map(u => u.id === user.id ? {...u, role: e.target.value} : u))}
                      className="role-select"
                    >
                      <option value="admin">Admin</option>
                      <option value="researcher">Researcher</option>
                      <option value="viewer">Viewer</option>
                    </select>
                  </td>
                  <td>{user.papers}</td>
                  <td>{user.apiCalls}</td>
                  <td>
                    <button className="action-btn"><Settings size={14} /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}