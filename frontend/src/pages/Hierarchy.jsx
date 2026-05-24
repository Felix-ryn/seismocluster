import { useEffect, useState } from "react";
import { getHierarchySummary } from "../services/api";
import { CLUSTER_COLORS } from "../utils/colors";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from "recharts";
import { Network, Layers, Activity, BarChart2, GitMerge } from "lucide-react";
import StatCard from "../components/StatCard";

export default function Hierarchy() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  useEffect(() => {
    getHierarchySummary()
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const total  = data.reduce((s, d) => s + (d.total_earthquakes || 0), 0);
  const sorted = [...data].sort((a, b) => b.total_earthquakes - a.total_earthquakes);

  const chartData = data.map((d) => ({
    name:  `H-${d.hierarchy_label}`,
    count: d.total_earthquakes,
    color: CLUSTER_COLORS[d.hierarchy_label % CLUSTER_COLORS.length],
  }));

  const avgPerZone = data.length > 0 ? Math.round(total / data.length) : 0;
  const topZone    = sorted[0];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Klaster Hierarki</h1>
        {data.length > 0 && (
          <span className="page-subtitle">
            {data.length} zona · {total.toLocaleString()} gempa · Ward Linkage
          </span>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data hierarki…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Belum ada data hierarki. Jalankan ETL dan Training terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <>
          <div className="stat-cards-grid">
            <StatCard icon={Network}   label="Total Zona Hierarki"  value={data.length}  gradient="purple" />
            <StatCard icon={Activity}  label="Total Gempa"           value={total}         gradient="cyan"   />
            <StatCard icon={BarChart2} label="Rata-rata per Zona"    value={avgPerZone}    gradient="green"  />
            <StatCard icon={Layers}    label="Zona Terpadat"
              value={topZone ? `H-${topZone.hierarchy_label}` : "—"} gradient="red" />
          </div>

          {/* Bar Chart */}
          <div className="panel" style={{ marginBottom: 14 }}>
            <p className="panel-title">Distribusi Gempa per Zona Hierarki</p>
            <div style={{ height: 260 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 4, right: 16, left: 0, bottom: 4 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 9, fill: "#94A3B8" }} />
                  <YAxis tick={{ fontSize: 9, fill: "#94A3B8" }} />
                  <Tooltip
                    contentStyle={{
                      background: "#ffffff", border: "1px solid rgba(0,0,0,0.10)",
                      borderRadius: "8px", fontSize: "12px", color: "#1e293b",
                    }}
                    formatter={(val) => [val.toLocaleString(), "Jumlah Gempa"]}
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

          {/* Detail Table */}
          <div className="panel">
            <p className="panel-title">Statistik per Zona Hierarki</p>
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ZONA</th>
                    <th>JUMLAH GEMPA</th>
                    <th>AVG MAGNITUDO</th>
                    <th>AVG KEDALAMAN</th>
                    <th>PROPORSI</th>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((d, i) => {
                    const pct   = total ? ((d.total_earthquakes / total) * 100).toFixed(1) : 0;
                    const color = CLUSTER_COLORS[d.hierarchy_label % CLUSTER_COLORS.length];
                    return (
                      <tr key={d.hierarchy_label ?? i}>
                        <td>
                          <span style={{
                            display: "inline-flex", alignItems: "center", gap: 6,
                            padding: "3px 10px", borderRadius: 9999,
                            background: `${color}1a`, border: `1px solid ${color}40`,
                            color: color, fontSize: 11, fontWeight: 700,
                          }}>
                            <GitMerge size={10} />
                            H-{d.hierarchy_label}
                          </span>
                        </td>
                        <td><strong>{d.total_earthquakes.toLocaleString()}</strong></td>
                        <td>{d.avg_magnitude?.toFixed(2) ?? "—"} SR</td>
                        <td className="td-mono">{d.avg_depth?.toFixed(1) ?? "—"} km</td>
                        <td>
                          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                            <div className="progress-bar">
                              <div
                                className="progress-fill"
                                style={{ width: `${pct}%`, background: color }}
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
        </>
      )}
    </div>
  );
}
