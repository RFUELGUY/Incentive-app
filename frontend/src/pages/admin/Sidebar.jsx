import React from "react";

const Sidebar = ({ activeSection, setActiveSection }) => {
  const navItems = [
    { key: "dashboard", label: "Dashboard" },
    { key: "outlets", label: "Outlets" },
    { key: "pending", label: "Approvals" },
    { key: "users", label: "Manage Users" },
    { key: "upload", label: "Upload Products" },
    { key: "products", label: "Product Manager" },
    { key: "sales", label: "Sales Upload" },
    { key: "claims", label: "Claims" },
    { key: "incentives", label: "Incentives" },
    { key: "streaks", label: "Streaks" },
    { key: "leaderboard", label: "Leaderboard" },
    { key: "traits", label: "Trait Config" },
    { key: "setup", label: "Setup Panel" },
  ];

  return (
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
  );
};

export default Sidebar;
