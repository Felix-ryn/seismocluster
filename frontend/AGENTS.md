# AGENTS.md

## Project Overview
**SeismoCluster** — Earthquake Clustering Dashboard with real-time seismic monitoring,
geographic visualization, and cluster analytics. Modern startup aesthetic, LMS-style
collapsible sidebar, bright and energetic color palette.

Referensi desain: **Daroma Dashboard** — dark gradient sidebar, white content area,
colorful gradient stat cards, interactive Leaflet map, donut chart, event schedule.

---

## Tech Stack
- **Framework**: React 18 + Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios via `services/api.js`
- **Styling**: SCSS (App.scss) + CSS Variables (index.css)
- **Maps**: **Leaflet.js** (`react-leaflet`) — untuk plotting lat/lng titik gempa
- **Charts**: Recharts (bar, line, donut, scatter)
- **Icons**: Lucide React (`lucide-react`)

---

## Layout Architecture — Daroma LMS Style

```
┌──────────────────────────────────────────────────────────────┐
│  SIDEBAR (dark gradient)     │  TOPBAR (white, 58px)         │
│  200px, collapsible → 58px   │  Greeting · Search · Live     │
│  ────────────────────        │  ────────────────────────────  │
│  [☰] 🟣 SeismoCluster        │  CONTENT (bg: #F2F4FC)        │
│                              │                                │
│  ● Dashboard                 │  [StatCard][StatCard]          │
│  ○ Cluster Map               │  [StatCard][StatCard]          │
│  ○ Centroid                  │                                │
│  ○ Hotspot                   │  ┌──────────────┐ ┌────────┐  │
│  ○ Trend                     │  │  LEAFLET MAP │ │ Donut  │  │
│  ○ Anomaly      [● 3]        │  │  + Tabel     │ │ Chart  │  │
│  ○ Realtime     [● LIVE]     │  │  Koordinat   │ │────────│  │
│  ○ Movement                  │  └──────────────┘ │ Event  │  │
│                              │                    │ Hari   │  │
│  [Avatar] Admin BMKG         │                    │ Ini    │  │
│  Seismologist                │                    └────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Sidebar Rules
- Background: `linear-gradient(175deg, #0f0f28 0%, #1a1a35 55%, #1e1a40 100%)`
- Default: **expanded** (200px lebar) di desktop
- Tombol hamburger `☰` di pojok kiri atas sidebar untuk collapse/expand
- Hamburger: `background: rgba(124,58,237,.3); color: #a78bfa; border-radius: 7px`
- Collapsed state: hanya tampilkan icon (58px lebar)
- Di mobile (< 768px): sidebar jadi **overlay drawer** dengan backdrop blur
- Nav item default: `color: rgba(255,255,255,.45)`
- Nav item hover: `background: rgba(255,255,255,.07); color: rgba(255,255,255,.8)`
- Nav item **active**: `background: rgba(124,58,237,.28); color: #c4b5fd`
- Active icon: `color: #a78bfa`
- Logo icon box: `linear-gradient(135deg, #7C3AED, #6D28D9); border-radius: 7px`
- Footer: `border-top: 1px solid rgba(255,255,255,.07)`
- **Saat collapse, wajib panggil `map.invalidateSize()`** agar Leaflet re-render

### Topbar Rules
- Tinggi 58px, background `#ffffff`, sticky
- Border bottom: `1px solid #E4E8F2`
- Kiri: greeting — "Selamat Datang, [nama]" (font 15px, weight 700) + subtitle tanggal
- Tengah: search box (`background: #F2F4FC; border: 1.5px solid #E4E8F2`)
- Kanan: Live badge (hijau) → notif button → avatar circle (gradient purple)

---

## Color System — Dark Sidebar + Bright Content

Gunakan CSS variables berikut di `index.css`:

```css
:root {
  /* === SIDEBAR GRADIENT === */
  --sb-gradient:     linear-gradient(175deg, #0f0f28 0%, #1a1a35 55%, #1e1a40 100%);
  --sb-active-bg:    rgba(124, 58, 237, 0.28);
  --sb-active-color: #c4b5fd;
  --sb-icon-active:  #a78bfa;
  --sb-text:         rgba(255, 255, 255, 0.45);
  --sb-hover:        rgba(255, 255, 255, 0.07);
  --sidebar-width:   200px;
  --sidebar-collapsed: 58px;

  /* === BRAND / ACCENT === */
  --accent-primary:    #7C3AED;   /* Purple utama */
  --accent-light:      #EDE9FE;   /* Purple light bg */
  --accent-text:       #6D28D9;   /* Purple text */
  --accent-secondary:  #06B6D4;   /* Cyan */
  --accent-success:    #10B981;   /* Emerald */
  --accent-warning:    #F59E0B;   /* Amber */
  --accent-danger:     #EF4444;   /* Red */

  /* === STAT CARD GRADIENTS === */
  --card-purple:     linear-gradient(135deg, #7C3AED, #9333EA);
  --card-cyan:       linear-gradient(135deg, #0891B2, #06B6D4);
  --card-red:        linear-gradient(135deg, #DC2626, #EF4444);
  --card-green:      linear-gradient(135deg, #059669, #10B981);

  /* === SURFACES === */
  --bg-page:         #F2F4FC;   /* Background utama halaman */
  --bg-card:         #ffffff;   /* Card/panel */
  --bg-input:        #F2F4FC;   /* Search box, input */
  --border-card:     #E4E8F2;   /* Border card */
  --border-input:    #E4E8F2;   /* Border input */

  /* === TYPOGRAPHY === */
  --text-heading:    #12122a;
  --text-body:       #475569;
  --text-muted:      #94A3B8;
  --text-on-accent:  #FFFFFF;

  /* === CLUSTER COLORS (map markers, donut chart, badges) === */
  --cluster-0:         #7C3AED;   /* Ungu */
  --cluster-1:         #06B6D4;   /* Cyan */
  --cluster-2:         #10B981;   /* Hijau */
  --cluster-3:         #F59E0B;   /* Kuning */
  --cluster-4:         #EC4899;   /* Pink */
  --cluster-5:         #3B82F6;   /* Biru */
  --cluster-6:         #14B8A6;   /* Teal */
  --cluster-7:         #F97316;   /* Oranye */
  --cluster-anomaly:   #EF4444;   /* Merah — anomali */

  /* === MAGNITUDE BADGES === */
  --mag-lo-bg:   #DCFCE7;  --mag-lo-text: #166534;  /* < 3.0 SR */
  --mag-md-bg:   #FEF9C3;  --mag-md-text: #854D0E;  /* 3.0–5.0 SR */
  --mag-hi-bg:   #FEE2E2;  --mag-hi-text: #991B1B;  /* > 5.0 SR */

  /* === LIVE BADGE === */
  --live-bg:     #DCFCE7;
  --live-border: #86EFAC;
  --live-text:   #166534;
  --live-dot:    #16A34A;

  /* === EVENT ITEM BACKGROUNDS === */
  --ev-anomaly:  #FEE2E2;
  --ev-high:     #EDE9FE;
  --ev-normal:   #DCFCE7;
}
```

---

## Typography

```css
:root {
  --font-base:  'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono:  'Courier New', monospace;

  --text-xs:    0.75rem;
  --text-sm:    0.875rem;
  --text-base:  1rem;
  --text-lg:    1.125rem;
  --text-xl:    1.25rem;
  --text-2xl:   1.5rem;
  --text-3xl:   1.875rem;
}
```

Aturan:
- **Heading halaman**: `Segoe UI`, weight 700, 17px, color `var(--text-heading)`
- **Greeting (topbar)**: `Segoe UI`, weight 700, 15px
- **Stat card value**: `Segoe UI`, weight 700, 20–22px, color `#fff`
- **Stat card label**: 9px, weight 700, UPPERCASE, `letter-spacing: .07em`, `color: rgba(255,255,255,.65)`
- **Card title**: 12–13px, weight 700, color `var(--text-heading)`
- **Nav label**: 12px, weight 400, color `var(--sb-text)`
- **Nav label active**: 12px, weight 600, color `var(--sb-active-color)`
- **Koordinat/lat-lng**: `'Courier New', monospace`, 10–11px, color `var(--text-muted)`
- **Badge/tag**: 9px, weight 700, UPPERCASE, `letter-spacing: .05em`

**JANGAN gunakan**: Inter, Roboto, Space Grotesk, Nunito, Arial — terlalu generik.

---

## Component Patterns

### 1. Stat Card (KPI) — Gradient Background
```
┌──────────────────────────────────┐
│  [icon-box]  LABEL KECIL         │  ← uppercase, 9px, white 65%
│              1.247               │  ← angka besar, 20px, white, bold
│              ↑ 12% kemarin       │  ← trend text, white 60%
│                          (ring)  │  ← dekorasi lingkaran pojok kanan bawah
└──────────────────────────────────┘
```
- Background: salah satu dari `var(--card-purple/cyan/red/green)`
- Border radius: `12px`
- Padding: `13px 14px`
- Icon box: `38×38px`, `border-radius: 10px`, `background: rgba(255,255,255,.2)`
- Dekorasi ring: `position: absolute; right: -10px; bottom: -10px; 52×52px; border-radius: 50%; background: rgba(255,255,255,.08)`

### 2. Data Table (koordinat gempa)
- Header: `background: #F8FAFF`, font weight 700, uppercase, 9px
- Kolom: **Lokasi** | **Latitude** | **Longitude** | **Magnitude** | **Cluster**
- Lat/Lng: font `Courier New`, 10px
- Row hover: `background: #F8FAFF`
- Anomaly row: highlight merah

### 3. Magnitude Badge
```jsx
const getMagClass = (mag) =>
  mag >= 5 ? 'mag-hi' : mag >= 3 ? 'mag-md' : 'mag-lo';
```
- `mag-lo`: bg `#DCFCE7`, text `#166534`
- `mag-md`: bg `#FEF9C3`, text `#854D0E`
- `mag-hi`: bg `#FEE2E2`, text `#991B1B`

### 4. Cluster Badge
- Background: `var(--cluster-N)`, text `#fff`
- Border-radius: `4px`, padding: `2px 6px`, font 9px bold

### 5. Donut Chart (distribusi cluster)
- Library: Recharts `<PieChart>` + `<Pie innerRadius outerRadius>`
- Data: count per `cluster_id`
- Cell fill: `var(--cluster-N)` per item
- Tengah donut: total count (SVG `<text>`)
- Legend di samping: dot warna + label + angka count

### 6. Event Item (schedule card)
```
┌────────────────────────────────────────┐
│  [icon]  Anomali Laut Banda     09:14  │
│          Mag.6.0 · -4.50°/129.88°      │
└────────────────────────────────────────┘
```
- Background per severity: anomali=`#FEE2E2`, high=`#EDE9FE`, normal=`#DCFCE7`
- Icon box: `28×28px`, `border-radius: 7px`, `background: rgba(255,255,255,.7)`
- Border-radius item: `8px`, margin-bottom: `5px`

### 7. Bar Chart (frekuensi gempa)
- Library: Recharts `<BarChart>`
- Bar fill: `var(--accent-primary)` opacity `.55`, bar aktif opacity `1`
- Tooltip custom: `background: #1a1a35; color: #fff; border-radius: 8px`
- Axis label: 9px, `var(--text-muted)`, uppercase

---

## Map Component — SPEC LENGKAP

### Library & Setup
```bash
npm install leaflet react-leaflet
```

### Map.jsx Props
```typescript
interface MapProps {
  points:   EarthquakePoint[];  // array titik gempa dari API
  clusters?: ClusterSummary[];  // opsional: data centroid cluster
  height?:  string;             // default "480px"
  center?:  [number, number];   // default [-2, 118] (Indonesia)
  zoom?:    number;             // default 5
}
```

### Implementation Pattern
```jsx
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const CLUSTER_COLORS = {
  0: 'var(--cluster-0)',  // #7C3AED
  1: 'var(--cluster-1)',  // #06B6D4
  2: 'var(--cluster-2)',  // #10B981
  3: 'var(--cluster-3)',  // #F59E0B
  4: 'var(--cluster-4)',  // #EC4899
  5: 'var(--cluster-5)',  // #3B82F6
  6: 'var(--cluster-6)',  // #14B8A6
  7: 'var(--cluster-7)',  // #F97316
};
const ANOMALY_COLOR = 'var(--cluster-anomaly)';  // #EF4444

// Radius marker proporsional ke magnitude
const getRadius = (mag) => Math.min(6 + mag * 2, 18);

// Warna berdasarkan cluster_id atau anomali
const getColor = (point) =>
  point.is_anomaly ? ANOMALY_COLOR : (CLUSTER_COLORS[point.cluster_id] || '#7C3AED');
```

### Map Container Style
```css
.map-container {
  height: 480px;
  min-height: 300px;
  border-radius: 8px;
  border: 1.5px solid var(--border-card);
  overflow: hidden;
}
```

### CircleMarker Spec
Setiap `EarthquakePoint` dirender sebagai `L.circleMarker`:
```jsx
<CircleMarker
  center={[point.latitude, point.longitude]}
  radius={getRadius(point.magnitude)}
  pathOptions={{
    fillColor: getColor(point),
    color: '#ffffff',        // border putih
    weight: 2,               // border width
    fillOpacity: 0.85,
  }}
>
  <Popup>
    <PopupContent point={point} />
  </Popup>
</CircleMarker>
```

### Popup Content (wajib)
Popup saat klik marker harus menampilkan:
```
┌─────────────────────────────┐
│  Sulawesi Tengah            │  ← nama lokasi, 13px bold
│  Lat:  -1.230°              │  ← font Courier New
│  Lng: 120.450°              │  ← font Courier New
│  ─────────────────          │
│  [5.1 SR]  [Anomali]        │  ← magnitude badge + cluster badge
└─────────────────────────────┘
```

### Map Legend
Di bawah peta, tampilkan legend cluster:
```
● Cluster 0 (412)  ● Cluster 1 (308)  ● Cluster 2 (267)  ...  ● Anomali (7)
```
- Dot: `8×8px`, border-radius `50%`, warna sesuai cluster
- Font: 10px, color `var(--text-body)`

### Tile Layer
```jsx
<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
```

### PENTING: Sidebar Collapse
Saat sidebar toggle, Leaflet perlu recalculate size:
```jsx
useEffect(() => {
  setTimeout(() => {
    mapRef.current?.invalidateSize();
  }, 300); // tunggu CSS transition selesai
}, [collapsed]);
```

---

## Koordinat Table (di bawah peta)

Tampilkan tabel data titik gempa di bawah map:

```
┌─────────────┬───────────┬────────────┬───────────┬─────────┐
│ LOKASI      │ LATITUDE  │ LONGITUDE  │ MAGNITUDO │ CLUSTER │
├─────────────┼───────────┼────────────┼───────────┼─────────┤
│ Sulawesi T. │ -1.230°   │ 120.450°   │ [5.1 SR]  │ [Anoml] │
│ Maluku Utr. │  0.870°   │ 127.340°   │ [3.8 SR]  │ [CL-1]  │
│ Jawa Timur  │ -7.550°   │ 112.780°   │ [2.4 SR]  │ [CL-2]  │
└─────────────┴───────────┴────────────┴───────────┴─────────┘
```
- Header: bg `#F8FAFF`, font 9px bold uppercase
- Lat/Lng cell: font `Courier New, monospace`
- Magnitudo: pakai `MagBadge` component
- Cluster: pakai `ClusterBadge` component (warna sesuai cluster)

---

## Project Structure

```
src/
  components/
    Chart.jsx       — wrapper Recharts, props: { type, data, title, color }
    Map.jsx         — Leaflet map + CircleMarker + Popup (lihat spec di atas)
    Navbar.jsx      — SIDEBAR navigasi kiri, dark gradient, collapsible
    Topbar.jsx      — header atas, greeting + search + live badge  ← BUAT BARU
    StatCard.jsx    — KPI card gradient reusable                    ← BUAT BARU
    DonutChart.jsx  — cluster distribution donut (Recharts)         ← BUAT BARU
    MagBadge.jsx    — magnitude badge (lo/md/hi)                    ← BUAT BARU
    ClusterBadge.jsx — cluster ID badge berwarna                    ← BUAT BARU
    EventItem.jsx   — event card di panel kanan                     ← BUAT BARU
  pages/
    ClusterMap.jsx  — peta Leaflet + tabel koordinat + donut + event panel
    Centroid.jsx    — tabel + scatter plot centroid
    Hotspot.jsx     — heatmap area frekuensi tinggi
    Anomaly.jsx     — list anomali + highlight merah
    Movement.jsx    — time-lapse pergerakan seismik
    Realtime.jsx    — feed live data terbaru
    Trend.jsx       — line chart tren historis
  services/
    api.js          — semua API calls
  App.jsx           — layout wrapper: Sidebar + Topbar + <Outlet>
  App.scss          — global overrides
  index.css         — CSS variables (color tokens di sini)
  main.jsx
```

---

## App.jsx Layout Wrapper

```jsx
// Struktur wajib di App.jsx
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
import Topbar from './components/Topbar';

export default function App() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={`app-shell ${collapsed ? 'sb-collapsed' : ''}`}>
      <Navbar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
      <div className="main-area">
        <Topbar collapsed={collapsed} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
```

```scss
/* App.scss */
.app-shell {
  display: flex;
  min-height: 100vh;
  background: var(--bg-page);
  font-family: var(--font-base);
}
.main-area {
  flex: 1;
  margin-left: var(--sidebar-width);
  transition: margin-left 0.25s ease;
  display: flex;
  flex-direction: column;
}
.app-shell.sb-collapsed .main-area {
  margin-left: var(--sidebar-collapsed);
}
.page-content {
  flex: 1;
  padding: 18px 22px;
}
```

---

## ClusterMap.jsx — Layout Halaman Utama

```
┌───────────────────────────────────────────────────┐
│ [StatCard 1] [StatCard 2] [StatCard 3] [StatCard 4]│  ← grid 4 kolom
├──────────────────────────────┬────────────────────┤
│                              │  Distribusi Cluster │
│      LEAFLET MAP             │  [Donut Chart]      │
│      (CircleMarkers)         │  [Legend]           │
│                              ├────────────────────┤
│      [Map Legend]            │  Event Hari Ini     │
│      [Tabel Koordinat]      │  [Date Strip]       │
│                              │  [EventItem 1]     │
│                              │  [EventItem 2]     │
│                              │  [EventItem 3]     │
└──────────────────────────────┴────────────────────┘
```

Grid layout: `grid-template-columns: 1fr 250px`

---

## Routing (React Router v6)

```jsx
// main.jsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<App />}>
      <Route index element={<ClusterMap />} />
      <Route path="centroid" element={<Centroid />} />
      <Route path="hotspot" element={<Hotspot />} />
      <Route path="anomaly" element={<Anomaly />} />
      <Route path="trend" element={<Trend />} />
      <Route path="realtime" element={<Realtime />} />
      <Route path="movement" element={<Movement />} />
    </Route>
  </Routes>
</BrowserRouter>
```

---

## Data Shape (dari api.js)

```js
// Earthquake data point
{
  id:         string,
  latitude:   number,       // contoh: -1.23
  longitude:  number,       // contoh: 120.45
  magnitude:  number,       // skala Richter
  depth:      number,       // kedalaman dalam km
  timestamp:  string,       // ISO 8601
  cluster_id: number,       // 0-7, mapping ke --cluster-N
  is_anomaly: boolean,
  location:   string        // nama wilayah (opsional)
}

// Cluster summary
{
  cluster_id:    number,
  centroid_lat:  number,
  centroid_lng:  number,
  count:         number,
  avg_magnitude: number,
  radius_km:     number
}
```

---

## Navbar.jsx — Nav Items

```js
const NAV_ITEMS = [
  { path: '/',          icon: LayoutDashboardIcon, label: 'Dashboard'   },
  { path: '/cluster',   icon: MapIcon,             label: 'Cluster Map' },
  { path: '/centroid',  icon: FocusIcon,           label: 'Centroid'    },
  { path: '/hotspot',   icon: FlameIcon,           label: 'Hotspot'     },
  { path: '/trend',     icon: TrendingUpIcon,      label: 'Trend'       },
  { path: '/anomaly',   icon: AlertTriangleIcon,   label: 'Anomaly',    badge: anomalyCount, badgeType: 'danger' },
  { path: '/realtime',  icon: ActivityIcon,         label: 'Realtime',   badge: 'LIVE', badgeType: 'success' },
  { path: '/movement',  icon: WavesIcon,           label: 'Movement'    },
];
```

---

## DO NOT
- Jangan hapus atau rename file yang sudah ada
- Jangan install library baru tanpa konfirmasi user (kecuali leaflet, react-leaflet, recharts, lucide-react)
- Jangan hardcode warna — WAJIB pakai `var(--token-name)`
- Jangan pakai font Inter, Roboto, Space Grotesk, Nunito, Arial
- Jangan buat light/dark toggle — hanya light mode
- Jangan pakai inline style untuk warna kecuali gradient card
- Jangan ubah struktur `services/api.js`
- Jangan gunakan `!important` dalam CSS
- Saat sidebar toggle, **wajib panggil `map.invalidateSize()`** agar Leaflet resize
- Jangan pakai `localStorage` atau `sessionStorage`