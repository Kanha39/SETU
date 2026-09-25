import { useParams, Link } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";

export default function ProjectOverviewPage() {
  const { projectId } = useParams();
  const { project, predictions } = useProject();

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
              Project Overview
            </span>
            <h1 className="mt-3 text-3xl font-bold text-[#002B49]">
              {project?.project_name || `Project ${projectId || "-"}`}
            </h1>
          </div>

          {predictions && (
            <div className="flex flex-wrap gap-2">
              <RiskBadge tier={predictions.overall_risk_tier} label="Overall" />
              <RiskBadge tier={predictions.cost_risk_tier} label="Cost" />
              <RiskBadge tier={predictions.time_risk_tier} label="Time" />
            </div>
          )}
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Project Details</h2>
          <dl className="space-y-3 text-sm text-slate-700">
            <div className="flex justify-between gap-4"><dt>Project ID</dt><dd className="font-semibold">{projectId || "N/A"}</dd></div>
            <div className="flex justify-between gap-4"><dt>Agency</dt><dd>{project?.agency || "—"}</dd></div>
            <div className="flex justify-between gap-4"><dt>Ministry</dt><dd>{project?.ministry || "—"}</dd></div>
            <div className="flex justify-between gap-4"><dt>Sector</dt><dd>{project?.sector || "—"}</dd></div>
            <div className="flex justify-between gap-4"><dt>State</dt><dd>{project?.state || "—"}</dd></div>
          </dl>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Risk Snapshot</h2>
          {predictions ? (
            <dl className="space-y-3 text-sm text-slate-700">
              <div className="flex justify-between gap-4"><dt>Predicted cost overrun</dt><dd>{predictions.predicted_overrun_pct}%</dd></div>
              <div className="flex justify-between gap-4"><dt>Predicted delay</dt><dd>{predictions.predicted_delay_days} days</dd></div>
              <div className="flex justify-between gap-4"><dt>Overall tier</dt><dd>{predictions.overall_risk_tier}</dd></div>
            </dl>
          ) : (
            <p className="text-sm text-slate-600">No risk analysis available yet. Submit a project for evaluation.</p>
          )}
        </div>
      </section>

      <div className="flex flex-wrap gap-3">
        <Link to="/projects/new" className="rounded bg-[#002B49] px-4 py-2 text-sm font-bold text-white">New Project</Link>
        <Link to={`/projects/${projectId || "demo"}/risk`} className="rounded border border-[#002B49] px-4 py-2 text-sm font-bold text-[#002B49]">Risk Details</Link>
        <Link to="/chatbot" className="rounded border border-[#D4AF37] bg-[#FFF7D6] px-4 py-2 text-sm font-bold text-[#7A5A00]">Ask Chatbot</Link>
      </div>
    </div>
  );
}
