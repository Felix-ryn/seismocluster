import { Bell, Search } from "lucide-react";

export default function Topbar() {
  const dateStr = new Date().toLocaleDateString("id-ID", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <header className="topbar">
      <div className="topbar-greeting">
        <span className="topbar-greeting-name">Selamat Datang, Admin BMKG</span>
        <span className="topbar-greeting-date">{dateStr}</span>
      </div>

      <div className="topbar-search">
        <Search size={14} className="topbar-search-icon" />
        <input
          type="text"
          className="topbar-search-input"
          placeholder="Cari lokasi gempa..."
        />
      </div>

      <div className="topbar-actions">
        <div className="topbar-live-badge">
          <span className="topbar-live-dot" />
          Live
        </div>
        <button className="topbar-notif-btn" aria-label="Notifikasi">
          <Bell size={18} />
        </button>
        <div className="topbar-avatar">A</div>
      </div>
    </header>
  );
}
