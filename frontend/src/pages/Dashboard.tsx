import React, { useEffect, useState } from "react";
import API from "../services/api";

type Coordinate = {
  lat: number;
  lng: number;
};

type Plantation = {
  id: number;
  owner_id: number;
  name: string;
  coordinates: Coordinate[];
  created_at: string;
};

type PlantationAnalysis = {
  id: number;
  plantation_id: number;
  tree_count: number | null;
  tree_density: number | null;
  ndvi_mean: number | null;
  aqi_prediction: number | null;
  green_credits: number | null;
  analyzed_at: string;
} | null;

type GreenCreditBalance = {
  id: number;
  plantation_id: number;
  total_credits: number;
  available_credits: number;
  locked_credits: number;
};

type CreditListing = {
  id: number;
  plantation_id: number;
  seller_id: number;
  total_credits: number;
  remaining_credits: number;
  price_per_credit: number;
  status: string;
  created_at: string;
};

type PlantationDashboard = {
  plantation: Plantation;
  latest_analysis: PlantationAnalysis;
  credit_balance: GreenCreditBalance;
  active_listings: CreditListing[];
};

const Dashboard: React.FC = () => {
  const [plantations, setPlantations] = useState<Plantation[]>([]);
  const [loadingPlantations, setLoadingPlantations] = useState(false);
  const [creating, setCreating] = useState(false);
  const [plantationName, setPlantationName] = useState("");
  const [selectedDashboard, setSelectedDashboard] = useState<PlantationDashboard | null>(null);
  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [analysisLoadingId, setAnalysisLoadingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function fetchPlantations() {
    try {
      setLoadingPlantations(true);
      const res = await API.get<Plantation[]>("/plantations");
      setPlantations(res.data);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load plantations");
    } finally {
      setLoadingPlantations(false);
    }
  }

  useEffect(() => {
    fetchPlantations();
  }, []);

  async function handleCreatePlantation() {
    if (!plantationName.trim()) return;
    try {
      setCreating(true);
      setError(null);

      // For now: simple demo coordinates (square around some lat/lng)
      const coords: Coordinate[] = [
        { lat: 30.1234, lng: 76.5432 },
        { lat: 30.1234, lng: 76.5440 },
        { lat: 30.1240, lng: 76.5440 },
        { lat: 30.1240, lng: 76.5432 },
      ];

      await API.post("/plantations", {
        name: plantationName.trim(),
        coordinates: coords,
      });

      setPlantationName("");
      await fetchPlantations();
    } catch (err: any) {
      console.error(err);
      setError("Failed to create plantation");
    } finally {
      setCreating(false);
    }
  }

  async function loadDashboard(plantationId: number) {
    try {
      setDashboardLoading(true);
      setError(null);
      const res = await API.get<PlantationDashboard>(`/plantations/${plantationId}/dashboard`);
      setSelectedDashboard(res.data);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load plantation dashboard");
    } finally {
      setDashboardLoading(false);
    }
  }

  async function runAnalysis(plantationId: number) {
    try {
      setAnalysisLoadingId(plantationId);
      setError(null);
      await API.post(`/plantations/${plantationId}/analyze`, { force_recompute: true });
      await loadDashboard(plantationId);
    } catch (err: any) {
      console.error(err);
      setError("Failed to run analysis");
    } finally {
      setAnalysisLoadingId(null);
    }
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl md:text-3xl font-semibold text-white">Plantation Dashboard</h1>
        <p className="mt-2 text-sm text-leafline-textMuted max-w-2xl">
          Register plantations, trigger ML analysis, and inspect green-credit computations and marketplace activity.
        </p>
      </section>

      {error && (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-2 text-sm text-red-100">
          {error}
        </div>
      )}

      {/* Create plantation */}
      <section className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-4 shadow-soft">
        <h2 className="text-lg font-semibold text-white">Create a plantation</h2>
        <p className="mt-1 text-xs text-leafline-textMuted">
          For now, we auto-generate a simple square geofence; only name is required.
        </p>

        <div className="mt-3 flex flex-col gap-3 md:flex-row">
          <input
            value={plantationName}
            onChange={(e) => setPlantationName(e.target.value)}
            placeholder="e.g. Gurman Mango Orchard"
            className="flex-1 rounded-xl border border-leafline-border bg-black/50 px-3 py-2 text-sm text-white outline-none focus:border-leafline-accent"
          />
          <button
            onClick={handleCreatePlantation}
            disabled={creating}
            className="rounded-xl bg-leafline-accent px-4 py-2 text-sm font-medium text-slate-900 hover:bg-emerald-500 disabled:opacity-60"
          >
            {creating ? "Creating..." : "Create plantation"}
          </button>
        </div>
      </section>

      {/* Plantations list + details */}
      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-4 shadow-soft">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-white">Your plantations</h2>
            {loadingPlantations && (
              <span className="text-xs text-leafline-textMuted">Loading…</span>
            )}
          </div>

          {plantations.length === 0 && !loadingPlantations ? (
            <p className="text-sm text-leafline-textMuted">
              No plantations yet. Create one above to get started.
            </p>
          ) : (
            <ul className="space-y-3">
              {plantations.map((p) => (
                <li
                  key={p.id}
                  className="rounded-xl border border-leafline-border/70 bg-black/40 p-3"
                >
                  <div className="flex items-center justify-between gap-2">
                    <div>
                      <h3 className="text-sm font-semibold text-white">{p.name}</h3>
                      <p className="text-[11px] text-leafline-textMuted">
                        ID #{p.id} · Coords: {p.coordinates.length} corners
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() => runAnalysis(p.id)}
                        className="rounded-full border border-leafline-accent/60 px-3 py-1 text-[11px] font-medium text-leafline-accent hover:bg-leafline-accent/10"
                        disabled={analysisLoadingId === p.id}
                      >
                        {analysisLoadingId === p.id ? "Analyzing…" : "Run analysis"}
                      </button>
                      <button
                        onClick={() => loadDashboard(p.id)}
                        className="rounded-full border border-leafline-border px-3 py-1 text-[11px] text-leafline-textMuted hover:border-leafline-accent hover:text-leafline-accent"
                      >
                        View dashboard
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-2xl border border-leafline-border bg-leafline-card/80 p-4 shadow-soft">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-white">Plantation details</h2>
            {dashboardLoading && (
              <span className="text-xs text-leafline-textMuted">Refreshing…</span>
            )}
          </div>

          {!selectedDashboard ? (
            <p className="text-sm text-leafline-textMuted">
              Select a plantation and click{" "}
              <span className="font-medium text-leafline-accent">View dashboard</span> to see ML
              analysis, credits and marketplace data.
            </p>
          ) : (
            <div className="space-y-4 text-sm">
              <div>
                <h3 className="font-semibold text-white">
                  {selectedDashboard.plantation.name}
                </h3>
                <p className="text-[11px] text-leafline-textMuted">
                  Plantation ID #{selectedDashboard.plantation.id} ·{" "}
                  {selectedDashboard.plantation.coordinates.length} corners
                </p>
              </div>

              <div className="grid gap-3 md:grid-cols-3">
                <div className="rounded-xl border border-leafline-border bg-black/40 p-3">
                  <p className="text-[10px] uppercase tracking-wide text-leafline-textMuted">
                    Tree estimate
                  </p>
                  <p className="mt-1 text-lg font-semibold text-white">
                    {selectedDashboard.latest_analysis?.tree_count ?? "—"}
                  </p>
                  <p className="text-[11px] text-leafline-textMuted">
                    Density: {selectedDashboard.latest_analysis?.tree_density ?? "—"}
                  </p>
                </div>

                <div className="rounded-xl border border-leafline-border bg-black/40 p-3">
                  <p className="text-[10px] uppercase tracking-wide text-leafline-textMuted">
                    Vegetation (NDVI)
                  </p>
                  <p className="mt-1 text-lg font-semibold text-white">
                    {selectedDashboard.latest_analysis?.ndvi_mean ?? "—"}
                  </p>
                  <p className="text-[11px] text-leafline-textMuted">
                    AQI prediction:{" "}
                    {selectedDashboard.latest_analysis?.aqi_prediction ?? "—"}
                  </p>
                </div>

                <div className="rounded-xl border border-leafline-border bg-black/40 p-3">
                  <p className="text-[10px] uppercase tracking-wide text-leafline-textMuted">
                    Green credits
                  </p>
                  <p className="mt-1 text-lg font-semibold text-leafline-accent">
                    {selectedDashboard.latest_analysis?.green_credits ?? "—"}
                  </p>
                  <p className="text-[11px] text-leafline-textMuted">
                    Total: {selectedDashboard.credit_balance.total_credits} · Available:{" "}
                    {selectedDashboard.credit_balance.available_credits}
                  </p>
                </div>
              </div>

              <div>
                <p className="text-[11px] font-semibold text-leafline-textMuted uppercase tracking-wide mb-1">
                  Active listings
                </p>
                {selectedDashboard.active_listings.length === 0 ? (
                  <p className="text-xs text-leafline-textMuted">
                    No active listings yet for this plantation.
                  </p>
                ) : (
                  <ul className="space-y-2 text-xs">
                    {selectedDashboard.active_listings.map((lst) => (
                      <li
                        key={lst.id}
                        className="flex items-center justify-between rounded-lg border border-leafline-border bg-black/30 px-3 py-2"
                      >
                        <span>
                          #{lst.id} · {lst.remaining_credits}/{lst.total_credits} credits
                        </span>
                        <span className="text-leafline-accent">
                          ₹{lst.price_per_credit.toFixed(2)} / credit
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
