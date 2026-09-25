export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
          Alert Center
        </span>
        <h1 className="mt-3 text-3xl font-bold text-[#002B49]">Operational alerts</h1>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="space-y-4">
          <div className="flex items-center justify-between rounded border border-slate-200 bg-[#FFFDF8] p-4">
            <div>
              <p className="font-semibold text-[#002B49]">High risk project: NH-48 Corridor</p>
              <p className="text-sm text-slate-600">Notification sent to project oversight team</p>
            </div>
            <span className="rounded bg-[#FDE7E7] px-2 py-1 text-xs font-bold text-[#B42318]">High</span>
          </div>

          <div className="flex items-center justify-between rounded border border-slate-200 bg-[#FFFDF8] p-4">
            <div>
              <p className="font-semibold text-[#002B49]">Delay warning: Metro Line 5</p>
              <p className="text-sm text-slate-600">Schedule deviation above tolerance threshold</p>
            </div>
            <span className="rounded bg-[#FFF3D6] px-2 py-1 text-xs font-bold text-[#9A5A00]">Medium</span>
          </div>

          <div className="flex items-center justify-between rounded border border-slate-200 bg-[#FFFDF8] p-4">
            <div>
              <p className="font-semibold text-[#002B49]">Cost escalation check</p>
              <p className="text-sm text-slate-600">Review revision cycle for road portfolio projects</p>
            </div>
            <span className="rounded bg-[#E8F8EE] px-2 py-1 text-xs font-bold text-[#1F6F3E]">Low</span>
          </div>
        </div>
      </section>
    </div>
  );
}
