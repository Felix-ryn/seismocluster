import { useMemo } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// ── Read a CSS variable from DESIGN.md tokens ────────────────
const cssVar = (name) =>
  getComputedStyle(document.documentElement).getPropertyValue(name).trim();

// ── Resolve cluster index (handles negative / out-of-range) ──
const clusterIndex = (clusterId) => ((clusterId % 5) + 5) % 5;

export default function Map({ data = [] }) {
  // Compute colors once from CSS variables — single source of truth is index.css
  const colors = useMemo(() => ({
    clusters: [0, 1, 2, 3, 4].map((i) => cssVar(`--cluster-${i}`)),
    anomaly:  cssVar("--color-accent-pink"),
    unknown:  cssVar("--color-on-dark-muted"),
    border:   cssVar("--color-hairline-violet"),
  }), []);

  function getColor(point) {
    if (point.is_anomaly) return colors.anomaly;
    const cid = point.cluster_id ?? point.cluster_label;
    if (cid === null || cid === undefined) return colors.unknown;
    return colors.clusters[clusterIndex(cid)];
  }

  // Scale marker radius by magnitude (M 1 → r 4, M 7 → r 18)
  function getRadius(magnitude) {
    if (!magnitude) return 5;
    return Math.max(4, Math.min(18, magnitude * 2.5));
  }

  const LEGEND_LABELS = ["Zone 0", "Zone 1", "Zone 2", "Zone 3", "Zone 4"];

  return (
    <div className="map-wrapper">
      <MapContainer
        center={[-2.5, 118.0]}
        zoom={5}
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom
      >
        {/* Dark tile — matches DESIGN.md surface-canvas-dark */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
          maxZoom={19}
        />

        {data.map((point) => {
          const fill   = getColor(point);
          const radius = getRadius(point.magnitude);
          const cid    = point.cluster_id ?? point.cluster_label;

          return (
            <CircleMarker
              key={point.id}
              center={[point.latitude, point.longitude]}
              radius={radius}
              pathOptions={{
                fillColor:   fill,
                fillOpacity: point.is_anomaly ? 0.95 : 0.72,
                color:       point.is_anomaly ? colors.anomaly : colors.border,
                weight:      point.is_anomaly ? 2 : 0.5,
              }}
            >
              <Popup>
                <div className="map-popup">
                  <p className="popup-place">
                    {point.place || "Unknown location"}
                  </p>
                  <div className="popup-stats">
                    <span>
                      <span className="popup-label">Mag</span>
                      {point.magnitude ?? "—"}
                    </span>
                    <span>
                      <span className="popup-label">Depth</span>
                      {point.depth ?? "—"} km
                    </span>
                    <span>
                      <span className="popup-label">Cluster</span>
                      {cid ?? "—"}
                    </span>
                  </div>
                  {point.is_anomaly && (
                    <p className="popup-anomaly">⚠ Anomaly detected</p>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      {/* ── Legend ────────────────────────────────────────────── */}
      <div className="map-legend">
        <p className="legend-title">Cluster Zones</p>
        {LEGEND_LABELS.map((label, i) => (
          <div key={i} className="legend-row">
            <span
              className="legend-dot"
              style={{ background: `var(--cluster-${i})` }}
            />
            <span className="legend-label">{label}</span>
          </div>
        ))}
        <div className="legend-row">
          <span
            className="legend-dot legend-dot--anomaly"
            style={{ background: `var(--color-accent-pink)` }}
          />
          <span className="legend-label">Anomaly</span>
        </div>
      </div>

      {data.length === 0 && (
        <div className="map-empty">
          <p>No data — run ETL then Training first</p>
        </div>
      )}
    </div>
  );
}
