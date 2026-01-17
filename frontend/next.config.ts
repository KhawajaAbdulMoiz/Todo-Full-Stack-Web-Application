import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    turbo: {
      enabled: false // Disable Turbopack for stable build
    }
  }
};

export default nextConfig;
