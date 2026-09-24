import { Link } from "react-router-dom";
import ActionCard from "../components/cards/ActionCard.jsx";
import { useProject } from "../context/ProjectContext.jsx";

// MoSPI SETU Real Data Summary
const mospiStats = [
  { label: "Total Central Infrastructure Projects", value: "1,775" },
  { label: "Total Original Cost", value: "₹ 33.70 Lakh Cr" },
  { label: "Total Cumulative Expenditure", value: "₹ 19.26 Lakh Cr" },
];

const highValueProjects = [
  {
    name: "Mumbai-Ahmedabad High Speed Rail Project (508 km)",
    ministry: "Railways (NHSRCL)",
    cost: "₹ 1,08,000 Cr",
    progress: "62%",
    completion: "31/12/2029",
  },
  {
    name: "Chennai Metro Rail Phase-II Development",
    ministry: "Urban Public Transport (CMRL)",
    cost: "₹ 63,246 Cr",
    progress: "56%",
    completion: "31/08/2029",
  },
  {
    name: "BharatNet Digital Connectivity Project",
    ministry: "Telecommunication (DoT)",
    cost: "₹ 61,109 Cr",
    progress: "100%",
    completion: "31/12/2025",
  },
  {
    name: "Ethylene Cracker Project at Bina Refinery",
    ministry: "Oil & Gas (BPCL)",
    cost: "₹ 43,367 Cr",
    progress: "34%",
    completion: "31/05/2028",
  },
];

export default function HomePage() {
  const { project } = useProject();

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
              Central Sector Infrastructure Projects Monitoring
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Monitoring and risk analysis for infrastructure projects costing ₹150 Crore and above across key Union Ministries.
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
            <p className="text-2xl font-bold text-[#002B49]">₹ 37.10L Cr</p>
            <p className="text-xs font-semibold text-slate-500">Latest Revised Total Cost</p>
            <ul className="mt-3 space-y-1 text-xs text-slate-600">
              <li>• Ministry of Health & Family Welfare: <strong>35 Projects</strong></li>
              <li>• Expenditure (MoHFW): <strong>₹ 10,844 Cr</strong></li>
              <li>• Tracked Ministries: <strong>15+ Departments</strong></li>
            </ul>
          </div>
        </div>
      </section>

      {/* Key Stats Cards */}
      <section className="grid gap-5 md:grid-cols-3">
        {mospiStats.map((stat) => (
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
          <span className="text-xs text-slate-500">MoSPI Live Tracker</span>
        </div>

        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 bg-[#FFFDF8] text-xs uppercase text-slate-500">
                <th className="py-2.5 px-3">Project Name</th>
                <th className="py-2.5 px-3">Sector / Ministry</th>
                <th className="py-2.5 px-3">Original Cost</th>
                <th className="py-2.5 px-3">Physical Progress</th>
                <th className="py-2.5 px-3">Target Completion</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {highValueProjects.map((proj, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-3 px-3 font-semibold text-[#002B49]">{proj.name}</td>
                  <td className="py-3 px-3 text-slate-600">{proj.ministry}</td>
                  <td className="py-3 px-3 font-mono text-slate-700">{proj.cost}</td>
                  <td className="py-3 px-3">
                    <span className="inline-block rounded bg-slate-100 px-2 py-0.5 text-xs font-bold text-[#002B49]">
                      {proj.progress}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-600">{proj.completion}</td>
                </tr>
              ))}
            </tbody>
          </table>
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