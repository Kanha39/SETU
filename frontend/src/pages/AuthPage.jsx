import { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client.js";
import { useProject } from "../context/ProjectContext.jsx";

export default function AuthPage() {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { loginUser } = useProject();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const endpoint = mode === "login" ? "/api/auth/login" : "/api/auth/register";
      const payload = mode === "login"
        ? { email: form.email, password: form.password }
        : { name: form.name, email: form.email, password: form.password };

      const { data } = await apiClient.post(endpoint, payload);
      const user = {
        token: data.token,
        name: data.name,
        email: data.email,
        role: data.role || "user",
      };

      loginUser(user);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg">
      <div className="rounded-lg border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-6 text-center">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            SETU ACCESS
          </span>
          <h1 className="mt-4 text-3xl font-bold text-[#002B49]">
            {mode === "login" ? "Login" : "Create account"}
          </h1>
        </div>

        <div className="mb-6 flex rounded bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => setMode("login")}
            className={`flex-1 rounded px-3 py-2 text-sm font-semibold ${mode === "login" ? "bg-[#002B49] text-white" : "text-slate-600"}`}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setMode("register")}
            className={`flex-1 rounded px-3 py-2 text-sm font-semibold ${mode === "register" ? "bg-[#002B49] text-white" : "text-slate-600"}`}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === "register" && (
            <label className="block">
              <span className="mb-1 block text-sm font-semibold text-slate-700">Full name</span>
              <input
                type="text"
                name="name"
                value={form.name}
                onChange={handleChange}
                className="field-input"
                required
              />
            </label>
          )}

          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-700">Email</span>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="field-input"
              required
            />
          </label>

          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-700">Password</span>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="field-input"
              required
            />
          </label>

          {error && <p className="text-sm font-medium text-[#B42318]">{error}</p>}

          <button type="submit" disabled={loading} className="w-full rounded bg-[#002B49] px-4 py-3 text-sm font-bold text-white disabled:opacity-60">
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </form>
      </div>
    </div>
  );
}
