import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Signup: React.FC = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    full_name: "",
    password: "",
    role: "PLANTATION_OWNER",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updateField(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      await signup(form);
      navigate("/");
    } catch (err: any) {
      console.error(err);
      setError("Signup failed. Maybe the email is already used.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 rounded-2xl border border-leafline-border bg-leafline-card/80 p-6 shadow-soft">
      <h1 className="text-xl font-semibold text-white">Create account</h1>
      <p className="mt-1 text-sm text-leafline-textMuted">
        Join as a plantation owner or an industry to trade green credits.
      </p>

      {error && (
        <div className="mt-3 rounded-md border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-4 space-y-3 text-sm">
        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Full name</label>
          <input
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={form.full_name}
            onChange={(e) => updateField("full_name", e.target.value)}
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Email</label>
          <input
            type="email"
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={form.email}
            onChange={(e) => updateField("email", e.target.value)}
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Password</label>
          <input
            type="password"
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={form.password}
            onChange={(e) => updateField("password", e.target.value)}
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-leafline-textMuted">Role</label>
          <select
            className="w-full rounded-lg border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
            value={form.role}
            onChange={(e) => updateField("role", e.target.value)}
          >
            <option value="PLANTATION_OWNER">Plantation Owner</option>
            <option value="INDUSTRY">Industry</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-2 w-full rounded-lg bg-leafline-accent py-2 text-sm font-medium text-slate-950 hover:bg-emerald-500 disabled:opacity-60"
        >
          {loading ? "Creating account…" : "Sign up"}
        </button>
      </form>

      <p className="mt-4 text-xs text-leafline-textMuted">
        Already have an account?{" "}
        <Link to="/login" className="text-leafline-accent hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
};

export default Signup;
