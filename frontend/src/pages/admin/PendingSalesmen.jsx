import { useEffect, useState } from "react";
import axios from "axios";
import Button from "../../components/ui/Button";
import API_BASE_URL from "../../config";

export default function PendingSalesmen() {
  const [pendingSalesmen, setPendingSalesmen] = useState([]);

  const fetchPendingSalesmen = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(`${API_BASE_URL}/api/auth/pending`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPendingSalesmen(res.data);
    } catch (err) {
      console.error("Failed to fetch pending signups", err);
    }
  };

  const handleApprove = async (salesmanId) => {
    const category = prompt("Enter category (FMCG / Grocery / Hyper):");
    const outlet = prompt("Enter outlet:");
    const password = prompt("Set initial password:");

    if (!category || !outlet || !password) return alert("All fields required.");

    try {
      const token = localStorage.getItem("token");
      await axios.post(
        `${API_BASE_URL}/api/auth/approve/${salesmanId}`,
        { category, outlet, password },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Salesman approved");
      fetchPendingSalesmen();
    } catch (err) {
      console.error("Approval failed", err);
      alert("Failed to approve");
    }
  };

  useEffect(() => {
    fetchPendingSalesmen();
  }, []);

  return (
    <section className="border p-4 rounded shadow">
      <h2 className="text-lg font-bold mb-4">🕐 Pending Signups</h2>
      {pendingSalesmen.length === 0 ? (
        <p className="text-gray-500">No pending signups.</p>
      ) : (
        <ul className="space-y-3">
          {pendingSalesmen.map((s) => (
            <li
              key={s.id}
              className="flex justify-between items-center border p-2 rounded"
            >
              <div>
                <p className="font-medium">{s.name}</p>
                <p className="text-sm text-gray-600">📞 {s.mobile}</p>
              </div>
              <Button onClick={() => handleApprove(s.id)}>Approve</Button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
