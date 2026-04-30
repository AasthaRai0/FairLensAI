import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Landing from './pages/Landing.jsx'
import Analyze from './pages/Analyze.jsx'
import Loading from './pages/Loading.jsx'
import Results from './pages/Results.jsx'
import History from './pages/History.jsx'

// Sample datasets config
export const SAMPLE_CONFIGS = {
  loan: {
    label: 'Loan Approval Dataset',
    attr: 'Gender',
    outcome: 'approved',
    refGroup: 'Male',
    score: 30,
    level: 'low',
    groups: { Male: 70, Female: 40 },
    tprGroups: { Male: 80, Female: 55 },
    fprGroups: { Male: 12, Female: 28 },
    dp: 23, eo: 48, eq: 52,
    geminiAnalysis: `Your loan approval model has a critical fairness violation. The Demographic Parity score of 23/100 reveals male applicants are approved at 70% while female applicants receive only 40% approval — a 30 percentage-point gap that strongly indicates systemic gender bias baked into the model's decision logic. This pattern mirrors historical lending discrimination where women were denied credit at disproportionate rates. Your model has learned and is now amplifying these historical inequities at scale. The Equal Opportunity score of 48/100 is particularly alarming: even among demonstrably creditworthy applicants, women are correctly identified as low-risk significantly less often than men. The Equalized Odds score of 52/100 confirms that false positive rates diverge sharply — male applicants who shouldn't qualify are approved at 12%, while female applicants who shouldn't qualify are approved at 28%, suggesting the model applies different risk thresholds by gender.`,
    fixes: [
      { title: 'Rebalance training data', detail: 'Apply SMOTE (Synthetic Minority Oversampling Technique) to increase female applicant representation. Target at least 45/55 gender balance before retraining. Use Fairlearn\'s resample() utility to generate balanced datasets.' },
      { title: 'Apply fairness constraints during retraining', detail: 'Use Fairlearn\'s ExponentiatedGradient optimizer with DemographicParity or EqualizedOdds constraint. This directly penalizes disparate impact during the training loop rather than patching it afterward.' },
      { title: 'Audit proxy feature correlations', detail: 'Check if features like employment sector, income type, or zip code are correlated with gender (Pearson r > 0.3). Remove or debias these proxy variables before the model uses them to avoid indirect discrimination.' },
    ]
  },
  hiring: {
    label: 'Hiring Records Q1 2025',
    attr: 'Race',
    outcome: 'hired',
    refGroup: 'White',
    score: 61,
    level: 'mid',
    groups: { White: 68, Hispanic: 52, Black: 45, Asian: 61 },
    tprGroups: { White: 75, Hispanic: 60, Black: 55, Asian: 70 },
    fprGroups: { White: 8, Hispanic: 15, Black: 18, Asian: 10 },
    dp: 58, eo: 67, eq: 62,
    geminiAnalysis: `Your hiring model shows moderate fairness issues with a score of 61/100. The Demographic Parity gap is most pronounced between White candidates (68% hire rate) and Black candidates (45% hire rate) — a 23-point disparity that exceeds the 80% rule threshold mandated by EEOC guidelines. Hispanic candidates are also underrepresented at 52%. The Equal Opportunity score of 67/100 suggests the model does reasonably well identifying qualified candidates across races, but still systematically undervalues qualified Black and Hispanic applicants. This pattern is consistent with resume screening bias where names, schools, and neighborhood zip codes act as racial proxies.`,
    fixes: [
      { title: 'Blind resume screening', detail: 'Remove name, address, graduation year, and school name from features. These are documented racial proxies. Use only skills, experience years, and assessment scores.' },
      { title: 'Apply threshold calibration by group', detail: 'Use Fairlearn\'s ThresholdOptimizer to set group-specific decision thresholds that equalize true positive rates across racial groups while maintaining overall accuracy.' },
      { title: 'Audit structured interview scoring', detail: 'If interview scores feed the model, audit interviewer scoring patterns by candidate race. Implement blind scoring rubrics and calibration sessions to reduce unconscious bias in human-generated features.' },
    ]
  },
  medical: {
    label: 'Medical Diagnosis Data',
    attr: 'Gender',
    outcome: 'diagnosed',
    refGroup: 'Male',
    score: 44,
    level: 'low',
    groups: { Male: 72, Female: 48 },
    tprGroups: { Male: 85, Female: 61 },
    fprGroups: { Male: 9, Female: 22 },
    dp: 41, eo: 49, eq: 55,
    geminiAnalysis: `Your medical diagnosis model has a serious fairness failure with a score of 44/100. Female patients are diagnosed correctly at a 48% rate versus 72% for male patients — a gap with direct life-or-death consequences. The Equal Opportunity score of 49/100 is the most critical finding: among truly ill female patients, only 61% are correctly identified versus 85% of ill male patients. This means female patients with real conditions are being sent home undiagnosed at alarming rates. This matches known medical AI bias patterns where training datasets are historically male-dominated (many foundational clinical datasets are 70%+ male). The model has learned that "typical patient" means "male patient."`,
    fixes: [
      { title: 'Urgent: audit training data composition', detail: 'Immediately check the gender ratio in your training dataset. If < 40% female, halt deployment and collect balanced training data before proceeding. The EU AI Act classifies medical diagnosis as high-risk AI requiring mandatory bias audits.' },
      { title: 'Implement gender-stratified model evaluation', detail: 'Split all model evaluation metrics by gender during development. Require equal sensitivity (recall) across genders as a hard constraint before any model is approved for clinical use.' },
      { title: 'Include gender as explicit feature with fairness constraint', detail: 'Rather than removing gender (which can worsen outcomes), include it with an Equalized Odds constraint so the model learns to account for biological differences while equalizing diagnostic accuracy.' },
    ]
  },
  credit: {
    label: 'Credit Scoring Dataset',
    attr: 'Age Group',
    outcome: 'approved',
    refGroup: 'Young (18–35)',
    score: 78,
    level: 'high',
    groups: { 'Young (18–35)': 65, 'Middle (36–55)': 71, 'Senior (55+)': 58 },
    tprGroups: { 'Young (18–35)': 70, 'Middle (36–55)': 76, 'Senior (55+)': 63 },
    fprGroups: { 'Young (18–35)': 14, 'Middle (36–55)': 11, 'Senior (55+)': 16 },
    dp: 75, eo: 81, eq: 79,
    geminiAnalysis: `Your credit scoring model performs well overall with a Fairness Score of 78/100 — above the 75-point compliance threshold. The model shows relatively balanced outcomes across age groups, with the largest gap being between Middle-aged applicants (71% approval) and Seniors (58% approval). This 13-point gap warrants monitoring but does not yet constitute a serious fairness violation under most regulatory frameworks. The Equal Opportunity score of 81/100 is strong, indicating qualified applicants are being correctly identified across all age groups. Minor improvements to Demographic Parity could push this model into excellent territory.`,
    fixes: [
      { title: 'Monitor Senior approval rates quarterly', detail: 'The 13-point gap between Middle and Senior applicants should be tracked over time. If it widens beyond 20 points, apply fairness retraining. Set automated alerts in your CI/CD fairness pipeline.' },
      { title: 'Review features that may proxy for age', detail: 'Features like years of credit history, retirement income classification, or employment status may inadvertently create age-correlated outcomes. Review feature importance scores for age proxies.' },
      { title: 'Maintain current fairness posture', detail: 'Your model is performing well. Continue regular quarterly audits, document this audit report for regulatory compliance, and use it as a baseline to measure future model drift.' },
    ]
  }
}

function App() {
  const [auditConfig, setAuditConfig] = useState(null)
  const [auditResult, setAuditResult] = useState(null)
  const [history, setHistory] = useState([
    { id: 1, label: 'Loan Approval Model v2.3', attr: 'Gender', score: 30, dp: 23, eo: 48, eq: 52, level: 'low', date: 'Apr 28, 2025', key: 'loan' },
    { id: 2, label: 'Hiring Algorithm Q1 2025', attr: 'Race', score: 61, dp: 58, eo: 67, eq: 62, level: 'mid', date: 'Mar 15, 2025', key: 'hiring' },
    { id: 3, label: 'Credit Scoring v1.8', attr: 'Age Group', score: 78, dp: 75, eo: 81, eq: 79, level: 'high', date: 'Feb 10, 2025', key: 'credit' },
  ])
  const [page, setPage] = useState('landing') // landing | analyze | loading | results | history

  const navigate = (p) => setPage(p)

  const addHistory = (entry) => {
    setHistory(prev => [entry, ...prev])
  }

  const renderPage = () => {
    switch (page) {
      case 'landing':  return <Landing navigate={navigate} />
      case 'analyze':  return <Analyze navigate={navigate} setAuditConfig={setAuditConfig} setAuditResult={setAuditResult} />
      case 'loading':  return <Loading navigate={navigate} auditConfig={auditConfig} setAuditResult={setAuditResult} addHistory={addHistory} />
      case 'results':  return <Results navigate={navigate} auditResult={auditResult} />
      case 'history':  return <History navigate={navigate} history={history} setAuditResult={setAuditResult} />
      default:         return <Landing navigate={navigate} />
    }
  }

  return (
    <div>
      <Navbar navigate={navigate} currentPage={page} />
      {renderPage()}
    </div>
  )
}

export default App