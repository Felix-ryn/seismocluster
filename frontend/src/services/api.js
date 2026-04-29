import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getClusters = () => API.get("/clusters");
export const runClustering = () => API.post("/clusters/run");
export const getSummary = () => API.get("/summary");
export const getEarthquakes = () => API.get("/earthquakes");