// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Enable static export
  trailingSlash: true, // Generate /about/index.html instead of /about.html
  images: {
    unoptimized: true // Required for static export
  }
}

module.exports = nextConfig