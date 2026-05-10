import { useState } from 'react'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    darkMode: true,
    emailNotifications: true,
    autoSave: true,
    publicProfile: false,
    researchInterests: 'AI, Machine Learning, NLP',
  })
  
  return (
    <div className="settings-page">
      <header className="page-header">
        <h1>Settings</h1>
      </header>
      
      <div className="settings-section">
        <h3>Preferences</h3>
        <div className="settings-card">
          <div className="setting-item toggle">
            <div className="setting-info">
              <h4>Dark Mode</h4>
              <p>Use dark theme</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.darkMode}
                onChange={(e) => setSettings({...settings, darkMode: e.target.checked})}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
          <div className="setting-item toggle">
            <div className="setting-info">
              <h4>Email Notifications</h4>
              <p>Receive updates about new papers</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.emailNotifications}
                onChange={(e) => setSettings({...settings, emailNotifications: e.target.checked})}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
          <div className="setting-item toggle">
            <div className="setting-info">
              <h4>Auto-save</h4>
              <p>Automatically save research progress</p>
            </div>
            <label className="toggle-switch">
              <input 
                type="checkbox" 
                checked={settings.autoSave}
                onChange={(e) => setSettings({...settings, autoSave: e.target.checked})}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>
    </div>
  )
}