import { useEffect, useState } from "react";
import apiClient from "../api/client.js";

export default function SectorPage() {
  const [sectors, setSectors] = useState([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadSectors = async () => {
    try {
      const { data } = await apiClient.get("/api/sectors");
      setSectors(data || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load sectors");
    }
  };

  useEffect(() => {
    loadSectors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await apiClient.post("/api/sectors", { name });
      setName("");
      await loadSectors();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create sector");
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
        <h1 className="mt-3 text-3xl font-bold text-[#002B49]">Sectors</h1>
      </section>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <form onSubmit={handleSubmit} className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-[#002B49]">Add sector</h2>
          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-700">Name</span>
            <input className="field-input" value={name} onChange={(e) => setName(e.target.value)} required />
          </label>

          {error && <p className="text-sm text-[#B42318]">{error}</p>}

          <button type="submit" disabled={loading} className="rounded bg-[#002B49] px-4 py-2 text-sm font-bold text-white disabled:opacity-60">
            {loading ? "Saving..." : "Create sector"}
          </button>
        </form>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-bold text-[#002B49]">Sector list</h2>
          <div className="space-y-3">
            {sectors.length === 0 ? (
              <p className="text-sm text-slate-600">No sectors yet.</p>
            ) : (
              sectors.map((item) => (
                <div key={item.id || item.name} className="rounded border border-slate-200 bg-[#FFFDF8] p-3">
                  <p className="font-semibold text-[#002B49]">{item.name}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
