import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    // Required for Tailscale serve exposure — allows requests from *.ts.net hosts.
    // Safe for a private-tailnet dev server; do not use in production.
    allowedHosts: true,
  },
})
