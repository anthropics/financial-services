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
  gateway_auth_source: {
    pattern: /^entra$/,
    hint: "'entra' to send the Entra SSO access token as the Bearer to your gateway, or to a Foundry resource named by azure_resource_name (no gateway_token / azure_api_key needed); requires entra_scope",
  },
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
    hint: "scope(s) for the resource the token targets: api://<your-app-guid>/.default for your own API, or https://cognitiveservices.azure.com/.default for Foundry direct — comma/space-separated list allowed, requires graph_client_id",
  },
  graph_cloud: {
    // The add-in rejects unrecognized values at load and falls back to global,
    // so a typo here degrades to commercial endpoints — heed the warning.
    pattern: /^(global|us-gov-high|us-gov-dod|china)$/,
    hint: "Microsoft national cloud: global | us-gov-high | us-gov-dod | china — only for sovereign clouds; GCC-High and 21Vianet are also auto-detected at sign-in",
  },
  allow_1p: {
    pattern: /^[01]$/,
    hint: "1 allows Claude.ai OAuth alongside 3P (default: locked when other keys present)",
  },
  disabled_features: {
    pattern: /^[\w.]+(,[\w.]+)*$/,
    hint: "comma-separated feature slugs to lock for users, e.g. skills.authoring",
  },
  access_policies: {
    pattern: /^\[.*\]$/s,
    hint: "JSON array of policy statements — see commands/access-policies.md; e.g. [{\"effect\":\"deny\",\"action\":\"addin.access\",\"resource\":{...}}]",
    validate: (v) => {
      let arr;
      try {
        arr = JSON.parse(v);
      } catch (e) {
        throw new Error(`access_policies is not valid JSON: ${e.message}`);
      }
      if (!Array.isArray(arr)) return ["expected a JSON array of statements"];
      return arr.flatMap((st, i) => validateStatement(st, `statement[${i}]`));
    },
  },
};

// Structural check for one access_policies statement. Warn-only: the add-in itself
// skips and reports malformed statements rather than failing, so this catches typos
// before deploy without being stricter than the runtime.
const EFFECTS = ["allow", "deny"];
const RESOURCE_TYPES = ["open_file", "uploaded_file"];
const STRING_OPS = ["equals", "startsWith", "endsWith"];
// Mirrors the add-in: a GUID supports only equals | exists (a prefix of a GUID is
// meaningless); a name supports the string operators too. Other pairings are dropped
// at runtime, so warn here.
const OPERATORS_BY_TYPE = {
  mip_label_guid: ["equals", "exists"],
  mip_label_name: ["equals", "startsWith", "endsWith", "exists"],
};

function validateStatement(st, at) {
  if (typeof st !== "object" || st === null || Array.isArray(st)) return [`${at}: expected an object`];
  const problems = [];
  if (!EFFECTS.includes(st.effect)) problems.push(`${at}.effect: expected "allow" or "deny"`);
  const slugs = Array.isArray(st.action) ? st.action : [st.action];
  const actionOk = slugs.length > 0 && slugs.every((a) => typeof a === "string" && a.trim());
  if (!actionOk) problems.push(`${at}.action: expected a non-empty slug string or array of them`);
  if (st.resource !== undefined) {
    const r = st.resource;
    if (typeof r !== "object" || r === null) return [...problems, `${at}.resource: expected an object`];
    if (!RESOURCE_TYPES.includes(r.type)) problems.push(`${at}.resource.type: expected ${RESOURCE_TYPES.join(" | ")}`);
    if (r.description !== undefined && typeof r.description !== "string") {
      problems.push(`${at}.resource.description: expected a string`);
    }
    if (!Array.isArray(r.identifiers)) {
      problems.push(`${at}.resource.identifiers: expected an array`);
    } else if (r.identifiers.length === 0) {
      problems.push(`${at}.resource.identifiers: empty — the statement will never match; drop \`resource\` to apply everywhere`);
    } else {
      r.identifiers.forEach((id, j) => problems.push(...validateIdentifier(id, `${at}.resource.identifiers[${j}]`)));
    }
  }
  return problems;
}

function validateIdentifier(id, at) {
  if (typeof id !== "object" || id === null) return [`${at}: expected an object`];
  const problems = [];
  const allowed = OPERATORS_BY_TYPE[id.type];
  if (!allowed) problems.push(`${at}.type: expected ${Object.keys(OPERATORS_BY_TYPE).join(" | ")}`);
  const ops = [...STRING_OPS.filter((op) => op in id), ..."exists" in id ? ["exists"] : []];
  if (ops.length !== 1) {
    problems.push(`${at}: expected exactly one operator (equals | startsWith | endsWith | exists), got ${ops.length}`);
    return problems;
  }
  const [op] = ops;
  if (allowed && !allowed.includes(op)) {
    problems.push(`${at}: ${id.type} does not support ${op} (only ${allowed.join(" | ")})`);
  } else if (op === "exists" ? typeof id.exists !== "boolean" : typeof id[op] !== "string" || !id[op].trim()) {
    problems.push(`${at}.${op}: expected a ${op === "exists" ? "boolean" : "non-empty string"}`);
  }
  return problems;
}

const NEEDS_ENTRA = ["aws_role_arn", "graph_client_id", "entra_scope", "gateway_auth_source"];

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
  // graph_client_id and graph_cloud apply to both manifests: in Outlook it steers Graph +
  // Entra sign-in; in office it steers the Entra SSO authority.

  const params = new URLSearchParams();
  for (const p of pairs) {
    const eq = p.indexOf("=");
    if (eq < 1) throw new Error(`bad arg: ${p} (expected key=value)`);
    const [k, v] = [p.slice(0, eq).trim(), p.slice(eq + 1).trim()];

    const spec = KEYS[k];
    if (!spec) throw new Error(`unknown key: ${k}\n  valid: ${Object.keys(KEYS).join(", ")}`);
    if (!v) throw new Error(`empty value for ${k}`);
    if (!spec.pattern.test(v)) console.warn(`warn: ${k}=${v} — expected ${spec.hint}`);
    for (const msg of spec.validate?.(v) ?? []) console.warn(`warn: ${k} ${msg}`);
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
  if (params.has("gateway_auth_source") && !params.has("entra_scope")) {
    throw new Error(
      "gateway_auth_source=entra requires entra_scope (the gateway Bearer must be audienced to your API, not Microsoft Graph)",
    );
  }
  if (params.has("gateway_auth_source") && params.has("gateway_token")) {
    console.warn("note: gateway_auth_source=entra supersedes gateway_token — drop gateway_token from this manifest");
  }
  // A non-global graph_cloud needs a BYO Entra app — Anthropic's multi-tenant
  // app exists only in the commercial cloud, so the default client_id against
  // a sovereign authority fails with an opaque AADSTS700016 at sign-in.
  const cloud = params.get("graph_cloud");
  if (cloud && cloud !== "global" && !params.has("graph_client_id")) {
    throw new Error(`graph_cloud=${cloud} requires a graph_client_id registered in that cloud`);
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
