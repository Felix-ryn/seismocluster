import { useState, useEffect, createContext, useContext } from "react";
import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";
import Navbar from "./components/Navbar";
import Topbar from "./components/Topbar";
import ClusterMap from "./pages/ClusterMap";
import Hotspot from "./pages/Hotspot";
import Centroid from "./pages/Centroid";
import Movement from "./pages/Movement";
import Anomaly from "./pages/Anomaly";
import Trend from "./pages/Trend";
import Realtime from "./pages/Realtime";
import Hierarchy from "./pages/Hierarchy";
import Landing from "./pages/Landing";
import "./App.scss";

export const SearchContext = createContext({ query: "", setQuery: () => {} });

export function useSearch() {
  return useContext(SearchContext);
}

function AppShell() {
  const [collapsed, setCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const t = setTimeout(() => window.dispatchEvent(new Event("resize")), 300);
    return () => clearTimeout(t);
  }, [collapsed]);

  return (
    <SearchContext.Provider value={{ query: searchQuery, setQuery: setSearchQuery }}>
      <div className={`app-shell${collapsed ? " sb-collapsed" : ""}`}>
        <Navbar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
        <div className="main-area">
          <Topbar />
          <main className="page-content">
            <Outlet />
          </main>
        </div>
      </div>
    </SearchContext.Provider>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<AppShell />}>
          <Route index element={<ClusterMap />} />
          <Route path="hotspot" element={<Hotspot />} />
          <Route path="centroid" element={<Centroid />} />
          <Route path="movement" element={<Movement />} />
          <Route path="anomaly" element={<Anomaly />} />
          <Route path="trend" element={<Trend />} />
          <Route path="realtime" element={<Realtime />} />
          <Route path="hierarchy" element={<Hierarchy />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}