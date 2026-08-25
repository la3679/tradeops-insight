import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("analyst investigates and supervisor approves synthetic resolution", async ({
  page,
}, testInfo) => {
  await page.goto("/exceptions");
  await expect(page.getByRole("heading", { name: "Exception queue" })).toBeVisible();
  await page
    .getByRole("link", { name: /Open TRD-DEMO/ })
    .first()
    .click();

  await page.getByRole("button", { name: "Start investigation" }).click();
  await expect(page.getByText(/mock · mock-v1/)).toBeVisible();
  await expect(page.getByText("Access not available")).toBeVisible();

  await page.getByLabel("Demo role").selectOption("reviewer");
  await page.getByRole("button", { name: "Approve", exact: true }).click();
  await expect(page.getByText("Resolution applied")).toBeVisible();

  if (testInfo.project.name === "chromium") {
    await page.screenshot({ path: "docs/assets/exception-workspace.png", fullPage: true });
  }
});

test("auditor remains read-only and critical pages meet automated accessibility checks", async ({
  page,
}) => {
  await page.goto("/exceptions");
  await page
    .getByRole("link", { name: /Open TRD-DEMO/ })
    .first()
    .click();

  await page.getByLabel("Demo role").selectOption("auditor");
  await expect(page.getByLabel("Demo role")).toHaveValue("auditor");
  await expect(page.getByRole("button", { name: "Start investigation" })).toBeDisabled();
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});

test("synthetic import replay is idempotent and unauthorized import is denied", async ({
  request,
}) => {
  const endpoint = "http://127.0.0.1:8000/api/v1/imports/synthetic";
  const key = `e2e-import-${Date.now()}`;
  const analyst = await request.post(endpoint, {
    headers: { "X-Demo-Role": "analyst", "Idempotency-Key": key },
  });
  const first = await request.post(endpoint, {
    headers: { "X-Demo-Role": "administrator", "Idempotency-Key": key },
  });
  const replay = await request.post(endpoint, {
    headers: { "X-Demo-Role": "administrator", "Idempotency-Key": key },
  });

  expect(analyst.status()).toBe(403);
  const firstBody: unknown = await first.json();
  const replayBody: unknown = await replay.json();
  expect(firstBody).toMatchObject({ status: "accepted" });
  expect(replayBody).toMatchObject({ status: "duplicate" });
  expect(replayBody).toMatchObject({ import_id: (firstBody as { import_id: string }).import_id });
});
