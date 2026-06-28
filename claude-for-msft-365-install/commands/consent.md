---
description: Azure admin consent URLs — one-time tenant approval for Entra SSO and Outlook Graph access
---

# Azure admin consent

**Only needed when `entra_sso=1`** in the manifest. Gateway and Vertex setups
with org-wide config don't use Entra and can skip this. If you set
`graph_client_id` (your own Entra app), this page doesn't apply either — you
manage consent on your app directly.

One-time per tenant. A Global Admin opens this URL, clicks Accept, done. Until
they do, NAA sign-in inside the add-in fails for every user in the tenant.

## The URL

Same URL for every customer — `/organizations/` resolves the tenant from
whoever signs in. No substitution needed.

```
https://login.microsoftonline.com/organizations/adminconsent?client_id=c2995f31-11e7-4882-b7a7-ef9def0a0266&redirect_uri=https://pivot.claude.ai/auth/callback
```

Print it. Tell them: open in a browser where a **Global Admin** for their
tenant is signed in. They'll see a permissions screen listing what the add-in
reads (user profile, extension attributes). After they click **Accept**, they
land on a confirmation page — "Admin consent granted, you can close this tab."

## Verify

```bash
az ad sp show --id c2995f31-11e7-4882-b7a7-ef9def0a0266 --query appId -o tsv
```

If that returns the same GUID, the service principal exists in their tenant —
consent worked. If it errors with "does not exist", consent didn't complete.

## Outlook — Microsoft Graph consent

**Only needed when deploying the Outlook manifest.** Separate from `entra_sso`
above; required even if `entra_sso` is off.

Claude for Outlook reads mail and calendar through Microsoft Graph. The Graph
token stays in the user's Outlook client and is never sent to the gateway or to
Anthropic, so this consent is the same regardless of which cloud serves the
model. A Global Admin opens the URL, clicks Accept, done.

```
https://login.microsoftonline.com/organizations/v2.0/adminconsent?client_id=c2995f31-11e7-4882-b7a7-ef9def0a0266&scope=https://graph.microsoft.com/Mail.ReadWrite%20https://graph.microsoft.com/Calendars.Read%20https://graph.microsoft.com/People.Read%20https://graph.microsoft.com/User.Read%20offline_access&redirect_uri=https://pivot.claude.ai/auth/callback
```

Without this, every user hits a "Need admin approval" wall the first time
Claude tries to read mail.

**If their policy forbids consenting to a third-party app:** they can register
their own single-tenant Entra app with the same delegated Graph permissions
(Mail.ReadWrite, Calendars.Read, People.Read, User.Read, offline_access), grant
admin consent on it, and pass its client ID as `graph_client_id` when generating
the Outlook manifest. Same data flow; approval lives under their app instead of
Anthropic's.