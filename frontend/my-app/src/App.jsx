import { useState } from "react";

const hospitals = [
  {
    name: "Hospital A",
    time: 7,
    beds: "40/100",
    score: 94,
    specialties: ["Cardiology", "Trauma"],
  },
  {
    name: "Hospital B",
    time: 15,
    beds: "5/100",
    score: 62,
    specialties: ["Burn", "ICU"],
  },
  {
    name: "Hospital C",
    time: 10,
    beds: "20/100",
    score: 80,
    specialties: ["Neurology", "Stroke"],
  },
];

const emergencyTypes = ["Cardiac", "Trauma", "Burn", "Stroke"];

const rankConfig = {
  0: {
    border: "border-emerald-500/60",
    badge: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40",
    glow: "shadow-emerald-500/10",
    dot: "bg-emerald-400",
    label: "OPTIMAL",
    labelColor: "text-emerald-400",
    scoreBar: "bg-emerald-500",
  },
  1: {
    border: "border-amber-500/60",
    badge: "bg-amber-500/20 text-amber-300 border border-amber-500/40",
    glow: "shadow-amber-500/10",
    dot: "bg-amber-400",
    label: "VIABLE",
    labelColor: "text-amber-400",
    scoreBar: "bg-amber-500",
  },
  2: {
    border: "border-red-500/60",
    badge: "bg-red-500/20 text-red-300 border border-red-500/40",
    glow: "shadow-red-500/10",
    dot: "bg-red-400",
    label: "FALLBACK",
    labelColor: "text-red-400",
    scoreBar: "bg-red-500",
  },
};

function MapPlaceholder() {
  return (
    <div className="relative w-full h-full min-h-[420px] rounded-2xl overflow-hidden border border-slate-700/60 shadow-2xl bg-slate-900">
      {/* Grid background */}
      <div
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage:
            "linear-gradient(rgba(99,179,237,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(99,179,237,0.3) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />
      {/* Diagonal accent lines */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage:
            "repeating-linear-gradient(45deg, rgba(99,179,237,0.6) 0, rgba(99,179,237,0.6) 1px, transparent 0, transparent 50%)",
          backgroundSize: "20px 20px",
        }}
      />

      {/* Vignette */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 via-transparent to-slate-900/80 pointer-events-none" />

      {/* Simulated map pins */}
      {[
        { top: "35%", left: "42%", color: "bg-emerald-400", pulse: "bg-emerald-400", label: "A" },
        { top: "55%", left: "61%", color: "bg-amber-400", pulse: "bg-amber-400", label: "B" },
        { top: "48%", left: "30%", color: "bg-red-400", pulse: "bg-red-400", label: "C" },
      ].map((pin, i) => (
        <div
          key={i}
          className="absolute flex flex-col items-center"
          style={{ top: pin.top, left: pin.left, transform: "translate(-50%,-50%)" }}
        >
          <div className="relative flex items-center justify-center w-7 h-7">
            <span
              className={`absolute inline-flex h-full w-full rounded-full ${pin.pulse} opacity-30 animate-ping`}
            />
            <span
              className={`relative inline-flex rounded-full w-5 h-5 ${pin.color} items-center justify-center text-[10px] font-bold text-slate-900`}
            >
              {pin.label}
            </span>
          </div>
          <div className={`w-0.5 h-3 ${pin.color}`} />
          <div className={`w-1 h-1 rounded-full ${pin.color}`} />
        </div>
      ))}

      {/* User location dot */}
      <div
        className="absolute flex items-center justify-center"
        style={{ top: "50%", left: "50%", transform: "translate(-50%,-50%)" }}
      >
        <span className="absolute inline-flex h-10 w-10 rounded-full bg-sky-400 opacity-20 animate-ping" />
        <span className="absolute inline-flex h-6 w-6 rounded-full bg-sky-400 opacity-30" />
        <span className="relative inline-flex w-3 h-3 rounded-full bg-sky-400 shadow-lg shadow-sky-400/60" />
      </div>

      {/* Corner labels */}
      <div className="absolute top-3 left-3 text-[10px] font-mono text-slate-500 tracking-widest">
        LAT 40.7128° N
      </div>
      <div className="absolute top-3 right-3 text-[10px] font-mono text-slate-500 tracking-widest">
        LNG 74.0060° W
      </div>
      <div className="absolute bottom-3 left-3 text-[10px] font-mono text-slate-500 tracking-widest">
        ZOOM LVL 12
      </div>

      {/* Scale bar */}
      <div className="absolute bottom-3 right-3 flex items-center gap-1.5">
        <div className="w-12 h-0.5 bg-slate-500" />
        <span className="text-[10px] font-mono text-slate-500">500m</span>
      </div>

      {/* Center label */}
      <div className="absolute inset-0 flex items-end justify-center pb-10 pointer-events-none">
        <span className="text-xs font-mono tracking-[0.25em] text-slate-600 uppercase">
          Live Map Feed
        </span>
      </div>
    </div>
  );
}

function HospitalCard({ hospital, rank, visible }) {
  const cfg = rankConfig[rank];

  return (
    <div
      className={`
        relative rounded-2xl border ${cfg.border} bg-slate-800/70 backdrop-blur-sm
        shadow-xl ${cfg.glow}
        transition-all duration-300 ease-out
        hover:-translate-y-1 hover:shadow-2xl hover:bg-slate-800/90
        ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
      `}
      style={{
        transitionDelay: visible ? `${rank * 100}ms` : "0ms",
        transition: `opacity 0.4s ease ${rank * 100}ms, transform 0.4s ease ${rank * 100}ms, box-shadow 0.2s ease, background 0.2s ease`,
      }}
    >
      {/* Rank stripe */}
      <div className={`absolute left-0 top-4 bottom-4 w-0.5 rounded-full ${cfg.dot} ml-3`} />

      <div className="p-4 pl-6">
        {/* Top row */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <span className={`text-[10px] font-mono font-bold tracking-widest ${cfg.labelColor}`}>
                #{rank + 1} {cfg.label}
              </span>
            </div>
            <h3 className="text-base font-semibold text-slate-100">{hospital.name}</h3>
          </div>
          <div className={`px-2.5 py-1 rounded-lg text-xs font-bold ${cfg.badge}`}>
            {hospital.score}
            <span className="font-normal opacity-70">/100</span>
          </div>
        </div>

        {/* Score bar */}
        <div className="mb-3">
          <div className="w-full h-1 bg-slate-700/60 rounded-full overflow-hidden">
            <div
              className={`h-full ${cfg.scoreBar} rounded-full transition-all duration-700`}
              style={{
                width: visible ? `${hospital.score}%` : "0%",
                transitionDelay: `${rank * 100 + 200}ms`,
              }}
            />
          </div>
        </div>

        {/* Stats row */}
        <div className="flex gap-4 mb-3">
          <div className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-xs text-slate-400">
              <span className="text-slate-200 font-medium">{hospital.time} min</span> ETA
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0H5m14 0h2M5 21H3" />
            </svg>
            <span className="text-xs text-slate-400">
              <span className="text-slate-200 font-medium">{hospital.beds}</span> beds
            </span>
          </div>
        </div>

        {/* Specialties */}
        <div className="flex flex-wrap gap-1.5">
          {hospital.specialties.map((s) => (
            <span
              key={s}
              className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-700/70 text-slate-400 border border-slate-700"
            >
              {s}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [emergency, setEmergency] = useState("Cardiac");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleFind = () => {
    setLoading(true);
    setResults([]);
    setSearched(false);
    setTimeout(() => {
      const sorted = [...hospitals].sort((a, b) => b.score - a.score);
      setResults(sorted);
      setLoading(false);
      setSearched(true);
    }, 900);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* ── Header ── */}
      <header
        className="relative overflow-hidden px-6 py-7"
        style={{
          background:
            "linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0c4a6e 70%, #0e7490 100%)",
        }}
      >
        {/* Subtle noise overlay */}
        <div
          className="absolute inset-0 opacity-5 pointer-events-none"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E\")",
          }}
        />
        <div className="relative max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2.5 mb-1">
              {/* Pulse indicator */}
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500" />
              </span>
              <span className="text-[11px] font-mono tracking-[0.2em] text-sky-400/80 uppercase">
                System Active
              </span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Emergency Response System
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">
              Find best hospitals in real-time
            </p>
          </div>
          <div className="hidden sm:flex items-center gap-6">
            {["Network", "Units", "Alerts"].map((item, i) => (
              <div key={item} className="text-center">
                <div className="text-lg font-bold text-white">
                  {["48", "12", "3"][i]}
                </div>
                <div className="text-[10px] text-slate-500 uppercase tracking-wider">
                  {item}
                </div>
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main className="max-w-6xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* LEFT — Map */}
        <div className="lg:col-span-3 flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <div className="w-1 h-4 rounded-full bg-sky-500" />
            <span className="text-xs font-mono tracking-widest text-slate-500 uppercase">
              Coverage Map
            </span>
          </div>
          <MapPlaceholder />
        </div>

        {/* RIGHT — Controls + Results */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {/* Control panel */}
          <div className="rounded-2xl border border-slate-700/60 bg-slate-800/50 backdrop-blur-sm p-4">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-1 h-4 rounded-full bg-sky-500" />
              <span className="text-xs font-mono tracking-widest text-slate-500 uppercase">
                Dispatch Control
              </span>
            </div>

            <label className="block text-xs text-slate-500 mb-1.5 uppercase tracking-wider font-medium">
              Emergency Type
            </label>
            <select
              value={emergency}
              onChange={(e) => setEmergency(e.target.value)}
              className="w-full mb-4 px-3 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/60 cursor-pointer transition-all"
            >
              {emergencyTypes.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>

            <button
              onClick={handleFind}
              disabled={loading}
              className="w-full py-2.5 px-4 rounded-xl font-semibold text-sm tracking-wide
                bg-sky-600 hover:bg-sky-500 active:scale-[0.98]
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-all duration-150 text-white shadow-lg shadow-sky-900/40
                flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Scanning…
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z" />
                  </svg>
                  Find Best Hospitals
                </>
              )}
            </button>
          </div>

          {/* Results */}
          <div className="flex flex-col gap-3">
            {!searched && !loading && (
              <div className="rounded-2xl border border-slate-700/40 bg-slate-800/30 p-6 text-center">
                <svg className="w-8 h-8 text-slate-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
                <p className="text-xs text-slate-600">Select an emergency type and run a search</p>
              </div>
            )}

            {results.map((h, i) => (
              <HospitalCard key={h.name} hospital={h} rank={i} visible={searched} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
