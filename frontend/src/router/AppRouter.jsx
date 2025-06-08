import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import AdminDashboard from "../pages/admin/AdminDashboard";
import SalesmanDashboard from "../pages/SalesmanDashboard";
import RequireAuth from "../auth/requireAuth";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default landing route → Signup */}
        <Route path="/" element={<Signup />} />

        {/* Login route */}
        <Route path="/login" element={<Login />} />

        {/* Protected Admin route */}
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <AdminDashboard />
            </RequireAuth>
          }
        />

        {/* Protected Salesman route */}
        <Route
          path="/salesman"
          element={
            <RequireAuth>
              <SalesmanDashboard />
            </RequireAuth>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
