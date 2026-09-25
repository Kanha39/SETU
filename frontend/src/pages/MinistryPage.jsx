import { useEffect, useState } from "react";
import apiClient from "../api/client.js";

export default function MinistryPage() {
  const [ministries, setMinistries] = useState([]);
  const [form, setForm] = useState({ name: "", department: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadMinistries = async () => {
    try {
      const { data } = await apiClient.get("/api/ministries");
      setMinistries(data || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load ministries");
    }
  };

  useEffect(() => {
    loadMinistries();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await apiClient.post("/api/ministries", form);
      setForm({ name: "", department: "" });
      await loadMinistries();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create ministry");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
          Ministry & Sector
        </span>
        <h1 className="mt-3 text-3xl font-bold text-[#002B49]">Ministries</h1>
      </section>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <form onSubmit={handleSubmit} className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-[#002B49]">Add ministry</h2>

          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-700">Name</span>
            <input className="field-input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-700">Department</span>
            <input className="field-input" value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} required />
          </label>

          {error && <p className="text-sm text-[#B42318]">{error}</p>}

          <button type="submit" disabled={loading} className="rounded bg-[#002B49] px-4 py-2 text-sm font-bold text-white disabled:opacity-60">
            {loading ? "Saving..." : "Create ministry"}
          </button>
        </form>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Ministry list</h2>
          <div className="space-y-3">
            {ministries.length === 0 ? (
              <p className="text-sm text-slate-600">No ministries yet.</p>
            ) : (
              ministries.map((item) => (
                <div key={item.id || item.name} className="rounded border border-slate-200 bg-[#FFFDF8] p-3">
                  <p className="font-semibold text-[#002B49]">{item.name}</p>
                  <p className="text-sm text-slate-600">{item.department || "Department not specified"}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
