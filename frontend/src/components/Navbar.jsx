import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Crosshair,
  Flame,
  TrendingUp,
  AlertTriangle,
  Activity,
  Waves,
  Menu,
} from "lucide-react";

const NAV_ITEMS = [
  { path: "/dashboard",          icon: LayoutDashboard, label: "Dashboard",  end: true                               },
  { path: "/dashboard/centroid", icon: Crosshair,       label: "Centroid"                                            },
  { path: "/dashboard/hotspot",  icon: Flame,           label: "Hotspot"                                             },
  { path: "/dashboard/trend",    icon: TrendingUp,      label: "Trend"                                               },
  { path: "/dashboard/anomaly",  icon: AlertTriangle,   label: "Anomaly",   badge: null,   badgeType: "danger"       },
  { path: "/dashboard/realtime", icon: Activity,        label: "Realtime",  badge: "LIVE", badgeType: "success"      },
  { path: "/dashboard/movement", icon: Waves,           label: "Movement"                                            },
];

export default function Navbar({ collapsed, onToggle, anomalyCount = 0 }) {
  const navItems = NAV_ITEMS.map((item) =>
    item.path === "/anomaly" && anomalyCount > 0
      ? { ...item, badge: String(anomalyCount) }
      : item
  );

  return (
    <aside className={`sidebar${collapsed ? " sidebar--collapsed" : ""}`}>
      <div className={`sidebar-header${collapsed ? " sidebar-header--collapsed" : ""}`}>
        <button className="sidebar-hamburger" onClick={onToggle} aria-label="Toggle sidebar">
          <Menu size={17} />
        </button>
        {!collapsed && (
          <div className="sidebar-brand">
            <span className="sidebar-brand-icon">S</span>
            <span className="sidebar-brand-name">SeismoCluster</span>
          </div>
        )}
      </div>

      <nav className="sidebar-nav">
        {navItems.map(({ path, icon: Icon, label, end, badge, badgeType }) => (
          <NavLink
            key={path}
            to={path}
            end={end}
            className={({ isActive }) =>
              `sidebar-nav-link${isActive ? " active" : ""}${collapsed ? " sidebar-nav-link--collapsed" : ""}`
            }
          >
            <Icon size={18} className="sidebar-nav-icon" />
            {!collapsed && <span className="sidebar-nav-label">{label}</span>}
            {!collapsed && badge && (
              <span className={`sidebar-badge sidebar-badge--${badgeType}`}>{badge}</span>
            )}
          </NavLink>
        ))}
      </nav>

      <div className={`sidebar-footer${collapsed ? " sidebar-footer--collapsed" : ""}`}>
        <div className="sidebar-avatar">A</div>
        {!collapsed && (
          <div className="sidebar-user-info">
            <div className="sidebar-username">Admin BMKG</div>
            <div className="sidebar-role">Seismologist</div>
          </div>
        )}
      </div>
    </aside>
  );
}
