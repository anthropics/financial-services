# Contributing to Claude for Financial Services

Thanks for improving the financial-services plugins and managed-agent templates.
This repository contains reference workflows, not investment, legal, tax, or
accounting advice. Keep every contribution consistent with that boundary:
outputs must remain reviewable by a qualified human and must not execute
transactions, post to a ledger, or approve an onboarding decision.

## Before you start

- Search open issues and pull requests for related work. Issue creation may be
  restricted, so add reproduction details to an existing report instead of
  opening a duplicate.
- Keep each pull request focused on one user-visible fix or improvement.
- Do not include client data, credentials, internal URLs, or proprietary
  financial documents. Use synthetic, anonymized examples only.

## Local setup

Use Python 3.10 or later. The repository checks require PyYAML; cookbook
dry-runs also require `jq` and `zip`.

```bash
git clone https://github.com/<your-account>/financial-services.git
cd financial-services
git remote add upstream https://github.com/anthropics/financial-services.git
git fetch upstream
python3 -m pip install pyyaml
git switch -c fix/short-description upstream/main
```

If you are contributing to a fork with a different upstream, substitute that
repository in the commands above.

## Repository conventions

### Skills and agents

- Author skills in `plugins/vertical-plugins/<vertical>/skills/`.
- Agent bundles under `plugins/agent-plugins/<slug>/skills/` are generated
  copies. Do not hand-edit them. After changing a source skill, run:

  ```bash
  python3 scripts/sync-agent-skills.py
  ```

- Keep an agent's system prompt in
  `plugins/agent-plugins/<slug>/agents/<slug>.md`. Its matching managed-agent
  cookbook should reference that canonical prompt and bundled skills.

### Plugin manifests

- Keep every JSON and YAML manifest valid and use two-space indentation.
- A plugin changed in a pull request must receive a patch-version bump in its
  `.claude-plugin/plugin.json`; otherwise installed users will not receive the
  update. `python3 scripts/check.py` installs the repository pre-commit hook,
  which applies this bump for staged plugin changes. Always review the staged
  manifest before committing.
- Empty hook configuration must use the supported shape:

  ```json
  { "hooks": {} }
  ```

  Do not use an empty array.

### Managed-agent safety

- Treat external documents as untrusted input.
- Preserve the existing separation between readers of untrusted material and
  workers that can access internal systems or write output files.
- Bound and schema-validate data crossing a subagent or cross-agent boundary.

## Validate before opening a pull request

Run the checks applicable to your change from the repository root:

```bash
python3 scripts/check.py
bash scripts/test-cookbooks.sh
```

For a plugin-manifest change, additionally validate the changed JSON and, when
Claude Code is available, install the plugin from a local marketplace and
confirm it loads successfully.

```bash
python3 -m json.tool plugins/vertical-plugins/<plugin>/hooks/hooks.json
claude plugin marketplace add .
claude plugin install <plugin>@claude-for-financial-services
claude plugin list
```

Do not run deployments against a production account as a pull-request test.
Use `scripts/deploy-managed-agent.sh <slug> --dry-run` for cookbook changes.

## Pull request expectations

Use a descriptive branch and a conventional commit message, for example:

```text
fix(plugins): correct empty hook manifest schema
```

Your PR description should include:

1. The user-facing problem and its reproduction.
2. The files and behaviour changed.
3. Related issue or PR links, including why the work is not a duplicate.
4. Exact validation commands and their results.
5. Any plugin versions changed and any follow-up work deliberately excluded.

Suggested PR body:

```markdown
## Summary
- <user-visible fix>
- <scope kept intentionally out of this PR>

## Reproduction and resolution
<what failed before, why it failed, and why this change resolves it>

## Validation
- [x] `python3 scripts/check.py`
- [x] `bash scripts/test-cookbooks.sh` (when applicable)
- [x] <targeted manual test>

## Compatibility
- Plugin versions bumped: `<plugin> <old> → <new>`
- No API, credential, or external-provider configuration changes
```

Respond to review feedback with follow-up commits; avoid force-pushing a
rewritten branch after reviewers have started work unless they ask for it.
