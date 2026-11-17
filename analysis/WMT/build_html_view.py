"""
Generate a tablet-friendly HTML view of the WMT deck content.
Single self-contained file with PNGs embedded as base64. Mirrors the 18-slide
deck as vertically-scrolling cards optimized for mobile/tablet portrait.

Run after build_deck.py (needs charts/comp_sales.png and charts/positioning.png).
"""
import base64
from pathlib import Path
HERE = Path(__file__).parent

def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")

comp_b64        = b64(HERE / "charts" / "comp_sales.png")
positioning_b64 = b64(HERE / "charts" / "positioning.png")

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
<title>Walmart — Competitive Analysis</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {{
    --navy: #17365D;
    --gold: #FFC220;          /* Walmart spark accent */
    --ink: #1f2937;
    --ink-2: #6b7280;
    --bg: #f8fafc;
    --card: #ffffff;
    --border: #e5e7eb;
    --good: #2E7D32;
    --bad: #C0392B;
    --warn: #d97706;
  }}
  html, body {{ background: var(--bg); color: var(--ink); font-family: ui-serif, Georgia, 'Times New Roman', serif; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  .slide-num {{ font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #b88e0a; font-weight: 600; }}
  h2.slide-title {{ font-family: ui-serif, Georgia, serif; font-size: 1.35rem; line-height: 1.3; color: var(--navy); font-weight: 700; margin-top: 0.25rem; }}
  .pill {{ display:inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.72rem; font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; letter-spacing: 0.02em; }}
  .pill-good {{ background: #dcfce7; color: #166534; }}
  .pill-warn {{ background: #fef3c7; color: #92400e; }}
  .pill-bad  {{ background: #fee2e2; color: #991b1b; }}
  .pill-navy {{ background: #dbeafe; color: #1e40af; }}
  .pill-gold {{ background: #fff7d6; color: #8a6a00; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th {{ background: var(--navy); color: #fff; padding: 8px 10px; text-align: left; font-weight: 600; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.8rem; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  tr:nth-child(even) td {{ background: #f9fafb; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  ul.dot {{ list-style: none; padding: 0; }}
  ul.dot li {{ position: relative; padding-left: 1.1em; margin: 0.4em 0; line-height: 1.55; }}
  ul.dot li::before {{ content: "\\2022"; color: #b88e0a; position: absolute; left: 0; font-weight: 700; }}
  .stage-pill {{ background: var(--navy); color: #fff; border-radius: 6px; padding: 6px 8px; font-size: 0.75rem; text-align: center; font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; }}
  .tier-bar {{ width: 4px; border-radius: 4px; }}
  .source {{ font-size: 0.72rem; color: var(--ink-2); font-style: italic; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid var(--border); }}
  .dots-3 {{ color: var(--good); }}
  .dots-2 {{ color: var(--warn); }}
  .dots-1 {{ color: var(--bad); }}
  .toc a {{ display: block; padding: 6px 0; color: var(--ink); border-bottom: 1px solid #f1f5f9; font-size: 0.85rem; }}
  .toc a:hover {{ color: #b88e0a; }}
  .toc-num {{ color: #b88e0a; font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; margin-right: 8px; font-size: 0.75rem; }}
  details summary {{ cursor: pointer; padding: 8px 12px; background: #f1f5f9; border-radius: 8px; font-weight: 600; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.9rem; }}
  @media (min-width: 1024px) {{
    .layout-2col {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.5rem; }}
    .layout-3col {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }}
  }}
</style>
</head>
<body class="antialiased">

<header class="bg-[var(--navy)] text-white">
  <div class="max-w-3xl mx-auto px-5 py-6">
    <div class="text-xs uppercase tracking-widest" style="color:var(--gold);">NYSE: WMT &middot; Investment Decision Frame</div>
    <h1 class="text-3xl font-bold mt-2">Walmart Inc.</h1>
    <div class="text-base mt-1 opacity-90">Competitive Landscape &amp; Investment Read</div>
    <div class="text-xs mt-3 opacity-70">As of May 2026 &middot; 18 sections</div>
  </div>
</header>

<!-- TOC -->
<nav class="max-w-3xl mx-auto px-5 py-5">
  <details>
    <summary>Jump to section</summary>
    <div class="toc mt-3 px-2">
      <a href="#s1"><span class="toc-num">01</span>Title / cover</a>
      <a href="#s2"><span class="toc-num">02</span>Executive summary</a>
      <a href="#s3"><span class="toc-num">03</span>The question</a>
      <a href="#s4"><span class="toc-num">04</span>Market context — comp sales</a>
      <a href="#s5"><span class="toc-num">05</span>Industry economics</a>
      <a href="#s6"><span class="toc-num">06</span>Walmart profile</a>
      <a href="#s7"><span class="toc-num">07</span>WMT moats</a>
      <a href="#s8"><span class="toc-num">08</span>Peer set</a>
      <a href="#s9"><span class="toc-num">09</span>2×2 positioning</a>
      <a href="#s10"><span class="toc-num">10</span>Costco deep dive</a>
      <a href="#s11"><span class="toc-num">11</span>Target / Kroger / BJ</a>
      <a href="#s12"><span class="toc-num">12</span>Amazon context</a>
      <a href="#s13"><span class="toc-num">13</span>Comparative scoreboard</a>
      <a href="#s14"><span class="toc-num">14</span>Strategic synthesis &amp; moats</a>
      <a href="#s15"><span class="toc-num">15</span>Bull / Base / Bear</a>
      <a href="#s16"><span class="toc-num">16</span>Catalysts timeline</a>
      <a href="#s17"><span class="toc-num">17</span>Decision frame</a>
      <a href="#s18"><span class="toc-num">18</span>Sources &amp; caveats</a>
    </div>
  </details>
</nav>

<main class="max-w-3xl mx-auto px-5 pb-16 space-y-5">

<section id="s2" class="card p-5">
  <div class="slide-num">Slide 02 &middot; Executive Summary</div>
  <h2 class="slide-title">Scale + omnichannel flywheel + ad/marketplace mix = a re-rating story, not a retail story</h2>
  <div class="mt-4 space-y-4 text-sm">
    <div><span class="pill pill-navy">1. The setup</span><p class="mt-2">Walmart is the largest retailer on earth (~$685B TTM revenue) and the only grocery-anchored peer compounding ad + marketplace + membership revenue at 20–30% annual growth — three tiers structurally higher-margin than core retail.</p></div>
    <div><span class="pill pill-gold">2. The flywheel</span><p class="mt-2">Stores + supply chain → low-cost grocery → traffic → high-margin ad inventory (Walmart Connect ~$5B run-rate) → marketplace 3P GMV → Walmart+ subscription. None of WMT's pure-play peers (COST, KR, BJ, TGT) replicate the full stack.</p></div>
    <div><span class="pill pill-warn">3. The risk</span><p class="mt-2">Stock at ~$95 (~$765B market cap, ~26x TTM EPS) is no longer 'cheap defensive.' Re-rating depends on continued ad/marketplace growth, consumer holding up through a soft-landing year, and Amazon not pressing harder into grocery.</p></div>
    <div><span class="pill pill-good">4. The read</span><p class="mt-2">Long thesis intact for the margin-mix re-rating; key question is duration. Pair against COST (premium peer) for relative-value framing. Avoid if you believe US consumer downtrades meaningfully in 2H 2026.</p></div>
  </div>
  <div class="source">Sources: WMT Q1 FY26 10-Q and IR commentary (May 2026); StockAnalysis.com.</div>
</section>

<section id="s3" class="card p-5">
  <div class="slide-num">Slide 03 &middot; The Question</div>
  <h2 class="slide-title">The question this analysis answers</h2>
  <blockquote class="mt-4 pl-4 border-l-4 border-[var(--gold)] text-base italic" style="color:var(--navy);">
    "Is Walmart's ad/marketplace/membership margin mix worth a premium re-rating from the 18–20x P/E of legacy mass-merch — and is the current ~26x TTM P/E a reasonable entry on that thesis?"
  </blockquote>
  <div class="mt-5 text-sm">
    <div class="font-semibold" style="color:var(--ink);">We test that question across five lenses:</div>
    <ol class="mt-2 space-y-1 pl-5 list-decimal">
      <li><b>Market</b> — is the US retail / e-com / retail-media environment supportive?</li>
      <li><b>Competitive</b> — does WMT have a defensible position vs warehouse clubs, mass merch, and AMZN?</li>
      <li><b>Financial</b> — what does the valuation look like vs peer comps?</li>
      <li><b>Strategic</b> — what's the moat and how durable is it?</li>
      <li><b>Decision</b> — what's the cleanest expression of conviction (or wait)?</li>
    </ol>
  </div>
</section>

<section id="s4" class="card p-5">
  <div class="slide-num">Slide 04 &middot; Market Context</div>
  <h2 class="slide-title">US retail $5T+; grocery share gains, e-com inflecting, retail-media the high-margin tier expanding fastest</h2>
  <img src="data:image/png;base64,{comp_b64}" alt="US comparable sales — Q1 FY26 by peer" class="mt-4 rounded-lg border border-[var(--border)] w-full" />
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What the chart says</div>
    <ul class="dot mt-2">
      <li>Warehouse clubs (COST, BJ) lead on comp-sales growth — membership pricing power + value-trade-down winners.</li>
      <li>WMT US comp <b>+4.5%</b> — above-trend mass-merch; outpaces TGT 2x.</li>
      <li>KR shows grocery still positive but slow; TGT lagging.</li>
      <li>AMZN omitted — no comparable-store metric, but online retail growing ~10% YoY.</li>
      <li>US retail-media ad spend ~$60B in 2025; growing ~20% YoY (eMarketer, IAB).</li>
    </ul>
  </div>
  <div class="source">Comp sales: each issuer's Q1 FY26 IR releases; ex-fuel/gas. Retail-media TAM: eMarketer / IAB (2025).</div>
</section>

<section id="s5" class="card p-5">
  <div class="slide-num">Slide 05 &middot; Industry Economics</div>
  <h2 class="slide-title">Grocery thin, general merch better; ads + 3P marketplace + membership are the margin pools</h2>
  <div class="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-2">
    {''.join(f'<div class="stage-pill">{s}</div>' for s in ["Grocery / Food","Consumables","General Merch","Apparel / Home","3P Marketplace","Ads + Mbrshp"])}
  </div>
  <table class="mt-4">
    <thead><tr><th>Tier</th><th>Typical EBIT margin</th><th>WMT presence</th></tr></thead>
    <tbody>
      <tr><td>Grocery / Food</td><td class="num">2–4%</td><td>#1 US</td></tr>
      <tr><td>Consumables</td><td class="num">5–8%</td><td>#1 US</td></tr>
      <tr><td>General Merch</td><td class="num">10–15%</td><td>Top-2</td></tr>
      <tr><td>Apparel / Home</td><td class="num">15–25%</td><td>Mid-tier</td></tr>
      <tr><td>3P Marketplace</td><td class="num">25–40%</td><td>Building, $50B+ GMV</td></tr>
      <tr><td>Ads + Membership</td><td class="num" style="color:var(--good);">60–80%</td><td><b>Connect $5B+ run-rate</b></td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What this means</div>
    <ul class="dot mt-2">
      <li>Grocery anchors the traffic but contributes little to margin. The story-shaping tier is the right two-thirds: <b>ads + 3P marketplace + membership</b>.</li>
      <li>Walmart Connect (ads) is reportedly running at &gt;40% EBIT margin — at $5B run-rate, that's ~$2B incremental EBIT growing 30%+ YoY.</li>
      <li>Amazon proved this template: AMZN advertising compounded to ~$60B TTM — directionally the WMT bull case.</li>
      <li>Costco doesn't play in ads (by design) — the margin lever WMT has, COST does not.</li>
      <li>Kroger's Precision Marketing ~$1.5B annualized vs WMT Connect ~$5B — only direct grocery-ad peer comp.</li>
    </ul>
  </div>
  <div class="source">Industry margin ranges: NRF, Bain, JP Morgan retail primers. Connect figures: WMT mgmt commentary.</div>
</section>

<section id="s6" class="card p-5">
  <div class="slide-num">Slide 06 &middot; Walmart Profile</div>
  <h2 class="slide-title">Q1 FY26: revenue +6%, ad+marketplace tiers compounding 20–30%, EBIT margin +25 bps</h2>
  <table class="mt-4">
    <thead><tr><th>Metric</th><th>Value</th><th>YoY</th></tr></thead>
    <tbody>
      <tr><td>Q1 FY26 revenue</td><td class="num">~$165B</td><td class="num" style="color:var(--good);">+6%</td></tr>
      <tr><td>Walmart US comp sales (ex-fuel)</td><td class="num">+4.5%</td><td class="num">—</td></tr>
      <tr><td>WMT US e-commerce</td><td class="num">~$110B run-rate</td><td class="num" style="color:var(--good);">+20%+</td></tr>
      <tr><td>Walmart Connect (ads)</td><td class="num">~$5B run-rate</td><td class="num" style="color:var(--good);">+30%+</td></tr>
      <tr><td>Marketplace 3P GMV</td><td class="num">~$50B+</td><td class="num" style="color:var(--good);">+30%+</td></tr>
      <tr><td>Membership rev (Sam's + Walmart+)</td><td class="num">~$3B</td><td class="num" style="color:var(--good);">Sam's +9%</td></tr>
      <tr><td>TTM revenue</td><td class="num">~$685B</td><td class="num">—</td></tr>
      <tr><td>TTM EBITDA / margin</td><td class="num">~$45B / ~6.6%</td><td class="num">—</td></tr>
      <tr><td>Market cap</td><td class="num">~$765B</td><td class="num">—</td></tr>
      <tr><td>P/E (TTM)</td><td class="num">~26x</td><td class="num">vs 5-yr avg ~22x</td></tr>
    </tbody>
  </table>
  <div class="source">Walmart Q1 FY26 release (May 2026); WMT 10-K FY25 (Mar 2026); StockAnalysis.com.</div>
</section>

<section id="s7" class="card p-5">
  <div class="slide-num">Slide 07 &middot; WMT Moats</div>
  <h2 class="slide-title">WMT moat — supply-chain density + EDLP + Connect ad business form three reinforcing layers</h2>
  <table class="mt-4">
    <thead><tr><th>Layer</th><th>KPI / detail</th></tr></thead>
    <tbody>
      <tr><td>Supply-chain scale</td><td>~4,600 US stores + ~150 DCs; ~90% of US population within 10 miles of a Walmart store</td></tr>
      <tr><td>EDLP price gap</td><td>Averages ~10–15% below TGT/KR on grocery basket (3rd-party tracking)</td></tr>
      <tr><td>Walmart+ subscription</td><td>~$1B revenue tier; bundles grocery delivery, Paramount+, fuel discount — household stickiness</td></tr>
      <tr><td>Marketplace 3P</td><td>~150K active sellers; intl ramp via Flipkart (India) and Mexico</td></tr>
      <tr><td>Walmart Connect (ads)</td><td>~$5B run-rate; ~40%+ EBIT margin per mgmt; growing 30%+ YoY</td></tr>
      <tr><td>Data + media network</td><td>~250M weekly customers → highest-quality first-party shopper-graph in US (vs AMZN's general e-com graph)</td></tr>
      <tr><td>Capex on DCs / automation</td><td>$15–17B annual capex modernizing DCs, automation, freight</td></tr>
      <tr><td>Geographic scale</td><td>Walmart International ~$120B; Mexico (Walmex), India (PhonePe + Flipkart), China</td></tr>
    </tbody>
  </table>
  <div class="source">WMT 10-K FY25; mgmt commentary Q4 FY25 / Q1 FY26; third-party price tracking (Bain, KeyBanc).</div>
</section>

<section id="s8" class="card p-5">
  <div class="slide-num">Slide 08 &middot; Peer Set</div>
  <h2 class="slide-title">Peer set — four strategic groups, three of which WMT competes in directly</h2>
  <div class="mt-4 space-y-3">
    {''.join(f'<div class="flex gap-3"><div class="tier-bar" style="background:{c};"></div><div class="flex-1"><div class="font-semibold" style="color:{c};">{t}</div><ul class="dot mt-1 text-sm">{"".join(f"<li>{i}</li>" for i in items)}</ul></div></div>'
      for t, items, c in [
        ("Tier 1 — Warehouse club premium", ["Costco (Nasdaq: COST) — premium-priced peer, membership economics", "BJ's Wholesale (NYSE: BJ) — smaller-scale COST follower"], "#17365D"),
        ("Tier 2 — Mass-merch / general", ["Walmart (NYSE: WMT) — scale leader, omnichannel + ad mix-shift", "Target (NYSE: TGT) — cheap-chic, smaller scale, lagging comps"], "#b88e0a"),
        ("Tier 3 — Marketplace / digital", ["Amazon (Nasdaq: AMZN) — marketplace + ads + AWS — partial retail comp", "(Shopify, eBay — out of scope for WMT direct competition)"], "#C0392B"),
        ("Tier 4 — Pure-play grocery", ["Kroger (NYSE: KR) — largest US pure-play grocer", "(Albertsons, Sprouts — smaller, excluded for tractability)"], "#7F8C8D"),
      ])}
  </div>
</section>

<section id="s9" class="card p-5">
  <div class="slide-num">Slide 09 &middot; 2×2 Positioning</div>
  <h2 class="slide-title">Scale × E-commerce mix: WMT and AMZN alone in the upper-right; COST premium at lower mix</h2>
  <img src="data:image/png;base64,{positioning_b64}" alt="2x2 positioning matrix" class="mt-4 rounded-lg border border-[var(--border)] w-full" />
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What the matrix says</div>
    <ul class="dot mt-2">
      <li>AMZN sits at the extreme — 100% e-com mix, $650B revenue. Pure-digital, AWS-distorted multiples.</li>
      <li>WMT is the only scaled (&gt;$500B) omnichannel player — ~18% e-com mix and rising, with stores as fulfillment nodes.</li>
      <li>COST sits at ~7.5% e-com — but commands ~40% P/E premium on membership economics alone.</li>
      <li>TGT has higher e-com mix (~20%) than WMT but a tenth of the scale — disadvantaged on supply-chain unit economics.</li>
      <li>KR and BJ are sub-scale on both axes.</li>
    </ul>
  </div>
</section>

<section id="s10" class="card p-5">
  <div class="slide-num">Slide 10 &middot; Costco Deep Dive</div>
  <h2 class="slide-title">Costco — Membership-first peer commanding ~40% P/E premium to WMT</h2>
  <div class="layout-2col mt-4">
    <div>
      <table>
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>
          <tr><td>Market cap</td><td>~$420B</td></tr>
          <tr><td>TTM revenue</td><td>~$270B</td></tr>
          <tr><td>Q3 FY26 comp sales</td><td>+6.2%</td></tr>
          <tr><td>Gross margin</td><td>~12.5%</td></tr>
          <tr><td>EBITDA / margin</td><td>~$13B / ~4.8%</td></tr>
          <tr><td>Net income (TTM)</td><td>~$8B</td></tr>
          <tr><td>P/E (TTM)</td><td>~50x (vs WMT ~26x)</td></tr>
          <tr><td>EV / EBITDA</td><td>~32x (vs WMT ~17x)</td></tr>
          <tr><td>Membership fees</td><td>~$5B TTM</td></tr>
          <tr><td>Renewal rate</td><td>~92–93% US/CA</td></tr>
          <tr><td>E-com mix</td><td>~7.5%</td></tr>
        </tbody>
      </table>
    </div>
    <div class="mt-4 lg:mt-0 text-sm">
      <div class="font-semibold" style="color:var(--navy);">Strengths</div>
      <ul class="dot mt-1"><li>Renewal ~92%+ creates recurring-revenue dynamic</li><li>Pricing power: dues raised in 2024 first time in 7 yrs</li><li>Negative net debt; no leverage risk</li><li>Executive-membership tier acts as ARPU lever</li></ul>
      <div class="font-semibold mt-3" style="color:var(--navy);">Weaknesses</div>
      <ul class="dot mt-1"><li>Limited assortment vs WMT (~3,800 SKUs vs ~120K)</li><li>No ad / retail-media business (by design)</li><li>High US/CA dependence; intl expansion slow</li><li>Premium valuation provides little error margin</li></ul>
      <div class="font-semibold mt-3" style="color:var(--navy);">Strategy</div>
      <ul class="dot mt-1"><li>~25 new warehouses/yr; gradual fee step-ups; slow intl. Avoids the ad lane.</li></ul>
    </div>
  </div>
  <div class="source">Costco FY25 10-K; Q3 FY26 monthly sales releases; StockAnalysis.com.</div>
</section>

<section id="s11" class="card p-5">
  <div class="slide-num">Slide 11 &middot; Target / Kroger / BJ</div>
  <h2 class="slide-title">Mid-tier scale, narrower moats, varying ad-mix progress</h2>
  <div class="layout-3col mt-4 text-sm">
    <div>
      <div class="font-semibold" style="color:#b88e0a;">Target (TGT)</div>
      <ul class="dot mt-2">
        <li><b>Business:</b> Mass-merch cheap-chic; ~1,950 stores</li>
        <li><b>TTM rev / NI:</b> ~$107B / ~$4.2B</li>
        <li><b>Q1 FY26 comp:</b> +2%</li>
        <li><b>Roundel ads:</b> ~$2B run-rate, +25%</li>
        <li><b>E-com mix:</b> ~20%</li>
        <li><b>Read:</b> Cheap multiple, real recovery, but no scale moat</li>
      </ul>
    </div>
    <div class="mt-5 lg:mt-0">
      <div class="font-semibold" style="color:#b88e0a;">Kroger (KR)</div>
      <ul class="dot mt-2">
        <li><b>Business:</b> Largest US pure-play grocer; ~2,700 stores</li>
        <li><b>TTM rev / NI:</b> ~$148B / ~$2.5B</li>
        <li><b>Q1 FY26 ident (ex-fuel):</b> +2.5%</li>
        <li><b>KPM ads:</b> ~$1.5B run-rate</li>
        <li><b>E-com mix:</b> ~10%</li>
        <li><b>Read:</b> Defensive; thin EBITDA margin caps multiple</li>
      </ul>
    </div>
    <div class="mt-5 lg:mt-0">
      <div class="font-semibold" style="color:#b88e0a;">BJ's Wholesale (BJ)</div>
      <ul class="dot mt-2">
        <li><b>Business:</b> Warehouse club; ~245 clubs</li>
        <li><b>TTM rev / NI:</b> ~$22B / ~$0.55B</li>
        <li><b>Q1 FY26 comp (ex-gas):</b> +3.8%</li>
        <li><b>Membership:</b> ~$470M fee revenue</li>
        <li><b>E-com mix:</b> ~5%</li>
        <li><b>Read:</b> Smaller-scale COST follower; discount until renewal-rate parity</li>
      </ul>
    </div>
  </div>
  <div class="source">TGT/KR/BJ Q1 FY26 IR releases; StockAnalysis.com market data.</div>
</section>

<section id="s12" class="card p-5">
  <div class="slide-num">Slide 12 &middot; Amazon Context</div>
  <h2 class="slide-title">Amazon — Comparability caveat (AWS distorts every multiple)</h2>
  <table class="mt-4">
    <thead><tr><th>Metric</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Market cap</td><td>~$2.2T</td></tr>
      <tr><td>TTM consolidated revenue</td><td>~$650B</td></tr>
      <tr><td>TTM EBITDA / margin</td><td>~$160B / ~25%</td></tr>
      <tr><td>TTM net income</td><td>~$65B</td></tr>
      <tr><td>TTM advertising services</td><td>~$60B (<span style="color:var(--good);">+20%+ YoY</span>)</td></tr>
      <tr><td>TTM AWS revenue</td><td>~$110B</td></tr>
      <tr><td>P/E (TTM)</td><td>~33x (vs WMT ~26x)</td></tr>
      <tr><td>EV / EBITDA</td><td>~14x (lower than WMT — AWS lifts EBITDA)</td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Why this matters for WMT</div>
    <ul class="dot mt-2">
      <li>AMZN's $60B ads and ~25% consolidated EBITDA margin are the WMT bull-case template directionally.</li>
      <li>But: AWS is ~70% of consolidated EBIT — strip it out and AMZN retail margin is ~3–4%, BELOW WMT.</li>
      <li>AMZN squeezes WMT specifically on grocery (Whole Foods + Amazon Fresh + same-day Prime grocery).</li>
      <li>Counter: WMT US grocery is 4–5x larger than AMZN grocery; logistics-density advantage remains.</li>
      <li><b>Pair-trade idea:</b> long WMT / short AMZN expresses confidence in stores-as-fulfillment + slowing AWS growth.</li>
    </ul>
  </div>
  <div class="source">AMZN Q1 FY26 earnings; segment reporting; StockAnalysis.com.</div>
</section>

<section id="s13" class="card p-5">
  <div class="slide-num">Slide 13 &middot; Comparative Scoreboard</div>
  <h2 class="slide-title">WMT leads scale &amp; ad-revenue trajectory; lags margin vs COST</h2>
  <div class="overflow-x-auto">
  <table class="mt-4" style="min-width: 720px;">
    <thead><tr><th>Dimension</th><th>WMT</th><th>COST</th><th>TGT</th><th>AMZN</th><th>KR</th><th>BJ</th></tr></thead>
    <tbody>
      <tr><td>Revenue scale (TTM)</td><td>●●● $685B</td><td>●●○ $270B</td><td>●○○ $107B</td><td>●●● $650B</td><td>●●○ $148B</td><td>●○○ $22B</td></tr>
      <tr><td>Comp sales growth</td><td>●●○ +4.5%</td><td>●●● +6.2%</td><td>●○○ +2.0%</td><td>○○○ n/a</td><td>●○○ +2.5%</td><td>●●○ +3.8%</td></tr>
      <tr><td>EBITDA margin</td><td>●●○ ~6.6%</td><td>●●○ ~4.8%</td><td>●●○ ~9.3%</td><td>●●● ~25%</td><td>●○○ ~4.7%</td><td>●○○ ~5.0%</td></tr>
      <tr><td>Ad / retail-media</td><td>●●● $5B+ Connect</td><td>○○○ Not played</td><td>●●○ $2B Roundel</td><td>●●● $60B Ads</td><td>●●○ $1.5B KPM</td><td>○○○ Minimal</td></tr>
      <tr><td>Membership / loyalty</td><td>●●○ WMT+ + Sam's</td><td>●●● $5B fees, 92%+</td><td>●○○ Circle 360 new</td><td>●●● Prime + subs</td><td>○○○ Boost free</td><td>●●○ $470M fees</td></tr>
      <tr><td>Capital intensity</td><td>●●○ Moderate</td><td>●●● Net cash</td><td>●●○ Moderate</td><td>●●○ Moderate</td><td>●○○ Elevated</td><td>●●○ Moderate</td></tr>
      <tr><td>Valuation absorbed</td><td>●●○ ~26x P/E</td><td>●○○ ~50x P/E</td><td>●●● ~17x P/E</td><td>●●○ ~33x P/E</td><td>●●● ~20x P/E</td><td>●●○ ~27x P/E</td></tr>
    </tbody>
  </table>
  </div>
  <div class="source">● = Strong · ○ = Weak. Calibrated against Operating Metrics / Valuation / Retail-Specific tabs in companion .xlsx.</div>
</section>

<section id="s14" class="card p-5">
  <div class="slide-num">Slide 14 &middot; Strategic Synthesis</div>
  <h2 class="slide-title">Moat: scale + data + logistics · Risk: consumer rollover + AMZN grocery</h2>
  <div class="overflow-x-auto">
  <table class="mt-4" style="min-width: 720px;">
    <thead><tr><th>Moat type</th><th>WMT</th><th>COST</th><th>TGT</th><th>AMZN</th><th>KR</th><th>Reading</th></tr></thead>
    <tbody>
      <tr><td>Network effects</td><td>Mod</td><td>Weak</td><td>Weak</td><td><b>Strong</b></td><td>Weak</td><td>WMT marketplace 3P building; AMZN dominant in 3P</td></tr>
      <tr><td>Switching costs</td><td>Mod</td><td><b>Strong</b></td><td>Weak</td><td><b>Strong</b></td><td>Weak</td><td>Membership creates highest switching cost</td></tr>
      <tr><td>Scale economies</td><td><b>Strong</b></td><td>Mod</td><td>Weak</td><td><b>Strong</b></td><td>Weak</td><td>WMT per-unit logistics cost below TGT/KR/BJ</td></tr>
      <tr><td>Intangibles (data)</td><td><b>Strong</b></td><td>Mod</td><td>Mod</td><td><b>Strong</b></td><td>Mod</td><td>First-party shopper data is input to ad-business growth</td></tr>
      <tr><td>Brand / EDLP</td><td><b>Strong</b></td><td><b>Strong</b></td><td>Mod</td><td>Mod</td><td>Mod</td><td>WMT and COST own the value-brand equity</td></tr>
    </tbody>
  </table>
  </div>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Net moat assessment</div>
    <p class="mt-2"><b>Durable advantages:</b> (i) only scaled omnichannel player with grocery anchor, (ii) ad + marketplace + membership all compounding 20–30%, (iii) supply-chain density unmatched ex-AMZN.</p>
    <p class="mt-1"><b>Structural vulnerabilities:</b> (i) consumer downtrade risk, (ii) AMZN pressing on grocery, (iii) Walmart+ subscriber growth opaque, (iv) ~$17B/yr capex crowds free cash flow.</p>
  </div>
</section>

<section id="s15" class="card p-5">
  <div class="slide-num">Slide 15 &middot; Bull / Base / Bear</div>
  <h2 class="slide-title">Outcomes anchored by ad-revenue compounding (upside) and consumer downtrade (downside)</h2>
  <table class="mt-4">
    <thead><tr><th>Scenario</th><th>Prob.</th><th>Key driver</th></tr></thead>
    <tbody>
      <tr><td><span class="pill pill-good">Bull</span></td><td class="num">30%</td><td>Connect → $10B+ run-rate by FY28; Walmart+ subs accelerate; EBIT margin reaches 5.5%; tariff dollar-cost-plus absorbed → P/E re-rates 28–30x; <b>~25% upside</b></td></tr>
      <tr><td><span class="pill pill-navy">Base</span></td><td class="num">50%</td><td>WMT comp +3–5%; Connect/marketplace 25%+ growth continues; EBIT margin 4.5–5%; consumer soft-lands → ~10–15% appreciation 18 mo</td></tr>
      <tr><td><span class="pill pill-bad">Bear</span></td><td class="num">20%</td><td>Consumer downtrade 2H 2026; AMZN grocery compresses WMT comps; tariffs squeeze general-merch GM; Connect decelerates → multiple compresses 20x P/E; <b>15–20% downside</b></td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Signposts to watch</div>
    <ol class="mt-2 space-y-1 pl-5 list-decimal">
      <li>Walmart Connect / marketplace growth on Q2 FY26 call</li>
      <li>US consumer-credit + jobs data through 2H 2026</li>
      <li>Tariff pass-through impact on Q3/Q4 FY26 GM</li>
    </ol>
  </div>
  <div class="source">Probabilities are author's judgment, not consensus.</div>
</section>

<section id="s16" class="card p-5">
  <div class="slide-num">Slide 16 &middot; Catalysts</div>
  <h2 class="slide-title">Catalysts &amp; signposts — 2026 → 2028</h2>
  <table class="mt-4">
    <thead><tr><th>When</th><th>Who</th><th>Event</th></tr></thead>
    <tbody>
      <tr><td>Q2 FY26</td><td><b>WMT</b></td><td>Walmart Connect ad-business breakout disclosure expected</td></tr>
      <tr><td>Q3 FY26</td><td><b>WMT</b></td><td>Holiday season — tariff pass-through visible in gross margin</td></tr>
      <tr><td>H2 2026</td><td>AMZN</td><td>Amazon Fresh / Whole Foods grocery footprint expansion</td></tr>
      <tr><td>FY27</td><td><b>WMT</b></td><td>Sam's Club new-store cadence accelerating (~10+ new clubs)</td></tr>
      <tr><td>FY27</td><td><b>WMT</b></td><td>Walmart+ subscriber count disclosure (rumored)</td></tr>
      <tr><td>FY27</td><td>COST</td><td>Membership-fee increase reset (last raise 2024)</td></tr>
      <tr><td>FY28</td><td><b>WMT</b></td><td>Walmart International — India (Flipkart) IPO timing</td></tr>
      <tr><td><b>FY28</b></td><td><b>WMT</b></td><td><b>EBIT margin tracking towards 5%+ long-term framework</b> — THESIS-CRITICAL</td></tr>
    </tbody>
  </table>
</section>

<section id="s17" class="card p-5">
  <div class="slide-num">Slide 17 &middot; Decision Frame</div>
  <h2 class="slide-title">Four ways to express the Walmart thesis</h2>
  <div class="mt-4 space-y-4 text-sm">
    <div>
      <span class="pill pill-gold">Long WMT outright (highest conviction)</span>
      <p class="mt-2"><b>Triggers:</b> Walmart Connect breakout disclosure on Q2 FY26; sustained 4%+ US comp; EBIT margin tracking ≥4.5%. <b>Risk:</b> consumer downtrade in 2H 2026; AMZN grocery escalation. 18–36 month hold.</p>
    </div>
    <div>
      <span class="pill pill-navy">Pair trade: long WMT / short TGT</span>
      <p class="mt-2"><b>Triggers:</b> WMT comp gap vs TGT widens; tariff pass-through more painful for TGT general-merch; WMT data/scale moat compounds. <b>Risk:</b> TGT mean-reverts faster than WMT compounds. Cleanest scale-divergence trade within mass-merch.</p>
    </div>
    <div>
      <span class="pill pill-warn">Relative value: long WMT / short COST</span>
      <p class="mt-2"><b>Triggers:</b> COST premium narrows as warehouse-club comp slows below WMT; WMT ad business closes margin-mix gap. <b>Risk:</b> COST has shown consistent execution premium — short side may be expensive to carry.</p>
    </div>
    <div>
      <span class="pill pill-bad">Avoid / wait</span>
      <p class="mt-2"><b>Re-enter triggers:</b> (i) Walmart+ subscriber count disclosed and credible vs Prime, (ii) P/E retraces to 22x peer-aligned band, (iii) tariff drag fully embedded. Acknowledges current ~26x P/E prices in significant mix-shift upside.</p>
    </div>
  </div>
  <div class="source">Research / decision framing — not investment advice. Cross-check valuation against a primary terminal before acting.</div>
</section>

<section id="s18" class="card p-5">
  <div class="slide-num">Slide 18 &middot; Sources &amp; Caveats</div>
  <h2 class="slide-title">Sources, data gaps, and caveats</h2>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Primary sources</div>
    <ul class="dot mt-2">
      <li>Walmart Q1 FY26 earnings release and 10-Q (May 2026); WMT 10-K FY25 (Mar 2026)</li>
      <li>Costco — Q3 FY26 monthly sales releases; COST 10-K FY25</li>
      <li>Target — Q1 FY26 earnings; TGT 10-K FY25</li>
      <li>Amazon — Q1 FY26 earnings; AMZN 10-K FY25; segment reporting</li>
      <li>Kroger — Q1 FY26 earnings; KR 10-K FY25</li>
      <li>BJ's Wholesale — Q1 FY26 earnings; BJ 10-K FY25</li>
      <li>Market data: StockAnalysis.com, Yahoo Finance (May 2026)</li>
      <li>Retail-media TAM: eMarketer / IAB US Retail Media report (2025)</li>
      <li>Industry context: Bain, KeyBanc retail primers; NRF; CNBC, Bloomberg coverage</li>
    </ul>
    <div class="font-semibold mt-4" style="color:var(--navy);">Data gaps and caveats</div>
    <ul class="dot mt-2">
      <li><b>MCP data sources</b> (CapIQ / FactSet / Daloopa) were NOT used — plugin connectors not configured. Cross-check before action.</li>
      <li><b>[E] flags</b> in companion .xlsx Inputs tab identify estimated figures with assumption documented in cell comments.</li>
      <li>Walmart Connect ad business is NOT separately disclosed in filings — ~$5B run-rate is aggregated mgmt commentary; range $4–6B.</li>
      <li>Operating-lease liabilities are excluded from Net Debt — material for AMZN (~$80B+); EV understates economic leverage proportionally.</li>
      <li>AMZN consolidated multiples include AWS — they distort a 'retail-only' comparison.</li>
      <li>This is research / decision framing — <b>not investment advice</b>.</li>
    </ul>
  </div>
</section>

</main>

<footer class="bg-[var(--navy)] text-white py-6 mt-8">
  <div class="max-w-3xl mx-auto px-5 text-xs opacity-80 flex justify-between flex-wrap gap-2">
    <span>Walmart competitive analysis · May 2026 · sourced public data</span>
    <span>Research only — not investment advice</span>
  </div>
</footer>

</body>
</html>
"""

OUT = HERE / "WMT-Competitive-Analysis.html"
OUT.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT} ({len(HTML):,} bytes)")
