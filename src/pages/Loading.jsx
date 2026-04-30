import { useEffect, useState } from 'react'
import { SAMPLE_CONFIGS } from '../App.jsx'
import './Loading.css'

const STEPS = [
  { id: 1, label: 'Uploading dataset to Google Cloud Storage' },
  { id: 2, label: 'Parsing CSV and validating structure' },
  { id: 3, label: 'Computing Demographic Parity' },
  { id: 4, label: 'Computing Equal Opportunity' },
  { id: 5, label: 'Computing Equalized Odds' },
  { id: 6, label: 'Generating Fairness Score (0–100)' },
  { id: 7, label: 'Sending metrics to Gemini AI via Vertex AI' },
  { id: 8, label: 'Building your audit report' },
]

function Loading({ navigate, auditConfig, setAuditResult, addHistory }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [done, setDone] = useState(false)

  useEffect(() => {
    let step = 0
    const interval = setInterval(() => {
      step++
      setCurrentStep(step)
      if (step >= STEPS.length) {
        clearInterval(interval)
        setTimeout(() => {
          setDone(true)
          // Build result from config
          const key = auditConfig?.key || 'loan'
          const cfg = SAMPLE_CONFIGS[key]
          const result = {
            ...cfg,
            label: auditConfig?.label || cfg.label,
            attr: auditConfig?.protectedAttr || cfg.attr,
            date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
          }
          setAuditResult(result)
          addHistory({
            id: Date.now(),
            label: result.label,
            attr: result.attr,
            score: result.score,
            dp: result.dp,
            eo: result.eo,
            eq: result.eq,
            level: result.level,
            date: result.date,
            key,
          })
          setTimeout(() => navigate('results'), 600)
        }, 300)
      }
    }, 520)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="loading-page">
      <div className="loading-inner">
        {/* Spinner */}
        <div className="spinner-wrap">
          <div className={`spinner-ring ${done ? 'done' : ''}`}>
            {done && (
              <div className="spinner-check">
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                  <path d="M5 14l7 7L23 7" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            )}
          </div>
        </div>

        <h2 className="loading-title">
          {done ? 'Audit complete!' : 'Analyzing your dataset…'}
        </h2>
        <p className="loading-sub">
          {done
            ? 'Your fairness report is ready. Redirecting…'
            : `Step ${Math.min(currentStep + 1, STEPS.length)} of ${STEPS.length} · Usually takes 10–30 seconds`}
        </p>

        {/* Steps list */}
        <div className="steps-list">
          {STEPS.map((step, i) => {
            const isDone   = i < currentStep
            const isActive = i === currentStep
            return (
              <div key={step.id} className={`step-row ${isDone ? 'done' : ''} ${isActive ? 'active' : ''}`}>
                <div className="step-dot-wrap">
                  {isDone ? (
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="8" fill="var(--accent)" fillOpacity=".2"/>
                      <path d="M4 8l3 3 5-5" stroke="var(--accent)" strokeWidth="1.4" strokeLinecap="round"/>
                    </svg>
                  ) : isActive ? (
                    <div className="dot-active" />
                  ) : (
                    <div className="dot-pending" />
                  )}
                </div>
                <span className="step-label">{step.label}</span>
                {isActive && <div className="step-spinner" />}
              </div>
            )
          })}
        </div>

        {/* Progress bar */}
        <div className="progress-track">
          <div
            className="progress-bar-fill"
            style={{ width: `${(currentStep / STEPS.length) * 100}%` }}
          />
        </div>
        <p className="progress-pct">{Math.round((currentStep / STEPS.length) * 100)}%</p>
      </div>
    </div>
  )
}

export default Loadings