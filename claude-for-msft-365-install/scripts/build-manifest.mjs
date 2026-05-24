#!/usr/bin/env node
// Fetches the canonical add-in manifest and writes a customized copy with your
// org's config baked into the taskpane URL as query parameters.
//
// Usage: node build-manifest.mjs <office|outlook> <out.xml> key=value [key=value ...]
// Example: node build-manifest.mjs office acme.xml gcp_project_id=acme gcp_region=us-east5

import { writeFileSync } from "node:fs";

const MANIFESTS = {
  office: "https://pivot.claude.ai/manifest.xml", // Excel + Word + PowerPoint (TaskPaneApp)
  outlook: "https://pivot.claude.ai/manifest-outlook-3p.xml", // Outlook (MailApp — separate schema)
};

// Every URL slot Office reads from must carry the same params. Outlook's MailApp
// schema repeats Taskpane.Url across V1_0 and V1_1 VersionOverrides, hence /g.
const URL_SLOTS = [/(<SourceLocation\s+DefaultValue=")([^"]+)(")/g, /(id="Taskpane\.Url"\s+DefaultValue=")([^"]+)(")/g];

// Recognized config keys. `pattern` is a shape hint — mismatches warn but don't block
// (your infra may look different). `secret` keys warn louder: the manifest is an
// org-wide file and its URL can land in deploy logs; per-user secrets typically go
// in Azure extension attributes instead.
const KEYS = {
  gcp_project_id: { pattern: /^[a-z][a-z0-9-]{4,28}[a-z0-9]$/, hint: "GCP project ID" },
  gcp_region: { pattern: /./, hint: "GCP region, e.g. us-east5 or global" },
  google_client_id: { pattern: /\.apps\.googleusercontent\.com$/, hint: "OAuth 2.0 client ID" },
  google_client_secret: { pattern: /^GOCSPX-/, hint: "OAuth 2.0 client secret" },
  aws_role_arn: {
    pattern: /^arn:aws:iam::\d{12}:role\//,
    hint: "e.g. arn:aws:iam::123456789012:role/ClaudeBedrockAccess",
  },
  aws_region: { pattern: /^[a-z]{2}-[a-z]+-\d+$/, hint: "e.g. us-east-1" },
  azure_resource_name: {
    pattern: /^[a-z0-9][a-z0-9-]{1,62}$/,
    hint: "Azure AI Foundry resource name — the subdomain of your endpoint URL, e.g. 'contoso-foundry' from https://contoso-foundry.services.ai.azure.com",
  },
  azure_api_key: {
    pattern: /^[A-Za-z0-9]{20,}$/,
    hint: "From Azure Portal → your Foundry resource → Keys and Endpoint → KEY 1",
  },
  graph_client_id: {
    pattern: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
    hint: "Entra app (client) ID for Microsoft Graph — Outlook only; omit to use Anthropic's multi-tenant app via the admin consent URL",
  },
  gateway_url: { pattern: /^https:\/\//, hint: "HTTPS base URL" },
  gateway_token: { pattern: /./, hint: "gateway API key", secret: true },
  gateway_auth_header: { pattern: /^(x-api-key|authorization)$/i, hint: "auth header scheme (default: x-api-key)" },
  gateway_api_format: { pattern: /^(anthropic|bedrock|vertex)$/i, hint: "anthropic | bedrock | vertex" },
  mcp_servers: { pattern: /^\[.*\]$/, hint: "JSON array of {url, label, headers?, discover?}" },
  inference_headers: { pattern: /^\{.*\}$/, hint: "JSON object of extra headers to attach to every model request" },
  bootstrap_url: { pattern: /^https:\/\//, hint: "HTTPS endpoint returning per-user config" },
  otlp_endpoint: { pattern: /^https:\/\//, hint: "OTLP/HTTP traces collector URL" },
  otlp_headers: { pattern: /./, hint: "comma-separated k=v pairs for the OTLP exporter" },
  otlp_resource_attributes: {
    pattern: /^([^=,\s]+=[^,]*)(,[^=,\s]+=[^,]*)*$/,
    hint: "comma-separated k=v pairs added to the OTEL Resource (same format as OTEL_RESOURCE_ATTRIBUTES)",
  },
  auto_connect: { pattern: /^[01]$/, hint: "0 shows form, 1 (or omit) auto-connects" },
  entra_sso: { pattern: /^[01]$/, hint: "1 enables Entra SSO (required for aws_role_arn)" },
  graph_client_id: {
    pattern: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
    hint: "your Entra app registration's Application (client) ID — overrides the default multi-tenant app",
  },
  entra_scope: {
    // Any non-blank string — Entra validates scope syntax, not us. May be a comma- or
    // whitespace-separated list (the add-in splits it); requires graph_client_id (enforced below).
    pattern: /\S/,
    hint: "scope(s) for your Entra-protected API, e.g. api://<your-app-guid>/.default — comma/space-separated list allowed, requires graph_client_id",
  },
  allow_1p: {
    pattern: /^[01]$/,
    hint: "1 allows Claude.ai OAuth alongside 3P (default: locked when other keys present)",
  },
  disabled_features: {
    pattern: /^[\w.]+(,[\w.]+)*$/,
    hint: "comma-separated feature slugs to lock for users, e.g. skills.authoring",
  },
};

const NEEDS_ENTRA = ["aws_role_arn", "graph_client_id", "entra_scope"];

async function main() {
  const [host, out, ...pairs] = process.argv.slice(2);
  const manifestUrl = process.env.MANIFEST_URL || MANIFESTS[host];
  if (!manifestUrl || !out || pairs.length === 0) {
    console.error("Usage: node build-manifest.mjs <office|outlook> <out.xml> key=value [key=value ...]");
    console.error(`Keys: ${Object.keys(KEYS).join(", ")}`);
    process.exit(1);
  }
  if (host === "outlook" && pairs.some((p) => p.startsWith("aws_"))) {
    console.error("error: Amazon Bedrock (aws_role_arn/aws_region) is not currently supported for Outlook");
    process.exit(1);
  }
  if (host !== "outlook" && pairs.some((p) => p.startsWith("graph_client_id="))) {
    console.warn("note: graph_client_id only applies to Outlook; it has no effect in the office manifest");
  }

  const params = new URLSearchParams();
  for (const p of pairs) {
    const eq = p.indexOf("=");
    if (eq < 1) throw new Error(`bad arg: ${p} (expected key=value)`);
    const [k, v] = [p.slice(0, eq).trim(), p.slice(eq + 1).trim()];

    const spec = KEYS[k];
    if (!spec) throw new Error(`unknown key: ${k}\n  valid: ${Object.keys(KEYS).join(", ")}`);
    if (!v) throw new Error(`empty value for ${k}`);
    if (!spec.pattern.test(v)) console.warn(`warn: ${k}=${v} — expected ${spec.hint}`);
    if (spec.secret) {
      console.warn(
        `note: ${k} in the manifest applies to every user. If it varies per user, set it via update-user-attrs instead.`,
      );
    }
    params.set(k, v);
  }

  const needsEntra = NEEDS_ENTRA.find((k) => params.has(k));
  if (needsEntra && params.get("entra_sso") !== "1") {
    throw new Error(`${needsEntra} requires entra_sso=1 (the add-in needs an Entra token to use it)`);
  }
  if (params.has("entra_scope") && !params.has("graph_client_id")) {
    throw new Error("entra_scope requires graph_client_id (the scope is requested as your own Entra app, not the default)");
  }

  // URLSearchParams joins with `&`; XML attribute values need it escaped.
  const qs = params.toString().replaceAll("&", "&amp;");

  const res = await fetch(manifestUrl);
  if (!res.ok) throw new Error(`fetch ${manifestUrl}: ${res.status} ${res.statusText}`);
  let xml = await res.text();

  for (const slot of URL_SLOTS) {
    slot.lastIndex = 0;
    if (!slot.test(xml)) throw new Error(`manifest missing expected URL slot: ${slot.source}`);
    slot.lastIndex = 0;
    // The template URL already carries ?m=<tag> — append with & not a second ?
    xml = xml.replace(slot, (_, pre, url, post) => pre + url + (url.includes("?") ? "&amp;" : "?") + qs + post);
  }

  writeFileSync(out, xml);
  console.log(`Wrote ${out} (${host}, params: ${params})`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
