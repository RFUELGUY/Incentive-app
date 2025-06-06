import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import AdminDashboard from "../pages/AdminDashboard";
import SalesmanDashboard from "../pages/SalesmanDashboard";
import RequireAuth from "../auth/requireAuth";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <AdminDashboard />
            </RequireAuth>
          }
        />
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
