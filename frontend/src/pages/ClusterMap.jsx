import { useEffect, useState } from "react";
import { getClusters } from "../services/api";
import Map from "../components/Map";

export default function ClusterMap() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getClusters().then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Cluster Map</h1>
      <Map data={data} />
    </div>
  );
}