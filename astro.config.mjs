import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
  site: "https://cablate.github.io",
  base: "/2026-world-cup-ai",
  trailingSlash: "ignore",
});
