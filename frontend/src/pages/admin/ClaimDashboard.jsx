import { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../../config";
import Button from "../../components/ui/Button";
import Input from "../../components/ui/Input";

export default function ClaimDashboard() {
  const [claims, setClaims] = useState([]);
  const [amendMap, setAmendMap] = useState({});
  const [editAmountId, setEditAmountId] = useState(null);
  const [editedAmount, setEditedAmount] = useState("");
  const [view, setView] = useState("pending"); // "pending" or "all"

  const token = localStorage.getItem("token");

  const fetchClaims = async () => {
    try {
      const endpoint =
        view === "pending" ? "/api/claims/pending" : "/api/claims";
      const res = await axios.get(`${API_BASE_URL}${endpoint}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setClaims(res.data);
    } catch (err) {
      console.error("Failed to load claims", err);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, [view]);

  const handleApprove = async (id) => {
    try {
      await axios.post(`${API_BASE_URL}/api/claims/approve/${id}`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchClaims();
    } catch (err) {
      alert("Approval failed");
    }
  };

  const handleReject = async (id) => {
    try {
      await axios.post(`${API_BASE_URL}/api/claims/reject/${id}`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchClaims();
    } catch (err) {
      alert("Rejection failed");
    }
  };

  const handleAmendRemarks = async (id) => {
    const newRemarks = amendMap[id];
    if (!newRemarks?.trim()) return alert("Remarks cannot be empty.");
    try {
      await axios.post(
        `${API_BASE_URL}/api/claims/amend/${id}`,
        { new_remarks: newRemarks },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchClaims();
    } catch (err) {
      alert("Amendment failed");
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">📄 {view === "pending" ? "Pending Claims" : "All Claims"}</h2>
        <Button onClick={() => setView(view === "pending" ? "all" : "pending")}>
          View {view === "pending" ? "All" : "Pending"} Claims
        </Button>
      </div>

      {claims.length === 0 ? (
        <p className="text-sm text-gray-600">No claims found.</p>
      ) : (
        <ul className="space-y-4">
          {claims.map((claim) => (
            <li
              key={claim.id}
              className="border p-4 rounded shadow flex flex-col gap-2"
            >
              <div className="flex justify-between flex-wrap">
                <div>
                  <p className="font-semibold">{claim.salesman_name || `Salesman #${claim.salesman_id}`}</p>
                  <p className="text-sm text-gray-700">
                    Amount: ₹{claim.total_amount}
                  </p>
                  <p className="text-xs text-gray-500">
                    Remarks: {claim.remarks || "—"}
                  </p>
                  <p className="text-xs text-gray-500">
                    Status: {claim.is_approved ? "✅ Approved" : "🕓 Pending"}
                  </p>
                </div>
                <div className="flex flex-col md:flex-row gap-2">
                  {!claim.is_approved && (
                    <>
                      <Button onClick={() => handleApprove(claim.id)}>Approve</Button>
                      <Button onClick={() => handleReject(claim.id)} variant="danger">
                        Reject
                      </Button>
                    </>
                  )}
                </div>
              </div>

              {/* Remarks Amendment */}
              {!claim.is_approved && (
                <div className="flex items-center gap-2">
                  <Input
                    placeholder="Edit remarks"
                    value={amendMap[claim.id] || ""}
                    onChange={(e) =>
                      setAmendMap({ ...amendMap, [claim.id]: e.target.value })
                    }
                  />
                  <Button onClick={() => handleAmendRemarks(claim.id)}>Save</Button>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
