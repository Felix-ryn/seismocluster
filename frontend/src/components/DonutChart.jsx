import { PieChart, Pie, Cell, Tooltip } from "recharts";
import { CLUSTER_COLORS, ANOMALY_COLOR } from "../utils/colors";

export default function DonutChart({ data = [] }) {
  const chartData = data.map((d) => ({
    name: `Cluster ${d.cluster}`,
    value: d.total_earthquakes || 0,
    color: d.cluster < 0 ? ANOMALY_COLOR : CLUSTER_COLORS[d.cluster % CLUSTER_COLORS.length],
  }));

  const total = chartData.reduce((s, d) => s + d.value, 0);

  if (!chartData.length) {
    return <p className="empty-state">Belum ada data cluster.</p>;
  }

  return (
    <div className="donut-wrapper">
      <div className="donut-chart-area">
        <PieChart width={170} height={170}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={52}
            outerRadius={76}
            dataKey="value"
            paddingAngle={2}
          >
            {chartData.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(val, name) => [val, name]}
            contentStyle={{
              background: "#fff",
              border: "1px solid #E4E8F2",
              borderRadius: "8px",
              fontSize: "12px",
            }}
          />
        </PieChart>
        <div className="donut-center">
          <span className="donut-total">{total}</span>
          <span className="donut-total-label">Total</span>
        </div>
      </div>
      <div className="donut-legend">
        {chartData.map((entry, i) => (
          <div key={i} className="donut-legend-row">
            <span className="donut-legend-dot" style={{ background: entry.color }} />
            <span className="donut-legend-name">{entry.name}</span>
            <span className="donut-legend-count">{entry.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
