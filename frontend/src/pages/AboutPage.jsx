import { Link } from "react-router-dom";

export default function AboutPage() {
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="border-b border-slate-100 pb-3">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            ABOUT SETU • MoSPI PORTAL
          </span>
        </div>

        <div className="mt-4">
          <h1 className="text-3xl font-extrabold text-[#002B49]">
            About SETU System
          </h1>
          <p className="mt-2 text-base text-slate-600">
            System for Evaluation, Tracking & Risk Assessment of Infrastructure Projects.
          </p>
        </div>
      </section>

      {/* Main Overview Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold text-[#002B49] mb-3">Institutional Overview</h2>
          <p className="text-sm text-slate-600 leading-relaxed">
            The <strong>Infrastructure and Project Monitoring Division (IPMD)</strong> under the Ministry of Statistics and Programme Implementation (MoSPI) is mandated to monitor central sector infrastructure projects costing ₹ 150 Crore and above.
          </p>
          <p className="mt-3 text-sm text-slate-600 leading-relaxed">
            <strong>SETU</strong> enhances traditional progress reporting with advanced AI & Machine Learning analytics to predict cost overrun percentages, estimate completion delay in days, and flag high-risk projects for proactive intervention.
          </p>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold text-[#002B49] mb-3">Core Pillars & Objectives</h2>
          <ul className="space-y-2.5 text-sm text-slate-700">
            <li className="flex items-start gap-2">
              <span className="text-[#D4AF37] font-bold">✔</span>
              <span><strong>ML Overrun Scoring:</strong> Gradient boosting models (XGBoost & LightGBM) trained on historical MoSPI project data.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#D4AF37] font-bold">✔</span>
              <span><strong>Operational Questionnaire:</strong> 7-factor weighted bottleneck diagnosis for root cause analysis.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#D4AF37] font-bold">✔</span>
              <span><strong>Real-time Alerting:</strong> Automated Telegram alerts dispatched instantly when high-risk tiers are triggered.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#D4AF37] font-bold">✔</span>
              <span><strong>Conversational Intelligence:</strong> Natural language assistant for querying ministry and sector data.</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Statistics Highlights */}
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-bold text-[#002B49] mb-4">MoSPI Monitoring Metrics</h2>
        <div className="grid gap-4 md:grid-cols-4 text-center">
          <div className="rounded-md bg-[#FFFDF8] p-4 border border-slate-100">
            <p className="text-2xl font-black text-[#002B49]">18,601</p>
            <p className="text-xs font-semibold text-slate-500 uppercase mt-1">Tracked Projects</p>
          </div>
          <div className="rounded-md bg-[#FFFDF8] p-4 border border-slate-100">
            <p className="text-2xl font-black text-[#002B49]">Rs. 39.60L Cr</p>
            <p className="text-xs font-semibold text-slate-500 uppercase mt-1">Total Original Cost</p>
          </div>
          <div className="rounded-md bg-[#FFFDF8] p-4 border border-slate-100">
            <p className="text-2xl font-black text-[#002B49]">Rs. 23.98L Cr</p>
            <p className="text-xs font-semibold text-slate-500 uppercase mt-1">Cumulative Spend</p>
          </div>
          <div className="rounded-md bg-[#FFFDF8] p-4 border border-slate-100">
            <p className="text-2xl font-black text-[#002B49]">17+</p>
            <p className="text-xs font-semibold text-slate-500 uppercase mt-1">Union Ministries</p>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex gap-4">
        <Link to="/dashboard" className="rounded-md bg-[#002B49] px-5 py-2.5 text-sm font-bold text-white shadow hover:bg-slate-800 transition-colors">
          Explore Dashboard
        </Link>
        <Link to="/chatbot" className="rounded-md bg-[#f59e0b] px-5 py-2.5 text-sm font-bold text-white shadow hover:bg-amber-600 transition-colors">
          Ask SETU Assistant
        </Link>
      </div>
    </div>
  );
}
