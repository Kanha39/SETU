import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ActionCard from "../components/cards/ActionCard.jsx";
import { useProject } from "../context/ProjectContext.jsx";
import mlClient from "../api/mlClient.js";
import { formatCrore, formatPercent } from "../utils/formatters.js";

export default function HomePage() {
  const { project } = useProject();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHomeData() {
      try {
        setLoading(true);
        const { data } = await mlClient.get("/api/dashboard/mega-projects");
        setSummary(data);
      } catch (err) {
        console.error("Failed to load home summary data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchHomeData();
  }, []);

  const statsList = summary ? [
    { label: "Total Mega Infrastructure Projects", value: summary.total_mega_projects },
    { label: "Total Original Cost (₹ Cr)", value: formatCrore(summary.totals.original_cost_cr) },
    { label: "Total Cumulative Expenditure (₹ Cr)", value: formatCrore(summary.totals["cumulative expenditure in rs. crore"]) },
  ] : [
    { label: "Total Mega Infrastructure Projects", value: "Loading..." },
    { label: "Total Original Cost", value: "Loading..." },
    { label: "Total Cumulative Expenditure", value: "Loading..." },
  ];

  const highValueProjects = summary?.top_10_mega_projects || [];

  return (
    <div className="space-y-8">
      {/* Current Monitor Header Banner */}
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="border-b border-slate-100 pb-3">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            GOVERNMENT OF INDIA • MoSPI PORTAL
          </span>
        </div>

        <div className="mt-4 grid gap-6 md:grid-cols-3 md:items-center">
          <div className="md:col-span-2">
            <h1 className="text-2xl font-bold text-[#002B49]">
              Central Sector Mega Infrastructure Projects Monitoring
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Monitoring and risk analysis for mega infrastructure projects costing ₹10,000 Crore and above across key Union Ministries.
            </p>
            <div className="mt-5 flex gap-3">
              <Link
                to="/projects/new"
                className="rounded bg-[#FFA500] px-4 py-2 text-sm font-bold text-white transition-colors hover:bg-[#e09200]"
              >
                + Add Project / Update
              </Link>
              <Link
                to="/dashboard"
                className="rounded border border-[#002B49] px-4 py-2 text-sm font-bold text-[#002B49] transition-colors hover:bg-[#002B49] hover:text-white"
              >
                View Dashboard
              </Link>
            </div>
          </div>

          <div className="rounded-md border border-slate-100 bg-[#FFFDF8] p-4">
            <p className="text-2xl font-bold text-[#002B49]">
              {loading ? "..." : formatCrore(summary?.totals.revised_cost_cr)}
            </p>
            <p className="text-xs font-semibold text-slate-500">Latest Revised Total Cost</p>
            <ul className="mt-3 space-y-1 text-xs text-slate-600">
              <li>• Total Progress: <strong>{formatPercent(summary?.totals["physical progress (in percentage)"])}</strong></li>
              <li>• Tracked Ministries: <strong>{summary?.tracked_ministries || 17} Union Departments</strong></li>
              <li>• Live Dataset: <strong>MoSPI Processed Pipeline</strong></li>
            </ul>
          </div>
        </div>
      </section>

      {/* Key Stats Cards */}
      <section className="grid gap-5 md:grid-cols-3">
        {statsList.map((stat) => (
          <div key={stat.label} className="rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm">
            <p className="text-2xl font-bold text-[#002B49]">{stat.value}</p>
            <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">{stat.label}</p>
          </div>
        ))}
      </section>

      {/* High-Value Government Projects List */}
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h2 className="text-lg font-bold text-[#002B49]">High Value Infrastructure Projects</h2>
          <span className="text-xs text-slate-500">MoSPI Live Endpoint Data</span>
        </div>

        <div className="mt-4 overflow-x-auto">
          {loading ? (
            <div className="py-8 text-center text-sm text-slate-500">Loading live endpoint data...</div>
          ) : (
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-[#FFFDF8] text-xs uppercase text-slate-500">
                  <th className="py-2.5 px-3">Project Name</th>
                  <th className="py-2.5 px-3">Sector / Ministry</th>
                  <th className="py-2.5 px-3">Original Cost</th>
                  <th className="py-2.5 px-3">Physical Progress</th>
                  <th className="py-2.5 px-3">Cumulative Expenditure</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {highValueProjects.map((proj, i) => (
                  <tr key={i} className="hover:bg-slate-50">
                    <td className="py-3 px-3 font-semibold text-[#002B49]">{proj.project_name}</td>
                    <td className="py-3 px-3 text-slate-600">{proj.agency}</td>
                    <td className="py-3 px-3 font-mono text-slate-700">{formatCrore(proj.original_cost_cr)}</td>
                    <td className="py-3 px-3">
                      <span className="inline-block rounded bg-slate-100 px-2 py-0.5 text-xs font-bold text-[#002B49]">
                        {formatPercent(proj["physical progress (in percentage)"])}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-600">{formatCrore(proj["cumulative expenditure in rs. crore"])} </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>

      {/* Action Cards */}
      <section className="grid gap-6 md:grid-cols-3">
        <ActionCard
          title="New Project Registration"
          description="Register central sector infrastructure projects (₹150 Cr+) and calculate cost/time overruns."
          to="/projects/new"
          badge="Registration"
          highlight
        />
        <ActionCard
          title="Project Intelligence"
          description="Analyze risk levels, predicted delays, and physical progress reports across sectors."
          to={project ? "/projects/analysis" : "/projects/new"}
          badge="Analytics"
        />
        <ActionCard
          title="SETU AI Assistant"
          description="Query specific ministry metrics, project statuses, and State-wise breakdowns."
          to="/chatbot"
          badge="AI Query"
        />
      </section>
    </div>
  );
}