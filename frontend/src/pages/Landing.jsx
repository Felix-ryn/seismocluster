import { useNavigate } from "react-router-dom";
import {
  Waves,
  Layers,
  AlertTriangle,
  Activity,
  MapPin,
  TrendingUp,
  ArrowRight,
  Globe,
  ShieldCheck,
  Database,
  ChevronRight,
  BarChart2,
  Cpu,
  Zap,
} from "lucide-react";
import "./Landing.scss";

const NAV_LINKS = [
  { label: "Tentang",    href: "#about"    },
  { label: "Fitur",      href: "#features" },
  { label: "Cara Kerja", href: "#how"      },
  { label: "Statistik",  href: "#stats"    },
];

const FEATURES = [
  {
    icon: Layers,
    color: "purple",
    title: "Clustering Seismik",
    desc: "Pengelompokan otomatis data gempa menggunakan algoritma DBSCAN & K-Means untuk identifikasi pola seismik secara akurat.",
  },
  {
    icon: AlertTriangle,
    color: "red",
    title: "Deteksi Anomali",
    desc: "Sistem deteksi dini untuk gempa anomali berdasarkan deviasi pola cluster yang signifikan dari baseline.",
  },
  {
    icon: MapPin,
    color: "cyan",
    title: "Peta Interaktif",
    desc: "Visualisasi persebaran gempa di seluruh Indonesia secara real-time di atas peta geospasial Leaflet.",
  },
  {
    icon: TrendingUp,
    color: "green",
    title: "Analisis Tren",
    desc: "Analisis tren historis dan pergerakan zona seismik untuk pemantauan jangka panjang berbasis data.",
  },
  {
    icon: Activity,
    color: "purple",
    title: "Monitor Realtime",
    desc: "Pemantauan aktivitas seismik secara langsung dengan data yang diperbarui otomatis dari sumber BMKG.",
  },
  {
    icon: Globe,
    color: "cyan",
    title: "Hotspot Zonasi",
    desc: "Identifikasi zona hotspot seismik berdasarkan kepadatan dan intensitas aktivitas gempa di setiap wilayah.",
  },
];

const STATS = [
  { value: "500+",  label: "Data Gempa Diproses",  icon: Database  },
  { value: "8",     label: "Zona Cluster Aktif",    icon: Layers    },
  { value: "99%",   label: "Akurasi Deteksi",       icon: ShieldCheck },
  { value: "24/7",  label: "Monitoring Aktif",      icon: Activity  },
];

const HOW_STEPS = [
  {
    num: "01",
    icon: Database,
    title: "Pengumpulan Data",
    desc: "Data seismik mentah dikumpulkan dari API BMKG secara otomatis melalui proses ETL yang terjadwal.",
  },
  {
    num: "02",
    icon: Cpu,
    title: "Proses Machine Learning",
    desc: "Model DBSCAN & K-Means menganalisis pola koordinat dan magnitudo untuk membentuk cluster yang bermakna.",
  },
  {
    num: "03",
    icon: BarChart2,
    title: "Visualisasi & Monitoring",
    desc: "Hasil clustering ditampilkan pada dashboard interaktif dengan peta, grafik, dan notifikasi anomali real-time.",
  },
];

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
}

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="lp">

      {/* ── HEADER ── */}
      <header className="lp-header">
        <div className="lp-container lp-header-inner">
          <div className="lp-logo">
            <span className="lp-logo-icon">S</span>
            <span className="lp-logo-name">SeismoCluster</span>
          </div>

          <nav className="lp-nav" aria-label="Main navigation">
            {NAV_LINKS.map(({ label, href }) => (
              <a
                key={href}
                className="lp-nav-link"
                href={href}
                onClick={(e) => { e.preventDefault(); scrollTo(href.slice(1)); }}
              >
                {label}
              </a>
            ))}
          </nav>

          <button className="lp-btn-primary" onClick={() => navigate("/dashboard")}>
            Buka Dashboard
            <ArrowRight size={15} />
          </button>
        </div>
      </header>

      {/* ── HERO ── */}
      <section className="lp-hero">
        <div className="lp-hero-bg-blob lp-hero-bg-blob--1" aria-hidden="true" />
        <div className="lp-hero-bg-blob lp-hero-bg-blob--2" aria-hidden="true" />

        <div className="lp-container lp-hero-inner">
          <div className="lp-hero-content">
            <div className="lp-eyebrow">
              <Waves size={12} />
              Sistem Monitoring Seismik Indonesia
            </div>

            <h1 className="lp-hero-title">
              Analisis Klaster Gempa
              <span className="lp-hero-title-accent"> Berbasis AI</span>
            </h1>

            <p className="lp-hero-desc">
              Platform cerdas untuk pemantauan, klasifikasi, dan analisis aktivitas seismik
              di seluruh wilayah Indonesia menggunakan machine learning dan visualisasi
              geospasial secara real-time.
            </p>

            <div className="lp-hero-actions">
              <button className="lp-btn-primary lp-btn-primary--lg" onClick={() => navigate("/dashboard")}>
                Mulai Sekarang
                <ArrowRight size={16} />
              </button>
              <button
                className="lp-btn-outline"
                onClick={() => scrollTo("about")}
              >
                Pelajari Lebih Lanjut
              </button>
            </div>

            <div className="lp-hero-badges">
              <span className="lp-badge lp-badge--green">
                <span className="lp-badge-dot" />
                Sistem Aktif
              </span>
              <span className="lp-badge lp-badge--purple">BMKG Data Source</span>
              <span className="lp-badge lp-badge--purple">Machine Learning</span>
            </div>
          </div>

          {/* Dashboard mockup preview */}
          <div className="lp-hero-mockup" aria-hidden="true">
            <div className="lp-mockup-card">
              <div className="lp-mockup-topbar">
                <div className="lp-mockup-dot lp-mockup-dot--red"   />
                <div className="lp-mockup-dot lp-mockup-dot--amber" />
                <div className="lp-mockup-dot lp-mockup-dot--green" />
                <span className="lp-mockup-title">Dashboard Seismik</span>
              </div>
              <div className="lp-mockup-body">
                <div className="lp-mockup-stat lp-mockup-stat--purple" />
                <div className="lp-mockup-stat lp-mockup-stat--cyan"   />
                <div className="lp-mockup-stat lp-mockup-stat--red"    />
                <div className="lp-mockup-stat lp-mockup-stat--green"  />
                <div className="lp-mockup-map"  />
                <div className="lp-mockup-chart">
                  {[40, 65, 45, 80, 55, 70, 50, 90, 60, 75].map((h, i) => (
                    <div key={i} className="lp-mockup-bar" style={{ height: `${h}%` }} />
                  ))}
                </div>
              </div>
            </div>
            <div className="lp-mockup-glow" />
          </div>
        </div>
      </section>

      {/* ── ABOUT ── */}
      <section id="about" className="lp-about">
        <div className="lp-container lp-about-inner">
          <div className="lp-about-text">
            <span className="lp-section-tag">Tentang Sistem</span>
            <h2 className="lp-section-title">Apa itu SeismoCluster?</h2>
            <p className="lp-about-desc">
              SeismoCluster adalah platform monitoring seismik berbasis kecerdasan buatan yang
              dirancang khusus untuk menganalisis dan memvisualisasikan aktivitas gempa bumi
              di seluruh wilayah Indonesia.
            </p>
            <p className="lp-about-desc">
              Sistem ini mengintegrasikan data real-time dari BMKG dengan algoritma machine
              learning untuk mengelompokkan gempa berdasarkan pola geografis, mendeteksi
              anomali berbahaya, dan menyajikan insight yang actionable bagi para seismolog
              dan pengambil kebijakan.
            </p>
            <div className="lp-about-points">
              {[
                "Data real-time dari sumber resmi BMKG",
                "Algoritma DBSCAN & K-Means yang teroptimasi",
                "Visualisasi peta geospasial interaktif",
                "Notifikasi anomali seismik otomatis",
              ].map((pt) => (
                <div key={pt} className="lp-about-point">
                  <ChevronRight size={14} className="lp-about-point-icon" />
                  <span>{pt}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="lp-about-cards">
            <div className="lp-about-card lp-about-card--purple">
              <Waves size={28} />
              <h3>Monitoring 24/7</h3>
              <p>Sistem berjalan terus-menerus memantau aktivitas seismik tanpa henti</p>
            </div>
            <div className="lp-about-card lp-about-card--cyan">
              <ShieldCheck size={28} />
              <h3>Deteksi Dini</h3>
              <p>Anomali seismik terdeteksi dan dilaporkan secara otomatis dalam hitungan detik</p>
            </div>
            <div className="lp-about-card lp-about-card--light">
              <Zap size={28} />
              <h3>Analitik Mendalam</h3>
              <p>Laporan cluster, tren historis, dan pergerakan zona seismik dalam satu platform</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section id="stats" className="lp-stats">
        <div className="lp-container">
          <div className="lp-stats-grid">
            {STATS.map(({ value, label, icon: Icon }) => (
              <div key={label} className="lp-stat-item">
                <div className="lp-stat-icon"><Icon size={22} /></div>
                <div className="lp-stat-value">{value}</div>
                <div className="lp-stat-label">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section id="features" className="lp-features">
        <div className="lp-container">
          <div className="lp-section-header">
            <span className="lp-section-tag">Fitur Unggulan</span>
            <h2 className="lp-section-title">Semua yang Anda Butuhkan</h2>
            <p className="lp-section-sub">
              Dilengkapi dengan modul analitik komprehensif untuk pemantauan seismik profesional
            </p>
          </div>
          <div className="lp-features-grid">
            {FEATURES.map(({ icon: Icon, color, title, desc }) => (
              <div key={title} className={`lp-feature-card lp-feature-card--${color}`}>
                <div className={`lp-feature-icon lp-feature-icon--${color}`}>
                  <Icon size={20} />
                </div>
                <h3 className="lp-feature-title">{title}</h3>
                <p className="lp-feature-desc">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section id="how" className="lp-how">
        <div className="lp-container">
          <div className="lp-section-header">
            <span className="lp-section-tag">Cara Kerja</span>
            <h2 className="lp-section-title">Bagaimana Sistem Bekerja</h2>
            <p className="lp-section-sub">
              Tiga tahap proses yang mengubah data gempa mentah menjadi insight yang bermakna
            </p>
          </div>
          <div className="lp-how-grid">
            {HOW_STEPS.map(({ num, icon: Icon, title, desc }, i) => (
              <div key={num} className="lp-how-step">
                <div className="lp-how-step-num">{num}</div>
                <div className="lp-how-step-icon">
                  <Icon size={24} />
                </div>
                <h3 className="lp-how-step-title">{title}</h3>
                <p className="lp-how-step-desc">{desc}</p>
                {i < HOW_STEPS.length - 1 && (
                  <div className="lp-how-arrow" aria-hidden="true">
                    <ArrowRight size={18} />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="lp-cta">
        <div className="lp-cta-glow" aria-hidden="true" />
        <div className="lp-container lp-cta-inner">
          <h2 className="lp-cta-title">Siap Memantau Aktivitas Seismik?</h2>
          <p className="lp-cta-sub">
            Akses dashboard lengkap dengan data seismik Indonesia terkini dan analitik berbasis AI
          </p>
          <button
            className="lp-btn-white"
            onClick={() => navigate("/dashboard")}
          >
            Buka Dashboard Sekarang
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="lp-footer">
        <div className="lp-container lp-footer-inner">
          <div className="lp-footer-brand">
            <div className="lp-logo">
              <span className="lp-logo-icon">S</span>
              <span className="lp-logo-name lp-logo-name--light">SeismoCluster</span>
            </div>
            <p className="lp-footer-tagline">
              Sistem Pemantauan Seismik Berbasis Machine Learning untuk Indonesia
            </p>
          </div>

          <div className="lp-footer-links">
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-title">Sistem</h4>
              <a className="lp-footer-link" onClick={() => scrollTo("about")} href="#about">Tentang</a>
              <a className="lp-footer-link" onClick={() => scrollTo("features")} href="#features">Fitur</a>
              <a className="lp-footer-link" onClick={() => scrollTo("how")} href="#how">Cara Kerja</a>
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-title">Dashboard</h4>
              <a className="lp-footer-link" onClick={() => navigate("/dashboard")} href="#">Cluster Map</a>
              <a className="lp-footer-link" onClick={() => navigate("/dashboard/anomaly")} href="#">Anomali</a>
              <a className="lp-footer-link" onClick={() => navigate("/dashboard/realtime")} href="#">Realtime</a>
            </div>
            <div className="lp-footer-col">
              <h4 className="lp-footer-col-title">Data</h4>
              <span className="lp-footer-text">Sumber: BMKG</span>
              <span className="lp-footer-text">Update: Real-time</span>
              <span className="lp-footer-text">Cakupan: Indonesia</span>
            </div>
          </div>
        </div>

        <div className="lp-footer-bottom">
          <div className="lp-container lp-footer-bottom-inner">
            <span className="lp-footer-copy">
              © 2025 SeismoCluster · Sistem Pemantauan Seismik Indonesia
            </span>
            <div className="lp-footer-live">
              <span className="lp-footer-live-dot" />
              Sistem Aktif
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
}
