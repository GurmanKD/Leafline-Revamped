/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        leafline: {
          bg: "#050816",
          card: "#0f172a",
          accent: "#22c55e",
          accentSoft: "#bbf7d0",
          textPrimary: "#f9fafb",
          textMuted: "#9ca3af",
          border: "#1f2937",
        },
      },
      boxShadow: {
        soft: "0 18px 40px rgba(15, 23, 42, 0.9)",
      },
    },
  },
  plugins: [],
};
