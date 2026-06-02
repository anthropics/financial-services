#!/usr/bin/env node

import fs from "node:fs";
import { createRequire } from "node:module";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

function parseArgs(argv) {
  const args = { format: "pdf" };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--input") args.input = argv[++index];
    else if (token === "--format") args.format = argv[++index];
    else if (token === "--output") args.output = argv[++index];
    else if (token === "--output-dir") args.outputDir = argv[++index];
  }
  if (!args.input) throw new Error("Missing --input <html>");
  if (args.format !== "pdf") {
    throw new Error(`Unsupported --format ${args.format}`);
  }
  return args;
}

function inputPath(value) {
  if (value.startsWith("file://")) {
    return new URL(value);
  }
  if (/^https?:\/\//.test(value)) {
    return value;
  }
  return pathToFileURL(path.resolve(value));
}

function outputPath(args, format) {
  if (args.output) return path.resolve(args.output);
  const rawInput = args.input.startsWith("file://") ? new URL(args.input).pathname : args.input;
  const input = /^https?:\/\//.test(args.input) ? "report.html" : rawInput;
  const parsed = path.parse(input);
  const directory = args.outputDir ? path.resolve(args.outputDir) : parsed.dir || process.cwd();
  return path.join(directory, `${parsed.name}.${format}`);
}

function cachedHeadlessShellPath() {
  const cacheRoot = path.join(os.homedir(), "Library", "Caches", "ms-playwright");
  if (!fs.existsSync(cacheRoot)) return null;
  const candidates = fs.readdirSync(cacheRoot)
    .filter(name => name.startsWith("chromium_headless_shell-"))
    .sort((left, right) => {
      const leftVersion = Number(left.split("-").pop());
      const rightVersion = Number(right.split("-").pop());
      return rightVersion - leftVersion;
    });
  for (const name of candidates) {
    const candidate = path.join(
      cacheRoot,
      name,
      "chrome-headless-shell-mac-arm64",
      "chrome-headless-shell",
    );
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

async function launchBrowser() {
  try {
    return await chromium.launch({ headless: true });
  } catch (error) {
    const headlessShell = cachedHeadlessShellPath();
    if (headlessShell) {
      return chromium.launch({ executablePath: headlessShell, headless: true });
    }
    const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    if (fs.existsSync(chromePath)) {
      return chromium.launch({ executablePath: chromePath, headless: true });
    }
    throw error;
  }
}

async function loadPage(browser, source) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  await page.goto(inputPath(source).toString(), { waitUntil: "networkidle" });
  await page.addStyleTag({
    content: "body{background:#F6F5F4!important}",
  });
  return page;
}

async function exportPdf(page, destination) {
  await fs.promises.mkdir(path.dirname(destination), { recursive: true });
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: destination,
    format: "Letter",
    printBackground: true,
    margin: { top: "0.3in", right: "0.25in", bottom: "0.3in", left: "0.25in" },
  });
  console.log(`Wrote PDF: ${destination}`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const browser = await launchBrowser();
  try {
    const page = await loadPage(browser, args.input);
    await exportPdf(page, outputPath(args, "pdf"));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(`Export failed: ${error.message}`);
  process.exit(1);
});
