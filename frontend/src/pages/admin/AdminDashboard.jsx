import React, { useState, useEffect } from "react";
import OutletManager from "./OutletManager";
import PendingSalesmen from "./PendingSalesmen";
import UserManager from "./UserManager";
import BaseUpload from "./BaseUpload";
import ProductManager from "./ProductManager";
import SalesUpload from "./SalesUpload";
import ClaimDashboard from "./ClaimDashboard";
import IncentiveControl from "./IncentiveControl";
import Streaks from "./Streaks";
import Leaderboard from "./Leaderboard";
import TraitsConfig from "./TraitsConfig";
import SetupPanel from "./SetupPanel";
// import socket from "@/utils/socket"; // to be implemented

const AdminDashboard = () => {
  const [activeSection, setActiveSection] = useState("dashboard");
  const [refreshKey, setRefreshKey] = useState(0);

  // Optional: WebSocket auto-refresh logic
  // useEffect(() => {
  //   socket.on("data-update", () => {
  //     setRefreshKey(prev => prev + 1);
  //   });
  //   return () => socket.off("data-update");
  // }, []);

  const renderSection = () => {
    const props = { key: refreshKey };

    switch (activeSection) {
      case "outlets": return <OutletManager {...props} />;
      case "pending": return <PendingSalesmen {...props} />;
      case "users": return <UserManager {...props} />;
      case "upload": return <BaseUpload {...props} />;
      case "products": return <ProductManager {...props} />;
      case "sales": return <SalesUpload {...props} />;
      case "claims": return <ClaimDashboard {...props} />;
      case "incentives": return <IncentiveControl {...props} />;
      case "streaks": return <Streaks {...props} />;
      case "leaderboard": return <Leaderboard {...props} />;
      case "traits": return <TraitsConfig {...props} />;
      case "setup": return <SetupPanel {...props} />;
      default:
        return <div className="text-xl font-semibold">Welcome to Admin Dashboard</div>;
    }
  };

  const navItems = [
    { key: "dashboard", label: "🏠 Dashboard" },
    { key: "outlets", label: "🏪 Outlets" },
    { key: "pending", label: "👤 Approvals" },
    { key: "users", label: "👥 Manage Users" },
    { key: "upload", label: "📤 Upload Products" },
    { key: "products", label: "📦 Product Manager" },
    { key: "sales", label: "🧾 Sales Upload" },
    { key: "claims", label: "📬 Claims" },
    { key: "incentives", label: "🎯 Incentives" },
    { key: "streaks", label: "🔥 Streaks" },
    { key: "leaderboard", label: "🏆 Leaderboard" },
    { key: "traits", label: "⚙️ Trait Config" },
    { key: "setup", label: "🧰 Setup Panel" },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-gray-100 border-r overflow-y-auto p-4 sticky top-0 h-full">
        <h2 className="text-lg font-bold mb-4">Admin Menu</h2>
        <div className="flex flex-col gap-2">
          {navItems.map(item => (
            <span
              key={item.key}
              onClick={() => setActiveSection(item.key)}
              className={`cursor-pointer px-2 py-1 rounded hover:bg-gray-200 ${
                activeSection === item.key ? "bg-gray-300 font-semibold" : ""
              }`}
            >
              {item.label}
            </span>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-4 overflow-y-auto">
        {renderSection()}
      </div>
    </div>
  );
};

export default AdminDashboard;
