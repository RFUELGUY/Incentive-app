import React from "react";
import './index.css';
import ReactDOM from "react-dom/client";
import AppRouter from "./router/AppRouter";
import "./index.css"; // Tailwind/global CSS

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>
);
