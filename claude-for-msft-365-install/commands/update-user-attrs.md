---
description: Set per-user config (tokens, region overrides) via Azure AD extension attributes
---

# Per-user config via extension attributes

The eight attributes below are already registered on Anthropic's app
(`c2995f31-…`) — you don't create schema, you just write values. You write
`extension_c2995f3111e74882b7a7ef9def0a0266_<key>` on the user with Graph; the
add-in reads it back as the `extn.<key>` claim in the user's ID token.

**Requires `entra_sso=1` in the manifest.** Without it the add-in never
acquires an Entra token, so these attributes are never read — they silently do
nothing.

**Only these eight keys work this way on Anthropic's app** — it issues `extn.*`
claims for no other attribute, so a value under any other attribute name never
reaches the add-in. Attrs override manifest params, and a [bootstrap](bootstrap.md)
response overrides both. All values are 256 chars max.

| Key | Per-user use case |
|---|---|
| `gateway_token` | Per-user API key (rotation) |
| `gateway_url` | Route different teams to different gateways |
| `gcp_project_id` | Different teams on different GCP projects |
| `gcp_region` | Data-residency override |
| `google_client_id` `google_client_secret` | Different OAuth client per team (uncommon) |
| `aws_role_arn` `aws_region` | Different Bedrock roles by team |

On Anthropic's app, anything else that varies per user — `azure_api_key`,
`disabled_features`, `available_models`, `inference_headers`,
`gateway_api_format`, the `otlp_*` telemetry keys — goes in a
[bootstrap endpoint](bootstrap.md) response, and `bootstrap_url` itself goes in
the manifest, one value for everyone; the endpoint tells users apart by the
Entra token it validates.

**Bring-your-own Entra app (`graph_client_id`):** the token comes from *your*
app, so the `extension_c2995f31…_<key>` attributes do nothing there. Either use
a bootstrap endpoint, or, for each key you need, register a directory extension
on your app named exactly as the config key, add it as an ID-token optional
claim (it reaches the add-in as `extn.<key>`), and swap your app's ID (no
hyphens) into the `extension_…_<key>` commands below. Any config key works this
way except `entra_sso`, `graph_client_id`, `graph_cloud`, `entra_scope`,
`gateway_auth_source` and `allow_1p`, which the add-in reads from the manifest
only. The 256-character limit still applies, so a longer value, such as most
`access_policies` arrays, goes in the manifest or a bootstrap response.

## One user

Substitute `<key>` with the attribute name from the table. For non-secret keys
(regions, project IDs) this is the normal path. For secrets (`gateway_token`,
`google_client_secret`) the value lands in shell history and this conversation's
transcript — use the bulk CSV path below if that's a problem.

```bash
az rest --method PATCH \
  --uri "https://graph.microsoft.com/v1.0/users/<upn>" \
  --body '{"extension_c2995f3111e74882b7a7ef9def0a0266_<key>":"<value>"}'
```

Success is silent — PATCH returns 204 with an empty body. To verify:

```bash
az rest --method GET --uri "https://graph.microsoft.com/v1.0/users/<upn>?\$select=extension_c2995f3111e74882b7a7ef9def0a0266_<key>"
```

Graph reads are immediately consistent with the write — no lag. To dump every
extension attr on a user (without knowing exact key names), use `/beta/`:

```bash
az rest --method GET --uri "https://graph.microsoft.com/beta/users/<upn>" | jq 'to_entries | map(select(.key | startswith("extension"))) | from_entries'
```

## Bulk (CSV, values never enter this chat)

Have the admin prepare `users.csv`. First column is UPN; remaining column
headers are the attribute keys. Empty cells skip that attr for that user.

```
upn,gateway_token,gcp_region
alice@acme.com,sk-live-aaa,
bob@acme.com,sk-live-bbb,europe-west4
carol@acme.com,,europe-west4
```

**macOS/Linux** — write this to `apply.sh` next to their CSV (the `read -a` array syntax is
bash-only; a bare paste into zsh breaks). They review it, then run
`bash apply.sh`. You only see ✓/✗ — don't `cat` either file.

```bash
#!/bin/bash
EXT=extension_c2995f3111e74882b7a7ef9def0a0266_
{
  IFS=, read -ra keys
  while IFS=, read -ra vals; do
    upn="${vals[0]}"
    for i in "${!keys[@]}"; do
      [ "$i" -eq 0 ] || [ -z "${vals[$i]}" ] && continue
      az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/users/$upn" \
        --body "{\"${EXT}${keys[$i]}\":\"${vals[$i]}\"}" \
        && echo "✓ $upn ${keys[$i]}" || echo "✗ $upn ${keys[$i]}"
    done
  done
} < users.csv
```

**Windows** — write this to `apply.ps1` next to their CSV. `Import-Csv` reads
the header as the schema directly; they run `.\apply.ps1` in PowerShell.

```powershell
$EXT = 'extension_c2995f3111e74882b7a7ef9def0a0266_'
Import-Csv users.csv | ForEach-Object {
  $upn = $_.upn
  $_.PSObject.Properties | Where-Object { $_.Name -ne 'upn' -and $_.Value } | ForEach-Object {
    $body = @{ "$EXT$($_.Name)" = $_.Value } | ConvertTo-Json -Compress
    az rest --method PATCH --uri "https://graph.microsoft.com/v1.0/users/$upn" --body $body
    if ($?) { "OK $upn $($_.Name)" } else { "FAIL $upn $($_.Name)" }
  }
}
```

Report the ✓ and ✗ counts. 404 means the UPN is wrong; 403
means `az login` lacks `User.ReadWrite.All` — they need to re-consent or use
an admin account.

## Propagation delay

Graph writes succeed immediately, but the add-in reads these via the user's
ID token at NAA sign-in — and Azure's STS caches token claims. Expect **up to
an hour** before the new value appears for a given user. If they open the
add-in right after the PATCH and it behaves as if unconfigured, that's the
cache, not a failure. Tell them to wait and retry; quitting the Office app
fully (not just closing the taskpane) forces a fresh NAA token on next launch.
