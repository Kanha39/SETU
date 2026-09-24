import { Link } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";

export default function ProjectAnalysisPage() {
  const { project, predictions } = useProject();

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
    </div>
  );
}
