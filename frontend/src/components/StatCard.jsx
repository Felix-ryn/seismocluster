export default function StatCard({ icon: Icon, label, value, gradient = "purple", trend }) {
  return (
    <div className={`stat-card stat-card--${gradient}`}>
      <div className="stat-card-top">
        <div className="stat-card-icon-box">
          <Icon size={18} />
        </div>
        <span className="stat-card-label">{label}</span>
      </div>
      <div className="stat-card-value">{value ?? "—"}</div>
      {trend && <div className="stat-card-trend">{trend}</div>}
      <div className="stat-card-ring" />
    </div>
  );
}
