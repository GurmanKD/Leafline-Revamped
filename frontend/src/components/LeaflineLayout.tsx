import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

type Props = {
  children: React.ReactNode;
};

export const LeaflineLayout: React.FC<Props> = ({ children }) => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-950 to-black text-leafline-textPrimary">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6 md:px-8 md:py-8">
        {/* Top nav */}
        <header className="mb-6 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-leafline-accent/10 ring-1 ring-leafline-accent/40">
              <span className="text-lg font-semibold text-leafline-accent">L</span>
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Leafline Revamped</div>
              <div className="text-xs text-leafline-textMuted">
                Green Credit Intelligence Platform
              </div>
            </div>
          </Link>

          <div className="flex items-center gap-3 text-xs text-leafline-textMuted">
            {user ? (
              <>
                <span className="hidden md:inline text-[11px]">
                  Logged in as{" "}
                  <span className="font-medium text-leafline-accent">{user.email}</span>
                </span>
                <button
                  onClick={logout}
                  className="rounded-full border border-leafline-border px-3 py-1 hover:border-red-400 hover:text-red-300 transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="rounded-full border border-leafline-border px-3 py-1 hover:border-leafline-accent hover:text-leafline-accent transition-colors"
                >
                  Log in
                </Link>
                <Link
                  to="/signup"
                  className="rounded-full bg-leafline-accent px-3 py-1 text-slate-950 font-medium hover:bg-emerald-500 transition-colors"
                >
                  Get started
                </Link>
              </>
            )}
          </div>
        </header>

        {/* Main */}
        <main className="flex-1">{children}</main>

        {/* Footer */}
        <footer className="mt-10 border-t border-leafline-border/70 pt-4 text-xs text-leafline-textMuted">
          <div className="flex flex-col gap-1 md:flex-row md:items-center md:justify-between">
            <p>
              Backend: FastAPI + SQLAlchemy · Frontend: React + Vite + Tailwind · Auth: JWT · Trades:
              Idempotency-key guarded
            </p>
            <p className="text-[11px]">
              Built as a demo of ML-backed green credit trading for interviews &amp; portfolio.
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};
