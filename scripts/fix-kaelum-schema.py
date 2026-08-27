import os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── FRONTMATTER for all 21 agent .md files ────────────────────────
AGENTS = {
  'api-engineer':          'Manages KAELUM Commerce API lifecycle, key issuance, webhooks, sandbox, and health monitoring',
  'compliance-regulatory': 'Audits transactions and platform operations against UK EMR 2011 and AMLD5/6 regulations',
  'content-notification':  'Generates personalised platform communications staged for admin approval before distribution',
  'creator-acquisition':   'Manages high-value creator acquisition pipeline with personalised outreach and audience impact modelling',
  'creator-studio':        'Ai advisor for creators covering listing optimisation, Paylinks, Commerce Drops, and creator support',
  'cybersecurity':         'Cross-system security monitoring across infrastructure, application, API, and user account layers',
  'finance':               'Financial intelligence covering budget tracking, revenue dashboards, cash flow forecasting, and investor reports',
  'fraud-scam-detection':  'Real-time anomaly detection and SENTINEL risk scoring across all KAELUM transactions',
  'kvi-governance':        'Quarterly ecosystem health assessment against the KVI Framework with appreciation recommendations',
  'legal-counsel':         'Ai legal advisor generating contracts, monitoring regulatory obligations, and maintaining legal risk register',
  'merchant-acquisition':  'Manages Founding Merchant KST slot acquisition pipeline with personalised outreach and proposal generation',
  'merchant-performance':  'Analyses daily merchant activity, transaction volumes, customer retention, and strategic recommendations',
  'merchant-support':      '24/7 Ai-powered support for KAELUM merchants covering redemption, KST, payments, and account management',
  'onboarding-concierge':  'Stateful agent guiding Customer, Creator, and Merchant accounts through KYC to first transaction',
  'people-operations':     'Manages K.A.T.E. agent fleet roster, contractor relationships, credit budgets, and operational reporting',
  'platform-engineer':     'Manages feature build queue, bug tracker, and deployment protocol for kaelum.app on Base44',
  'platform-health':       'Continuous monitoring of API response times, transaction success rates, and system health indicators',
  'quality-assurance':     'Automated test suites, compliance scans, performance benchmarks, and E2E user journey testing',
  'research-scout':        'Autonomous market intelligence monitoring competitor activity, regulatory changes, and investor landscape',
  'transaction-insights':  'Aggregates and enriches transaction data surfacing spending trends, patterns, and KVI metrics',
  'user-personal':         'Dedicated per-user commerce assistant operating on Observe, Recommend, or Autonomous permission tiers',
}

print("Adding frontmatter to agent .md files...")
for slug, desc in AGENTS.items():
    path = ROOT / 'plugins' / 'agent-plugins' / slug / 'agents' / f'{slug}.md'
    if not path.exists():
        print(f"  SKIP (not found): {slug}")
        continue
    content = path.read_text(encoding='utf-8')
    if content.startswith('---'):
        print(f"  SKIP (already has frontmatter): {slug}")
        continue
    frontmatter = f'---\nname: kaelum-{slug}\ndescription: >-\n  {desc}\n---\n\n'
    path.write_text(frontmatter + content, encoding='utf-8')
    print(f"  OK: {slug}")

# ── COOKBOOK FILES for 8 KAELUM cookbooks ─────────────────────────
COOKBOOKS = {
  'audivo-transaction': {
    'desc': 'Executes KLM transfer logic for every validated KAELUM transaction after SENTINEL clearance',
    'api_mode': 'standard_api', 'model': 'claude-haiku-4-5',
    'example_input': 'Execute KLM transfer: sender kaelum_user_001, merchant kaelum_merchant_001, amount 100 KLM, SENTINEL token abc123',
    'example_output': 'Transaction completed. Receipt: txn_001, 100 KLM transferred, 1.2 KLM TPR allocated to KPR, clearance confirmed.'
  },
  'commerce-drop-moderation': {
    'desc': 'Reviews all Commerce Drop listings before publication for prohibited content and regulatory compliance',
    'api_mode': 'managed_agent', 'model': 'claude-sonnet-4-6',
    'example_input': 'Review this Commerce Drop listing: Title: Exclusive Art Print, Description: Limited edition digital artwork, Price: 500 KLM',
    'example_output': 'Listing approved. No prohibited content detected. Regulatory language compliant. Ready for publication.'
  },
  'invoice-to-insights': {
    'desc': 'Parses invoices and transforms them into actionable financial intelligence for merchants and creators',
    'api_mode': 'managed_agent', 'model': 'claude-sonnet-4-6',
    'example_input': 'Parse this invoice: Supplier: ABC Print Co, Amount: £450, Due: 2026-06-01, Items: 500 printed cards',
    'example_output': 'Invoice parsed. Category: Marketing/Print. Cash flow impact: -£450 in 24 days. Reconciliation: no matching KAELUM transaction found. Recommendation: settle within 14 days to maintain supplier terms.'
  },
  'kate-chatbot': {
    'desc': 'Public-facing K.A.T.E. conversational interface for kaelum.app visitors answering questions about KAELUM',
    'api_mode': 'standard_api', 'model': 'claude-sonnet-4-6',
    'example_input': 'Is KAELUM a cryptocurrency?',
    'example_output': 'No. KAELUM is fundamentally different from cryptocurrency. KLM is an Ai-governed, non-crypto, closed-loop digital commerce currency with a fixed floor price of £0.09, regulated under UK electronic money law. There is no blockchain, no speculation, and no exchange trading.'
  },
  'kate-orchestrator': {
    'desc': 'Routes incoming Paperclip events to the correct K.A.T.E. agent or functional handler',
    'api_mode': 'standard_api', 'model': 'claude-haiku-4-5',
    'example_input': 'Event received: { "event": "transaction_event", "payload": { "transaction_ref": "txn_001" } }',
    'example_output': '{ "routed_to": "fraud-scam-detection", "status": "dispatched", "timestamp": "2026-05-07T10:00:00Z" }'
  },
  'kst-assessment': {
    'desc': 'Assesses KST sub-token ownership applications and produces CEO-ready recommendation reports',
    'api_mode': 'managed_agent', 'model': 'claude-sonnet-4-6',
    'example_input': 'Assess KST application: Applicant: Merchant A, KYC verified 45 days ago, SENTINEL clean, business turnover £800K/year, proposes to circulate sub-token across 200 retail locations',
    'example_output': 'Score: 13/15. Recommendation: Approved. Strong applicant verification, credible circulation network, adequate financial capacity. Regulatory alignment confirmed. Recommend CEO sign-off.'
  },
  'sentinel-batch': {
    'desc': 'Daily batch analysis of all transactions for AML patterns, SAR candidates, and compliance intelligence',
    'api_mode': 'managed_agent', 'model': 'claude-sonnet-4-6',
    'example_input': 'Run SENTINEL compliance batch for 2026-05-07. Total transactions: 1,247. Date range: 00:00-23:59 UTC.',
    'example_output': 'Batch complete. 1,247 transactions scanned. Flags: 3 medium (velocity), 1 high (structuring pattern). SAR candidates: 1 (transaction ref txn_891). New patterns: none. Recommended actions: review txn_891 for SAR filing.'
  },
  'sentinel-per-transaction': {
    'desc': 'Real-time SENTINEL risk scoring for every KAELUM transaction before execution clearance',
    'api_mode': 'standard_api', 'model': 'claude-haiku-4-5',
    'example_input': 'Score transaction: sender_id user_001, merchant_id merchant_042, amount 850 KLM, device_fingerprint abc, ip 82.1.2.3, timestamp 2026-05-07T14:23:00Z',
    'example_output': '{ "score": 22, "clearance": "cleared", "clearance_token": "tok_abc123", "flags": [] }'
  },
}

print("\nCreating missing cookbook files...")
for slug, cfg in COOKBOOKS.items():
    cb_dir = ROOT / 'managed-agent-cookbooks' / slug
    cb_dir.mkdir(exist_ok=True)

    # agent.yaml
    yaml_path = cb_dir / 'agent.yaml'
    if not yaml_path.exists():
        yaml_content = f"""name: kaelum-{slug}
description: >-
  {cfg['desc']}
model: {cfg['model']}
api_mode: {cfg['api_mode']}
system_prompt_file: {slug}.md
"""
        yaml_path.write_text(yaml_content, encoding='utf-8')
        print(f"  Created: {slug}/agent.yaml")

    # README.md
    readme_path = cb_dir / 'README.md'
    if not readme_path.exists():
        readme_content = f"""# {slug.replace('-', ' ').title()}

{cfg['desc']}

## API Mode
{cfg['api_mode']} | Model: {cfg['model']}

## Part of
KAELUM K.A.T.E. Architecture | Kaelum Technologies Ltd
"""
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"  Created: {slug}/README.md")

    # steering-examples.json
    examples_path = cb_dir / 'steering-examples.json'
    if not examples_path.exists():
        examples = [{"input": cfg['example_input'], "output": cfg['example_output']}]
        examples_path.write_text(
            json.dumps(examples, indent=2), encoding='utf-8'
        )
        print(f"  Created: {slug}/steering-examples.json")

print("\nDone. Run python scripts/check.py to verify.")