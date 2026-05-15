import { useEffect, useState, useRef } from "react";
import { getEarthquakes } from "../services/api";
import MagBadge from "../components/MagBadge";
import { Activity, RefreshCw } from "lucide-react";

const REFRESH_MS = 30_000;

export default function Realtime() {
  const [data, setData]       = useState([]);
  const [total, setTotal]     = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const timerRef = useRef(null);

  const fetchData = () => {
    setLoading(true);
    getEarthquakes(100, 0, true)
      .then((res) => {
        setData(res.data.data ?? []);
        setTotal(res.data.total ?? 0);
        setLastUpdated(new Date());
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
    timerRef.current = setInterval(fetchData, REFRESH_MS);
    return () => clearInterval(timerRef.current);
  }, []);

  const fmtDT = (iso) =>
    iso
      ? new Date(iso).toLocaleString("id-ID", {
          day: "2-digit", month: "short",
          hour: "2-digit", minute: "2-digit",
        })
      : "—";

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Data Realtime</h1>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {lastUpdated && (
            <span className="page-subtitle">
              Update: {lastUpdated.toLocaleTimeString("id-ID")}
            </span>
          )}
          <div className="topbar-live-badge">
            <span className="topbar-live-dot" />
            Live
          </div>
          <button className="btn-secondary" onClick={fetchData} disabled={loading}>
            <RefreshCw size={14} className={loading ? "spin" : ""} />
            Refresh
          </button>
        </div>
      </div>

      <div className="anomaly-stats-strip" style={{ marginBottom: 14 }}>
        <div className="anomaly-stat-item">
          <Activity size={16} style={{ color: "#7C3AED" }} />
          <span className="anomaly-stat-label">Total Data Tersimpan</span>
          <span className="anomaly-stat-value">{total}</span>
        </div>
        <div className="anomaly-stat-item">
          <span className="anomaly-stat-label">Ditampilkan</span>
          <span className="anomaly-stat-value">{data.length} terbaru</span>
        </div>
        <div className="anomaly-stat-item">
          <span className="anomaly-stat-label">Refresh otomatis</span>
          <span className="anomaly-stat-value">30 detik</span>
        </div>
      </div>

      {error && <p className="error-text">{error}</p>}

      {!loading && data.length === 0 && (
        <p className="empty-state">
          Belum ada data gempa. Jalankan ETL terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <div className="panel">
          <p className="panel-title">Gempa Terbaru</p>
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>WAKTU</th>
                  <th>LOKASI</th>
                  <th>LATITUDE</th>
                  <th>LONGITUDE</th>
                  <th>MAGNITUDO</th>
                  <th>KEDALAMAN</th>
                </tr>
              </thead>
              <tbody>
                {data.map((d, i) => (
                  <tr key={d.id ?? i}>
                    <td className="td-mono" style={{ fontSize: 10 }}>{fmtDT(d.time)}</td>
                    <td className="td-ellipsis">{d.place || "—"}</td>
                    <td className="td-mono">{d.latitude?.toFixed(3) ?? "—"}°</td>
                    <td className="td-mono">{d.longitude?.toFixed(3) ?? "—"}°</td>
                    <td><MagBadge magnitude={d.magnitude} /></td>
                    <td className="td-mono">{d.depth ?? "—"} km</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
