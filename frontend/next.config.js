// @ts-check

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // This creates a static export suitable for Vercel deployment
  trailingSlash: true, // Add trailing slashes to all routes
  images: {
    unoptimized: true // Since we're exporting statically, disable image optimization
  },
  // Handle the middleware deprecation warning by disabling it in build
  experimental: {
    serverComponentsExternalPackages: ['jose'],
  }
};

module.exports = nextConfig;