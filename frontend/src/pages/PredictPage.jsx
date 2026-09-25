import { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client.js";
import { sendHighRiskAlert, sendManualAlert } from "../api/telegramClient.js";
import { useProject } from "../context/ProjectContext.jsx";
import RiskBadge from "../components/RiskBadge.jsx";

const emptyForm = {
  project_name: "",
  agency: "",
  state: "",
  ministry: "",
  sector: "",
  original_cost_cr: "",
  cumulative_expenditure: "",
  physical_progress: "",
  date_of_approval: "",
  start_date: "",
  target_doc: "",
};

export default function PredictPage() {
  const [form, setForm] = useState(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [alertStatus, setAlertStatus] = useState(null);
  const [note, setNote] = useState("");
  const { project, predictions, setSubmittedProject } = useProject();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setAlertStatus(null);

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
        "cumulative expenditure in rs. crore": payload.cumulative_expenditure,
        "physical progress (in percentage)": payload.physical_progress,
      };

      setSubmittedProject(submittedProject, data.predictions, data.session_id);

      // Auto-alert trigger point: lives here in the frontend, right where
      // the risk tier first becomes known -- api.py itself is untouched.
      if (data.predictions.overall_risk_tier === "High") {
        try {
          await sendHighRiskAlert(submittedProject, data.predictions);
          setAlertStatus("High risk detected — the team was notified on Telegram automatically.");
        } catch (alertErr) {
          setAlertStatus(
            "High risk detected, but the Telegram alert couldn't be sent. Check the telegram-bot service is running."
          );
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed. Check that the chatbot API is running.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleManualAlert = async () => {
    setAlertStatus(null);
    try {
      await sendManualAlert(project, predictions, note);
      setAlertStatus("Alert sent to Telegram.");
      setNote("");
    } catch (err) {
      setAlertStatus("Couldn't send the alert. Check that the telegram-bot service is running.");
    }
  };

  return (
    <div className="relative grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
      <section className="panel rounded-3xl p-6 sm:p-8">
        <div className="page-header">
          <span className="soft-pill w-fit">SETU risk prediction</span>
          <h1>Submit a project for risk scoring</h1>
          <p>
            Enter what is known about a project. SETU predicts cost overrun and delay before either happens.
          </p>
        </div>

        <p className="mt-3 text-xs text-steel">
          Scoring assumes an ongoing project — the model is tuned for live projects rather than completed,
          frozen, or deleted records.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 grid gap-5">
          <Field label="Project name" name="project_name" value={form.project_name} onChange={handleChange} required />

          <div className="grid gap-5 md:grid-cols-2">
            <Field label="Agency" name="agency" value={form.agency} onChange={handleChange} required />
            <Field label="Ministry" name="ministry" value={form.ministry} onChange={handleChange} required />
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            <Field label="State" name="state" value={form.state} onChange={handleChange} required />
            <Field label="Sector" name="sector" value={form.sector} onChange={handleChange} required />
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            <Field
              label="Original cost (₹ Cr)"
              name="original_cost_cr"
              type="number"
              value={form.original_cost_cr}
              onChange={handleChange}
              required
            />
            <Field
              label="Expenditure so far (₹ Cr)"
              name="cumulative_expenditure"
              type="number"
              value={form.cumulative_expenditure}
              onChange={handleChange}
              required
            />
            <Field
              label="Physical progress (%)"
              name="physical_progress"
              type="number"
              value={form.physical_progress}
              onChange={handleChange}
              required
            />
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            <Field
              label="Date of approval"
              name="date_of_approval"
              placeholder="MM/YYYY"
              value={form.date_of_approval}
              onChange={handleChange}
              required
            />
            <Field
              label="Start date"
              name="start_date"
              placeholder="MM/YYYY"
              value={form.start_date}
              onChange={handleChange}
              required
            />
            <Field
              label="Target completion"
              name="target_doc"
              placeholder="MM/YYYY"
              value={form.target_doc}
              onChange={handleChange}
              required
            />
          </div>

          {error && <p className="text-sm text-brick">{error}</p>}

          <button
            type="submit"
            disabled={submitting}
            className="mt-2 w-fit rounded-full bg-ink px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-blueprint disabled:opacity-50"
          >
            {submitting ? "Scoring…" : "Predict risk"}
          </button>
        </form>
      </section>

      <aside className="lg:sticky lg:top-24 lg:self-start">
        {!predictions ? (
          <div className="panel rounded-3xl p-8 text-sm text-steel">
            Results will appear here once you submit a project.
          </div>
        ) : (
          <div className="panel rounded-3xl p-6">
            <p className="text-xs uppercase tracking-[0.2em] text-steel">Result for</p>
            <h2 className="mt-2 font-display text-2xl tracking-tight">{project.project_name}</h2>
            <p className="mt-1 font-mono text-xs text-steel">{project.project_code}</p>

            <div className="mt-5 flex flex-wrap gap-2">
              <RiskBadge tier={predictions.overall_risk_tier} label="Overall" />
              <RiskBadge tier={predictions.cost_risk_tier} label="Cost" />
              <RiskBadge tier={predictions.time_risk_tier} label="Time" />
            </div>

            <dl className="mt-6 grid grid-cols-2 gap-4 text-sm">
              <div className="rounded-2xl border border-ink/10 bg-white/50 p-4">
                <dt className="text-steel text-xs">Predicted overrun</dt>
                <dd className="mt-2 font-mono text-xl">{predictions.predicted_overrun_pct}%</dd>
              </div>
              <div className="rounded-2xl border border-ink/10 bg-white/50 p-4">
                <dt className="text-steel text-xs">Predicted delay</dt>
                <dd className="mt-2 font-mono text-xl">{predictions.predicted_delay_days} days</dd>
              </div>
            </dl>

            <div className="blueprint-rule mt-6 pt-6">
              <p className="text-xs text-steel mb-2">
                Send this result to the team on Telegram — regardless of risk level.
              </p>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Optional note to include"
                rows={2}
                className="field-input rounded-2xl"
              />
              <button
                onClick={handleManualAlert}
                className="mt-3 rounded-full border border-ink px-5 py-2.5 text-sm transition-colors hover:bg-ink hover:text-paper"
              >
                Send Telegram alert
              </button>
            </div>

            {alertStatus && <p className="mt-4 text-xs text-steel">{alertStatus}</p>}

            <button
              onClick={() => navigate("/chat")}
              className="mt-6 text-sm font-medium text-blueprint underline decoration-2 underline-offset-4"
            >
              Ask SETU about this project
            </button>
          </div>
        )}
      </aside>
    </div>
  );
}

function Field({ as = "input", label, name, type = "text", value, onChange, required, placeholder, children }) {
  const Tag = as;
  return (
    <label className="grid gap-1.5 text-sm">
      <span className="text-steel text-xs">{label}</span>
      <Tag
        name={name}
        type={as === "input" ? type : undefined}
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        className="field-input rounded-2xl"
      >
        {children}
      </Tag>
    </label>
  );
}