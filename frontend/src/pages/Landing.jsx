import { useNavigate } from "react-router-dom";
import {
  LayoutDashboard, Crosshair, Flame, TrendingUp,
  AlertTriangle, Activity, Waves, ArrowRight, ChevronRight,
  Database, Cpu, BarChart2,
} from "lucide-react";
import "./Landing.scss";

// ── Data — sesuai halaman dashboard yang ada ─────────────────
const FEATURES = [
  {
    icon: LayoutDashboard,
    label: "Cluster Map",
    path: "/dashboard",
    title: "Peta Sebaran Cluster",
    desc: "Visualisasi interaktif 5 zona cluster gempa Indonesia di atas peta Leaflet dengan marker berwarna per cluster dan popup detail.",
  },
  {
    icon: Crosshair,
    label: "Centroid",
    path: "/dashboard/centroid",
    title: "Analisis Centroid",
    desc: "Koordinat pusat setiap cluster beserta statistik rata-rata magnitudo, kedalaman, dan scatter plot distribusi spasial.",
  },
  {
    icon: Flame,
    label: "Hotspot",
    path: "/dashboard/hotspot",
    title: "Zonasi Hotspot",
    desc: "Identifikasi zona kepadatan seismik tinggi berdasarkan frekuensi kejadian dan intensitas magnitudo per wilayah.",
  },
  {
    icon: TrendingUp,
    label: "Trend",
    path: "/dashboard/trend",
    title: "Tren Temporal",
    desc: "Grafik tren historis frekuensi gempa per cluster, pola musiman, dan proyeksi aktivitas berbasis data BMKG.",
  },
  {
    icon: AlertTriangle,
    label: "Anomaly",
    path: "/dashboard/anomaly",
    title: "Deteksi Anomali",
    desc: "Isolation Forest mendeteksi gempa anomali di luar pola cluster normal, dengan highlight merah dan notifikasi real-time.",
  },
  {
    icon: Activity,
    label: "Realtime",
    path: "/dashboard/realtime",
    title: "Monitor Realtime",
    desc: "Feed live data terbaru dari BMKG yang diperbarui otomatis, dilengkapi badge status dan timestamp kejadian terakhir.",
  },
  {
    icon: Waves,
    label: "Movement",
    path: "/dashboard/movement",
    title: "Pergerakan Zona",
    desc: "Analisis displacement pusat cluster antar periode waktu, menampilkan arah dan jarak pergeseran zona seismik.",
  },
];

// 5 cluster — data & warna sesuai dashboard (donut chart + peta)
const CLUSTERS = [
  { id: 0, label: "Cluster 0", region: "Sulawesi — Maluku",             color: "#7C3AED", count: 4582  },
  { id: 1, label: "Cluster 1", region: "Sumatera — Selat Malaka",       color: "#06B6D4", count: 1905  },
  { id: 2, label: "Cluster 2", region: "Jawa — Bali — NTT",             color: "#10B981", count: 1462  },
  { id: 3, label: "Cluster 3", region: "Papua — Laut Banda",            color: "#F59E0B", count: 3643  },
  { id: 4, label: "Cluster 4", region: "Papua Timur — Laut Arafura",    color: "#EC4899", count: 1028  },
];

// svgX = (lon - 95) * 10,  svgY = (7 - lat) * 13  (viewBox 0 0 460 220)
// 2 pins per cluster — placed at representative earthquake epicenter zones
const QUAKE_PINS = [
  { svgX:  15, svgY:  52, c: 1, size: 1.1, delay: 0.0 },
  { svgX:  62, svgY: 148, c: 1, size: 0.9, delay: 1.1 },
  { svgX: 148, svgY: 196, c: 2, size: 1.0, delay: 0.5 },
  { svgX: 222, svgY: 203, c: 2, size: 0.9, delay: 1.4 },
  { svgX: 268, svgY:  88, c: 0, size: 1.2, delay: 0.3 },
  { svgX: 328, svgY: 120, c: 0, size: 1.0, delay: 1.2 },
  { svgX: 358, svgY: 150, c: 3, size: 1.1, delay: 0.8 },
  { svgX: 394, svgY: 138, c: 3, size: 0.9, delay: 1.6 },
  { svgX: 430, svgY: 175, c: 4, size: 1.0, delay: 0.6 },
  { svgX: 450, svgY: 198, c: 4, size: 0.85, delay: 1.9 },
];

const STEPS = [
  { num: "01", icon: Database, title: "ETL Pipeline",       desc: "Data gempa diambil dari API USGS/BMKG, dibersihkan, dan disimpan ke PostgreSQL secara otomatis." },
  { num: "02", icon: Cpu,      title: "ML Clustering",      desc: "KMeans & Hierarchical Clustering membagi 12.000+ titik gempa ke dalam 5 zona bermakna secara spasial." },
  { num: "03", icon: BarChart2, title: "Dashboard Analitik", desc: "Hasil ditampilkan real-time: peta interaktif, distribusi cluster, anomali, tren, dan monitoring live." },
];

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
}

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="lp">

      {/* ── HEADER ─────────────────────────────────────────── */}
      <header className="lp-nav">
        <div className="lp-wrap lp-nav-inner">
          <a className="lp-logo" onClick={() => scrollTo("hero")} href="#">
            <span className="lp-logo-mark">S</span>
            <span className="lp-logo-text">SeismoCluster</span>
          </a>

          <nav className="lp-nav-links">
            {[["Fitur","features"],["Cluster","clusters"],["Pipeline","pipeline"]].map(([l,id]) => (
              <a key={id} className="lp-nav-link" href={`#${id}`}
                onClick={e => { e.preventDefault(); scrollTo(id); }}>
                {l}
              </a>
            ))}
          </nav>

          <div className="lp-nav-cta">
            <button className="lp-btn-secondary" onClick={() => scrollTo("features")}>
              Lihat Fitur
            </button>
            <button className="lp-btn-primary" onClick={() => navigate("/dashboard")}>
              Buka Dashboard
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </header>

      {/* ── HERO ────────────────────────────────────────────── */}
      <section id="hero" className="lp-hero">
        <div className="lp-wrap lp-hero-inner">
          <div className="lp-hero-text">
            <div className="lp-eyebrow">
              <span className="lp-eyebrow-dot" />
              Sistem Aktif · Data BMKG Real-time
            </div>

            <h1 className="lp-display">
              Monitoring Gempa<br />
              <span className="lp-display-accent">Berbasis Klaster AI</span>
            </h1>

            <p className="lp-hero-body">
              Platform analitik seismik untuk Indonesia — mengelompokkan 12.000+ kejadian
              gempa ke dalam 5 zona bermakna, mendeteksi anomali, dan menyajikan
              insight real-time bagi seismolog dan pengambil kebijakan.
            </p>

            <div className="lp-hero-actions">
              <button className="lp-btn-primary lp-btn-primary--lg"
                onClick={() => navigate("/dashboard")}>
                Mulai Sekarang
                <ArrowRight size={16} />
              </button>
              <button className="lp-btn-ghost"
                onClick={() => scrollTo("features")}>
                Lihat Semua Fitur
                <ChevronRight size={14} />
              </button>
            </div>
          </div>

          {/* Seismic Cluster Map */}
          <div className="lp-hero-mockup" aria-hidden="true">
            <div className="lp-seismo">
              <div className="lp-seismo-topbar">
                <span className="lp-seismo-title">Peta Klaster Seismik · Indonesia</span>
                <span className="lp-seismo-live">
                  <span className="lp-seismo-live-dot" />
                  LIVE
                </span>
              </div>

              <div className="lp-seismo-stage">
                <div className="lp-seismo-world">
                  {/* Indonesia map — flat layer that gets 3D-tilted by parent */}
                  <svg viewBox="0 0 460 220" xmlns="http://www.w3.org/2000/svg"
                    style={{width:'100%',height:'auto',display:'block'}}>
                    <defs>
                      <pattern id="sgrid" width="46" height="22" patternUnits="userSpaceOnUse">
                        <path d="M 46 0 L 0 0 0 22" fill="none" stroke="#A8BCDA" strokeWidth="0.5"/>
                      </pattern>
                    </defs>
                    {/* Sea */}
                    <rect width="460" height="220" fill="#B8CCE8"/>
                    <rect width="460" height="220" fill="url(#sgrid)" opacity="0.55"/>

                    {/* 3D extrusion shadow (+2,+4 offset) */}
                    <g fill="#8090B8" stroke="none" transform="translate(2,4)">
                      {/* Sumatera — 25 pts */}
                      <path d="M 3,14 L 18,20 L 30,33 L 35,42 L 40,52 L 50,65 L 65,74 L 70,85 L 80,91 L 85,104 L 95,119 L 100,130 L 107,156 L 108,167 L 95,168 L 80,166 L 72,160 L 62,152 L 52,140 L 42,126 L 34,110 L 24,90 L 18,68 L 10,44 L 4,22 Z"/>
                      {/* Jawa — 15 pts */}
                      <path d="M 108,169 L 112,166 L 118,164 L 130,162 L 148,161 L 168,162 L 188,165 L 204,169 L 214,174 L 213,184 L 196,192 L 172,192 L 148,190 L 124,188 L 110,182 Z"/>
                      {/* Kalimantan — 24 pts */}
                      <path d="M 136,86 L 134,68 L 136,48 L 140,32 L 142,20 L 152,10 L 165,4 L 182,0 L 200,0 L 215,4 L 228,10 L 235,22 L 235,38 L 232,56 L 228,78 L 224,100 L 218,124 L 208,143 L 190,150 L 175,152 L 158,150 L 150,143 L 145,126 L 140,106 Z"/>
                      {/* Sulawesi — 21 pts (N arm + E arm + SW peninsula) */}
                      <path d="M 245,98 L 248,84 L 252,74 L 264,72 L 278,74 L 294,69 L 302,77 L 302,88 L 290,100 L 282,112 L 276,130 L 274,152 L 276,163 L 264,167 L 254,162 L 248,152 L 242,162 L 246,150 L 248,136 L 250,122 L 252,108 Z"/>
                      {/* Halmahera */}
                      <path d="M 330,60 L 338,50 L 346,55 L 348,70 L 342,88 L 330,86 Z"/>
                      {/* Seram */}
                      <ellipse cx="350" cy="105" rx="18" ry="6"/>
                      {/* Bali */}
                      <ellipse cx="204" cy="198" rx="5" ry="4"/>
                      {/* Lombok */}
                      <ellipse cx="218" cy="199" rx="4" ry="5"/>
                      {/* Sumbawa */}
                      <ellipse cx="234" cy="200" rx="7" ry="4"/>
                      {/* Flores */}
                      <ellipse cx="260" cy="203" rx="10" ry="4"/>
                      {/* Timor */}
                      <path d="M 278,204 L 292,198 L 308,196 L 318,200 L 314,208 L 295,212 L 278,210 Z"/>
                      {/* Ambon */}
                      <circle cx="332" cy="142" r="4"/>
                      {/* Papua — 19 pts (bird's head + body) */}
                      <path d="M 360,78 L 362,92 L 358,108 L 354,124 L 364,132 L 376,112 L 390,91 L 408,84 L 428,82 L 445,88 L 458,104 L 458,130 L 448,158 L 435,182 L 418,200 L 395,206 L 374,194 L 356,172 L 352,148 Z"/>
                    </g>

                    {/* Island surfaces */}
                    <g fill="#EEF2FC" stroke="#C0CCE6" strokeWidth="0.6">
                      {/* Sumatera */}
                      <path d="M 3,14 L 18,20 L 30,33 L 35,42 L 40,52 L 50,65 L 65,74 L 70,85 L 80,91 L 85,104 L 95,119 L 100,130 L 107,156 L 108,167 L 95,168 L 80,166 L 72,160 L 62,152 L 52,140 L 42,126 L 34,110 L 24,90 L 18,68 L 10,44 L 4,22 Z"/>
                      {/* Jawa */}
                      <path d="M 108,169 L 112,166 L 118,164 L 130,162 L 148,161 L 168,162 L 188,165 L 204,169 L 214,174 L 213,184 L 196,192 L 172,192 L 148,190 L 124,188 L 110,182 Z"/>
                      {/* Kalimantan */}
                      <path d="M 136,86 L 134,68 L 136,48 L 140,32 L 142,20 L 152,10 L 165,4 L 182,0 L 200,0 L 215,4 L 228,10 L 235,22 L 235,38 L 232,56 L 228,78 L 224,100 L 218,124 L 208,143 L 190,150 L 175,152 L 158,150 L 150,143 L 145,126 L 140,106 Z"/>
                      {/* Sulawesi */}
                      <path d="M 245,98 L 248,84 L 252,74 L 264,72 L 278,74 L 294,69 L 302,77 L 302,88 L 290,100 L 282,112 L 276,130 L 274,152 L 276,163 L 264,167 L 254,162 L 248,152 L 242,162 L 246,150 L 248,136 L 250,122 L 252,108 Z"/>
                      {/* Halmahera */}
                      <path d="M 330,60 L 338,50 L 346,55 L 348,70 L 342,88 L 330,86 Z"/>
                      {/* Seram */}
                      <ellipse cx="350" cy="105" rx="18" ry="6"/>
                      {/* Bali */}
                      <ellipse cx="204" cy="198" rx="5" ry="4"/>
                      {/* Lombok */}
                      <ellipse cx="218" cy="199" rx="4" ry="5"/>
                      {/* Sumbawa */}
                      <ellipse cx="234" cy="200" rx="7" ry="4"/>
                      {/* Flores */}
                      <ellipse cx="260" cy="203" rx="10" ry="4"/>
                      {/* Timor */}
                      <path d="M 278,204 L 292,198 L 308,196 L 318,200 L 314,208 L 295,212 L 278,210 Z"/>
                      {/* Ambon */}
                      <circle cx="332" cy="142" r="4"/>
                      {/* Papua */}
                      <path d="M 360,78 L 362,92 L 358,108 L 354,124 L 364,132 L 376,112 L 390,91 L 408,84 L 428,82 L 445,88 L 458,104 L 458,130 L 448,158 L 435,182 L 418,200 L 395,206 L 374,194 L 356,172 L 352,148 Z"/>
                    </g>
                  </svg>

                  {/* Earthquake location pins */}
                  {QUAKE_PINS.map((pin, i) => (
                    <div key={i} className="eq-pin"
                      style={{
                        left: `${(pin.svgX / 460) * 100}%`,
                        top:  `${(pin.svgY / 220) * 100}%`,
                        '--eq-color': CLUSTERS[pin.c].color,
                      }}>
                      <div className="eq-pin-bob" style={{animationDelay:`${pin.delay}s`}}>
                        <svg viewBox="0 0 20 28" className="eq-pin-svg"
                          style={{
                            width:  `${Math.round(13 * pin.size)}px`,
                            height: `${Math.round(20 * pin.size)}px`,
                          }}>
                          <path
                            d="M 10,0 C 4.5,0 0,4.5 0,10 C 0,15 4,19.5 10,26 C 16,19.5 20,15 20,10 C 20,4.5 15.5,0 10,0 Z"
                            fill="var(--eq-color)"/>
                          <circle cx="10" cy="10" r="6.5" fill="white" opacity="0.95"/>
                          <path className="eq-wave"
                            d="M 4,10 L 5.5,10 L 6.5,8 L 7.5,12 L 8.5,8 L 9.5,11 L 10.5,9.5 L 11.5,10 L 16,10"
                            fill="none" stroke="var(--eq-color)" strokeWidth="1.3"
                            strokeLinecap="round" strokeLinejoin="round"
                            style={{animationDelay:`${pin.delay + 0.5}s`}}
                          />
                        </svg>
                      </div>
                      <div className="eq-ring"
                        style={{borderColor:'var(--eq-color)', animationDelay:`${pin.delay}s`}}/>
                      <div className="eq-ring eq-ring--2"
                        style={{borderColor:'var(--eq-color)', animationDelay:`${pin.delay + 0.9}s`}}/>
                    </div>
                  ))}
                </div>
              </div>

              <div className="lp-seismo-legend">
                {CLUSTERS.map(c => (
                  <div key={c.id} className="lp-seismo-legend-item">
                    <span className="lp-seismo-legend-dot" style={{background: c.color}}/>
                    <span>{c.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS STRIP ─────────────────────────────────────── */}
      <div className="lp-stats-strip">
        <div className="lp-wrap lp-stats-inner">
          {[
            ["12.620+", "Data Gempa Diproses"],
            ["5",       "Zona Cluster Aktif"],
            ["99%",     "Akurasi Deteksi"],
            ["24/7",    "Monitoring Aktif"],
          ].map(([v, l]) => (
            <div key={l} className="lp-stat">
              <span className="lp-stat-value">{v}</span>
              <span className="lp-stat-label">{l}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── CLUSTER ZONES ───────────────────────────────────── */}
      <section id="clusters" className="lp-section">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-eyebrow lp-eyebrow--center">5 Zona Cluster</span>
            <h2 className="lp-headline">Peta Seismik Indonesia<br />dalam 5 Klaster</h2>
            <p className="lp-section-sub">
              Algoritma KMeans mengelompokkan seluruh data gempa Indonesia ke dalam 5 zona
              bermakna berdasarkan pola spasial koordinat dan kedalaman.
            </p>
          </div>

          <div className="lp-cluster-grid">
            {CLUSTERS.map(c => (
              <div key={c.id} className="lp-cluster-card">
                <div className="lp-cluster-pill" style={{background: `${c.color}18`, borderColor: `${c.color}40`}}>
                  <span className="lp-cluster-dot" style={{background: c.color}} />
                  <span style={{color: c.color, fontSize: '11px', fontWeight: 700}}>{c.label}</span>
                </div>
                <p className="lp-cluster-region">{c.region}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES ────────────────────────────────────────── */}
      <section id="features" className="lp-section lp-section--raised">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-eyebrow lp-eyebrow--center">7 Modul Analitik</span>
            <h2 className="lp-headline">Satu Platform,<br />Semua Perspektif Seismik</h2>
            <p className="lp-section-sub">
              Dashboard yang dirancang untuk seismolog profesional — dari peta cluster
              interaktif hingga deteksi anomali dan monitoring data real-time.
            </p>
          </div>

          <div className="lp-features-grid">
            {FEATURES.map(({ icon: Icon, label, path, title, desc }) => (
              <div key={path} className="lp-feature-card"
                onClick={() => navigate(path)} role="button" tabIndex={0}>
                <div className="lp-feature-head">
                  <div className="lp-feature-icon">
                    <Icon size={16} />
                  </div>
                  <span className="lp-feature-label">{label}</span>
                </div>
                <h3 className="lp-feature-title">{title}</h3>
                <p className="lp-feature-desc">{desc}</p>
                <div className="lp-feature-link">
                  Buka halaman <ChevronRight size={12} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PIPELINE ────────────────────────────────────────── */}
      <section id="pipeline" className="lp-section">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-eyebrow lp-eyebrow--center">Pipeline ML</span>
            <h2 className="lp-headline">Data Mentah Menjadi<br />Insight Seismik</h2>
          </div>

          <div className="lp-steps">
            {STEPS.map(({ num, icon: Icon, title, desc }, i) => (
              <div key={num} className="lp-step">
                <div className="lp-step-num">{num}</div>
                <div className="lp-step-icon"><Icon size={20} /></div>
                <h3 className="lp-step-title">{title}</h3>
                <p className="lp-step-desc">{desc}</p>
                {i < STEPS.length - 1 && (
                  <div className="lp-step-connector" aria-hidden="true" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA BANNER ──────────────────────────────────────── */}
      <section className="lp-cta-banner">
        <div className="lp-wrap lp-cta-inner">
          <div className="lp-cta-text">
            <h2 className="lp-cta-title">Siap Memulai Monitoring?</h2>
            <p className="lp-cta-sub">
              Akses seluruh 7 modul analitik dengan data seismik Indonesia terkini.
            </p>
          </div>
          <button className="lp-btn-white"
            onClick={() => navigate("/dashboard")}>
            Buka Dashboard
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      {/* ── FOOTER ──────────────────────────────────────────── */}
      <footer className="lp-footer">
        <div className="lp-wrap lp-footer-inner">
          <div className="lp-footer-brand">
            <div className="lp-logo">
              <span className="lp-logo-mark">S</span>
              <span className="lp-logo-text lp-logo-text--muted">SeismoCluster</span>
            </div>
            <p className="lp-footer-tag">
              Sistem Pemantauan Seismik Berbasis<br />Machine Learning · Indonesia
            </p>
          </div>

          <div className="lp-footer-cols">
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Dashboard</h4>
              {FEATURES.slice(0,4).map(f => (
                <a key={f.path} className="lp-footer-link"
                  onClick={() => navigate(f.path)} href="#">
                  {f.label}
                </a>
              ))}
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Analitik</h4>
              {FEATURES.slice(4).map(f => (
                <a key={f.path} className="lp-footer-link"
                  onClick={() => navigate(f.path)} href="#">
                  {f.label}
                </a>
              ))}
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Sistem</h4>
              <span className="lp-footer-meta">5 Zona Cluster</span>
              <span className="lp-footer-meta">Data Source: USGS/BMKG</span>
              <span className="lp-footer-meta">Model: KMeans + DBSCAN</span>
              <span className="lp-footer-meta">MLflow Model Registry</span>
            </div>
          </div>
        </div>

        <div className="lp-footer-bar">
          <div className="lp-wrap lp-footer-bar-inner">
            <span className="lp-footer-copy">© 2025 SeismoCluster</span>
            <div className="lp-status-pill">
              <span className="lp-status-dot" />
              Sistem Aktif
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
}
