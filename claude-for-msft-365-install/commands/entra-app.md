# Register your own Entra app

Several manifest configurations require an Entra (Azure AD) app registration in
**your** tenant rather than Anthropic's default multi-tenant app — because the
token's `aud` must match a resource you control, or because your tenant is in a
sovereign cloud where Anthropic's app doesn't exist. This page is the single
set of registration steps; the per-feature docs link here and tell you which
row of the permissions table applies.

You need this when setting any of:

| Manifest key | Why your own app |
|---|---|
| `graph_client_id` (Outlook) | Graph permissions are consented against your app, not Anthropic's |
| `entra_scope` | Access token must be audienced to *your* API resource |
| `gateway_auth_source=entra` | Gateway validates a token audienced to your API |
| `graph_cloud` ≠ `global` | Anthropic's app exists only in the commercial cloud |

## Register the app

In [Entra admin center](https://entra.microsoft.com) → *App registrations* →
*New registration*. Single-tenant. The simplest topology is one app acting as
both client (the add-in signs in as it) and resource (your backend validates
tokens audienced to it); split into two if your policy requires.

### 1. Redirect URIs

*Authentication* → *Add a platform* → **Single-page application** → add
**both**:

| URI | Used by |
|---|---|
| `brk-multihub://pivot.claude.ai` | [NAA broker](https://learn.microsoft.com/office/dev/add-ins/develop/enable-nested-app-authentication-in-your-add-in) — desktop Office and Outlook web. Missing this → `AADSTS50011` at sign-in. |
| `https://pivot.claude.ai/msal-redirect.html` | SPA fallback — Excel/Word/PowerPoint on Office for the web, which don't inject the NAA bridge. |

Both go under the SPA platform (not Web, not Mobile/desktop).

### 2. Permissions / API setup

What you configure here depends on what the token is for:

| Use case | Configure |
|---|---|
| **Outlook (Graph)** | *API permissions* → *Microsoft Graph* → Delegated → `Mail.ReadWrite`, `Calendars.Read`, `People.Read`, `User.Read`, `offline_access`. |
| **Gateway / bootstrap auth** (`entra_scope`, `gateway_auth_source=entra`) | *Expose an API* → set Application ID URI `api://<app-guid>` → *Add a scope* (e.g. `access_as_user`, admin-consent enabled). Then *API permissions* → *My APIs* → add that scope as a delegated permission (the app to itself, in single-app topology). |
| **Bedrock WIF** (`aws_role_arn`) | No API permissions needed — the ID token alone is the web identity. |

In all cases finish with *API permissions* → **Grant admin consent for
&lt;tenant&gt;**. Without it every user sees a consent prompt (or is blocked, if
user consent is disabled).

### 3. Token version

Only if you set up *Expose an API* above: in the app *Manifest*, set
`"accessTokenAcceptedVersion": 2`. Leave it unset and Entra issues v1.0 access
tokens (`iss` without `/v2.0`, no `preferred_username`), which most JWT
middleware rejects by default.

## What your backend validates

For `entra_scope` / `gateway_auth_source=entra`, the access token the add-in
sends as `Authorization: Bearer` carries:

| Claim | Expected |
|---|---|
| `iss` | `https://login.microsoftonline.com/<tenant-id>/v2.0` |
| `aud` | your Application ID URI (`api://<app-guid>`) |
| `scp` | the scope(s) you exposed, space-separated |
| JWKS | `https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys` |

## GCC High / DoD / 21Vianet

Same steps, different portal and endpoints — apps don't replicate across
Microsoft national clouds.

- **Register at** [`portal.azure.us`](https://portal.azure.us) (US Gov) or
  [`portal.azure.cn`](https://portal.azure.cn) (21Vianet), not the commercial
  portal.
- **Redirect URIs** are unchanged — `brk-multihub://pivot.claude.ai` and
  `https://pivot.claude.ai/msal-redirect.html`. The add-in is served from the
  same domain in every cloud.
- **Manifest** — add `graph_cloud=us-gov-high` (or `us-gov-dod`, `china`) per
  the [sovereign clouds](manifest.md#sovereign--national-clouds-gcc-high-dod-21vianet)
  table.
- **Admin consent URL** uses the sovereign authority:
  `https://login.microsoftonline.us/<tenant-id>/adminconsent?client_id=<app-id>`
- **Backend validation** — the token's `iss` and JWKS use the `.us` host:
  `https://login.microsoftonline.us/<tenant-id>/v2.0` and
  `https://login.microsoftonline.us/<tenant-id>/discovery/v2.0/keys`. A
  validator pinned to `.com` rejects every request. The same applies to any AWS
  OIDC identity provider in the chain.

## Troubleshooting

**`AADSTS50011` (redirect URI mismatch)** — one of the two URIs above is
missing, or was added under the wrong platform (must be SPA).

**`Tag: 9n156` on Outlook for Mac** — the host's auth broker can't complete.
Almost always a sovereign-cloud account hitting an app registered in commercial
(fix: register in `portal.azure.us` and set `graph_cloud`). If the app is
already in the right cloud, check Conditional Access — the deprecated *Require
approved client app* grant blocks NAA. The Correlation Id in the dialog is
resolvable in your Entra sign-in logs, not Anthropic's.

**`AADSTS65001` (consent required)** — *Grant admin consent* wasn't clicked, or
a permission was added after consent was granted (re-grant).
