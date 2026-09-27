import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import apiClient from "../api/client.js";
import { sendManualAlert } from "../api/telegramClient.js";
import { formatCrore, formatPercent } from "../utils/formatters.js";

const QUESTIONS = [
  {
    id: "land_acquisition",
    question: "Q1. Are there delays in land acquisition, site handover, or utility shifting?",
    weight: 25,
    why: "This is the strongest operational delay driver seen in infrastructure projects. It aligns with schedule slippage and low progress.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  },
  {
    id: "financial_result",
    question: "Q2. Are funds / budget releases / cash flow delays affecting execution?",
    weight: 20,
    why: "The historical dataset strongly supports cost overrun risk when expenditure rises faster than physical progress.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  },
  {
    id: "approval_clearance",
    question: "Q3. Are approvals, clearances, or administrative decisions pending?",
    weight: 20,
    why: "Approval delays often produce schedule revision and target date shifts.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  },
  {
    id: "procurement_result",
    question: "Q4. Are there contractor, vendor, or procurement bottlenecks?",
    weight: 15,
    why: "Execution delays often come from contractor performance or supply-chain slowdowns.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  },
  {
    id: "scope_design",
    question: "Q5. Has the project scope or design changed after sanction?",
    weight: 10,
    why: "Scope revision often leads to both cost and schedule impact.",
    options: ["No change", "Minor changes", "Moderate changes", "Major changes", "Severe changes"]
  },
  {
    id: "execution_pace",
    question: "Q6. Is the execution pace slower than planned due to site issues, labor, or coordination problems?",
    weight: 10,
    why: "Persistent site execution issues are a common cause of poor progress-to-spend mismatch.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  },
  {
    id: "interagency_coordination",
    question: "Q7. Are there local-level or inter-agency coordination problems?",
    weight: 5,
    why: "This covers a broad residual category that often compounds other issues.",
    options: ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"]
  }
];

export default function ProjectAnalysisPage() {
  const { project, predictions } = useProject();

  const [answers, setAnswers] = useState({
    land_acquisition: "No issue",
    financial_result: "No issue",
    approval_clearance: "No issue",
    procurement_result: "No issue",
    scope_design: "No change",
    execution_pace: "No issue",
    interagency_coordination: "No issue"
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [alertNote, setAlertNote] = useState("");
  const [alertStatus, setAlertStatus] = useState("");
  const [sendingAlert, setSendingAlert] = useState(false);

  const evaluationRef = useRef(null);

  if (!project || !predictions) {
    return (
      <div className="panel empty-state-panel">
        <h1>Project analysis</h1>
        <p>No project has been submitted yet. Create a new project to generate risk analysis.</p>
        <div className="hero-panel__actions">
          <Link to="/projects/new" className="primary-btn">
            Create project
          </Link>
          <Link to="/dashboard" className="secondary-btn">
            Open dashboard
          </Link>
        </div>
      </div>
    );
  }

  const handleOptionChange = (questionId, optionValue) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: optionValue
    }));
  };

  const handleManualAlert = async () => {
    setSendingAlert(true);
    setAlertStatus("");

    try {
      await sendManualAlert(project, predictions, alertNote);
      setAlertStatus("Alert sent to Telegram.");
      setAlertNote("");
    } catch (err) {
      console.error("Manual Telegram alert failed:", err);
      setAlertStatus("The alert could not be sent. Please try again.");
    } finally {
      setSendingAlert(false);
    }
  };

  const handleQuestionnaireSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const payload = {
        projectName: project.project_name,
        landAcquisition: answers.land_acquisition,
        financialResult: answers.financial_result,
        approvalClearance: answers.approval_clearance,
        procurementResult: answers.procurement_result,
        scopeDesign: answers.scope_design,
        executionPace: answers.execution_pace,
        interagencyCoordination: answers.interagency_coordination,
      };

      const { data: questionnaire } = await apiClient.post("/api/mitigation/questionnaire", payload);
      const { data } = await apiClient.post("/api/mitigation/generate", {
        projectName: questionnaire.projectName,
        sessionId: questionnaire.sessionId,
      });
      const strategies = data.mitigation_strategies || data.mitigation_stratergies || [data.mitigationStrategy].filter(Boolean);

      setEvaluation({
        project_name: data.project_name || project.project_name,
        mitigation_strategies: strategies,
      });

      setTimeout(() => {
        evaluationRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (err) {
      setError(err.response?.data?.detail || "Questionnaire submission failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <section className="panel detail-panel">
        <div className="section-heading section-heading--stacked">
          <div>
            <span className="soft-pill">Project intelligence</span>
            <h1>{project.project_name}</h1>
          </div>
          <div className="status-group">
            <RiskBadge tier={predictions.overall_risk_tier} label="Overall" />
            <RiskBadge tier={predictions.cost_risk_tier} label="Cost" />
            <RiskBadge tier={predictions.time_risk_tier} label="Time" />
          </div>
        </div>

        <div className="stats-grid stats-grid--compact">
          <div className="metric-tile">
            <span>Predicted overrun</span>
            <strong>{predictions.predicted_overrun_pct ?? "Not available"}{predictions.predicted_overrun_pct !== null && predictions.predicted_overrun_pct !== undefined ? "%" : ""}</strong>
          </div>
          <div className="metric-tile">
            <span>Predicted delay</span>
            <strong>{predictions.predicted_delay_days ?? "Not available"}{predictions.predicted_delay_days !== null && predictions.predicted_delay_days !== undefined ? " days" : ""}</strong>
          </div>
          <div className="metric-tile">
            <span>Sector</span>
            <strong>{project.sector || "Not available"}</strong>
          </div>
          <div className="metric-tile">
            <span>State</span>
            <strong>{project.state || "Not available"}</strong>
          </div>
        </div>

        <div className="analysis-grid">
          <div className="info-card">
            <h3>Project details</h3>
            <dl>
              <div><dt>Agency</dt><dd>{project.agency || "—"}</dd></div>
              <div><dt>Ministry</dt><dd>{project.ministry || "—"}</dd></div>
              <div><dt>Original cost (₹ Cr)</dt><dd>{formatCrore(project.original_cost_cr)}</dd></div>
              <div><dt>Expenditure (₹ Cr)</dt><dd>{formatCrore(project["cumulative expenditure in rs. crore"] ?? project.cumulative_expenditure)}</dd></div>
              <div><dt>Physical progress</dt><dd>{formatPercent(project["physical progress (in percentage)"] ?? project.physical_progress)}</dd></div>
              <div><dt>Approval date</dt><dd>{project.date_of_approval || "—"}</dd></div>
            </dl>
          </div>

          <div className="info-card">
            <h3>Recommended action</h3>
            <ul className="bullet-list">
              <li>Review cost escalation triggers with the implementing agency.</li>
              <li>Validate schedule assumptions against procurement and land acquisition status.</li>
              <li>Escalate project oversight if the risk remains elevated for the next review cycle.</li>
            </ul>
            <div className="hero-panel__actions hero-panel__actions--stacked">
              <Link to="/chatbot" className="primary-btn">
                Ask chatbot
              </Link>
              <Link to="/dashboard" className="secondary-btn">
                Dashboard
              </Link>
            </div>
            <div className="mt-6 border-t border-slate-200 pt-5">
              <h4 className="font-semibold text-[#002B49]">Send Telegram alert</h4>
              <p className="mt-1 text-sm text-slate-600">Notify the team manually, regardless of the project risk value.</p>
              <textarea
                value={alertNote}
                onChange={(event) => setAlertNote(event.target.value)}
                placeholder="Add a note for the team (optional)"
                rows={3}
                className="field-input mt-3 w-full resize-y"
              />
              <button
                type="button"
                onClick={handleManualAlert}
                disabled={sendingAlert}
                className="primary-btn mt-3"
              >
                {sendingAlert ? "Sending alert..." : "Send Telegram alert"}
              </button>
              {alertStatus && <p className="mt-2 text-sm text-slate-600">{alertStatus}</p>}
            </div>
          </div>
        </div>
      </section>

      {/* QUESTIONNAIRE SECTION AT THE BOTTOM OF ANALYSIS PAGE */}
      <section className="questionnaire-panel">
        <div className="page-header" style={{ marginBottom: "1rem" }}>
          <span className="soft-pill">Root Cause Analysis</span>
          <h2 style={{ fontSize: "1.8rem", color: "#002B49", margin: "0.25rem 0" }}>
            Operational Risk & Bottleneck Questionnaire
          </h2>
          <p>
            Complete the 7 multiple-choice operational questions below to calculate weighted bottleneck scores and receive tailored mitigation strategies from the PAIMANA backend.
          </p>
        </div>

        <form onSubmit={handleQuestionnaireSubmit}>
          {QUESTIONS.map((q) => (
            <div key={q.id} className="question-card">
              <div className="question-card__header">
                <h3 className="question-title">{q.question}</h3>
                <span className="weight-tag">Weight: {q.weight}</span>
              </div>

              <div className="option-pills-grid">
                {q.options.map((opt) => {
                  const isActive = answers[q.id] === opt;
                  return (
                    <button
                      key={opt}
                      type="button"
                      className={`option-btn ${isActive ? "option-btn--active" : ""}`}
                      onClick={() => handleOptionChange(q.id, opt)}
                    >
                      {isActive ? "✓ " : ""}{opt}
                    </button>
                  );
                })}
              </div>

              <div className="question-why">
                <strong>Why:</strong> {q.why}
              </div>
            </div>
          ))}

          {error && <p className="form-message form-message--error mt-4">{error}</p>}

          <div className="mt-6 flex gap-4 items-center">
            <button type="submit" className="primary-btn" disabled={submitting}>
              {submitting ? "Evaluating Risk & Generating Strategy..." : "Submit Questionnaire & Evaluate"}
            </button>
          </div>
        </form>

        {/* EVALUATION RESULTS DISPLAYED ON THE SAME PAGE WITHOUT REFRESH */}
        {evaluation && (
          <div ref={evaluationRef} className="evaluation-results-panel">
            <div className="eval-header">
              <div>
                <span style={{ fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "rgba(255,255,255,0.7)" }}>
                  Mitigation Strategies
                </span>
                <h2 style={{ margin: "0.25rem 0 0", fontSize: "1.8rem", color: "#ffffff" }}>
                  {evaluation.project_name}
                </h2>
              </div>
            </div>

            <div>
              <h3 style={{ fontSize: "1.1rem", color: "#D4AF37", marginBottom: "0.75rem", fontWeight: 700 }}>
                Recommended actions ({evaluation.mitigation_strategies.length})
              </h3>
              {evaluation.mitigation_strategies.length === 0 ? (
                <p style={{ color: "rgba(255,255,255,0.8)", fontSize: "0.95rem" }}>
                  All operational parameters are currently within normal thresholds.
                </p>
              ) : (
                <div>
                  {evaluation.mitigation_strategies.map((m, idx) => (
                    <div key={idx} className="mitigation-item">
                      <p style={{ margin: 0, fontSize: "0.92rem", color: "rgba(255,255,255,0.9)", lineHeight: 1.5 }}>
                        {m}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
