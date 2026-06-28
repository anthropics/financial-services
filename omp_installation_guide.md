# Installing the `plugins/` into omp (Oh My Pi) only

This guide installs the repository's `plugins/` (Claude Code plugin format) into
**omp** and omp alone. omp and Claude Code keep separate plugin stores, so an
`omp plugin install` writes only to omp's store — Claude Code never receives it.

> Verified against **omp 16.1.15**. The `plugins/` ship as markdown-only
> (skills + agent prompts), so they load into omp with no loss. The
> `managed-agent-cookbooks/` directory is a *different surface* (Anthropic
> hosted Managed Agent deploy manifests) and is **not** installable here — see
> `managed-agent-cookbooks/README.md`.

All commands are run from the repo root:

```bash
cd ~/Desktop/random_projects/financial-services
```

---

## What "omp-only" means

| Layer | omp | Claude Code |
|---|---|---|
| **Installed plugin store** | `<repo>/.omp/plugins/` (project) or `~/.omp/plugins/` (user) | separate — never written by omp |
| **Marketplace catalog discovery** | reads `.omp-plugin/marketplace.json`, else `.claude-plugin/marketplace.json` | reads `.claude-plugin/marketplace.json` |

Installing via omp makes the *plugin* omp-only by construction. The only shared
artifact is the **catalog** file, which both harnesses can *discover* — but
discovery is not installation. Step 5 (optional) restricts even discovery to omp.

---

## Step 1 — Register the marketplace (omp only)

```bash
omp plugin marketplace add ./.
```

- Must be `./.` for the current directory — a bare `.` is rejected.
- Registers under the catalog's `name`: **`claude-for-financial-services`**.

## Step 2 — Confirm the plugins are discoverable

```bash
omp plugin discover claude-for-financial-services
```

Lists all 20 plugins with their descriptions.

## Step 3 — Install (use `--scope project` for the strongest omp-only guarantee)

`--scope project` ties the install to this repo's `.omp/plugins/installed_plugins.json`
(only omp reads `.omp/`). `--scope user` (the default) installs to `~/.omp/plugins/`
across all projects — still omp-only, just not repo-scoped.

**Cherry-pick one plugin:**

```bash
omp plugin install gl-reconciler@claude-for-financial-services --scope project
```

**Install all 20:**

```bash
for p in \
  financial-analysis investment-banking equity-research private-equity \
  wealth-management fund-admin operations pitch-agent market-researcher \
  earnings-reviewer meeting-prep-agent model-builder gl-reconciler \
  kyc-screener valuation-reviewer month-end-closer statement-auditor \
  lseg sp-global claude-for-msft-365-install; do
  omp plugin install "$p@claude-for-financial-services" --scope project
done
```

## Step 4 — Verify

```bash
omp plugin list          # each shows as "...@claude-for-financial-services (<version>) (project)"
```

Skills and agents load at **session startup**. Restart your omp session (or open
a new one) for the new skills to appear via `skill://<name>` and `/skill:<name>`.

---

## Caveats

- **`--dry-run` is NOT honored** for marketplace `install` in 16.1.15 — it performs
  a real install (writes `installed_plugins.json` + the cache). Do not rely on it to
  preview.
- **`lseg` and `sp-global`** ship `.mcp.json` MCP servers. They install cleanly but
  need external API credentials to be useful — see
  `plugins/partner-built/lseg/CONNECTORS.md`.
- **`claude-for-msft-365-install`** is itself an *installer* plugin for the
  Microsoft 365 add-in, not a daily-use skill pack. Skip it unless you are
  provisioning that add-in.
- A plugin that is already installed errors with *"…is already installed. Use force option to reinstall."*;
  pass `--force` to reinstall.

---

## Step 5 (optional) — Make the catalog omp-discoverable-only

Only needed if you also want to stop Claude Code from *discovering* this
marketplace inside the repo. omp prefers `.omp-plugin/marketplace.json` over
`.claude-plugin/marketplace.json`:

```bash
mkdir -p .omp-plugin
cp .claude-plugin/marketplace.json .omp-plugin/marketplace.json
git rm .claude-plugin/marketplace.json          # removes Claude Code's catalog view
omp plugin marketplace update                    # re-read from the new path
```

**Tradeoff:** this is a repo change that drops Claude Code marketplace
compatibility at the root. The per-plugin `.claude-plugin/plugin.json` files stay
intact; only the root catalog listing them for Claude Code is removed. Skip this
if Steps 1–4 are enough (the *installed* plugins are already omp-only).

---

## Managing installed plugins

```bash
omp plugin list                                              # show installed
omp plugin uninstall gl-reconciler@claude-for-financial-services --scope project
omp plugin install gl-reconciler@claude-for-financial-services --scope project --force   # reinstall
omp plugin upgrade                                            # reinstall any with newer marketplace versions
omp plugin marketplace list                                  # registered marketplaces
omp plugin marketplace update                                # re-fetch catalog(s)
omp plugin marketplace remove claude-for-financial-services  # unregister
```

| On-disk location | Scope |
|---|---|
| `<repo>/.omp/plugins/installed_plugins.json` | project |
| `~/.omp/plugins/installed_plugins.json` | user |
| `~/.omp/plugins/cache/plugins/<marketplace>___<plugin>___<version>/` | cached copy (both scopes) |
