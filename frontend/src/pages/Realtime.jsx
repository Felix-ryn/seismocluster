import { useEffect, useState } from "react";
import { getEarthquakes } from "../services/api";

export default function Realtime() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      getEarthquakes().then(res => setData(res.data));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Realtime Data</h1>
      {data.slice(0, 10).map((d, i) => (
        <p key={i}>{d.lat} - {d.lon}</p>
      ))}
    </div>
  );
}