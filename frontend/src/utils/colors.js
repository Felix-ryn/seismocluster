// Hex values matching AGENTS.md CSS variable tokens (recharts needs actual hex, not var())
export const CLUSTER_COLORS = [
  '#7C3AED', // --cluster-0 purple
  '#06B6D4', // --cluster-1 cyan
  '#10B981', // --cluster-2 emerald
  '#F59E0B', // --cluster-3 amber
  '#EC4899', // --cluster-4 pink
  '#3B82F6', // --cluster-5 blue
  '#14B8A6', // --cluster-6 teal
  '#F97316', // --cluster-7 orange
];

export const ANOMALY_COLOR = '#EF4444'; // --cluster-anomaly

export const clusterColor = (id) =>
  CLUSTER_COLORS[Math.abs(id ?? 0) % CLUSTER_COLORS.length];
