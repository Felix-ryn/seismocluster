export default function Chart({ data }) {
  return (
    <div>
      <h3>Chart</h3>
      {data.map((d, i) => (
        <p key={i}>
          Cluster {d.cluster} → {d.total}
        </p>
      ))}
    </div>
  );
}