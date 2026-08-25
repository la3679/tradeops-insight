import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "tablet", use: { viewport: { width: 768, height: 1024 } } },
  ],
  webServer: [
    {
      command:
        "uv run --directory backend --locked uvicorn tradeops.api.app:app --host 127.0.0.1 --port 8000",
      url: "http://127.0.0.1:8000/api/v1/health/ready",
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      env: { TRADEOPS_ENVIRONMENT: "test" },
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 3000",
      url: "http://127.0.0.1:3000",
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
  ],
});
