import { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../../config";
import Button from "../../components/ui/Button";

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState({
    day: [],
    week: [],
    month: [],
    streak: [],
  });

  const fetchLeaderboard = async () => {
    const token = localStorage.getItem("token");
    try {
      const [day, week, month, streak] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/leaderboard/day`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${API_BASE_URL}/api/leaderboard/week`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${API_BASE_URL}/api/leaderboard/month`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${API_BASE_URL}/api/leaderboard/streak`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);
      setLeaderboard({
        day: day.data,
        week: week.data,
        month: month.data,
        streak: streak.data,
      });
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
      alert("Error loading leaderboard data.");
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const renderTable = (title, data) => (
    <section className="border p-4 rounded shadow mb-6">
      <h2 className="text-lg font-bold mb-2">{title}</h2>
      {data.length === 0 ? (
        <p className="text-gray-500">No entries yet.</p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-1">#</th>
              <th>Name</th>
              <th>Mobile</th>
              <th>Outlet</th>
              <th>Sales</th>
            </tr>
          </thead>
          <tbody>
            {data.map((entry, idx) => (
              <tr key={entry.id} className="border-b">
                <td className="py-1">{idx + 1}</td>
                <td>{entry.name}</td>
                <td>{entry.mobile}</td>
                <td>{entry.outlet}</td>
                <td>{entry.total_sales}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-bold">🏆 Leaderboard Overview</h1>
        <Button onClick={fetchLeaderboard}>🔄 Refresh</Button>
      </div>
      {renderTable("⭐ Star of the Day", leaderboard.day)}
      {renderTable("🌟 Star of the Week", leaderboard.week)}
      {renderTable("🌙 Star of the Month", leaderboard.month)}
      {renderTable("⚡ Streak Breakers", leaderboard.streak)}
    </div>
  );
}
