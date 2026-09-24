import { useEffect, useMemo, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import apiClient from "../api/client.js";
import StatCard from "../components/StatCard.jsx";
import RiskBadge from "../components/RiskBadge.jsx";

const TIER_COLORS = {
  High: "#B3441E",
  Medium: "#C08A2E",
  Low: "#3F6B4F",
  Unknown: "#5C728A",
};
const TIER_ORDER = ["High", "Medium", "Low", "Unknown"];

export default function DashboardPage() {
  const [riskSummary, setRiskSummary] = useState(null);
  const [sectorRisk, setSectorRisk] = useState([]);
  const [topRisky, setTopRisky] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const summaryPromise = apiClient.get("/api/dashboard/summary").catch(() => apiClient.get("/api/dashboard/risk-summary"));
        const sectorPromise = apiClient.get("/api/dashboard/sector-risk").catch(() => []);
        const topRiskyPromise = apiClient.get("/api/dashboard/top-risky").catch(() => []);

        const [riskRes, sectorRes, topRes] = await Promise.all([summaryPromise, sectorPromise, topRiskyPromise]);

        if (!active) return;

        const normalizedSummary = normalizeRiskSummary(riskRes.data || {});
        const normalizedSectorRisk = normalizeSectorRisk(sectorRes.data || []);
        const normalizedTopRisky = normalizeTopRisky(topRes.data || []);

        setRiskSummary(normalizedSummary);
        setSectorRisk(normalizedSectorRisk);
        setTopRisky(normalizedTopRisky);
      } catch (err) {
        if (!active) return;

        const requestUrl = `${err.config?.baseURL || ""}${err.config?.url || ""}`;
        console.error("Dashboard load failed:", {
          requestUrl,
          status: err.response?.status,
          data: err.response?.data,
          message: err.message,
          error: err,
        });

        setError(
          `Dashboard request failed for ${requestUrl}. ${
            err.response?.status ? `HTTP ${err.response.status}. ` : ""
          }${
            err.response?.data?.detail ||
            err.message ||
            "Couldn't load dashboard data. Is the chatbot API running?"
          }`
        );
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      active = false;
    };
  }, []);

  const pieData = useMemo(() => {
    const summary = riskSummary || {};
    return Object.entries(summary)
      .filter(([tier, count]) => tier && Number(count) >= 0)
      .map(([tier, count]) => ({
        name: tier,
        value: Number(count) || 0,
      }));
  }, [riskSummary]);

  const totalProjects = useMemo(
    () => Object.values(riskSummary || {}).reduce((sum, value) => sum + (Number(value) || 0), 0),
    [riskSummary]
  );

  const totalHigh = Number(riskSummary?.High || 0);
  const sectorsCovered = sectorRisk.length;

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <p className="text-sm text-steel">Loading dashboard…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <p className="text-sm text-brick">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="border-b border-slate-100 pb-3">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            Risk Dashboard
          </span>
        </div>

        <div className="mt-4">
          <h1 className="text-2xl font-bold text-[#002B49]">Project risk dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            Live view of predicted risk across every project in the dataset.
          </p>
        </div>
      </section>

      <div className="grid gap-5 md:grid-cols-3">
        <StatCard label="Total projects scored" value={totalProjects} />
        <StatCard
          label="High risk projects"
          value={totalHigh}
          sub="Auto-alerted on Telegram at submission time"
        />
        <StatCard label="Sectors covered" value={sectorsCovered} />
      </div>

      <div className="grid gap-10 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Overall risk distribution</h2>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={60}
                  outerRadius={95}
                  paddingAngle={2}
                >
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={TIER_COLORS[entry.name] || "#5C728A"} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-[260px] items-center justify-center text-sm text-slate-600">
              No risk summary data available.
            </div>
          )}
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Risk by sector</h2>
          {sectorRisk.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={sectorRisk} layout="vertical" margin={{ left: 24 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                <XAxis type="number" tick={{ fill: "#475569", fontSize: 11 }} />
                <YAxis type="category" dataKey="sector" width={110} tick={{ fill: "#475569", fontSize: 11 }} />
                <Tooltip />
                <Legend />
                {TIER_ORDER.map((tier) => (
                  <Bar
                    key={tier}
                    dataKey={tier}
                    stackId="risk"
                    fill={TIER_COLORS[tier] || "#5C728A"}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-[260px] items-center justify-center text-sm text-slate-600">
              No sector risk data available.
            </div>
          )}
        </div>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-bold text-[#002B49]">Top 10 highest-risk projects</h2>

        {topRisky.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-[#FFFDF8] text-left text-xs uppercase text-slate-500">
                  <th className="py-2.5 px-3">Project</th>
                  <th className="py-2.5 px-3">Sector</th>
                  <th className="py-2.5 px-3">State</th>
                  <th className="py-2.5 px-3">Risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {topRisky.map((row) => (
                  <tr key={`${row.project_code || row.project_name}-${row.sector || "sector"}`} className="hover:bg-slate-50">
                    <td className="py-3 px-3">
                      <p className="font-semibold text-[#002B49]">{row.project_name || "Unnamed project"}</p>
                      <p className="font-mono text-xs text-slate-500">{row.project_code || "N/A"}</p>
                    </td>
                    <td className="py-3 px-3 text-slate-600">{row.sector || "Not available"}</td>
                    <td className="py-3 px-3 text-slate-600">{row.state || "Not available"}</td>
                    <td className="py-3 px-3">
                      <RiskBadge tier={row._risk_tier || "Unknown"} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-sm text-slate-600">No top risky projects available at the moment.</div>
        )}
      </div>
    </div>
  );
}

function normalizeRiskSummary(input) {
  if (!input || typeof input !== "object") return {};

  return Object.entries(input).reduce((acc, [tier, count]) => {
    if (tier && count !== undefined && count !== null) {
      acc[tier] = Number(count) || 0;
    }
    return acc;
  }, {});
}

function normalizeSectorRisk(records) {
  const bySector = new Map();

  for (const record of records || []) {
    const sector = record?.sector || "Unspecified";
    if (!bySector.has(sector)) {
      bySector.set(sector, { sector, High: 0, Medium: 0, Low: 0, Unknown: 0 });
    }

    const bucket = bySector.get(sector);
    const tier = record?._risk_tier || "Unknown";
    bucket[tier] = Number(record?.count || 0);
  }

  return Array.from(bySector.values())
    .sort((a, b) => (b.High || 0) - (a.High || 0))
    .slice(0, 8);
}

function normalizeTopRisky(records) {
  return (records || []).map((row) => ({
    ...row,
    project_name: row.project_name || "Unnamed project",
    project_code: row.project_code || "N/A",
    sector: row.sector || "Not available",
    state: row.state || "Not available",
    _risk_tier: row._risk_tier || "Unknown",
  }));
}
