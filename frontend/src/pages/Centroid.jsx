import { useEffect, useState } from "react";
import { getSummary } from "../services/api";
import ClusterBadge from "../components/ClusterBadge";
import { CLUSTER_COLORS } from "../utils/colors";

export default function Centroid() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    getSummary()
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const total = data.reduce((s, d) => s + (d.total_earthquakes || 0), 0);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Centroid Cluster</h1>
        {total > 0 && (
          <span className="page-subtitle">
            {total} gempa dalam {data.length} cluster
          </span>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data cluster…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Belum ada data cluster. Jalankan ETL dan Training terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <div className="panel">
          <p className="panel-title">Ringkasan per Cluster</p>
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>CLUSTER</th>
                  <th>JUMLAH GEMPA</th>
                  <th>AVG MAGNITUDO</th>
                  <th>AVG KEDALAMAN</th>
                  <th>PROPORSI</th>
                </tr>
              </thead>
              <tbody>
                {data.map((d, i) => {
                  const pct = total ? ((d.total_earthquakes / total) * 100).toFixed(1) : 0;
                  const barColor = CLUSTER_COLORS[d.cluster % CLUSTER_COLORS.length];
                  return (
                    <tr key={d.cluster ?? i}>
                      <td><ClusterBadge clusterId={d.cluster} /></td>
                      <td><strong>{d.total_earthquakes}</strong></td>
                      <td>{d.avg_magnitude?.toFixed(2) ?? "—"} SR</td>
                      <td className="td-mono">{d.avg_depth?.toFixed(1) ?? "—"} km</td>
                      <td>
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                          <div className="progress-bar">
                            <div
                              className="progress-fill"
                              style={{ width: `${pct}%`, background: barColor }}
                            />
                          </div>
                          <span className="progress-pct">{pct}%</span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
