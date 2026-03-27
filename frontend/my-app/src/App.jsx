import React, { useState, useEffect } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// --- CUSTOM MAP ICON (Glow Effect) ---
const createIcon = (color) => L.divIcon({
  className: "custom-icon",
  html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px ${color};"></div>`,
  iconSize: [12, 12],
});

export default function App() {
  const [emergency, setEmergency] = useState("cardiology");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userPos, setUserPos] = useState([36.8065, 10.1815]);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (res) => setUserPos([res.coords.latitude, res.coords.longitude]),
        () => console.log("Defaulting to Tunis Center")
      );
    }
  }, []);

  const handleFind = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/emergency", {
        lat: userPos[0],
        lng: userPos[1],
        type: emergency,
      });
      setResults(response.data.results || []);
      setHasSearched(true);
    } catch (err) {
      alert("System Offline: Check Backend Connection");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[#020617] text-slate-100 font-sans selection:bg-sky-500/30">
      
      {/* TOP NAV BAR */}
      <nav className="h-20 border-b border-slate-800 bg-[#0f172a]/80 backdrop-blur-md flex items-center justify-between px-8 z-50">
        <div className="flex items-center gap-4">
          <div className="h-10 w-10 bg-sky-500 rounded-lg flex items-center justify-center shadow-[0_0_20px_rgba(14,165,233,0.4)]">
            <span className="text-2xl">📡</span>
          </div>
          <div>
            <h1 className="text-xl font-black tracking-tighter uppercase leading-none">Geo-Response <span className="text-sky-500">System</span></h1>
            <div className="flex items-center gap-2 mt-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Network Link Active</span>
            </div>
          </div>
        </div>

        <div className="flex gap-10">
          <StatBox label="Active Nodes" value="50" />
          <StatBox label="Network Load" value="12%" color="text-emerald-400" />
          <StatBox label="Response Latency" value="48ms" />
        </div>
      </nav>

      <div className="flex-1 flex overflow-hidden">
        
        {/* LEFT SIDE: THE MAP AREA */}
        <section className="flex-[2] relative group">
          <div className="absolute inset-0 z-0">
            <MapContainer center={userPos} zoom={13} zoomControl={false} className="h-full w-full">
              <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
              <RecenterMap pos={results.length > 0 ? [results[0].lat, results[0].lng] : userPos} />
              
              <Marker position={userPos} icon={createIcon('#0ea5e9')}>
                <Popup className="custom-popup">You are here</Popup>
              </Marker>

              {results.map((h, i) => (
                <Marker key={i} position={[h.lat, h.lng]} icon={createIcon(i === 0 ? '#10b981' : '#f43f5e')}>
                  <Popup>
                    <div className="text-slate-900 font-bold">{h.hospital_name}</div>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>
          
          {/* MAP OVERLAY: Coordinates */}
          <div className="absolute bottom-6 left-6 bg-slate-900/90 border border-slate-700 px-4 py-2 rounded-md font-mono text-[10px] text-sky-400 backdrop-blur shadow-2xl">
            LAT: {userPos[0].toFixed(4)} // LNG: {userPos[1].toFixed(4)}
          </div>
        </section>

        {/* RIGHT SIDE: CONTROL PANEL */}
        <aside className="w-[450px] bg-[#0f172a] border-l border-slate-800 flex flex-col p-8 overflow-y-auto">
          <div className="mb-8">
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Emergency Parameters</h2>
            <div className="space-y-4">
              <div className="relative">
                <select 
                  value={emergency} 
                  onChange={(e) => setEmergency(e.target.value)}
                  className="w-full bg-slate-800/50 border border-slate-700 p-4 rounded-xl text-sm focus:ring-2 focus:ring-sky-500 outline-none appearance-none transition-all cursor-pointer"
                >
                  <option value="cardiology">🫀 Cardiology</option>
                  <option value="trauma">🤕 Trauma / Surgery</option>
                  <option value="burn unit">🔥 Burn Unit</option>
                  <option value="general">🏥 General Admission</option>
                </select>
              </div>

              <button 
                onClick={handleFind}
                disabled={loading}
                className="w-full bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-bold py-4 rounded-xl shadow-[0_0_20px_rgba(14,165,233,0.2)] transition-all flex items-center justify-center gap-2 group active:scale-[0.98]"
              >
                {loading ? "PROCESSING..." : "INITIATE SEARCH"}
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </button>
            </div>
          </div>

          <div className="flex-1 space-y-4">
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 flex justify-between">
              <span>Optimization Results</span>
              {hasSearched && <span>{results.length} Found</span>}
            </h2>
            
            {results.map((h, i) => (
              <ResultCard key={i} hospital={h} index={i} />
            ))}

            {!hasSearched && (
              <div className="border-2 border-dashed border-slate-800 rounded-2xl h-40 flex items-center justify-center text-slate-600 text-sm">
                Awaiting System Input...
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

// --- SUB-COMPONENTS ---

function StatBox({ label, value, color = "text-white" }) {
  return (
    <div className="text-right">
      <div className={`text-sm font-bold ${color}`}>{value}</div>
      <div className="text-[9px] uppercase tracking-tighter text-slate-500">{label}</div>
    </div>
  );
}

function ResultCard({ hospital, index }) {
  const isTop = index === 0;
  return (
    <div className={`relative p-5 rounded-2xl border transition-all duration-500 hover:scale-[1.02] cursor-default ${
      isTop ? 'bg-sky-500/10 border-sky-500/50 shadow-[0_0_15px_rgba(14,165,233,0.1)]' : 'bg-slate-800/30 border-slate-700'
    }`}>
      {isTop && (
        <span className="absolute -top-2 -right-2 bg-emerald-500 text-[10px] font-black px-2 py-1 rounded-md shadow-lg uppercase">Best Match</span>
      )}
      <div className="flex justify-between items-start mb-3">
        <h3 className="font-bold text-slate-100 text-sm leading-tight max-w-[70%]">{hospital.hospital_name}</h3>
        <div className={`text-sm font-mono font-bold ${isTop ? 'text-sky-400' : 'text-slate-400'}`}>
          {hospital.total_score}%
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4 text-[11px] text-slate-400">
        <div className="flex items-center gap-2">
          <span>📍</span> {hospital.distance_km} KM
        </div>
        <div className="flex items-center gap-2">
          <span>🛌</span> {hospital.bed_score}% AVAIL
        </div>
      </div>
    </div>
  );
}

function RecenterMap({ pos }) {
  const map = useMap();
  useEffect(() => { if (pos) map.flyTo(pos, 14, { duration: 1.5 }); }, [pos]);
  return null;
}