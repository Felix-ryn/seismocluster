import { useEffect, useState } from "react";
import { getSummary } from "../services/api";
import Chart from "../components/Chart";

export default function Hotspot() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getSummary().then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Hotspot</h1>
      <Chart data={data} />
    </div>
  );
}