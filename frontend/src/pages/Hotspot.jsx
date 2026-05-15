import { useEffect, useState } from "react";
import { getSummary } from "../services/api";
import ClusterBadge from "../components/ClusterBadge";
import { CLUSTER_COLORS } from "../utils/colors";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from "recharts";

export default function Hotspot() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    getSummary()
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const sorted = [...data].sort((a, b) => (b.total_earthquakes || 0) - (a.total_earthquakes || 0));

  const chartData = sorted.map((d) => ({
    name:  `CL-${d.cluster}`,
    count: d.total_earthquakes,
    color: CLUSTER_COLORS[d.cluster % CLUSTER_COLORS.length],
  }));

  const top = sorted[0];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Hotspot Zone</h1>
        {top && (
          <span className="page-subtitle">
            Zona paling aktif: Cluster {top.cluster} ({top.total_earthquakes} gempa)
          </span>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data hotspot…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Belum ada data. Jalankan ETL dan Training terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <>
          <div className="panel" style={{ marginBottom: 14 }}>
            <p className="panel-title">Frekuensi Gempa per Zona Cluster</p>
            <div style={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 4, right: 16, left: 0, bottom: 4 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E4E8F2" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 9, fill: "#94A3B8" }} />
                  <YAxis tick={{ fontSize: 9, fill: "#94A3B8" }} />
                  <Tooltip
                    contentStyle={{ background: "#fff", border: "1px solid #E4E8F2", borderRadius: "8px", fontSize: "12px" }}
                    formatter={(val) => [val, "Jumlah Gempa"]}
                  />
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} fillOpacity={0.85} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="panel">
            <p className="panel-title">Detail Zona</p>
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ZONA</th>
                    <th>JUMLAH GEMPA</th>
                    <th>AVG MAGNITUDO</th>
                    <th>AVG KEDALAMAN</th>
                    <th>LEVEL AKTIVITAS</th>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((d, i) => {
                    const lvl = d.total_earthquakes > 100 ? "high" : d.total_earthquakes > 50 ? "medium" : "low";
                    return (
                      <tr key={d.cluster ?? i}>
                        <td><ClusterBadge clusterId={d.cluster} /></td>
                        <td><strong>{d.total_earthquakes}</strong></td>
                        <td>{d.avg_magnitude?.toFixed(2) ?? "—"} SR</td>
                        <td className="td-mono">{d.avg_depth?.toFixed(1) ?? "—"} km</td>
                        <td>
                          <span className={`level-badge level-badge--${lvl}`}>
                            {lvl === "high" ? "Tinggi" : lvl === "medium" ? "Sedang" : "Rendah"}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
