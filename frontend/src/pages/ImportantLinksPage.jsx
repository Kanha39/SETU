export default function ImportantLinksPage() {
  const governmentLinks = [
    {
      title: "Ministry of Statistics & Programme Implementation (MoSPI)",
      desc: "Official portal of the Ministry of Statistics and Programme Implementation.",
      url: "https://mospi.gov.in",
      category: "Government Portal"
    },
    {
      title: "Infrastructure and Project Monitoring Division (IPMD)",
      desc: "Central sector project monitoring division for projects costing ₹150 Cr and above.",
      url: "https://www.cspm.gov.in",
      category: "Project Division"
    },
    {
      title: "PM Gati Shakti National Master Plan",
      desc: "Integrated portal for multimodal connectivity and infrastructure planning.",
      url: "https://gatishakti.mofpi.gov.in",
      category: "National Master Plan"
    },
    {
      title: "NITI Aayog - Infrastructure Division",
      desc: "National Institution for Transforming India - Infrastructure policy & oversight.",
      url: "https://niti.gov.in",
      category: "Policy Body"
    },
    {
      title: "Press Information Bureau - MoSPI Releases",
      desc: "Official press announcements and monthly flash reports on infrastructure projects.",
      url: "https://pib.gov.in",
      category: "Official Press"
    }
  ];

  const sectoralLinks = [
    { title: "Ministry of Railways (MoR)", desc: "Railway line construction, chord lines, and high-speed rail corridor tracking.", url: "https://indianrailways.gov.in" },
    { title: "Ministry of Road Transport & Highways (MoRTH)", desc: "National highways, expressways, and economic corridor infrastructure.", url: "https://morth.nic.in" },
    { title: "Ministry of Petroleum & Natural Gas (MoPNG)", desc: "Refinery expansions, ethylene crackers, and pipeline infrastructure.", url: "https://mopng.gov.in" },
    { title: "Ministry of Power (MoP)", desc: "Thermal, hydro, solar generation and inter-state transmission lines.", url: "https://powermin.gov.in" }
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="border-b border-slate-100 pb-3">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            RESOURCES & PORTALS • MoSPI
          </span>
        </div>

        <div className="mt-4">
          <h1 className="text-3xl font-extrabold text-[#002B49]">
            Important Links & Portals
          </h1>
          <p className="mt-2 text-base text-slate-600">
            Access official Union Ministries, infrastructure divisions, and project governance resources.
          </p>
        </div>
      </section>

      {/* Official Government Portals */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-[#002B49]">Official Government Portals</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {governmentLinks.map((item, idx) => (
            <a
              key={idx}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group block rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-[#D4AF37] hover:shadow-md"
            >
              <div className="flex items-center justify-between">
                <span className="rounded bg-amber-50 px-2 py-0.5 text-xs font-bold text-amber-700 border border-amber-200">
                  {item.category}
                </span>
                <span className="text-xs text-slate-400 group-hover:text-[#002B49] transition-colors">↗ External Link</span>
              </div>
              <h3 className="mt-2 text-base font-bold text-[#002B49] group-hover:text-[#D4AF37] transition-colors">
                {item.title}
              </h3>
              <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                {item.desc}
              </p>
            </a>
          ))}
        </div>
      </section>

      {/* Union Ministry Portals */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-[#002B49]">Tracked Union Ministry Portals</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {sectoralLinks.map((sec, idx) => (
            <a
              key={idx}
              href={sec.url}
              target="_blank"
              rel="noopener noreferrer"
              className="block rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-[#002B49]"
            >
              <h3 className="text-base font-bold text-[#002B49]">{sec.title}</h3>
              <p className="mt-1 text-xs text-slate-600">{sec.desc}</p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
