import React from "react";
import { LeaflineLayout } from "./components/LeaflineLayout";

const App: React.FC = () => {
  return (
    <LeaflineLayout>
      <div className="space-y-6">
        <section>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight text-white">
            Leafline Revamped
          </h1>
          <p className="mt-2 text-leafline-textMuted max-w-2xl">
            A green credit trading platform connecting{" "}
            <span className="text-leafline-accent font-medium">
              plantation owners
            </span>{" "}
            and{" "}
            <span className="text-leafline-accent font-medium">
              industries
            </span>{" "}
            using geofencing, ML-based analysis, and a transparent marketplace.
          </p>
        </section>

        <section className="grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-5 shadow-soft">
            <p className="text-xs font-semibold uppercase tracking-wide text-leafline-accentSoft">
              Step 1
            </p>
            <h2 className="mt-2 text-lg font-semibold text-white">
              Onboard plantations
            </h2>
            <p className="mt-1 text-sm text-leafline-textMuted">
              Geofence fields, upload 360° captures, and let the backend ML
              pipeline estimate trees, NDVI, and local AQI impact.
            </p>
          </div>

          <div className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-5 shadow-soft">
            <p className="text-xs font-semibold uppercase tracking-wide text-leafline-accentSoft">
              Step 2
            </p>
            <h2 className="mt-2 text-lg font-semibold text-white">
              Compute green credits
            </h2>
            <p className="mt-1 text-sm text-leafline-textMuted">
              Combine tree counts, vegetation health, and pollution levels to
              derive fair, scientifically grounded green credits.
            </p>
          </div>

          <div className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-5 shadow-soft">
            <p className="text-xs font-semibold uppercase tracking-wide text-leafline-accentSoft">
              Step 3
            </p>
            <h2 className="mt-2 text-lg font-semibold text-white">
              Trade transparently
            </h2>
            <p className="mt-1 text-sm text-leafline-textMuted">
              Plantation owners list credits and industries buy them via
              idempotent, auditable marketplace APIs.
            </p>
          </div>
        </section>

        <section className="rounded-2xl border border-dashed border-leafline-border/70 bg-leafline-card/40 p-5">
          <h2 className="text-lg font-semibold text-white">
            Frontend wiring coming next…
          </h2>
          <p className="mt-1 text-sm text-leafline-textMuted">
            In the next commits we&apos;ll connect this UI to the FastAPI
            backend: authentication, plantation dashboards, ML analysis triggers
            and marketplace views.
          </p>
        </section>
      </div>
    </LeaflineLayout>
  );
};

export default App;
