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

        const [riskRes, sectorRes, topRes] = await Promise.all([
          apiClient.get("/api/dashboard/risk-summary").catch((err) => {
            throw new Error(`Risk summary failed: ${err.message}`);
          }),
          apiClient.get("/api/dashboard/sector-risk").catch((err) => {
            throw new Error(`Sector risk failed: ${err.message}`);
          }),
          apiClient.get("/api/dashboard/top-risky").catch((err) => {
            throw new Error(`Top risky projects failed: ${err.message}`);
          }),
        ]);

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
    <div>
      <h1 className="font-display text-3xl">Risk dashboard</h1>
      <p className="mt-2 text-sm text-steel">
        Live view of predicted risk across every project in the dataset.
      </p>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        <StatCard label="Total projects scored" value={totalProjects} />
        <StatCard
          label="High risk projects"
          value={totalHigh}
          sub="Auto-alerted on Telegram at submission time"
        />
        <StatCard label="Sectors covered" value={sectorsCovered} />
      </div>

      <div className="mt-10 grid gap-10 lg:grid-cols-2">
        <div className="border border-ink/15 bg-white/40 p-6">
          <h2 className="mb-4 font-display text-lg">Overall risk distribution</h2>
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
            <div className="flex h-[260px] items-center justify-center text-sm text-steel">
              No risk summary data available.
            </div>
          )}
        </div>

        <div className="border border-ink/15 bg-white/40 p-6">
          <h2 className="mb-4 font-display text-lg">Risk by sector</h2>
          {sectorRisk.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={sectorRisk} layout="vertical" margin={{ left: 24 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" />
                <YAxis type="category" dataKey="sector" width={110} tick={{ fontSize: 11 }} />
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
            <div className="flex h-[260px] items-center justify-center text-sm text-steel">
              No sector risk data available.
            </div>
          )}
        </div>
      </div>

      <div className="mt-10 border border-ink/15 bg-white/40 p-6">
        <h2 className="mb-4 font-display text-lg">Top 10 highest-risk projects</h2>

        {topRisky.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-ink/15 text-left text-xs text-steel">
                  <th className="py-2 pr-4">Project</th>
                  <th className="py-2 pr-4">Sector</th>
                  <th className="py-2 pr-4">State</th>
                  <th className="py-2 pr-4">Risk</th>
                </tr>
              </thead>
              <tbody>
                {topRisky.map((row) => (
                  <tr key={`${row.project_code || row.project_name}-${row.sector || "sector"}`} className="border-b border-ink/10">
                    <td className="py-2.5 pr-4">
                      <p>{row.project_name || "Unnamed project"}</p>
                      <p className="font-mono text-xs text-steel">{row.project_code || "N/A"}</p>
                    </td>
                    <td className="py-2.5 pr-4">{row.sector || "Not available"}</td>
                    <td className="py-2.5 pr-4">{row.state || "Not available"}</td>
                    <td className="py-2.5 pr-4">
                      <RiskBadge tier={row._risk_tier || "Unknown"} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-sm text-steel">No top risky projects available at the moment.</div>
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
