import { CLUSTER_COLORS } from "../utils/colors";

export default function ClusterBadge({ clusterId }) {
  if (clusterId === null || clusterId === undefined) {
    return <span className="cluster-badge cluster-badge--noise">Noise</span>;
  }
  const color = CLUSTER_COLORS[Math.abs(clusterId) % CLUSTER_COLORS.length];
  return (
    <span className="cluster-badge" style={{ background: color }}>
      CL-{clusterId}
    </span>
  );
}
