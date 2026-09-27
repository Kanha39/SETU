import apiClient from "./client.js";

function toIsoDate(value) {
  if (!value) return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;

  const match = value.match(/^(\d{1,2})[/-](\d{4})$/);
  if (!match) return null;

  return `${match[2]}-${match[1].padStart(2, "0")}-01`;
}

function findId(items, value) {
  if (!value || !Array.isArray(items)) return null;
  const wanted = value.toLowerCase().replace(/\s+/g, " ").trim();
  const match = items.find((item) => {
    const name = String(item.name || "").toLowerCase().replace(/\s+/g, " ").trim();
    return name === wanted || name.includes(wanted) || wanted.includes(name);
  });
  return match?.id ?? match?.ministryId ?? match?.sectorId ?? null;
}

export async function createProjectAndGenerateRisk(form) {
  const [ministriesResult, sectorsResult] = await Promise.allSettled([
    apiClient.get("/api/ministries"),
    apiClient.get("/api/sectors"),
  ]);

  const ministries = ministriesResult.status === "fulfilled" ? ministriesResult.value.data : [];
  const sectors = sectorsResult.status === "fulfilled" ? sectorsResult.value.data : [];

  const projectRequest = {
    name: form.project_name,
    ministryId: findId(ministries, form.ministry),
    sectorId: findId(sectors, form.sector),
    implementingAgency: form.agency,
    approvedCost: Number(form.original_cost_cr),
    revisedCost: Number(form.original_cost_cr),
    cumulativeExpenditure: Number(form.cumulative_expenditure),
    startDate: toIsoDate(form.start_date),
    scheduledEndDate: toIsoDate(form.target_doc),
    revisedEndDate: toIsoDate(form.target_doc),
    physicalProgressPercent: Number(form.physical_progress),
  };

  const { data: project } = await apiClient.post("/api/projects", projectRequest);
  const { data: risk } = await apiClient.post(
    `/api/projects/${project.projectId}/risk/generate`,
  );

  const predictions = {
    predicted_overrun_pct: risk.predictedOverrunPct ?? null,
    predicted_delay_days: risk.predictedDelayDays ?? null,
    cost_risk_tier: risk.costRiskLevel ?? "Unknown",
    time_risk_tier: risk.timeRiskLevel ?? "Unknown",
    overall_risk_tier: risk.riskLevel ?? "Unknown",
  };

  return {
    project: {
      projectId: project.projectId,
      project_name: project.name,
      agency: project.implementingAgency,
      ministry: project.ministryName || form.ministry,
      sector: project.sectorName || form.sector,
      state: form.state,
      original_cost_cr: project.approvedCost ?? form.original_cost_cr,
      cumulative_expenditure: project.cumulativeExpenditure ?? form.cumulative_expenditure,
      physical_progress: project.physicalProgressPercent ?? form.physical_progress,
      date_of_approval: form.date_of_approval,
      start_date: project.startDate || form.start_date,
      target_doc: project.scheduledEndDate || form.target_doc,
    },
    predictions,
    projectId: project.projectId,
  };
}
