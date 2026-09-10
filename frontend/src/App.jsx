import { useEffect, useMemo, useState } from 'react'
import {
  AlertTriangle,
  BarChart3,
  Building2,
  CalendarClock,
  CircleDollarSign,
  Gauge,
  MapPin,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import { sendTelegramAlert } from './services/telegramService'
import './App.css'

const initialForm = {
  project_name: '',
  agency: '',
  state: '',
  ministry: '',
  sector: '',
  status: 'Ongoing',
  original_cost_cr: 0,
  cumulative_expenditure: 0,
  physical_progress: 0,
  date_of_approval: '2024-01-15',
  start_date: '2024-02-01',
  target_date_of_completion: '2027-12-31',
}

const riskToneMap = {
  Low: 'badge-green',
  Moderate: 'badge-yellow',
  High: 'badge-red',
  Critical: 'badge-red',
}

const fieldConfig = [
  { name: 'project_name', label: 'Project name', type: 'text', placeholder: 'e.g. NH-48 Capacity Upgrade' },
  { name: 'agency', label: 'Agency', type: 'text', placeholder: 'e.g. NHAI / PWD / Railways' },
  { name: 'state', label: 'State', type: 'text', placeholder: 'e.g. Maharashtra' },
  { name: 'ministry', label: 'Ministry', type: 'text', placeholder: 'e.g. Ministry of Road Transport' },
  { name: 'sector', label: 'Sector', type: 'text', placeholder: 'e.g. Roads / Rail / Power' },
  { name: 'status', label: 'Status', type: 'text', placeholder: 'e.g. Ongoing / Delayed / Critical' },
  { name: 'original_cost_cr', label: 'Original cost (₹ Cr)', type: 'number', placeholder: '2500' },
  { name: 'cumulative_expenditure', label: 'Cumulative expenditure (₹ Cr)', type: 'number', placeholder: '980' },
  { name: 'physical_progress', label: 'Physical progress (%)', type: 'number', placeholder: '42' },
  { name: 'date_of_approval', label: 'Date of approval', type: 'date' },
  { name: 'start_date', label: 'Start date', type: 'date' },
  { name: 'target_date_of_completion', label: 'Target completion date', type: 'date' },
]

const formatCurrency = (value) =>
  Number(value || 0).toLocaleString('en-IN', {
    maximumFractionDigits: 2,
  })

export default function App() {
  const [formData, setFormData] = useState(initialForm)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [aiOpen, setAiOpen] = useState(false)
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [chatMessages, setChatMessages] = useState([
    { role: 'assistant', text: 'Namaste! Ask me about this project risk, delay, or cost profile.' },
  ])

  const summaryCards = useMemo(() => {
    if (!analysis) return []

    const p = analysis.predictions
    return [
      {
        label: 'Predicted overrun',
        value: `${Number(p.predicted_overrun_pct || 0).toFixed(1)}%`,
        tone: 'danger',
        icon: CircleDollarSign,
      },
      {
        label: 'Predicted delay',
        value: `${Number(p.predicted_delay_days || 0).toFixed(1)} days`,
        tone: 'warning',
        icon: CalendarClock,
      },
      {
        label: 'Cost risk tier',
        value: p.cost_risk_tier || 'Moderate',
        tone: 'neutral',
        icon: Gauge,
      },
      {
        label: 'Overall risk',
        value: p.overall_risk_tier || 'Moderate',
        tone: 'strong',
        icon: ShieldCheck,
      },
    ]
  }, [analysis])

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((current) => ({
      ...current,
      [name]: ['original_cost_cr', 'cumulative_expenditure', 'physical_progress'].includes(name)
        ? Number(value || 0)
        : value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const text = await response.text()
      if (!response.ok) {
        throw new Error(text || 'Prediction failed')
      }

      const payload = JSON.parse(text)
      setAnalysis(payload)
    } catch (err) {
      console.error(err)
      setError(err.message || 'Prediction failed. Please check the backend server.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setAnalysis(null)
    setError('')
    setAiOpen(false)
    setChatInput('')
    setChatMessages([{ role: 'assistant', text: 'Namaste! Ask me about this project risk, delay, or cost profile.' }])
    setFormData(initialForm)
  }

  const handleChatSubmit = async (event) => {
    event.preventDefault()
    const message = chatInput.trim()
    if (!message || !analysis?.session_id) return

    setChatMessages((current) => [...current, { role: 'user', text: message }])
    setChatInput('')
    setChatLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: analysis.session_id,
          message,
        }),
      })

      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload?.detail || 'Chat failed')
      }

      setChatMessages((current) => [...current, { role: 'assistant', text: payload.answer }])
    } catch (err) {
      setChatMessages((current) => [
        ...current,
        { role: 'assistant', text: `Chat error: ${err.message || 'Please try again.'}` },
      ])
    } finally {
      setChatLoading(false)
    }
  }

  const overallRisk = analysis?.predictions?.overall_risk_tier || 'Moderate'
  const isHighRiskProject = ['High', 'Critical'].includes(overallRisk)

  useEffect(() => {
    if (!analysis || !isHighRiskProject) return

    const autoSend = async () => {
      await sendTelegramAlert(
        {
          project_name: formData.project_name || 'Submitted Project',
          risk_level: overallRisk,
          id: analysis.session_id,
        },
        'Automatic high-risk trigger'
      )
    }

    autoSend()
  }, [analysis, formData.project_name, isHighRiskProject, overallRisk])

  const handleManualTelegramAlert = async () => {
    if (!analysis?.session_id) return

    const result = await sendTelegramAlert(
      {
        project_name: formData.project_name || 'Submitted Project',
        risk_level: overallRisk,
        id: analysis.session_id,
      },
      'Manual dispatch button'
    )

    if (result.success) {
      setError('')
      setChatMessages((current) => [
        ...current,
        { role: 'assistant', text: `📣 Telegram alert sent successfully to chat ID 8951589926.` },
      ])
    } else {
      setError(result.error || 'Telegram alert could not be sent.')
    }
  }

  return (
    <div className="paimana-app">
      <header className="topbar">
        <div className="brand-block">
          <div className="brand-mark">P</div>
          <div>
            <p className="eyebrow">Project Intelligence Platform</p>
            <h1>PAIMANA</h1>
          </div>
        </div>

        <div className="topbar-actions">
          <span className="header-badge">
            <Sparkles size={14} /> Live risk engine
          </span>
          {analysis && (
            <button type="button" className="secondary-btn" onClick={handleReset}>
              New project form
            </button>
          )}
        </div>
      </header>

      {!analysis ? (
        <main className="page-shell">
          <section className="form-hero">
            <div>
              <span className="hero-tag">Infrastructure risk evaluation</span>
              <h2>Project intake form</h2>
              <p>
                Enter project data here. On submit, the backend will calculate predicted overrun,
                delay, and risk tier, and the dashboard below will render from that result.
              </p>
            </div>
          </section>

          <form className="project-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              {fieldConfig.map((field) => (
                <label key={field.name} className="field-wrap">
                  <span>{field.label}</span>
                  <input
                    name={field.name}
                    type={field.type}
                    value={formData[field.name]}
                    onChange={handleChange}
                    placeholder={field.placeholder || ''}
                    required={field.type !== 'date' ? true : false}
                  />
                </label>
              ))}
            </div>

            {error && <div className="error-box">{error}</div>}

            <div className="form-actions">
              <button type="submit" className="primary-btn" disabled={loading}>
                {loading ? 'Calculating risk...' : 'Generate dashboard'}
              </button>
            </div>
          </form>
        </main>
      ) : (
        <main className="dashboard-shell">
          <section className="result-hero">
            <div>
              <span className="hero-tag">User submitted project</span>
              <h2>{formData.project_name}</h2>
              <p>
                {formData.agency} • {formData.state} • {formData.ministry} • {formData.sector}
              </p>
            </div>
            <div className="result-hero-actions">
              <div className={`risk-badge ${riskToneMap[overallRisk] || 'badge-yellow'}`}>
                {overallRisk} risk
              </div>
              <button type="button" className="primary-btn" onClick={handleManualTelegramAlert}>
                Send Telegram alert
              </button>
            </div>
          </section>

          <section className="stats-grid">
            {summaryCards.map(({ label, value, tone, icon: Icon }) => (
              <article key={label} className={`stat-card ${tone}`}>
                <div className="stat-header">
                  <span>{label}</span>
                  <span className="icon-wrap"><Icon size={18} /></span>
                </div>
                <strong>{value}</strong>
              </article>
            ))}
          </section>

          <section className="dashboard-grid">
            <article className="panel-card">
              <div className="panel-title-row">
                <div>
                  <p className="panel-kicker">Project overview</p>
                  <h3>Submitted data summary</h3>
                </div>
                <Building2 size={18} />
              </div>

              <ul className="detail-list">
                <li>
                  <span>Agency</span>
                  <strong>{formData.agency}</strong>
                </li>
                <li>
                  <span>State</span>
                  <strong>{formData.state}</strong>
                </li>
                <li>
                  <span>Ministry</span>
                  <strong>{formData.ministry}</strong>
                </li>
                <li>
                  <span>Sector</span>
                  <strong>{formData.sector}</strong>
                </li>
                <li>
                  <span>Status</span>
                  <strong>{formData.status}</strong>
                </li>
                <li>
                  <span>Approval date</span>
                  <strong>{formData.date_of_approval}</strong>
                </li>
              </ul>
            </article>

            <article className="panel-card">
              <div className="panel-title-row">
                <div>
                  <p className="panel-kicker">Financial check</p>
                  <h3>Budget vs execution</h3>
                </div>
                <CircleDollarSign size={18} />
              </div>

              <ul className="detail-list">
                <li>
                  <span>Original cost</span>
                  <strong>₹{formatCurrency(formData.original_cost_cr)} Cr</strong>
                </li>
                <li>
                  <span>Cumulative expenditure</span>
                  <strong>₹{formatCurrency(formData.cumulative_expenditure)} Cr</strong>
                </li>
                <li>
                  <span>Physical progress</span>
                  <strong>{formData.physical_progress}%</strong>
                </li>
                <li>
                  <span>Target completion</span>
                  <strong>{formData.target_date_of_completion}</strong>
                </li>
              </ul>
            </article>
          </section>

          <section className="bottom-grid">
            <article className="panel-card">
              <div className="panel-title-row">
                <div>
                  <p className="panel-kicker">Risk analysis</p>
                  <h3>ML risk output</h3>
                </div>
                <BarChart3 size={18} />
              </div>

              <div className="risk-meter-block">
                <div className="risk-meter-row">
                  <span>Cost risk tier</span>
                  <strong>{analysis.predictions.cost_risk_tier}</strong>
                </div>
                <div className="meter">
                  <span className="meter-fill cost" style={{ width: `${analysis.predictions.predicted_overrun_pct * 2}%` }} />
                </div>

                <div className="risk-meter-row">
                  <span>Time risk tier</span>
                  <strong>{analysis.predictions.time_risk_tier}</strong>
                </div>
                <div className="meter">
                  <span className="meter-fill time" style={{ width: `${Math.min(analysis.predictions.predicted_delay_days / 4, 100)}%` }} />
                </div>
              </div>
            </article>

            <article className="panel-card">
              <div className="panel-title-row">
                <div>
                  <p className="panel-kicker">AI interpretation</p>
                  <h3>Executive takeaway</h3>
                </div>
                <AlertTriangle size={18} />
              </div>

              <div className="insight-box">
                <p>
                  Based on the submitted project profile, the platform estimates a <strong>{analysis.predictions.predicted_overrun_pct}%</strong>{' '}
                  cost overrun and <strong>{analysis.predictions.predicted_delay_days} days</strong> of delay risk.
                </p>
                <p>
                  The current assessment places this project in the <strong>{overallRisk}</strong> band.
                  This dashboard is generated directly from the user-entered data and backend model output.
                </p>
              </div>
            </article>
          </section>
        </main>
      )}

      <button type="button" className="floating-ai-tab" onClick={() => setAiOpen((open) => !open)} aria-label="Open AI chat assistant">
        <Sparkles size={22} />
      </button>

      {aiOpen && (
        <aside className="ai-chat-panel">
          <div className="ai-chat-header">
            <div>
              <p>PAIMANA AI</p>
              <span>Project assistant</span>
            </div>
            <button type="button" className="close-chat" onClick={() => setAiOpen(false)} aria-label="Close AI chat">
              ×
            </button>
          </div>

          <div className="ai-chat-body">
            {chatMessages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`chat-bubble ${message.role}`}>
                {message.text}
              </div>
            ))}
            {chatLoading && <div className="chat-bubble assistant">Thinking...</div>}
          </div>

          <form className="ai-chat-form" onSubmit={handleChatSubmit}>
            <input
              type="text"
              value={chatInput}
              onChange={(event) => setChatInput(event.target.value)}
              placeholder={analysis?.session_id ? 'Ask about this project...' : 'Analyze project first...'}
              disabled={!analysis?.session_id || chatLoading}
            />
            <button type="submit" disabled={!analysis?.session_id || chatLoading}>
              Send
            </button>
          </form>
        </aside>
      )}
    </div>
  )
}
