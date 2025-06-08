import { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../../config";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";

export default function SetupPanel() {
  const [setupComplete, setSetupComplete] = useState(null);
  const [outletName, setOutletName] = useState("");
  const [verticleName, setVerticleName] = useState("");
  const [verticleDesc, setVerticleDesc] = useState("");
  const [outlets, setOutlets] = useState([]);
  const [verticles, setVerticles] = useState([]);

  const token = localStorage.getItem("token");

  useEffect(() => {
    checkSetupStatus();
    fetchOutlets();
    fetchVerticles();
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

  const fetchVerticles = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/admin/verticles`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setVerticles(res.data);
    } catch (err) {
      console.error("Failed to fetch verticles", err);
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

  const handleAddVerticle = async () => {
    if (!verticleName.trim()) return alert("Enter verticle name.");
    const exists = verticles.some(
      (v) => v.name.toLowerCase() === verticleName.trim().toLowerCase()
    );
    if (exists) {
      alert("A verticle with this name already exists.");
      return;
    }

    try {
      await axios.post(
        `${API_BASE_URL}/api/admin/verticles`,
        {
          name: verticleName.trim(),
          description: verticleDesc.trim(),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setVerticleName("");
      setVerticleDesc("");
      fetchVerticles();
    } catch (err) {
      console.error("Verticle creation failed", err);
    }
  };

  const handleEditVerticle = async (id, currentName, currentDesc) => {
    const newName = prompt("Edit verticle name:", currentName);
    if (!newName || newName.trim() === "") return;

    const duplicate = verticles.some(
      (v) => v.name.toLowerCase() === newName.toLowerCase() && v.id !== id
    );
    if (duplicate) {
      alert("A verticle with this name already exists.");
      return;
    }

    const newDesc = prompt("Edit description (optional):", currentDesc || "");

    try {
      await axios.put(
        `${API_BASE_URL}/api/admin/verticles/${id}`,
        {
          name: newName.trim(),
          description: newDesc.trim(),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      fetchVerticles();
    } catch (err) {
      console.error("Verticle update failed", err);
    }
  };

  const handleDeleteVerticle = async (id) => {
    if (!window.confirm("Are you sure you want to delete this verticle?")) return;
    try {
      await axios.delete(`${API_BASE_URL}/api/admin/verticles/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchVerticles();
    } catch (err) {
      console.error("Verticle deletion failed", err);
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

      {/* Verticle Setup */}
      <div>
        <h3 className="font-semibold mb-2">📦 Verticles</h3>
        <div className="flex gap-2 flex-wrap">
          <Input
            placeholder="Verticle name"
            value={verticleName}
            onChange={(e) => setVerticleName(e.target.value)}
          />
          <Input
            placeholder="Description (optional)"
            value={verticleDesc}
            onChange={(e) => setVerticleDesc(e.target.value)}
          />
          <Button onClick={handleAddVerticle}>Add</Button>
        </div>
        <ul className="text-sm mt-2 list-disc ml-6 space-y-1">
          {verticles.map((v) => (
            <li key={v.id} className="flex justify-between items-center">
              <span>
                <strong>{v.name}</strong>
                {v.description && ` – ${v.description}`}
              </span>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={() => handleEditVerticle(v.id, v.name, v.description)}
                >
                  ✏️
                </Button>
                <Button size="sm" variant="danger" onClick={() => handleDeleteVerticle(v.id)}>
                  ❌
                </Button>
              </div>
            </li>
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
