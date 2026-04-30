import { useState } from 'react'
import { SAMPLE_CONFIGS } from '../App.jsx'
import './Analyze.css'

const SAMPLES = [
  { key: 'loan',    icon: '🏦', label: 'Loan Approval Data',     rows: '12,450 rows' },
  { key: 'hiring',  icon: '💼', label: 'Hiring Records',          rows: '8,200 rows' },
  { key: 'medical', icon: '🏥', label: 'Medical Diagnosis Data',  rows: '15,300 rows' },
  { key: 'credit',  icon: '💳', label: 'Credit Scoring Data',     rows: '22,700 rows' },
]

function Analyze({ navigate, setAuditConfig, setAuditResult }) {
  const [selectedSample, setSelectedSample] = useState(null)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [config, setConfig] = useState({
    protectedAttr: 'gender',
    outcomeCol: 'approved',
    refGroup: 'male',
    threshold: 'moderate',
    label: '',
  })

  const hasData = selectedSample || uploadedFile

  const handleFile = (e) => {
    const f = e.target.files[0]
    if (!f) return
    setUploadedFile(f)
    setSelectedSample(null)
    setConfig(c => ({ ...c, label: f.name.replace('.csv', '') }))
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f && f.name.endsWith('.csv')) {
      setUploadedFile(f)
      setSelectedSample(null)
    }
  }

  const selectSample = (key) => {
    setSelectedSample(key)
    setUploadedFile(null)
    setConfig(c => ({ ...c, label: SAMPLE_CONFIGS[key].label }))
  }

  const removeData = () => {
    setSelectedSample(null)
    setUploadedFile(null)
    setConfig(c => ({ ...c, label: '' }))
  }

  const handleStart = () => {
    const key = selectedSample || 'loan'
    setAuditConfig({ key, ...config })
    // Clear previous result
    setAuditResult(null)
    navigate('loading')
  }

  return (
    <div className="analyze-page">
      <div className="analyze-header">
        <p className="section-tag">New Audit</p>
        <h2>Run a Fairness Audit</h2>
        <p className="analyze-sub">
          Upload your dataset or pick a sample — our engine will detect bias, score fairness, and Gemini AI will explain everything in plain English.
        </p>
      </div>

      {/* Upload zone */}
      {!hasData ? (
        <div
          className={`upload-zone ${dragging ? 'dragging' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          <input type="file" accept=".csv" onChange={handleFile} id="fileInput" />
          <label htmlFor="fileInput" className="upload-inner">
            <div className="upload-icon-wrap">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M16 22V10M10 16l6-6 6 6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <rect x="4" y="4" width="24" height="24" rx="6" stroke="var(--border2)" strokeWidth="1.5" fill="none"/>
              </svg>
            </div>
            <h3>Drop your CSV file here</h3>
            <p>or click to browse · Supports CSV up to 100MB</p>
          </label>
        </div>
      ) : (
        <div className="file-selected">
          <div className="file-selected-icon">{selectedSample ? SAMPLES.find(s=>s.key===selectedSample)?.icon || '📄' : '📄'}</div>
          <div className="file-selected-info">
            <div className="file-selected-name">{config.label || (selectedSample ? SAMPLE_CONFIGS[selectedSample].label : uploadedFile?.name)}</div>
            <div className="file-selected-meta">
              {selectedSample ? `Sample dataset · ${SAMPLES.find(s=>s.key===selectedSample)?.rows}` : `${(uploadedFile?.size / 1024).toFixed(0)} KB · Uploaded`}
            </div>
          </div>
          <div className="file-selected-badge badge badge-accent">Ready</div>
          <button className="file-remove" onClick={removeData} title="Remove">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2 2l10 10M12 2L2 12" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
            </svg>
          </button>
        </div>
      )}

      {/* Sample picker */}
      <div className="samples-section">
        <div className="samples-divider">
          <span className="divider-line" /><span className="divider-text">or try a sample dataset</span><span className="divider-line" />
        </div>
        <div className="samples-grid">
          {SAMPLES.map(s => (
            <button
              key={s.key}
              className={`sample-btn ${selectedSample === s.key ? 'active' : ''}`}
              onClick={() => selectSample(s.key)}
            >
              <span className="sample-icon">{s.icon}</span>
              <span className="sample-label">{s.label}</span>
              <span className="sample-rows">{s.rows}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Config */}
      <div className="config-card card">
        <h3 className="config-title">Audit Configuration</h3>

        <div className="config-grid">
          <div className="form-group">
            <label className="form-label">Protected Attribute</label>
            <select className="form-control" value={config.protectedAttr} onChange={e => setConfig(c => ({...c, protectedAttr: e.target.value}))}>
              <option value="gender">Gender</option>
              <option value="race">Race / Ethnicity</option>
              <option value="age">Age Group</option>
              <option value="disability">Disability Status</option>
              <option value="religion">Religion</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Outcome Column</label>
            <select className="form-control" value={config.outcomeCol} onChange={e => setConfig(c => ({...c, outcomeCol: e.target.value}))}>
              <option value="approved">approved</option>
              <option value="hired">hired</option>
              <option value="diagnosed">diagnosed</option>
              <option value="granted">granted</option>
              <option value="score">score</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Reference Group (privileged)</label>
            <select className="form-control" value={config.refGroup} onChange={e => setConfig(c => ({...c, refGroup: e.target.value}))}>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="white">White</option>
              <option value="young">Young (18–35)</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Fairness Threshold</label>
            <select className="form-control" value={config.threshold} onChange={e => setConfig(c => ({...c, threshold: e.target.value}))}>
              <option value="strict">Strict (80/20 rule)</option>
              <option value="moderate">Moderate (75/25 rule)</option>
              <option value="lenient">Lenient (70/30 rule)</option>
            </select>
          </div>
        </div>

        <div className="form-group" style={{marginTop:'16px'}}>
          <label className="form-label">Audit Label (for history tracking)</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g. Q4 2024 Loan Model v2.3"
            value={config.label}
            onChange={e => setConfig(c => ({...c, label: e.target.value}))}
          />
        </div>

        {/* Metric toggles */}
        <div className="metric-toggles">
          <p className="form-label" style={{marginBottom:'10px'}}>Metrics to calculate</p>
          <div className="toggle-row">
            {[
              { id:'dp', label:'Demographic Parity', color:'var(--accent)' },
              { id:'eo', label:'Equal Opportunity',  color:'var(--info)' },
              { id:'eq', label:'Equalized Odds',     color:'var(--purple)' },
            ].map(m => (
              <div key={m.id} className="toggle-item">
                <div className="toggle-check" style={{borderColor: m.color, background: m.color}}>
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5l2 2 4-4" stroke="#000" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </div>
                <span style={{fontSize:'13px', color:'var(--text2)'}}>{m.label}</span>
              </div>
            ))}
          </div>
        </div>

        <button
          className="run-btn"
          disabled={!hasData}
          onClick={handleStart}
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <polygon points="5,3 16,9 5,15" fill="currentColor"/>
          </svg>
          {hasData ? 'Run Fairness Audit' : 'Upload a dataset or pick a sample to start'}
        </button>
      </div>

      {/* Info chips */}
      <div className="analyze-info-row">
        <div className="info-chip">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1a6 6 0 100 12A6 6 0 007 1zM7 6v4M7 4v.5" stroke="var(--text3)" strokeWidth="1.2" strokeLinecap="round"/></svg>
          Results powered by Fairlearn + Gemini 1.5 Pro via Vertex AI
        </div>
        <div className="info-chip">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1a6 6 0 100 12A6 6 0 007 1zM7 6v4M7 4v.5" stroke="var(--text3)" strokeWidth="1.2" strokeLinecap="round"/></svg>
          Audit reports saved to Firestore for history tracking
        </div>
        <div className="info-chip">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1a6 6 0 100 12A6 6 0 007 1zM7 6v4M7 4v.5" stroke="var(--text3)" strokeWidth="1.2" strokeLinecap="round"/></svg>
          CSV uploaded securely to Google Cloud Storage
        </div>
      </div>
    </div>
  )
}

export default Analyze