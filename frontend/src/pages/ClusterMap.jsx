import { useEffect, useState, useCallback, useMemo } from "react";
import {
  getClusterResults, getSummary, getSummaryStats,
  getAnomalies, runETL, runTraining, getSchedulerStatus,
} from "../services/api";
import Map from "../components/Map";
import StatCard from "../components/StatCard";
import DonutChart from "../components/DonutChart";
import { useSearch } from "../App";
import MagBadge from "../components/MagBadge";
import ClusterBadge from "../components/ClusterBadge";
import {
  Activity, Layers, AlertOctagon, MapPin,
  Database, Cpu, Loader2, AlertTriangle, Clock, Flame,
} from "lucide-react";

const MAG_FILTERS = [
  { label: "Semua", value: 0 },
  { label: "M3+", value: 3 },
  { label: "M4+", value: 4 },
  { label: "M5+", value: 5 },
];

export default function ClusterMap() {
  const [points, setPoints] = useState([]);
  const [stats, setStats] = useState({});
  const [summary, setSummary] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [etlLoading, setEtlLoading] = useState(false);
  const [trainLoading, setTrainLoading] = useState(false);
  const [msg, setMsg] = useState(null);
  const [magFilter, setMagFilter] = useState(0);
  const [nextEtl, setNextEtl] = useState(null);

  const refreshData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, pointsRes, summaryRes, anomaliesRes] = await Promise.all([
        getSummaryStats(),
        getClusterResults(1000),
        getSummary(),
        getAnomalies(1000),
      ]);
      setStats(statsRes.data.data ?? {});
      setPoints(pointsRes.data.data ?? []);
      setSummary(summaryRes.data.data ?? []);
      setAnomalies(anomaliesRes.data.data ?? []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshData();
    getSchedulerStatus()
      .then((res) => {
        const job = res.data.jobs?.find((j) => j.id === "auto_etl");
        if (job?.next_run) setNextEtl(new Date(job.next_run));
      })
      .catch(() => { });
  }, [refreshData]);

  const handleETL = async () => {
    setEtlLoading(true);
    setMsg(null);
    try {
      const res = await runETL();
      const count = res.data.result?.inserted_count ?? res.data.result?.total ?? "selesai";
      setMsg({ type: "success", text: `ETL berhasil — ${count} data baru disimpan.` });
      await refreshData();
    } catch (err) {
      setMsg({ type: "error", text: `ETL gagal: ${err.response?.data?.detail ?? err.message}` });
    } finally {
      setEtlLoading(false);
    }
  };

  const handleTrain = async () => {
    setTrainLoading(true);
    setMsg(null);
    try {
      const res = await runTraining();
      const zones = res.data.result?.hotspot_zones_found ?? "?";
      setMsg({ type: "success", text: `Training selesai — ${zones} zona hotspot ditemukan.` });
      await refreshData();
    } catch (err) {
      setMsg({ type: "error", text: `Training gagal: ${err.response?.data?.detail ?? err.message}` });
    } finally {
      setTrainLoading(false);
    }
  };

  const { query } = useSearch();

  const mapPoints = useMemo(() => {
    const ids = new Set(points.map(p => p.id));
    const extra = anomalies
      .filter(a => !ids.has(a.id))
      .map(a => ({ ...a, is_anomaly: true }));
    let all = [...points, ...extra];
    if (magFilter > 0) all = all.filter(p => (p.magnitude ?? 0) >= magFilter);
    if (query.trim()) all = all.filter(p =>
      (p.place ?? "").toLowerCase().includes(query.toLowerCase())
    );
    return all;
  }, [points, anomalies, magFilter, query]);

  const top5 = useMemo(() =>
    [...points]
      .filter(p => p.magnitude != null)
      .sort((a, b) => b.magnitude - a.magnitude)
      .slice(0, 5),
    [points]
  );

  const fmtTime = (iso) =>
    iso ? new Date(iso).toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" }) : "";

  const fmtNextEtl = (date) => {
    if (!date) return null;
    const diff = date - Date.now();
    if (diff <= 0) return "sebentar lagi";
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    return h > 0 ? `${h}j ${m}m lagi` : `${m}m lagi`;
  };

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <h1 className="page-title">Dashboard Seismik</h1>
        <div className="action-btn-group">
          <button className="btn-secondary" onClick={handleETL} disabled={etlLoading || trainLoading}>
            {etlLoading ? <Loader2 size={14} className="spin" /> : <Database size={14} />}
            {etlLoading ? "ETL berjalan…" : "Run ETL"}
          </button>
          <button className="btn-primary" onClick={handleTrain} disabled={etlLoading || trainLoading}>
            {trainLoading ? <Loader2 size={14} className="spin" /> : <Cpu size={14} />}
            {trainLoading ? "Training…" : "Run Training"}
          </button>
        </div>
      </div>

      {/* Jadwal ETL Otomatis */}
      {nextEtl && (
        <div className="scheduler-info">
          <Clock size={13} />
          <span>ETL otomatis berikutnya: <strong>{fmtNextEtl(nextEtl)}</strong></span>
          <span className="scheduler-time">({nextEtl.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })} WIB)</span>
        </div>
      )}

      {msg && (
        <div className={`status-msg status-msg--${msg.type}`}>
          <span>{msg.text}</span>
          <button className="status-msg-close" onClick={() => setMsg(null)}>×</button>
        </div>
      )}

      {/* KPI Cards */}
      <div className="stat-cards-grid">
        <StatCard icon={Activity} label="Total Gempa" value={stats.total_earthquakes_processed ?? 0} gradient="purple" />
        <StatCard icon={Layers} label="Total Cluster" value={stats.total_clusters ?? 0} gradient="cyan" />
        <StatCard icon={AlertOctagon} label="Anomali" value={stats.total_anomalies ?? 0} gradient="red" />
        <StatCard icon={MapPin} label="Data Raw Indonesia" value={stats.total_raw_indonesia ?? 0} gradient="green" />
      </div>

      {loading && <p className="loading-text">Memuat data cluster…</p>}
      {error && <p className="error-text">{error}</p>}

      {/* Main Grid */}
      <div className="cluster-main-grid">
        {/* Left */}
        <div className="cluster-left">
          <div className="panel panel--flush">
            {/* Filter Magnitudo */}
            <div className="mag-filter-bar">
              <span className="mag-filter-label">Filter:</span>
              {MAG_FILTERS.map((f) => (
                <button
                  key={f.value}
                  className={`mag-filter-btn${magFilter === f.value ? " mag-filter-btn--active" : ""}`}
                  onClick={() => setMagFilter(f.value)}
                >
                  {f.label}
                </button>
              ))}
              <span className="mag-filter-count">{mapPoints.length} titik</span>
            </div>
            <Map data={mapPoints} />
          </div>

          {points.length > 0 && (
            <div className="panel">
              <p className="panel-title">Tabel Koordinat</p>
              <div className="table-scroll">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>LOKASI</th><th>LATITUDE</th><th>LONGITUDE</th><th>MAGNITUDO</th><th>CLUSTER</th>
                    </tr>
                  </thead>
                  <tbody>
                    {points.slice(0, 15).map((p, i) => (
                      <tr key={p.id ?? i} className={p.is_anomaly ? "row-anomaly" : ""}>
                        <td className="td-ellipsis">{p.place || "—"}</td>
                        <td className="td-mono">{p.latitude?.toFixed(3) ?? "—"}°</td>
                        <td className="td-mono">{p.longitude?.toFixed(3) ?? "—"}°</td>
                        <td><MagBadge magnitude={p.magnitude} /></td>
                        <td><ClusterBadge clusterId={p.cluster_label ?? p.cluster_id} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* Right */}
        <div className="cluster-right">
          <div className="panel">
            <p className="panel-title">Distribusi Cluster</p>
            <DonutChart data={summary} />
          </div>

          {/* Top 5 Gempa Terkuat */}
          {top5.length > 0 && (
            <div className="panel">
              <p className="panel-title">
                <Flame size={13} style={{ display: "inline", marginRight: 6, color: "#F97316" }} />
                Top 5 Gempa Terkuat
              </p>
              {top5.map((p, i) => (
                <div key={p.id ?? i} className="event-item">
                  <div className="event-rank">#{i + 1}</div>
                  <div className="event-info">
                    <div className="event-place">{p.place || "Unknown"}</div>
                    <div className="event-meta">
                      {p.latitude?.toFixed(2)}°/{p.longitude?.toFixed(2)}°
                      {p.depth != null ? ` · ${p.depth} km` : ""}
                    </div>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 4 }}>
                    <MagBadge magnitude={p.magnitude} />
                    <ClusterBadge clusterId={p.cluster_label ?? p.cluster_id} />
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="panel">
            <p className="panel-title">Event Anomali Terkini</p>
            {anomalies.length === 0 ? (
              <p className="empty-state">Tidak ada anomali terdeteksi.</p>
            ) : (
              anomalies.slice(0, 6).map((a, i) => (
                <div key={a.id ?? i} className="event-item event-item--anomaly">
                  <div className="event-icon-box">
                    <AlertTriangle size={13} style={{ color: "#991B1B" }} />
                  </div>
                  <div className="event-info">
                    <div className="event-place">{a.place || "Unknown"}</div>
                    <div className="event-meta">
                      Mag.{a.magnitude ?? "—"} · {a.latitude?.toFixed(2)}°/{a.longitude?.toFixed(2)}°
                    </div>
                  </div>
                  {a.time && <div className="event-time">{fmtTime(a.time)}</div>}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
