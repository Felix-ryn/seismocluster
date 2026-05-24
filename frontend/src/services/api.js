import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

// ── Earthquake CRUD ──────────────────────────────────────────
export const getEarthquakes = (limit = 500, offset = 0, indonesiaOnly = false) =>
  API.get(`/api/v1/earthquakes/?limit=${limit}&offset=${offset}&indonesia_only=${indonesiaOnly}`);

export const getEarthquakeById = (id) =>
  API.get(`/api/v1/earthquakes/${id}`);

// ── Clustering ───────────────────────────────────────────────
export const runETL = () =>
  API.post("/api/v1/clusters/etl");

export const runTraining = () =>
  API.post("/api/v1/clusters/train");

export const getClusterResults = (limit = 500, offset = 0) =>
  API.get(`/api/v1/clusters/results?limit=${limit}&offset=${offset}`);

export const getAnomalies = (limit = 200) =>
  API.get(`/api/v1/clusters/anomalies?limit=${limit}`);

// ── Summary ──────────────────────────────────────────────────
export const getSummary = () =>
  API.get("/api/v1/summary/");

export const getSummaryStats = () =>
  API.get("/api/v1/summary/stats");

// ── Hierarchy ─────────────────────────────────────────────────
export const getHierarchySummary = () =>
  API.get("/api/v1/clusters/hierarchy/summary");
