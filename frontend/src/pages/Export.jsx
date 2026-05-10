import { useState } from 'react'
import { Download } from 'lucide-react'

export default function ExportPage() {
  const [exportFormat, setExportFormat] = useState('bibtex')
  const formats = [
    { id: 'bibtex', name: 'BibTeX', desc: 'LaTeX bibliography format' },
    { id: 'ris', name: 'RIS', desc: 'EndNote, Zotero format' },
    { id: 'json', name: 'JSON', desc: 'Machine-readable format' },
    { id: 'csv', name: 'CSV', desc: 'Spreadsheet compatible' },
  ]
  
  return (
    <div className="export-page">
      <header className="page-header"><h1>Export Citations</h1></header>
      <div className="export-section">
        <h3>Select Format</h3>
        <div className="format-grid">
          {formats.map((format) => (
            <button key={format.id} className={`format-card ${exportFormat === format.id ? 'active' : ''}`} onClick={() => setExportFormat(format.id)}>
              <h4>{format.name}</h4><p>{format.desc}</p>
            </button>
          ))}
        </div>
      </div>
      <div className="export-actions">
        <button className="primary-button"><Download size={18} /> Export Citations</button>
      </div>
    </div>
  )
}