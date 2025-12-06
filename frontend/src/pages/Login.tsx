import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      await login(email, password);
      navigate("/");
    } catch (err: any) {
      console.error(err);
      setError("Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 rounded-2xl border border-leafline-border bg-leafline-card/80 p-6 shadow-soft">
      <h1 className="text-xl font-semibold text-white">Log in</h1>
      <p className="mt-1 text-sm text-leafline-textMuted">
        Access your plantations, ML analysis and marketplace.
      </p>

      {error && (
        <div className="mt-3 rounded-md border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-4 space-y-3 text-sm">
        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Email</label>
          <input
            type="email"
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Password</label>
          <input
            type="password"
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-2 w-full rounded-lg bg-leafline-accent py-2 text-sm font-medium text-slate-950 hover:bg-emerald-500 disabled:opacity-60"
        >
          {loading ? "Logging in…" : "Log in"}
        </button>
      </form>

      <p className="mt-4 text-xs text-leafline-textMuted">
        Don&apos;t have an account?{" "}
        <Link to="/signup" className="text-leafline-accent hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
};

export default Login;
