import { useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import MagBadge from "./MagBadge";
import ClusterBadge from "./ClusterBadge";

const cssVar = (name) =>
  getComputedStyle(document.documentElement).getPropertyValue(name).trim();

const clusterIndex = (clusterId) => ((clusterId % 8) + 8) % 8;

function createCircleIcon(color, radius) {
  const size = Math.round(radius * 2);
  return L.divIcon({
    html: `<div style="
      width:${size}px;
      height:${size}px;
      border-radius:50%;
      background:${color};
      opacity:0.85;
      border:1.5px solid rgba(255,255,255,0.8);
      box-sizing:border-box;
    "></div>`,
    className: "",
    iconSize: [size, size],
    iconAnchor: [radius, radius],
  });
}

export default function Map({ data = [] }) {
  const colors = useMemo(() => ({
    clusters: [0, 1, 2, 3, 4, 5, 6, 7].map((i) => cssVar(`--cluster-${i}`)),
    anomaly: cssVar("--cluster-anomaly"),
    unknown: cssVar("--text-muted"),
  }), []);

  function getColor(point) {
    if (point.is_anomaly) return colors.anomaly;
    const cid = point.cluster_id ?? point.cluster_label;
    if (cid === null || cid === undefined) return colors.unknown;
    return colors.clusters[clusterIndex(cid)];
  }

  function getRadius(magnitude) {
    if (!magnitude) return 5;
    return Math.max(4, Math.min(18, 6 + magnitude * 2));
  }

  const legendData = useMemo(() => {
    const clusterCounts = {};
    let anomalyCount = 0;
    data.forEach((p) => {
      if (p.is_anomaly) {
        anomalyCount++;
      } else {
        const cid = p.cluster_id ?? p.cluster_label;
        if (cid !== null && cid !== undefined) {
          clusterCounts[cid] = (clusterCounts[cid] || 0) + 1;
        }
      }
    });
    return { clusterCounts, anomalyCount };
  }, [data]);

  return (
    <>
      <div className="map-wrapper">
        <MapContainer
          center={[-2.5, 118.0]}
          zoom={5}
          style={{ height: "100%", width: "100%" }}
          scrollWheelZoom
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
            maxZoom={19}
          />

          <MarkerClusterGroup
            chunkedLoading
            maxClusterRadius={60}
            showCoverageOnHover={false}
          >
            {data.map((point) => {
              const fill = getColor(point);
              const radius = getRadius(point.magnitude);
              const cid = point.cluster_id ?? point.cluster_label;

              return (
                <Marker
                  key={point.id}
                  position={[point.latitude, point.longitude]}
                  icon={createCircleIcon(fill, radius)}
                >
                  <Popup>
                    <div className="map-popup">
                      <p className="popup-place">{point.place || "Unknown location"}</p>
                      <div className="popup-coords">
                        <span>Lat: <span className="popup-coord">{point.latitude?.toFixed(3)}°</span></span>
                        <span>Lng: <span className="popup-coord">{point.longitude?.toFixed(3)}°</span></span>
                      </div>
                      <hr className="popup-divider" />
                      <div className="popup-badges">
                        <MagBadge magnitude={point.magnitude} />
                        <ClusterBadge clusterId={cid} />
                        {point.is_anomaly && (
                          <span className="popup-anomaly-badge">Anomali</span>
                        )}
                      </div>
                      {point.depth != null && (
                        <div className="popup-depth">Kedalaman: {point.depth} km</div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MarkerClusterGroup>
        </MapContainer>

        {data.length === 0 && (
          <div className="map-empty">
            <p>Belum ada data — jalankan ETL dan Training terlebih dahulu</p>
          </div>
        )}
      </div>

      {data.length > 0 && (
        <div className="map-legend-bar">
          {Object.entries(legendData.clusterCounts).map(([cid, count]) => (
            <div key={cid} className="map-legend-bar-item">
              <span
                className="map-legend-bar-dot"
                style={{ background: colors.clusters[clusterIndex(parseInt(cid))] }}
              />
              <span>Cluster {cid} ({count})</span>
            </div>
          ))}
          {legendData.anomalyCount > 0 && (
            <div className="map-legend-bar-item">
              <span className="map-legend-bar-dot" style={{ background: colors.anomaly }} />
              <span>Anomali ({legendData.anomalyCount})</span>
            </div>
          )}
        </div>
      )}
    </>
  );
}