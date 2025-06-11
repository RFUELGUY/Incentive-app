import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import AdminDashboard from "../pages/admin/AdminDashboard";
import RequireAuth from "../auth/requireAuth";

// Salesman screens
import SalesmanLanding from "../pages/salesman/SalesmanLanding";
import ProfilePage       from "../pages/salesman/ProfilePage";
import SalesPage         from "../pages/salesman/SalesPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/"        element={<Signup />} />
        <Route path="/login"   element={<Login />}  />

        {/* Admin (protected) */}
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <AdminDashboard />
            </RequireAuth>
          }
        />

        {/* Salesman (protected) */}
        <Route
          path="/salesman"
          element={
            <RequireAuth>
              <SalesmanLanding />
            </RequireAuth>
          }
        />
        <Route
          path="/salesman/profile"
          element={
            <RequireAuth>
              <ProfilePage />
            </RequireAuth>
          }
        />
        <Route
          path="/salesman/sales"
          element={
            <RequireAuth>
              <SalesPage />
            </RequireAuth>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
