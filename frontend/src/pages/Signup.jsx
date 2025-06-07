import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import API_BASE_URL from "../config";

export default function Signup() {
  const [formData, setFormData] = useState({
    name: "",
    mobile: "",
    outlet: "",
    password: "",
  });
  const [outlets, setOutlets] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOutlets = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/api/public/outlets`);
        setOutlets(res.data);
      } catch (err) {
        console.error("Failed to load outlets:", err);
        alert("Could not load outlet list.");
      }
    };
    fetchOutlets();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/api/auth/signup`, formData);
      alert("Signup successful! Please wait for admin approval.");
      navigate("/login");
    } catch (err) {
      console.error("Signup error:", err);
      alert("Signup failed");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm space-y-4 bg-white p-6 rounded shadow"
      >
        <h2 className="text-xl font-bold text-center">Create Your Account</h2>

        <Input
          label="Full Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <Input
          label="Phone Number"
          name="mobile"
          value={formData.mobile}
          onChange={handleChange}
          required
        />

        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Select Outlet</label>
          <select
            name="outlet"
            value={formData.outlet}
            onChange={handleChange}
            required
            className="border px-3 py-2 rounded text-sm"
          >
            <option value="">-- Select an outlet --</option>
            {outlets.map((outlet) => (
              <option key={outlet.id} value={outlet.name}>
                {outlet.name}
              </option>
            ))}
          </select>
        </div>

        <Input
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <Button type="submit" full>
          Sign Up
        </Button>

        <p className="text-center text-sm">
          Already a member?{" "}
          <span
            className="text-blue-600 cursor-pointer underline"
            onClick={() => navigate("/login")}
          >
            Login here
          </span>
        </p>
      </form>
    </div>
  );
}
