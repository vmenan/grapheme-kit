import type { NextConfig } from "next";

// Static export so the site deploys to Cloudflare Pages with no Node server.
// The frontend talks to the FastAPI backend over NEXT_PUBLIC_API_BASE_URL.
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
};

export default nextConfig;
