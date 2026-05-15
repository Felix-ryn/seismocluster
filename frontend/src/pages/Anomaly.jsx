import { useEffect, useState } from "react";
import { getAnomalies } from "../services/api";
import MagBadge from "../components/MagBadge";
import ClusterBadge from "../components/ClusterBadge";
import Map from "../components/Map";
import { AlertOctagon, RefreshCw } from "lucide-react";

export default function Anomaly() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  const fetchData = () => {
    setLoading(true);
    getAnomalies(200)
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchData(); }, []);

  const maxMag = data.length
    ? Math.max(...data.map((d) => d.magnitude ?? 0)).toFixed(1)
    : null;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Anomali Terdeteksi</h1>
        <button className="btn-secondary" onClick={fetchData} disabled={loading}>
          <RefreshCw size={14} className={loading ? "spin" : ""} />
          Refresh
        </button>
      </div>

      <div className="anomaly-stats-strip">
        <div className="anomaly-stat-item">
          <AlertOctagon size={16} style={{ color: "#EF4444" }} />
          <span className="anomaly-stat-label">Total Anomali</span>
          <span className="anomaly-stat-value">{data.length}</span>
        </div>
        {maxMag && (
          <div className="anomaly-stat-item">
            <span className="anomaly-stat-label">Magnitudo Tertinggi</span>
            <span className="anomaly-stat-value">{maxMag} SR</span>
          </div>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data anomali…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Tidak ada anomali terdeteksi. Jalankan ETL dan Training terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <>
          <div className="panel panel--flush" style={{ marginBottom: 14 }}>
            <Map data={data} />
          </div>

          <div className="panel">
            <p className="panel-title">Daftar Anomali</p>
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>LOKASI</th>
                    <th>LATITUDE</th>
                    <th>LONGITUDE</th>
                    <th>MAGNITUDO</th>
                    <th>KEDALAMAN</th>
                    <th>CLUSTER</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((d, i) => (
                    <tr key={d.id ?? i} className="row-anomaly">
                      <td className="td-ellipsis">{d.place || "—"}</td>
                      <td className="td-mono">{d.latitude?.toFixed(3) ?? "—"}°</td>
                      <td className="td-mono">{d.longitude?.toFixed(3) ?? "—"}°</td>
                      <td><MagBadge magnitude={d.magnitude} /></td>
                      <td className="td-mono">{d.depth ?? "—"} km</td>
                      <td><ClusterBadge clusterId={d.cluster_label ?? d.cluster_id} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
