import { useEffect, useState } from "react";
import { getClusterResults } from "../services/api";
import Map from "../components/Map";

export default function ClusterMap() {
  const [data, setData]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    getClusterResults(500)
      .then((res) => setData(res.data.data ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1>Cluster Map</h1>
      {loading && <p>Loading cluster data…</p>}
      {error   && <p style={{ color: "var(--color-accent-pink)" }}>Error: {error}</p>}
      <Map data={data} />
    </div>
  );
}
