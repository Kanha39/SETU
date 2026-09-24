import { useNavigate } from "react-router-dom";
import { useState } from "react";
import apiClient from "../api/client.js";
import { sendHighRiskAlert } from "../api/telegramClient.js";
import { useProject } from "../context/ProjectContext.jsx";

export const MOSPI_SECTORS = [
  "Railways",
  "Urban Public Transport",
  "Telecommunication",
  "Oil & Gas",
  "Electricity Generation",
  "Real Estate & Construction",
  "Coal & Mining",
  "Transmission & Distribution",
  "Water Resources & Sewerage",
  "Logistics & Multi Modal Hubs",
  "Road Transport & Highways",
  "Civil Aviation"
];

export const MOSPI_MINISTRIES = [
  "Ministry of Railways (MoR)",
  "Ministry of Housing & Urban Affairs (MoHUA)",
  "Department of Telecommunications (DoT)",
  "Ministry of Petroleum & Natural Gas (MoPNG)",
  "Ministry of Power (MoP)",
  "Ministry of Road Transport & Highways (MoRTH)",
  "Ministry of Health & Family Welfare (MoHFW)",
  "Department of Water Resources (DWR, RD & GR)"
];

const emptyForm = {
  project_name: "",
  agency: "",
  ministry: "",
  state: "",
  sector: "",
  status: "Ongoing",
  original_cost_cr: "",
  cumulative_expenditure: "",
  physical_progress: "",
  date_of_approval: "",
  start_date: "",
  target_doc: "",
};

export default function ProjectFormPage() {
  const [form, setForm] = useState(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const { setSubmittedProject } = useProject();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setMessage("");

    try {
      const payload = {
        ...form,
        status: "Ongoing",
        original_cost_cr: Number(form.original_cost_cr),
        cumulative_expenditure: Number(form.cumulative_expenditure),
        physical_progress: Number(form.physical_progress),
      };

      const { data } = await apiClient.post("/api/predict", payload);

      const submittedProject = data.project_data || {
        ...payload,
        project_code: "NEW-USER-PROJECT",
      };

      setSubmittedProject(submittedProject, data.predictions, data.session_id);
      setMessage("Project submitted successfully.");

      if (data.predictions.overall_risk_tier === "High") {
        try {
          await sendHighRiskAlert(submittedProject, data.predictions);
        } catch (alertErr) {
          console.error("Telegram alert failed", alertErr);
        }
      }

      navigate("/projects/analysis");
    } catch (err) {
      setError(err.response?.data?.detail || "Project could not be submitted.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="panel form-panel">
      <div className="page-header">
        <span className="soft-pill">New project intake</span>
        <h1>Register project for analysis</h1>
        <p>Capture the current delivery status and generate a digital risk assessment.</p>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 grid gap-5">
        <div className="form-grid form-grid--two">
          <label>
            <span>Project name</span>
            <input name="project_name" value={form.project_name} onChange={handleChange} className="field-input" required />
          </label>
          <label>
            <span>Agency</span>
            <input name="agency" value={form.agency} onChange={handleChange} className="field-input" required />
          </label>
        </div>

        <div className="form-grid form-grid--two">
          <label>
            <span>Ministry</span>
            <input name="ministry" value={form.ministry} onChange={handleChange} className="field-input" required />
          </label>
          <label>
            <span>State</span>
            <input name="state" value={form.state} onChange={handleChange} className="field-input" required />
          </label>
        </div>

        <div className="form-grid form-grid--three">
          <label>
            <span>Sector</span>
            <input name="sector" value={form.sector} onChange={handleChange} className="field-input" required />
          </label>
          <label>
            <span>Original cost (₹ Cr)</span>
            <input name="original_cost_cr" type="number" value={form.original_cost_cr} onChange={handleChange} className="field-input" required />
          </label>
          <label>
            <span>Expenditure so far (₹ Cr)</span>
            <input name="cumulative_expenditure" type="number" value={form.cumulative_expenditure} onChange={handleChange} className="field-input" required />
          </label>
        </div>

        <div className="form-grid form-grid--three">
          <label>
            <span>Physical progress (%)</span>
            <input name="physical_progress" type="number" value={form.physical_progress} onChange={handleChange} className="field-input" required />
          </label>
          <label>
            <span>Date of approval</span>
            <input name="date_of_approval" value={form.date_of_approval} onChange={handleChange} className="field-input" placeholder="MM/YYYY" required />
          </label>
          <label>
            <span>Target completion</span>
            <input name="target_doc" value={form.target_doc} onChange={handleChange} className="field-input" placeholder="MM/YYYY" required />
          </label>
        </div>

        <div className="form-grid form-grid--one">
          <label>
            <span>Start date</span>
            <input name="start_date" value={form.start_date} onChange={handleChange} className="field-input" placeholder="MM/YYYY" required />
          </label>
        </div>

        {error && <p className="form-message form-message--error">{error}</p>}
        {message && <p className="form-message form-message--success">{message}</p>}

        <button type="submit" className="primary-btn w-fit" disabled={submitting}>
          {submitting ? "Submitting..." : "Generate analysis"}
        </button>
      </form>
    </div>
  );
}
