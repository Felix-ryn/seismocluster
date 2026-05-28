import { useEffect, useState, useMemo } from "react";
import { getEarthquakes } from "../services/api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Dot,
} from "recharts";

export default function Trend() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    getEarthquakes(500, 0, true)
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const trendData = useMemo(() => {
    const counts = {};
    data.forEach((d) => {
      if (!d.time) return;
      const key = new Date(d.time).toISOString().slice(0, 10);
      counts[key] = (counts[key] || 0) + 1;
    });
    return Object.entries(counts)
      .sort(([a], [b]) => a.localeCompare(b))
      .slice(-30)
      .map(([date, count]) => ({
        date: new Date(date).toLocaleDateString("id-ID", { day: "2-digit", month: "short" }),
        count,
      }));
  }, [data]);

  const avgMag = useMemo(() => {
    if (!data.length) return 0;
    return (data.reduce((s, d) => s + (d.magnitude || 0), 0) / data.length).toFixed(2);
  }, [data]);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Tren Gempa</h1>
        {data.length > 0 && (
          <span className="page-subtitle">
            {data.length} data · Rata-rata {avgMag} SR
          </span>
        )}
      </div>

      {loading && <p className="loading-text">Memuat data tren…</p>}
      {error   && <p className="error-text">{error}</p>}

      {!loading && !error && data.length === 0 && (
        <p className="empty-state">
          Belum ada data gempa. Jalankan ETL terlebih dahulu.
        </p>
      )}

      {trendData.length > 0 && (
        <div className="panel">
          <p className="panel-title">Frekuensi Gempa per Hari (30 hari terakhir)</p>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={trendData}
                margin={{ top: 8, right: 16, left: 0, bottom: 30 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 9, fill: "#94A3B8" }}
                  angle={-45}
                  textAnchor="end"
                  height={50}
                  interval={Math.floor(trendData.length / 8) || 0}
                />
                <YAxis tick={{ fontSize: 9, fill: "#94A3B8" }} />
                <Tooltip
                  contentStyle={{
                    background: "#ffffff",
                    border: "1px solid rgba(0,0,0,0.10)",
                    borderRadius: "8px",
                    fontSize: "12px",
                    color: "#1e293b",
                  }}
                  formatter={(val) => [val, "Gempa"]}
                />
                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#7C3AED"
                  strokeWidth={2}
                  dot={<Dot r={3} fill="#7C3AED" />}
                  activeDot={{ r: 5, fill: "#7C3AED" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
