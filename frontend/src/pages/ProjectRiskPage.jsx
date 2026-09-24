import { useParams } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";

export default function ProjectRiskPage() {
  const { projectId } = useParams();
  const { project, predictions } = useProject();

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
          Risk Intelligence
        </span>
        <h1 className="mt-3 text-3xl font-bold text-[#002B49]">
          {project?.project_name || `Project ${projectId || "-"}`} Risk Profile
        </h1>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-wider text-slate-500">Cost Risk</p>
          <div className="mt-3"><RiskBadge tier={predictions?.cost_risk_tier || "Unknown"} /></div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-wider text-slate-500">Time Risk</p>
          <div className="mt-3"><RiskBadge tier={predictions?.time_risk_tier || "Unknown"} /></div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-wider text-slate-500">Overall Risk</p>
          <div className="mt-3"><RiskBadge tier={predictions?.overall_risk_tier || "Unknown"} /></div>
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-bold text-[#002B49]">Latest Risk Details</h2>
        {predictions ? (
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded border border-slate-200 bg-[#FFFDF8] p-4">
              <p className="text-xs uppercase tracking-wider text-slate-500">Predicted cost overrun</p>
              <p className="mt-2 text-2xl font-bold text-[#002B49]">{predictions.predicted_overrun_pct}%</p>
            </div>
            <div className="rounded border border-slate-200 bg-[#FFFDF8] p-4">
              <p className="text-xs uppercase tracking-wider text-slate-500">Predicted delay</p>
              <p className="mt-2 text-2xl font-bold text-[#002B49]">{predictions.predicted_delay_days} days</p>
            </div>
          </div>
        ) : (
          <p className="text-sm text-slate-600">No latest risk record found. Submit or load a project to generate the risk analysis.</p>
        )}
      </section>
    </div>
  );
}
