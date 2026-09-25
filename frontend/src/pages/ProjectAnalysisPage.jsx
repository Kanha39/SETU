import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import apiClient from "../api/client.js";

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
  const { project, predictions, sessionId } = useProject();

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

  const handleQuestionnaireSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const payload = {
        session_id: sessionId,
        project_name: project.project_name,
        ...answers
      };

      const { data } = await apiClient.post("/api/questionnaire/evaluate", payload);
      setEvaluation(data);

      setTimeout(() => {
        evaluationRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (err) {
      setError(err.response?.data?.detail || "Questionnaire submission failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const getTierClass = (tier) => {
    switch (tier?.toLowerCase()) {
      case "low": return "tier-pill--low";
      case "medium": return "tier-pill--medium";
      case "high": return "tier-pill--high";
      case "critical": return "tier-pill--critical";
      default: return "tier-pill--medium";
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
            <strong>{predictions.predicted_overrun_pct}%</strong>
          </div>
          <div className="metric-tile">
            <span>Predicted delay</span>
            <strong>{predictions.predicted_delay_days} days</strong>
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
              <div><dt>Original cost</dt><dd>{project.original_cost_cr || "—"}</dd></div>
              <div><dt>Expenditure</dt><dd>{project.cumulative_expenditure || "—"}</dd></div>
              <div><dt>Physical progress</dt><dd>{project.physical_progress || "—"}</dd></div>
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
                  Operational Assessment Result
                </span>
                <h2 style={{ margin: "0.25rem 0 0", fontSize: "1.8rem", color: "#ffffff" }}>
                  {evaluation.project_name} Operational Diagnosis
                </h2>
              </div>
              <div className="flex items-center gap-3">
                <div className="eval-score-box">
                  <span className="eval-score-num">{evaluation.operational_risk_score}</span>
                  <span className="eval-score-total">/ 100</span>
                </div>
                <span className={`tier-pill ${getTierClass(evaluation.operational_risk_tier)}`}>
                  {evaluation.operational_risk_tier} Operational Risk
                </span>
              </div>
            </div>

            {/* AI / EXECUTIVE SUMMARY */}
            <div className="ai-summary-box">
              <h3>Executive Strategic Insights</h3>
              <p>{evaluation.ai_summary}</p>
            </div>

            {/* BOTTLENECKS IDENTIFIED */}
            <div className="mb-6">
              <h3 style={{ fontSize: "1.1rem", color: "#D4AF37", marginBottom: "0.75rem", fontWeight: 700 }}>
                Identified Bottlenecks & Friction Drivers ({evaluation.bottlenecks.length})
              </h3>
              {evaluation.bottlenecks.length === 0 ? (
                <p style={{ color: "rgba(255,255,255,0.8)", fontSize: "0.95rem" }}>
                  No operational bottlenecks were flagged for this project.
                </p>
              ) : (
                <div className="grid gap-3">
                  {evaluation.bottlenecks.map((b) => (
                    <div key={b.id} className="bottleneck-item">
                      <div>
                        <strong style={{ fontSize: "1rem", color: "#ffffff", display: "block" }}>
                          {b.question}
                        </strong>
                        <span style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.7)", marginTop: "0.2rem", display: "inline-block" }}>
                          Selected Status: <strong>{b.selected_option}</strong> &bull; Weight: {b.weight}
                        </span>
                      </div>
                      <div className="text-right whitespace-nowrap">
                        <span style={{ fontSize: "0.75rem", textTransform: "uppercase", padding: "0.25rem 0.6rem", borderRadius: "0.4rem", background: b.weighted_score >= 15 ? "rgba(239,68,68,0.3)" : "rgba(234,179,8,0.3)", color: "#ffffff", fontWeight: 700 }}>
                          {b.severity_status} (+{b.weighted_score} pts)
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* ACTIONABLE MITIGATION STRATEGIES */}
            <div>
              <h3 style={{ fontSize: "1.1rem", color: "#D4AF37", marginBottom: "0.75rem", fontWeight: 700 }}>
                Tailored Mitigation Action Plan ({evaluation.mitigation_strategies.length})
              </h3>
              {evaluation.mitigation_strategies.length === 0 ? (
                <p style={{ color: "rgba(255,255,255,0.8)", fontSize: "0.95rem" }}>
                  All operational parameters are currently within normal thresholds.
                </p>
              ) : (
                <div>
                  {evaluation.mitigation_strategies.map((m, idx) => (
                    <div key={idx} className="mitigation-item">
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.3rem" }}>
                        <strong style={{ fontSize: "0.95rem", color: "#D4AF37" }}>
                          Area: {m.category} ({m.selected_issue})
                        </strong>
                        <span style={{ fontSize: "0.75rem", fontWeight: 700, padding: "0.15rem 0.5rem", borderRadius: "999px", background: m.priority === "High" ? "rgba(239,68,68,0.2)" : "rgba(59,130,246,0.2)", color: "#ffffff" }}>
                          {m.priority} Priority
                        </span>
                      </div>
                      <p style={{ margin: 0, fontSize: "0.92rem", color: "rgba(255,255,255,0.9)", lineHeight: 1.5 }}>
                        {m.action}
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
