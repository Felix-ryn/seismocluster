export default function MagBadge({ magnitude }) {
  const mag = parseFloat(magnitude) || 0;
  const tier = mag >= 5 ? "hi" : mag >= 3 ? "md" : "lo";
  return (
    <span className={`mag-badge mag-badge--${tier}`}>
      {magnitude != null ? `${Number(magnitude).toFixed(1)} SR` : "—"}
    </span>
  );
}
