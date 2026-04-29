import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <Link to="/">Cluster</Link> |
      <Link to="/hotspot">Hotspot</Link> |
      <Link to="/centroid">Centroid</Link> |
      <Link to="/movement">Movement</Link> |
      <Link to="/anomaly">Anomaly</Link> |
      <Link to="/trend">Trend</Link> |
      <Link to="/realtime">Realtime</Link>
    </nav>
  );
}