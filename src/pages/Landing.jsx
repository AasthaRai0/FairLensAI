import { SAMPLE_CONFIGS } from '../App.jsx'
import './Landing.css'

function Landing({ navigate }) {
  return (
    <div className="landing">

      {/* ── HERO ── */}
      <section className="hero">
        <div className="hero-glow" />
        <div className="hero-content">
          <div className="badge badge-accent animate-fade-up">
            <span className="pulse-dot" />
            Powered by Google Gemini AI &amp; Cloud Run
          </div>

          <h1 className="hero-title animate-fade-up">
            AI That Measures<br />
            <span className="hero-grad">Fairness,<br />Not Just Accuracy</span>
          </h1>

          <p className="hero-desc animate-fade-up">
            Upload your dataset. Get a mathematical bias audit, a Gemini-powered
            plain-English explanation, and exact steps to fix discrimination — in under 2 minutes.
            No code. No expertise required.
          </p>

          <div className="hero-actions animate-fade-up">
            <button className="btn-primary btn-lg" onClick={() => navigate('analyze')}>
              Start Free Audit
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button className="btn-outline btn-lg" onClick={() => navigate('results')}>
              View Sample Report
            </button>
          </div>

          {/* Trust line */}
          <div className="trust-row animate-fade-up">
            <span className="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7l4 4 6-6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
              Google Cloud Native
            </span>
            <span className="trust-sep" />
            <span className="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7l4 4 6-6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
              Gemini AI Explanations
            </span>
            <span className="trust-sep" />
            <span className="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7l4 4 6-6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
              EU AI Act Ready
            </span>
          </div>
        </div>

        {/* Hero preview card */}
        <div className="hero-preview animate-fade-up">
          <div className="preview-card">
            <div className="preview-header">
              <span className="preview-label">FAIRNESS AUDIT RESULT</span>
              <span className="badge badge-danger" style={{fontSize:'11px'}}>LOW FAIRNESS</span>
            </div>
            <div className="preview-score-row">
              <div className="preview-score-circle" style={{'--score-pct':'30%'}}>
                <span className="preview-score-num" style={{color:'var(--danger)'}}>30</span>
                <span className="preview-score-sub">/100</span>
              </div>
              <div className="preview-metrics">
                <PreviewMetric label="Dem. Parity" score={23} color="var(--danger)" />
                <PreviewMetric label="Equal Opp." score={48} color="var(--warn)" />
                <PreviewMetric label="Eq. Odds" score={52} color="var(--warn)" />
              </div>
            </div>
            <div className="preview-gemini">
              <span className="gemini-badge">GEMINI AI</span>
              <p className="preview-gemini-text">
                Male applicants approved at 70% vs 40% for females. Recommend rebalancing training data and applying fairness constraints…
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section className="stats-bar">
        <div className="stat"><span className="stat-num">3</span><span className="stat-label">Fairness Metrics</span></div>
        <div className="stat-divider" />
        <div className="stat"><span className="stat-num">0–100</span><span className="stat-label">Universal Score</span></div>
        <div className="stat-divider" />
        <div className="stat"><span className="stat-num">0</span><span className="stat-label">Lines of Code Needed</span></div>
        <div className="stat-divider" />
        <div className="stat"><span className="stat-num">GCP</span><span className="stat-label">Fully Cloud Native</span></div>
        <div className="stat-divider" />
        <div className="stat"><span className="stat-num">~$0</span><span className="stat-label">MVP Cost (Free Tier)</span></div>
      </section>

      {/* ── FEATURES ── */}
      <section className="section">
        <div className="section-inner">
          <p className="section-tag">Core Metrics</p>
          <h2 className="section-title">Three metrics.<br/>One fairness score.</h2>
          <p className="section-sub">Industry-standard mathematical definitions, calculated automatically and explained by Gemini AI.</p>

          <div className="features-grid">
            <div className="feature-card card card-hover">
              <div className="feature-icon" style={{background:'var(--accent-dim)'}}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <rect x="3" y="8" width="4" height="11" rx="1" fill="var(--accent)" opacity=".5"/>
                  <rect x="9" y="4" width="4" height="15" rx="1" fill="var(--accent)"/>
                  <rect x="15" y="6" width="4" height="13" rx="1" fill="var(--accent)" opacity=".5"/>
                </svg>
              </div>
              <h3>Demographic Parity</h3>
              <p>Checks whether <strong>selection rates are equal</strong> across all demographic groups — catching approval rate disparities before they harm real people.</p>
              <div className="feature-formula">P(Ŷ=1|A=0) = P(Ŷ=1|A=1)</div>
            </div>

            <div className="feature-card card card-hover">
              <div className="feature-icon" style={{background:'var(--info-dim)'}}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <circle cx="11" cy="11" r="8" stroke="var(--info)" strokeWidth="1.5" fill="none"/>
                  <path d="M7 11l3 3 5-5" stroke="var(--info)" strokeWidth="1.8" strokeLinecap="round"/>
                </svg>
              </div>
              <h3>Equal Opportunity</h3>
              <p>Measures if <strong>true positive rates are equal</strong> — ensuring qualified individuals from all groups are identified correctly.</p>
              <div className="feature-formula">P(Ŷ=1|A=0, Y=1) = P(Ŷ=1|A=1, Y=1)</div>
            </div>

            <div className="feature-card card card-hover">
              <div className="feature-icon" style={{background:'var(--purple-dim)'}}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <path d="M4 11h14M4 7h14M4 15h14" stroke="var(--purple)" strokeWidth="1.5" strokeLinecap="round"/>
                  <circle cx="9" cy="7" r="2" fill="var(--purple)"/>
                  <circle cx="14" cy="11" r="2" fill="var(--purple)"/>
                  <circle cx="9" cy="15" r="2" fill="var(--purple)"/>
                </svg>
              </div>
              <h3>Equalized Odds</h3>
              <p>Verifies that <strong>error rates are balanced</strong> across groups — both false positives and false negatives are examined together.</p>
              <div className="feature-formula">FPR equal AND TPR equal across groups</div>
            </div>

            <div className="feature-card card card-hover">
              <div className="feature-icon" style={{background:'var(--warn-dim)'}}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <path d="M11 3L3 19h16L11 3z" stroke="var(--warn)" strokeWidth="1.5" fill="none" strokeLinejoin="round"/>
                  <path d="M11 9v5M11 16v1" stroke="var(--warn)" strokeWidth="1.8" strokeLinecap="round"/>
                </svg>
              </div>
              <h3>Gemini AI Explanations</h3>
              <p>Google Gemini converts raw metric numbers into <strong>plain-English diagnosis</strong> and specific fix recommendations anyone can understand.</p>
              <div className="feature-formula">Numbers → Human Language → Action Plan</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section className="section how-section">
        <div className="section-inner">
          <p className="section-tag">Process</p>
          <h2 className="section-title">From CSV to report<br/>in under 2 minutes</h2>

          <div className="steps-grid">
            {[
              { num:'01', title:'Upload Dataset', desc:'Upload any CSV — loan records, hiring data, medical decisions. No coding, no setup.', icon:'📂', color:'var(--accent)' },
              { num:'02', title:'Auto Analysis', desc:'Our engine automatically calculates all 3 fairness metrics and generates your 0–100 Fairness Score.', icon:'⚡', color:'var(--info)' },
              { num:'03', title:'Gemini Report', desc:'Get a plain-English explanation + step-by-step fix recommendations powered by Google Gemini.', icon:'🤖', color:'var(--purple)' },
            ].map((step, i) => (
              <div key={i} className="step-card card">
                <div className="step-num" style={{color: step.color}}>{step.num}</div>
                <div className="step-icon">{step.icon}</div>
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── COMPARISON TABLE ── */}
      <section className="section">
        <div className="section-inner">
          <p className="section-tag">Why FairLens</p>
          <h2 className="section-title">Built for everyone,<br/>not just data scientists</h2>

          <div className="compare-table-wrap card">
            <table className="compare-table">
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>IBM AIF360</th>
                  <th>Fairlearn</th>
                  <th className="highlight-col">FairLens</th>
                </tr>
              </thead>
              <tbody>
                {[
                  ['No-code web upload', false, false, true],
                  ['Gemini AI plain-English explanations', false, false, true],
                  ['Fairness Score (0–100)', false, false, true],
                  ['Fix recommendations', false, false, true],
                  ['Cloud deployed', false, false, true],
                  ['Audit history dashboard', false, false, true],
                  ['Built for non-technical users', false, false, true],
                  ['Calculates fairness metrics', true, true, true],
                ].map(([feature, ibm, fl, ours], i) => (
                  <tr key={i}>
                    <td>{feature}</td>
                    <td><Tick val={ibm} /></td>
                    <td><Tick val={fl} /></td>
                    <td className="highlight-col"><Tick val={ours} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ── SDGs ── */}
      <section className="section sdg-section">
        <div className="section-inner">
          <p className="section-tag">Impact</p>
          <h2 className="section-title">Aligned with UN Sustainable<br/>Development Goals</h2>
          <div className="sdg-grid">
            <div className="sdg-card card"><span className="sdg-num">SDG 10</span><span className="sdg-label">Reduced Inequalities</span></div>
            <div className="sdg-card card"><span className="sdg-num">SDG 16</span><span className="sdg-label">Justice & Strong Institutions</span></div>
            <div className="sdg-card card"><span className="sdg-num">SDG 8</span><span className="sdg-label">Decent Work & Economic Growth</span></div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="cta-section">
        <div className="cta-glow" />
        <h2>Ready to audit your AI?</h2>
        <p>It's free. No account needed. No code required.</p>
        <div style={{display:'flex', gap:'12px', justifyContent:'center', flexWrap:'wrap'}}>
          <button className="btn-primary btn-lg" onClick={() => navigate('analyze')}>
            Start Audit Now →
          </button>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-logo">
          <div className="logo-icon" style={{width:'24px',height:'24px'}}>
            <svg viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" style={{width:'14px',height:'14px'}}>
              <circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
            </svg>
          </div>
          <span style={{fontFamily:'Syne,sans-serif',fontWeight:700,fontSize:'15px'}}>Fair<span style={{color:'var(--accent)'}}>Lens</span></span>
        </div>
        <p className="footer-text">Built for Google Solution Challenge 2025 · Powered by Gemini AI &amp; Google Cloud</p>
        <div className="footer-tech">
          <span>Vertex AI</span><span>Cloud Run</span><span>Firebase</span><span>Firestore</span><span>Fairlearn</span>
        </div>
      </footer>
    </div>
  )
}

function PreviewMetric({ label, score, color }) {
  return (
    <div style={{display:'flex',flexDirection:'column',gap:'4px'}}>
      <div style={{fontSize:'11px',color:'var(--text3)'}}>{label}</div>
      <div style={{height:'6px',background:'var(--surface3)',borderRadius:'3px',overflow:'hidden'}}>
        <div style={{height:'100%',width:`${score}%`,background:color,borderRadius:'3px'}} />
      </div>
      <div style={{fontSize:'12px',fontWeight:'600',color}}>{score}/100</div>
    </div>
  )
}

function Tick({ val }) {
  if (val) return <span style={{color:'var(--accent)',fontWeight:'700',fontSize:'16px'}}>✓</span>
  return <span style={{color:'var(--text3)',fontSize:'16px'}}>–</span>
}

export default Landing