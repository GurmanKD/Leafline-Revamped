import React from "react";
import { Navigate } from "react-router-dom";

type Props = {
  children: React.ReactNode;
};

export const ProtectedRoute: React.FC<Props> = ({ children }) => {
  const token = localStorage.getItem("leafline_token");
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};
