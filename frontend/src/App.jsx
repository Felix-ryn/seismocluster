import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import ClusterMap from "./pages/ClusterMap";
import Hotspot from "./pages/Hotspot";
import Centroid from "./pages/Centroid";
import Movement from "./pages/Movement";
import Anomaly from "./pages/Anomaly";
import Trend from "./pages/Trend";
import Realtime from "./pages/Realtime";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<ClusterMap />} />
        <Route path="/hotspot" element={<Hotspot />} />
        <Route path="/centroid" element={<Centroid />} />
        <Route path="/movement" element={<Movement />} />
        <Route path="/anomaly" element={<Anomaly />} />
        <Route path="/trend" element={<Trend />} />
        <Route path="/realtime" element={<Realtime />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;