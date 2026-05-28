import { useEffect, useState, useMemo } from "react";
import { getClusterResults } from "../services/api";
import { CLUSTER_COLORS, ANOMALY_COLOR } from "../utils/colors";
import {
  ScatterChart, Scatter, XAxis, YAxis, ZAxis,
  CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

export default function Movement() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    getClusterResults(500)
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const grouped = useMemo(() => {
    const g = {};
    data.forEach((d) => {
      const key = d.is_anomaly
        ? "anomaly"
        : String(d.cluster_label ?? d.cluster_id ?? "unknown");
      if (!g[key]) g[key] = [];
      g[key].push({ magnitude: d.magnitude ?? 0, depth: d.depth ?? 0 });
    });
    return g;
  }, [data]);

  const getColor = (key) => {
    if (key === "anomaly") return ANOMALY_COLOR;
    if (key === "unknown") return "#94A3B8";
    return CLUSTER_COLORS[parseInt(key) % CLUSTER_COLORS.length];
  };

  const getName = (key) =>
    key === "anomaly" ? "Anomali" : key === "unknown" ? "Unknown" : `Cluster ${key}`;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Pergerakan Seismik</h1>
        {data.length > 0 && (
          <span className="page-subtitle">
            {data.length} titik dalam {Object.keys(grouped).length} zona
          </span>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data pergerakan…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Belum ada data clustering. Jalankan ETL dan Training terlebih dahulu.
        </p>
      )}

      {data.length > 0 && (
        <div className="panel">
          <p className="panel-title">Distribusi Magnitudo vs Kedalaman per Cluster</p>
          <p style={{ fontSize: 11, color: "rgba(148,163,184,0.6)", marginBottom: 16 }}>
            Sumbu X = Magnitudo (SR) · Sumbu Y = Kedalaman (km) · Setiap titik = 1 gempa
          </p>
          <div style={{ height: 360 }}>
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 4, right: 24, left: 0, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis
                  dataKey="magnitude"
                  name="Magnitudo"
                  type="number"
                  domain={["auto", "auto"]}
                  tick={{ fontSize: 9, fill: "#94A3B8" }}
                  label={{ value: "Magnitudo (SR)", position: "insideBottomRight", offset: -10, fontSize: 9, fill: "#94A3B8" }}
                />
                <YAxis
                  dataKey="depth"
                  name="Kedalaman"
                  type="number"
                  domain={["auto", "auto"]}
                  tick={{ fontSize: 9, fill: "#94A3B8" }}
                  label={{ value: "Kedalaman (km)", angle: -90, position: "insideLeft", fontSize: 9, fill: "#94A3B8" }}
                />
                <ZAxis range={[20, 20]} />
                <Tooltip
                  contentStyle={{ background: "#ffffff", border: "1px solid rgba(0,0,0,0.10)", borderRadius: "8px", fontSize: "12px", color: "#1e293b" }}
                  cursor={{ strokeDasharray: "3 3" }}
                  formatter={(val, name) => [
                    name === "Magnitudo" ? `${val} SR` : `${val} km`,
                    name,
                  ]}
                />
                {Object.entries(grouped).map(([key, points]) => (
                  <Scatter
                    key={key}
                    name={getName(key)}
                    data={points}
                    fill={getColor(key)}
                    fillOpacity={0.72}
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          <div className="map-legend-bar" style={{ marginTop: 12 }}>
            {Object.keys(grouped).map((key) => (
              <div key={key} className="map-legend-bar-item">
                <span className="map-legend-bar-dot" style={{ background: getColor(key) }} />
                <span>{getName(key)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
