import React, { createContext, useContext, useEffect, useState } from "react";
import API from "../services/api";

type User = {
  email: string;
};

type SignupPayload = {
  email: string;
  full_name: string;
  password: string;
  role: string; // "PLANTATION_OWNER" | "INDUSTRY"
};

type AuthContextType = {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (data: SignupPayload) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  async function login(email: string, password: string) {
    const res = await API.post("/auth/login", { email, password });
    localStorage.setItem("leafline_token", res.data.access_token);
    localStorage.setItem("leafline_email", email);
    setUser({ email });
  }

  async function signup(data: SignupPayload) {
    await API.post("/auth/signup", data);
    await login(data.email, data.password); // auto-login after signup
  }

  function logout() {
    localStorage.removeItem("leafline_token");
    localStorage.removeItem("leafline_email");
    setUser(null);
  }

  // Restore from localStorage on page refresh
  useEffect(() => {
    const token = localStorage.getItem("leafline_token");
    const email = localStorage.getItem("leafline_email");
    if (token && email) {
      setUser({ email });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
