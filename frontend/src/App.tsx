import React from "react";
import { Routes, Route } from "react-router-dom";
import { LeaflineLayout } from "./components/LeaflineLayout";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import { ProtectedRoute } from "./components/ProtectedRoute";

const App: React.FC = () => {
  return (
    <LeaflineLayout>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </LeaflineLayout>
  );
};

export default App;
