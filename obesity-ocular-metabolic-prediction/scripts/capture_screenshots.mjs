import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/potato/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

const projectRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const screenshotDir = join(projectRoot, "screenshots");
const cachedChromium = "/Users/potato/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell";

async function capture() {
  await mkdir(screenshotDir, { recursive: true });
  const browser = await chromium.launch({
    executablePath: cachedChromium,
    headless: true,
  });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1050 },
    deviceScaleFactor: 1,
  });

  await page.goto("http://127.0.0.1:5173/", { waitUntil: "networkidle" });
  await page.screenshot({ path: join(screenshotDir, "dashboard.png"), fullPage: false });

  await page.getByRole("button", { name: "Prediction" }).click();
  await page.getByRole("button", { name: "Predict Risk" }).click();
  await page.locator(".risk-summary").waitFor({ timeout: 15000 });
  await page.waitForTimeout(400);
  await page.screenshot({ path: join(screenshotDir, "prediction.png"), fullPage: false });

  await page.getByRole("button", { name: "Analytics" }).click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: join(screenshotDir, "analytics.png"), fullPage: false });

  await page.getByRole("button", { name: "Models" }).click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: join(screenshotDir, "model-comparison.png"), fullPage: false });

  await page.goto(`file://${join(projectRoot, "reports", "test-output.html")}`, { waitUntil: "load" });
  await page.screenshot({ path: join(screenshotDir, "testing-phase.png"), fullPage: false });

  await browser.close();
}

capture()
  .then(() => console.log(`Screenshots saved to ${screenshotDir}`))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
