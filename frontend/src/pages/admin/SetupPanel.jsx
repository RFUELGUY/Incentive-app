import { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../../config";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

export default function SetupPanel() {
  const [setupComplete, setSetupComplete] = useState(null);
  const [outletName, setOutletName] = useState("");
  const [categoryName, setCategoryName] = useState("");
  const [outlets, setOutlets] = useState([]);
  const [categories, setCategories] = useState([]);

  const token = localStorage.getItem("token");

  useEffect(() => {
    checkSetupStatus();
    fetchOutlets();
    fetchCategories();
  }, []);

  const checkSetupStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/admin/setup/status`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSetupComplete(res.data.setup_complete);
    } catch (err) {
      console.error("Failed to check setup status", err);
    }
  };

  const fetchOutlets = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/admin/outlets`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setOutlets(res.data);
    } catch (err) {
      console.error("Failed to fetch outlets", err);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/admin/categories`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCategories(res.data);
    } catch (err) {
      console.error("Failed to fetch categories", err);
    }
  };

  const handleAddOutlet = async () => {
    if (!outletName.trim()) return alert("Enter outlet name.");
    try {
      await axios.post(
        `${API_BASE_URL}/api/admin/outlets`,
        { name: outletName },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setOutletName("");
      fetchOutlets();
    } catch (err) {
      console.error("Outlet creation failed", err);
    }
  };

  const handleAddCategory = async () => {
    if (!categoryName.trim()) return alert("Enter category name.");
    try {
      await axios.post(
        `${API_BASE_URL}/api/admin/categories`,
        { name: categoryName },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setCategoryName("");
      fetchCategories();
    } catch (err) {
      console.error("Category creation failed", err);
    }
  };

  const markSetupDone = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/api/admin/setup/complete`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setSetupComplete(true);
      alert("Setup complete.");
    } catch (err) {
      console.error("Failed to mark setup complete", err);
    }
  };

  if (setupComplete) return null;

  return (
    <div className="border rounded p-6 space-y-6 shadow bg-white">
      <h2 className="text-xl font-bold">🔧 Initial Setup</h2>

      {/* Outlet Setup */}
      <div>
        <h3 className="font-semibold mb-2">📍 Outlets</h3>
        <div className="flex gap-2">
          <Input
            placeholder="Outlet name"
            value={outletName}
            onChange={(e) => setOutletName(e.target.value)}
          />
          <Button onClick={handleAddOutlet}>Add</Button>
        </div>
        <ul className="text-sm mt-2 list-disc ml-6">
          {outlets.map((o) => (
            <li key={o.id}>{o.name}</li>
          ))}
        </ul>
      </div>

      {/* Category Setup */}
      <div>
        <h3 className="font-semibold mb-2">🏷️ Categories / Verticals</h3>
        <div className="flex gap-2">
          <Input
            placeholder="Category name"
            value={categoryName}
            onChange={(e) => setCategoryName(e.target.value)}
          />
          <Button onClick={handleAddCategory}>Add</Button>
        </div>
        <ul className="text-sm mt-2 list-disc ml-6">
          {categories.map((c) => (
            <li key={c.id}>{c.name}</li>
          ))}
        </ul>
      </div>

      <div className="pt-4">
        <Button onClick={markSetupDone} full>
          ✅ Mark Setup Complete
        </Button>
      </div>
    </div>
  );
}

