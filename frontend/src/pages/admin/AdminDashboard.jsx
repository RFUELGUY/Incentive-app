import React, { useState } from "react";
import Sidebar from "./Sidebar";
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

const AdminDashboard = () => {
  const [activeSection, setActiveSection] = useState("dashboard");
  const [refreshKey, setRefreshKey] = useState(0);

  const renderSection = () => {
    switch (activeSection) {
      case "outlets": return <OutletManager key={refreshKey} />;
      case "pending": return <PendingSalesmen key={refreshKey} />;
      case "users": return <UserManager key={refreshKey} />;
      case "upload": return <BaseUpload key={refreshKey} />;
      case "products": return <ProductManager key={refreshKey} />;
      case "sales": return <SalesUpload key={refreshKey} />;
      case "claims": return <ClaimDashboard key={refreshKey} />;
      case "incentives": return <IncentiveControl key={refreshKey} />;
      case "streaks": return <Streaks key={refreshKey} />;
      case "leaderboard": return <Leaderboard key={refreshKey} />;
      case "traits": return <TraitsConfig key={refreshKey} />;
      case "setup": return <SetupPanel key={refreshKey} />;
      default:
        return (
          <div className="text-xl font-semibold">
            Welcome to Admin Dashboard
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar activeSection={activeSection} setActiveSection={setActiveSection} />
      <div className="flex-1 p-4 overflow-y-auto">
        {renderSection()}
      </div>
    </div>
  );
};

export default AdminDashboard;
