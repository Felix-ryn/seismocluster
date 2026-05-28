import { useNavigate } from "react-router-dom";
import {
  LayoutDashboard, TrendingUp, AlertTriangle, Activity,
  ArrowRight, ChevronRight, Database, Cpu, BarChart2,
  Search, Crosshair, Flame, Waves, Network,
} from "lucide-react";
import { CLUSTER_COLORS } from "../utils/colors";
import bgImg from "../assets/background.jpeg";
import "./Landing.scss";

// ── Data ─────────────────────────────────────────────────────
const CLUSTERS = [
  { id: 0, label: "Cluster 0", region: "Sumatera — Selat Malaka",    color: CLUSTER_COLORS[0] },
  { id: 1, label: "Cluster 1", region: "Jawa — Bali — NTT",          color: CLUSTER_COLORS[1] },
  { id: 2, label: "Cluster 2", region: "Sulawesi — Maluku",          color: CLUSTER_COLORS[2] },
  { id: 3, label: "Cluster 3", region: "Papua — Laut Banda",         color: CLUSTER_COLORS[3] },
  { id: 4, label: "Cluster 4", region: "Papua Timur — Laut Arafura", color: CLUSTER_COLORS[4] },
];

const FEATURES = [
  { icon: LayoutDashboard, label: "Cluster Map", path: "/dashboard",           title: "Peta Sebaran Cluster",   desc: "Visualisasi interaktif 5 zona cluster gempa Indonesia di atas peta Leaflet dengan marker berwarna per cluster.", accent: CLUSTER_COLORS[0] },
  { icon: Crosshair,       label: "Centroid",    path: "/dashboard/centroid",  title: "Analisis Centroid",      desc: "Koordinat pusat setiap cluster beserta statistik rata-rata magnitudo, kedalaman, dan scatter plot spasial.", accent: CLUSTER_COLORS[1] },
  { icon: Flame,           label: "Hotspot",     path: "/dashboard/hotspot",   title: "Zonasi Hotspot",         desc: "Identifikasi zona kepadatan seismik tinggi berdasarkan frekuensi kejadian dan intensitas magnitudo per wilayah.", accent: CLUSTER_COLORS[2] },
  { icon: TrendingUp,      label: "Trend",       path: "/dashboard/trend",     title: "Tren Temporal",          desc: "Grafik tren historis frekuensi gempa per cluster, pola musiman, dan proyeksi aktivitas berbasis data BMKG.", accent: CLUSTER_COLORS[3] },
  { icon: AlertTriangle,   label: "Anomaly",     path: "/dashboard/anomaly",   title: "Deteksi Anomali",        desc: "Isolation Forest mendeteksi gempa anomali di luar pola cluster normal, dengan highlight dan notifikasi real-time.", accent: CLUSTER_COLORS[4] },
  { icon: Activity,        label: "Realtime",    path: "/dashboard/realtime",  title: "Monitor Realtime",       desc: "Feed live data terbaru dari BMKG yang diperbarui otomatis, dilengkapi badge status dan timestamp kejadian.", accent: CLUSTER_COLORS[5] },
  { icon: Waves,           label: "Movement",    path: "/dashboard/movement",  title: "Pergerakan Zona",        desc: "Analisis displacement pusat cluster antar periode waktu, menampilkan arah dan jarak pergeseran zona seismik.", accent: CLUSTER_COLORS[6] },
  { icon: Network,         label: "Hierarchy",   path: "/dashboard/hierarchy", title: "Klaster Hierarki",       desc: "Hierarchical clustering Ward linkage membangun dendrogram zona seismik secara agglomeratif dari data koordinat radian.", accent: CLUSTER_COLORS[7] },
];

const STEPS = [
  { num: "01", icon: Database,  title: "ETL Pipeline",       desc: "Data gempa diambil dari API USGS/BMKG, dibersihkan, dan disimpan ke PostgreSQL secara otomatis." },
  { num: "02", icon: Cpu,       title: "ML Clustering",      desc: "KMeans & Hierarchical Clustering membagi 12.000+ titik gempa ke dalam 5 zona bermakna secara spasial." },
  { num: "03", icon: BarChart2, title: "Dashboard Analitik", desc: "Hasil ditampilkan real-time: peta interaktif, distribusi cluster, anomali, tren, dan monitoring live." },
];

// ── Hero feature buttons — sesuai route dashboard ────────────
const HERO_FEATURES = [
  { icon: LayoutDashboard, title: "Peta Cluster",     sub: "Sebaran 5 zona seismik",      path: "/dashboard",           accent: CLUSTER_COLORS[0] },
  { icon: Crosshair,       title: "Centroid",         sub: "Pusat tiap zona cluster",     path: "/dashboard/centroid",  accent: CLUSTER_COLORS[1] },
  { icon: Flame,           title: "Hotspot",          sub: "Zona kepadatan tinggi",        path: "/dashboard/hotspot",   accent: CLUSTER_COLORS[2] },
  { icon: TrendingUp,      title: "Tren Temporal",    sub: "Historis & proyeksi",         path: "/dashboard/trend",     accent: CLUSTER_COLORS[3] },
  { icon: AlertTriangle,   title: "Deteksi Anomali",  sub: "Isolation Forest real-time",  path: "/dashboard/anomaly",   accent: CLUSTER_COLORS[4] },
  { icon: Activity,        title: "Monitor Realtime", sub: "Feed live data BMKG",         path: "/dashboard/realtime",  accent: CLUSTER_COLORS[5] },
  { icon: Waves,           title: "Pergerakan Zona",  sub: "Displacement antar periode",  path: "/dashboard/movement",  accent: CLUSTER_COLORS[6] },
  { icon: Network,         title: "Klaster Hierarki", sub: "Ward linkage agglomeratif",   path: "/dashboard/hierarchy", accent: CLUSTER_COLORS[7] },
];

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
}

// ── Component ────────────────────────────────────────────────
export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="lp">

      {/* ── HERO ───────────────────────────────────────────── */}
      <section id="hero" className="lp-hero"
        style={{ backgroundImage: `url(${bgImg})` }}>

        <div className="lp-hero-overlay" />

        {/* NAV */}
        <header className="lp-nav">
          <div className="lp-wrap lp-nav-inner">
            <a className="lp-logo" href="#" onClick={e => { e.preventDefault(); scrollTo("hero"); }}>
              <span className="lp-logo-mark">S</span>
              <span className="lp-logo-text">SeismoCluster</span>
            </a>

            <nav className="lp-nav-links">
              {[["Fitur","features"],["Cluster","clusters"],["Pipeline","pipeline"]].map(([l,id]) => (
                <a key={id} className="lp-nav-link" href={`#${id}`}
                  onClick={e => { e.preventDefault(); scrollTo(id); }}>{l}</a>
              ))}
            </nav>

            <div className="lp-nav-right">
              <button className="lp-nav-ghost" onClick={() => navigate("/dashboard")}>
                Buka Dashboard
              </button>
              <button className="lp-nav-icon" aria-label="search">
                <Search size={16} />
              </button>
            </div>
          </div>
        </header>

        {/* HERO BODY */}
        <div className="lp-wrap lp-hero-body">
          {/* LEFT TEXT */}
          <div className="lp-hero-text">
            <h1 className="lp-display">
              SEISMO<br />
              <span className="lp-display-sub">CLUSTER</span>
            </h1>

            <p className="lp-hero-desc">
              Platform visualisasi data gempa bumi real-time dan analisis klaster
              untuk kepulauan Indonesia. Dapatkan wawasan berharga untuk mitigasi bencana.
            </p>

            <button className="lp-arrow-btn" onClick={() => navigate("/dashboard")}
              aria-label="Buka Dashboard">
              <span className="lp-arrow-line" />
              <ArrowRight size={20} strokeWidth={1.5} />
            </button>

            <div className="lp-hero-tagline">
              <p className="lp-tagline-title">Mulai Analisis.</p>
              <p className="lp-tagline-sub">
                Pelajari pola, tren, dan klaster<br />gempa di berbagai wilayah.
              </p>
            </div>
          </div>

          {/* RIGHT — feature navigation buttons */}
          <div className="lp-hero-btns">
            {HERO_FEATURES.map(({ icon: Icon, title, sub, path, accent }) => (
              <button key={path} className="lp-hero-btn" onClick={() => navigate(path)}
                style={{ '--hb-accent': accent }}>
                <div className="lp-hero-btn-icon" style={{ color: accent }}>
                  <Icon size={16} />
                </div>
                <div className="lp-hero-btn-text">
                  <span className="lp-hero-btn-title">{title}</span>
                  <span className="lp-hero-btn-sub">{sub}</span>
                </div>
                <ChevronRight size={12} className="lp-hero-btn-arrow" />
              </button>
            ))}
          </div>
        </div>

        {/* HERO BOTTOM */}
        <div className="lp-hero-bottom">
          <div className="lp-wrap lp-hero-bottom-inner">
            <div />
            <div className="lp-live-badge">
              <span className="lp-live-dot" />
              Pembaruan Terakhir: Real-time
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ──────────────────────────────────────────── */}
      <div className="lp-stats-strip">
        <div className="lp-wrap lp-stats-inner">
          {[["12.620+","Data Gempa Diproses"],["5","Zona Cluster Aktif"],["99%","Akurasi Deteksi"],["24/7","Monitoring Aktif"]].map(([v,l]) => (
            <div key={l} className="lp-stat">
              <span className="lp-stat-value">{v}</span>
              <span className="lp-stat-label">{l}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── CLUSTER ZONES ──────────────────────────────────── */}
      <section id="clusters" className="lp-section">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-tag">5 Zona Cluster</span>
            <h2 className="lp-headline">Peta Seismik Indonesia<br />dalam 5 Klaster</h2>
            <p className="lp-section-sub">
              Algoritma KMeans mengelompokkan seluruh data gempa Indonesia ke dalam 5 zona
              bermakna berdasarkan pola spasial koordinat dan kedalaman.
            </p>
          </div>
          <div className="lp-cluster-grid">
            {CLUSTERS.map(c => (
              <div key={c.id} className="lp-cluster-card" style={{ '--cc': c.color }}>
                <div className="lp-cluster-pill">
                  <span className="lp-cluster-dot" style={{ background: c.color }} />
                  <span style={{ color: c.color, fontSize: 11, fontWeight: 700 }}>{c.label}</span>
                </div>
                <p className="lp-cluster-region">{c.region}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES ───────────────────────────────────────── */}
      <section id="features" className="lp-section lp-section--alt">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-tag">7 Modul Analitik</span>
            <h2 className="lp-headline">Satu Platform,<br />Semua Perspektif Seismik</h2>
            <p className="lp-section-sub">
              Dashboard untuk seismolog profesional — dari peta cluster interaktif
              hingga deteksi anomali dan monitoring data real-time.
            </p>
          </div>
          <div className="lp-features-grid">
            {FEATURES.map(({ icon: Icon, label, path, title, desc, accent }) => (
              <div key={path} className="lp-feature-card"
                onClick={() => navigate(path)} role="button" tabIndex={0}
                style={{ '--fa': accent }}>
                <div className="lp-feature-head">
                  <div className="lp-feature-icon" style={{ background: `${accent}1a`, border: `1px solid ${accent}30` }}>
                    <Icon size={15} color={accent} />
                  </div>
                  <span className="lp-feature-label">{label}</span>
                </div>
                <h3 className="lp-feature-title">{title}</h3>
                <p className="lp-feature-desc">{desc}</p>
                <div className="lp-feature-link" style={{ color: accent }}>
                  Buka halaman <ChevronRight size={12} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PIPELINE ───────────────────────────────────────── */}
      <section id="pipeline" className="lp-section">
        <div className="lp-wrap">
          <div className="lp-section-head">
            <span className="lp-tag">Pipeline ML</span>
            <h2 className="lp-headline">Data Mentah Menjadi<br />Insight Seismik</h2>
          </div>
          <div className="lp-steps">
            {STEPS.map(({ num, icon: Icon, title, desc }) => (
              <div key={num} className="lp-step">
                <div className="lp-step-num">{num}</div>
                <div className="lp-step-icon"><Icon size={20} /></div>
                <h3 className="lp-step-title">{title}</h3>
                <p className="lp-step-desc">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ────────────────────────────────────────────── */}
      <section className="lp-cta">
        <div className="lp-cta-glow" />
        <div className="lp-wrap lp-cta-inner">
          <div>
            <h2 className="lp-cta-title">Siap Memulai Monitoring?</h2>
            <p className="lp-cta-sub">Akses seluruh 7 modul analitik dengan data seismik Indonesia terkini.</p>
          </div>
          <button className="lp-btn-white" onClick={() => navigate("/dashboard")}>
            Buka Dashboard <ArrowRight size={16} />
          </button>
        </div>
      </section>

      {/* ── FOOTER ─────────────────────────────────────────── */}
      <footer className="lp-footer">
        <div className="lp-wrap lp-footer-inner">
          <div className="lp-footer-brand">
            <div className="lp-logo">
              <span className="lp-logo-mark">S</span>
              <span className="lp-logo-text">SeismoCluster</span>
            </div>
            <p className="lp-footer-tag">Sistem Pemantauan Seismik Berbasis<br />Machine Learning · Indonesia</p>
          </div>
          <div className="lp-footer-cols">
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Dashboard</h4>
              {FEATURES.slice(0,4).map(f => (
                <a key={f.path} className="lp-footer-link" href="#"
                  onClick={e => { e.preventDefault(); navigate(f.path); }}>{f.label}</a>
              ))}
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Analitik</h4>
              {FEATURES.slice(4, 8).map(f => (
                <a key={f.path} className="lp-footer-link" href="#"
                  onClick={e => { e.preventDefault(); navigate(f.path); }}>{f.label}</a>
              ))}
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-h">Sistem</h4>
              <span className="lp-footer-meta">5 Zona Cluster</span>
              <span className="lp-footer-meta">Source: USGS/BMKG</span>
              <span className="lp-footer-meta">KMeans + DBSCAN</span>
              <span className="lp-footer-meta">MLflow Registry</span>
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
