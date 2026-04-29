export default function Map({ data }) {
  return (
    <div>
      <h3>Map (Dummy View)</h3>
      {data.slice(0, 10).map((d, i) => (
        <p key={i}>
          {d.lat}, {d.lon} → Cluster {d.cluster}
        </p>
      ))}
    </div>
  );
}