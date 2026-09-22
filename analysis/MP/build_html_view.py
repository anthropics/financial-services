"""
Generate a tablet-friendly HTML view of the MP deck content.
Single self-contained file with PNGs embedded as base64. Mirrors the 18-slide
deck as vertically-scrolling cards optimized for mobile/tablet portrait.

Run after build_deck.py (needs charts/ndpr.png and charts/positioning.png).
"""
import base64
from pathlib import Path
HERE = Path(__file__).parent

def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")

ndpr_b64       = b64(HERE / "charts" / "ndpr.png")
positioning_b64 = b64(HERE / "charts" / "positioning.png")

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
<title>MP Materials — Competitive Analysis</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {{
    --navy: #17365D;
    --copper: #B26B1E;
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
  .slide-num {{ font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--copper); font-weight: 600; }}
  h2.slide-title {{ font-family: ui-serif, Georgia, serif; font-size: 1.35rem; line-height: 1.3; color: var(--navy); font-weight: 700; margin-top: 0.25rem; }}
  .pill {{ display:inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.72rem; font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; letter-spacing: 0.02em; }}
  .pill-good {{ background: #dcfce7; color: #166534; }}
  .pill-warn {{ background: #fef3c7; color: #92400e; }}
  .pill-bad  {{ background: #fee2e2; color: #991b1b; }}
  .pill-navy {{ background: #dbeafe; color: #1e40af; }}
  .pill-copper {{ background: #fef0e0; color: var(--copper); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th {{ background: var(--navy); color: #fff; padding: 8px 10px; text-align: left; font-weight: 600; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.8rem; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  tr:nth-child(even) td {{ background: #f9fafb; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  ul.dot {{ list-style: none; padding: 0; }}
  ul.dot li {{ position: relative; padding-left: 1.1em; margin: 0.4em 0; line-height: 1.55; }}
  ul.dot li::before {{ content: "\\2022"; color: var(--copper); position: absolute; left: 0; font-weight: 700; }}
  .stage-pill {{ background: var(--navy); color: #fff; border-radius: 6px; padding: 6px 8px; font-size: 0.75rem; text-align: center; font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; }}
  .tier-bar {{ width: 4px; border-radius: 4px; }}
  .source {{ font-size: 0.72rem; color: var(--ink-2); font-style: italic; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid var(--border); }}
  .dots-3 {{ color: var(--good); }}
  .dots-2 {{ color: var(--warn); }}
  .dots-1 {{ color: var(--bad); }}
  .toc a {{ display: block; padding: 6px 0; color: var(--ink); border-bottom: 1px solid #f1f5f9; font-size: 0.85rem; }}
  .toc a:hover {{ color: var(--copper); }}
  .toc-num {{ color: var(--copper); font-family: ui-sans-serif, system-ui, sans-serif; font-weight: 600; margin-right: 8px; font-size: 0.75rem; }}
  details summary {{ cursor: pointer; padding: 8px 12px; background: #f1f5f9; border-radius: 8px; font-weight: 600; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.9rem; }}
  @media (min-width: 1024px) {{
    .layout-2col {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.5rem; }}
  }}
</style>
</head>
<body class="antialiased">

<header class="bg-[var(--navy)] text-white">
  <div class="max-w-3xl mx-auto px-5 py-6">
    <div class="text-xs uppercase tracking-widest" style="color:var(--copper);">NYSE: MP &middot; Investment Decision Frame</div>
    <h1 class="text-3xl font-bold mt-2">MP Materials</h1>
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
      <a href="#s4"><span class="toc-num">04</span>Market context — NdPr price</a>
      <a href="#s5"><span class="toc-num">05</span>Industry economics</a>
      <a href="#s6"><span class="toc-num">06</span>MP profile</a>
      <a href="#s7"><span class="toc-num">07</span>DoD deal</a>
      <a href="#s8"><span class="toc-num">08</span>Peer set</a>
      <a href="#s9"><span class="toc-num">09</span>2×2 positioning</a>
      <a href="#s10"><span class="toc-num">10</span>Lynas deep dive</a>
      <a href="#s11"><span class="toc-num">11</span>US juniors (UUUU, USAR)</a>
      <a href="#s12"><span class="toc-num">12</span>Chinese majors (CNREG)</a>
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

<!-- Slide 2 (1 is the cover above) -->
<section id="s2" class="card p-5">
  <div class="slide-num">Slide 02 &middot; Executive Summary</div>
  <h2 class="slide-title">Only scaled US rare-earth play; DoD as anchor shareholder rewrites the risk profile</h2>
  <div class="mt-4 space-y-4 text-sm">
    <div><span class="pill pill-navy">1. The setup</span><p class="mt-2">MP is the only fully scaled US rare-earth miner and the only Western producer with end-to-end mine-to-magnet ambition. Q1 2026 marked an inflection: revenue $90.6M (+49% YoY), record 917 MT NdPr oxide (+63%), Adj EBITDA flipped positive to $36.6M.</p></div>
    <div><span class="pill pill-copper">2. The moat</span><p class="mt-2">US Department of Defense holds ~15% via preferred + warrant at $30.03/sh (Jul 2025 deal). The 10-year DoD offtake includes a $110/kg NdPr price floor — structural downside protection no peer has.</p></div>
    <div><span class="pill pill-warn">3. The risk</span><p class="mt-2">Market cap ~$9.8B on TTM revenue $275M = priced for the magnet ramp. Stage III first commercial product is 2028. China still controls &gt;70% of mining, &gt;80% of processing — NdPr is exposed to Chinese export policy.</p></div>
    <div><span class="pill pill-good">4. The read</span><p class="mt-2">Long thesis intact for investors who accept multi-year execution risk in exchange for asymmetric upside on Section 232 / decoupling tailwinds and a 2028 magnet revenue inflection. Pair-trade vs CNREG offers tighter risk profile.</p></div>
  </div>
  <div class="source">Sources: MP Q1 2026 10-Q; MP DoD partnership release (Jul 2025); CNBC; S&amp;P Global.</div>
</section>

<section id="s3" class="card p-5">
  <div class="slide-num">Slide 03 &middot; The Question</div>
  <h2 class="slide-title">The question this analysis answers</h2>
  <blockquote class="mt-4 pl-4 border-l-4 border-[var(--copper)] text-base italic" style="color:var(--navy);">
    "Can MP convert rare-earth scarcity and US industrial policy into durable cash flow ahead of a competitive peer ramp — and is today's ~$10B market cap a reasonable entry on that thesis?"
  </blockquote>
  <div class="mt-5 text-sm">
    <div class="font-semibold" style="color:var(--ink);">We test that question across five lenses:</div>
    <ol class="mt-2 space-y-1 pl-5 list-decimal">
      <li><b>Market</b> — is the NdPr price environment supportive?</li>
      <li><b>Competitive</b> — does MP have a defensible position vs Western and Chinese peers?</li>
      <li><b>Financial</b> — what does the valuation look like vs peer comps?</li>
      <li><b>Strategic</b> — what's the moat and how durable is it?</li>
      <li><b>Decision</b> — what's the cleanest expression of conviction (or wait)?</li>
    </ol>
  </div>
</section>

<section id="s4" class="card p-5">
  <div class="slide-num">Slide 04 &middot; Market Context</div>
  <h2 class="slide-title">Rare-earth demand structurally tight; NdPr +&gt;100% YTD with $110/kg DoD floor under MP</h2>
  <img src="data:image/png;base64,{ndpr_b64}" alt="NdPr YTD price chart" class="mt-4 rounded-lg border border-[var(--border)] w-full" />
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What the chart says</div>
    <ul class="dot mt-2">
      <li>NdPr spot opened 2026 ~$53/kg.</li>
      <li>By end-April hit ~$140/kg in some retail benchmarks; SMM industrial ~$100/kg in May. Roughly +100–160% YTD depending on benchmark.</li>
      <li><b>MP's $110/kg DoD price floor</b> sits above current SMM spot — MP earns the floor on PPA-covered volume.</li>
      <li>Lynas, UUUU, USAR are <b>unhedged</b> — they ride spot in both directions.</li>
      <li>Drivers: China export quotas tightening, accelerating EV magnet demand, US decoupling capex.</li>
    </ul>
  </div>
  <div class="source">NdPr prices: SMM, strategicmetalsinvest.com (May 2026). DoD floor: MP investor relations, Jul 2025.</div>
</section>

<section id="s5" class="card p-5">
  <div class="slide-num">Slide 05 &middot; Industry Economics</div>
  <h2 class="slide-title">China owns &gt;70% of mining and &gt;80% of processing — value pools sit downstream</h2>
  <div class="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-2">
    {''.join(f'<div class="stage-pill">{s}</div>' for s in ["Mining","Cracking &amp; Leaching","Separation","Metal / Alloy","Sintered Magnets","Downstream apps"])}
  </div>
  <table class="mt-4">
    <thead><tr><th>Stage</th><th>Typical margin</th><th>China share</th></tr></thead>
    <tbody>
      <tr><td>Mining</td><td class="num">10–20%</td><td class="num" style="color:var(--bad);">~70%</td></tr>
      <tr><td>Cracking &amp; Leaching</td><td class="num">5–10%</td><td class="num" style="color:var(--bad);">~80%</td></tr>
      <tr><td>Separation (NdPr / HRE)</td><td class="num">15–25%</td><td class="num" style="color:var(--bad);">~85%</td></tr>
      <tr><td>Metal / Alloy</td><td class="num">5–10%</td><td class="num" style="color:var(--bad);">~90%</td></tr>
      <tr><td>Sintered Magnets</td><td class="num">20–30%</td><td class="num" style="color:var(--bad);">~90%</td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What this means</div>
    <ul class="dot mt-2">
      <li>Highest-margin stages (Separation, Sintered Magnets) are where strategic value sits — and where China is most dominant.</li>
      <li>MP and USAR are the only Western names targeting Sintered Magnets at scale. Lynas stops at Separation.</li>
      <li>MP's Stage III magnet facility (Independence, TX, commercial 2028) is <b>thesis-critical</b>.</li>
    </ul>
  </div>
  <div class="source">Discovery Alert, Farmonaut, SMM (2025/26 industry reports).</div>
</section>

<section id="s6" class="card p-5">
  <div class="slide-num">Slide 06 &middot; MP Profile</div>
  <h2 class="slide-title">MP profile — Q1'26 inflection: revenue +49%, NdPr +63%, Adj EBITDA flipped to +$36.6M</h2>
  <table class="mt-4">
    <thead><tr><th>Metric</th><th>Value</th><th>YoY</th></tr></thead>
    <tbody>
      <tr><td>Q1 2026 Revenue</td><td class="num">$90.6M</td><td class="num" style="color:var(--good);">+49%</td></tr>
      <tr><td>Q1 2026 NdPr oxide production</td><td class="num">917 MT</td><td class="num" style="color:var(--good);">+63%</td></tr>
      <tr><td>Q1 2026 NdPr oxide sales</td><td class="num">1,006 MT</td><td class="num" style="color:var(--good);">+117%</td></tr>
      <tr><td>Q1 2026 Adj EBITDA</td><td class="num">$36.6M</td><td class="num" style="color:var(--good);">+$49.9M</td></tr>
      <tr><td>Magnetics segment revenue</td><td class="num">$21.1M</td><td class="num" style="color:var(--good);">+$15.9M</td></tr>
      <tr><td>TTM revenue</td><td class="num">$275M</td><td class="num">—</td></tr>
      <tr><td>Market cap (May 15, 2026)</td><td class="num">$9.81B</td><td class="num">—</td></tr>
      <tr><td>52-week range</td><td class="num">$18.64 – $100.25</td><td class="num">stock $61.74</td></tr>
      <tr><td>FY26 consensus rev growth</td><td class="num">+67%</td><td class="num">—</td></tr>
    </tbody>
  </table>
  <div class="source">MP Q1 2026 earnings release; 10-Q FY2026 Q1; StockAnalysis.com.</div>
</section>

<section id="s7" class="card p-5">
  <div class="slide-num">Slide 07 &middot; DoD Deal</div>
  <h2 class="slide-title">DoD ~15% + 10-yr offtake + $110/kg NdPr floor = public–private moat</h2>
  <table class="mt-4">
    <thead><tr><th>Element</th><th>Detail</th></tr></thead>
    <tbody>
      <tr><td>Form</td><td>$400M preferred stock (convertible) + warrant for additional common</td></tr>
      <tr><td>Aggregate stake</td><td>~15% post-conversion + warrant exercise</td></tr>
      <tr><td>Conversion price</td><td>$30.03 / common share</td></tr>
      <tr><td>Close date</td><td>July 11, 2025</td></tr>
      <tr><td>DoD position</td><td><b>Largest single shareholder</b> in MP</td></tr>
      <tr><td>Offtake</td><td>10-year DoD off-take agreement</td></tr>
      <tr><td>NdPr price floor (PPA)</td><td><b>$110/kg</b> on covered NdPr, effective Oct 1, 2025</td></tr>
      <tr><td>Use of proceeds</td><td>Separation/processing + magnet production capacity</td></tr>
      <tr><td>Stage III magnet facility</td><td>Construction begins 2026; first commercial product expected 2028</td></tr>
    </tbody>
  </table>
  <div class="source">MP press release (Jul 10, 2025); CNBC; Center on Global Energy Policy (Columbia SIPA).</div>
</section>

<section id="s8" class="card p-5">
  <div class="slide-num">Slide 08 &middot; Peer Set</div>
  <h2 class="slide-title">Peer set — four strategic groups, two of which MP competes in directly</h2>
  <div class="mt-4 space-y-3">
    {''.join(f'<div class="flex gap-3"><div class="tier-bar" style="background:{c};"></div><div class="flex-1"><div class="font-semibold" style="color:{c};">{t}</div><ul class="dot mt-1 text-sm">{"".join(f"<li>{i}</li>" for i in items)}</ul></div></div>'
      for t, items, c in [
        ("Tier 1 — Western pure-plays", ["MP Materials (NYSE: MP) — only scaled US name", "Lynas Rare Earths (ASX: LYC) — only scaled non-US Western name"], "#17365D"),
        ("Tier 2 — US juniors / ramping", ["Energy Fuels (NYSE: UUUU) — uranium with REE pivot", "USA Rare Earth (Nasdaq: USAR) — magnet-focused, $1.6B US gov't investment"], "#B26B1E"),
        ("Tier 3 — Chinese majors (context)", ["China Northern Rare Earth (SHA: 600111) — world's largest, state-owned", "(Shenghe, JL Mag, etc. — not investable for most Western mandates)"], "#C0392B"),
        ("Tier 4 — Critical-minerals adjacent", ["Albemarle (NYSE: ALB) — lithium leader, not REE", "Included for broader critical-minerals reference only"], "#7F8C8D"),
      ])}
  </div>
</section>

<section id="s9" class="card p-5">
  <div class="slide-num">Slide 09 &middot; 2×2 Positioning</div>
  <h2 class="slide-title">Scale × Integration: MP and Lynas alone occupy the Western 'fully-integrated' quadrant</h2>
  <img src="data:image/png;base64,{positioning_b64}" alt="2x2 positioning matrix" class="mt-4 rounded-lg border border-[var(--border)] w-full" />
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">What the matrix says</div>
    <ul class="dot mt-2">
      <li>China Northern RE is the only fully integrated, scaled producer globally — but un-investable for many.</li>
      <li>MP sits top-right Western quadrant, alone with Lynas — and uniquely targets sintered magnets (vs Lynas which does not).</li>
      <li>USAR is a magnet-only pure-play; small scale.</li>
      <li>Energy Fuels is processing-only with REE optionality.</li>
      <li>Albemarle is in adjacent lithium / bromine — not a true comp.</li>
    </ul>
  </div>
</section>

<section id="s10" class="card p-5">
  <div class="slide-num">Slide 10 &middot; Lynas Deep Dive</div>
  <h2 class="slide-title">Lynas — Most-profitable Western pure-play, slower up the value chain</h2>
  <div class="layout-2col mt-4">
    <div>
      <table>
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>
          <tr><td>Market cap</td><td>~US$10.8B (A$15.1B)</td></tr>
          <tr><td>Q3 FY26 revenue</td><td>A$265M (+115% YoY)</td></tr>
          <tr><td>H1 FY26 revenue / NI</td><td>A$413.7M / A$80.2M</td></tr>
          <tr><td>FY26 forecast revenue</td><td>~A$1.1B (~2x FY25)</td></tr>
          <tr><td>FY26 NdPr volume</td><td>~8,800 MT (+35% YoY)</td></tr>
          <tr><td>FY26 NdPr avg realised</td><td>A$118/kg (+48%)</td></tr>
          <tr><td>TTM EBITDA / margin</td><td>US$211M / ~36%</td></tr>
          <tr><td>TTM P/E (Fwd)</td><td>~209x (~37x)</td></tr>
          <tr><td>Key asset</td><td>Mt Weld, WA</td></tr>
        </tbody>
      </table>
    </div>
    <div class="mt-4 lg:mt-0 text-sm">
      <div class="font-semibold" style="color:var(--navy);">Strengths</div>
      <ul class="dot mt-1"><li>Highest-grade REE deposit globally</li><li>Already profitable (TTM EBITDA $211M)</li><li>US heavy-REE pivot with DoD support</li></ul>
      <div class="font-semibold mt-3" style="color:var(--navy);">Weaknesses</div>
      <ul class="dot mt-1"><li>Stops at separation — no magnet revenue</li><li>Single-mine concentration (Mt Weld)</li><li>FX exposure (AUD revenue, USD pricing)</li></ul>
      <div class="font-semibold mt-3" style="color:var(--navy);">Strategy</div>
      <ul class="dot mt-1"><li>Volume growth + US footprint expansion; will compete with MP in heavy REE.</li></ul>
    </div>
  </div>
  <div class="source">Lynas H1 FY26 results; Q3 FY26 update; StockAnalysis; S&amp;P Global (Dec 2025).</div>
</section>

<section id="s11" class="card p-5">
  <div class="slide-num">Slide 11 &middot; US Juniors</div>
  <h2 class="slide-title">US juniors — capacity optionality, execution risk, long-dated</h2>
  <div class="layout-2col mt-4 text-sm">
    <div>
      <div class="font-semibold" style="color:var(--copper);">Energy Fuels (UUUU)</div>
      <ul class="dot mt-2">
        <li><b>Business:</b> US uranium producer pivoting into REE processing at White Mesa Mill (Utah)</li>
        <li><b>Phase 2 plan:</b> 6,000 tpa NdPr + 240 tpa Dy + 66 tpa Tb</li>
        <li><b>Latest:</b> BFS published Jan 15, 2026 — "lowest-cost NdPr in the world"</li>
        <li><b>Strengths:</b> existing infrastructure, low CAPEX</li>
        <li><b>Weakness:</b> REE revenue still pre-commercial</li>
      </ul>
    </div>
    <div class="mt-5 lg:mt-0">
      <div class="font-semibold" style="color:var(--copper);">USA Rare Earth (USAR)</div>
      <ul class="dot mt-2">
        <li><b>Business:</b> Mine-to-magnet integrated supply chain (TX → OK)</li>
        <li><b>Q2 2026:</b> Stillwater, OK magnet line commercial production begins</li>
        <li><b>Financing:</b> $1.5B PIPE + $1.6B US gov't investment</li>
        <li><b>Strengths:</b> magnet pure-play, gov't backing</li>
        <li><b>Weakness:</b> pre-meaningful revenue, small scale</li>
      </ul>
    </div>
  </div>
  <div class="source">UUUU Phase 2 BFS (Jan 2026); USAR 8-K (Q2 2026 commissioning); Motley Fool.</div>
</section>

<section id="s12" class="card p-5">
  <div class="slide-num">Slide 12 &middot; Chinese Majors</div>
  <h2 class="slide-title">China Northern Rare Earth — sets the price; un-investable for most Western capital</h2>
  <table class="mt-4">
    <thead><tr><th>Metric</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Global share — mining</td><td>~60–70% (China overall &gt;70%)</td></tr>
      <tr><td>Global share — processing</td><td>&gt;80%</td></tr>
      <tr><td>FY2025 revenue</td><td>¥42.6B (US$5,910M) — <span style="color:var(--good);">+29%</span></td></tr>
      <tr><td>FY2025 net income</td><td>¥2.25B (US$313M) — <span style="color:var(--good);">+124%</span></td></tr>
      <tr><td>Q1 2026 net profit guidance</td><td>US$125–131M (<span style="color:var(--good);">+109–118%</span>)</td></tr>
      <tr><td>Owner</td><td>Baogang Group (state-owned, Inner Mongolia)</td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Why this matters for MP</div>
    <ul class="dot mt-2">
      <li>CNREG sets the marginal NdPr clearing price — MP's economics ride that benchmark outside the DoD floor.</li>
      <li>China can introduce heavy-REE export restrictions at policy speed — upside for MP/Lynas.</li>
      <li>CNREG +124% YoY profit says China is winning today even as the West tries to decouple.</li>
      <li><b>Pair-trade idea:</b> long MP / short CNREG — cleaner geopolitical-decoupling expression.</li>
    </ul>
  </div>
  <div class="source">Shanghai Metals Market (SMM); Discovery Alert; Farmonaut (2025/26 reports).</div>
</section>

<section id="s13" class="card p-5">
  <div class="slide-num">Slide 13 &middot; Comparative Scoreboard</div>
  <h2 class="slide-title">MP leads scale &amp; integration vector; lags near-term margins</h2>
  <div class="overflow-x-auto">
  <table class="mt-4" style="min-width: 720px;">
    <thead><tr><th>Dimension</th><th>MP</th><th>Lynas</th><th>UUUU</th><th>USAR</th><th>CNREG</th><th>ALB</th></tr></thead>
    <tbody>
      <tr><td>Revenue scale (TTM)</td><td>●●○ $275M</td><td>●●○ $578M</td><td>●○○ $70M[E]</td><td>○○○ Pre-rev</td><td>●●● $5.9B</td><td>●●● $5.85B</td></tr>
      <tr><td>Vertical integration</td><td>●●● Mine→Mag plan</td><td>●●○ Mine→Sep+HRE</td><td>●○○ Proc</td><td>●○○ Magnet only</td><td>●●● Full</td><td>○○○ Adjacent</td></tr>
      <tr><td>TTM profitability</td><td>●○○ Neg→Pos Adj</td><td>●●● +36% EBITDA</td><td>○○○ Neg</td><td>○○○ Neg</td><td>●●○ +12% EBITDA</td><td>●●● +43% EBITDA</td></tr>
      <tr><td>Govt backing</td><td>●●● DoD 15% + floor</td><td>●●○ US/AU grants</td><td>●○○ Modest</td><td>●●● $1.6B US inv.</td><td>●●● State-owned</td><td>●○○ IRA / DoE</td></tr>
      <tr><td>China-policy upside</td><td>●●● Direct</td><td>●●● Direct</td><td>●●○ Modest</td><td>●●● Direct</td><td>○○○ Negative</td><td>●○○ Indirect</td></tr>
      <tr><td>Valuation absorb-shock</td><td>●●○ Floor protects</td><td>●●● Profitable</td><td>●○○ Capacity bet</td><td>●○○ Optionality</td><td>●●● Cheap</td><td>●●○ Improving</td></tr>
      <tr><td>Investability (US mandate)</td><td>●●● Yes</td><td>●●○ ASX-listed</td><td>●●● Yes</td><td>●●● Yes</td><td>○○○ No</td><td>●●● Yes</td></tr>
    </tbody>
  </table>
  </div>
  <div class="source">● = Strong · ○ = Weak. Calibrated against Operating Metrics / Valuation / REE-Specific tabs in companion .xlsx.</div>
</section>

<section id="s14" class="card p-5">
  <div class="slide-num">Slide 14 &middot; Strategic Synthesis</div>
  <h2 class="slide-title">Moat: integration + govt partnership · Risk: NdPr cycle + Stage III timing</h2>
  <div class="overflow-x-auto">
  <table class="mt-4" style="min-width: 720px;">
    <thead><tr><th>Moat type</th><th>MP</th><th>Lynas</th><th>UUUU</th><th>USAR</th><th>CNREG</th><th>Reading</th></tr></thead>
    <tbody>
      <tr><td>Network effects</td><td>Weak</td><td>Weak</td><td>Weak</td><td>Weak</td><td>Mod</td><td>Limited — industrial supply, not platform</td></tr>
      <tr><td>Switching costs</td><td><b>Strong</b></td><td>Mod</td><td>Weak</td><td>Mod</td><td>Strong</td><td>Mag spec-in is sticky; 10-yr offtake locks customers</td></tr>
      <tr><td>Scale economies</td><td>Mod</td><td>Mod</td><td>Weak</td><td>Weak</td><td>Strong</td><td>Cost curve favors integrated scale</td></tr>
      <tr><td>Intangibles (govt)</td><td><b>Strong</b></td><td>Mod</td><td>Weak</td><td>Mod</td><td>Strong</td><td>MP–DoD relationship is biggest Western intangible</td></tr>
      <tr><td>Permits / location</td><td><b>Strong</b></td><td>Mod</td><td>Mod</td><td>Mod</td><td>Mod</td><td>Mountain Pass = only operating US REE mine</td></tr>
    </tbody>
  </table>
  </div>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Net moat assessment</div>
    <p class="mt-2"><b>Durable advantages:</b> (i) only operating US REE mine, (ii) DoD anchor + price floor, (iii) only Western mine→magnet ambition at scale.</p>
    <p class="mt-1"><b>Structural vulnerabilities:</b> (i) magnet revenue not until 2028, (ii) NdPr spot still drives marginal volume, (iii) capex-heavy through 2028.</p>
  </div>
</section>

<section id="s15" class="card p-5">
  <div class="slide-num">Slide 15 &middot; Bull / Base / Bear</div>
  <h2 class="slide-title">Range of outcomes anchored by $110/kg floor (downside) and 2028 magnet revenue (upside)</h2>
  <table class="mt-4">
    <thead><tr><th>Scenario</th><th>Prob.</th><th>Key driver</th></tr></thead>
    <tbody>
      <tr><td><span class="pill pill-good">Bull</span></td><td class="num">30%</td><td>Section 232 tariffs; China heavy-REE export restrictions; Apple/GM magnet volume expansion; Stage III on schedule → re-rate 50–100%; magnet rev 2028 → 2–3x</td></tr>
      <tr><td><span class="pill pill-navy">Base</span></td><td class="num">50%</td><td>NdPr $80–$150/kg; DoD floor protects covered volume; Stage III on time; Lynas/USAR add supply, market absorbs → ~20–40% upside over 18 mo</td></tr>
      <tr><td><span class="pill pill-bad">Bear</span></td><td class="num">20%</td><td>China–US trade détente collapses NdPr; Stage III delays; USAR/UUUU ramp faster than expected → re-rate 30–40% lower (≈4x EV/Sales)</td></tr>
    </tbody>
  </table>
  <div class="mt-4 text-sm">
    <div class="font-semibold" style="color:var(--navy);">Signposts to watch</div>
    <ol class="mt-2 space-y-1 pl-5 list-decimal">
      <li>NdPr spot vs $110/kg floor</li>
      <li>Stage III construction milestone in H2 2026</li>
      <li>Section 232 / export-control decisions on critical minerals</li>
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
      <tr><td>Q2 2026</td><td>USAR</td><td>Stillwater (OK) sintered NdFeB magnet line commercial production begins</td></tr>
      <tr><td>H2 2026</td><td><b>MP</b></td><td>Stage III magnet facility construction commences (Independence, TX)</td></tr>
      <tr><td>H2 2026</td><td>Lynas</td><td>US heavy-REE (Dy/Tb) plant at Seadrift TX ramps</td></tr>
      <tr><td>Q4 2026</td><td>UUUU</td><td>Phase 2 REE circuit final investment decision expected</td></tr>
      <tr><td>Ongoing</td><td>US Policy</td><td>Section 232 review / China export-quota decisions</td></tr>
      <tr><td>2027</td><td><b>MP</b></td><td>Apple / GM magnet supply expansion expected</td></tr>
      <tr><td><b>2028</b></td><td><b>MP</b></td><td><b>First commercial sintered magnet product</b> — THESIS-CRITICAL</td></tr>
    </tbody>
  </table>
</section>

<section id="s17" class="card p-5">
  <div class="slide-num">Slide 17 &middot; Decision Frame</div>
  <h2 class="slide-title">Four ways to express the rare-earths thesis</h2>
  <div class="mt-4 space-y-4 text-sm">
    <div>
      <span class="pill pill-copper">Long MP outright (highest conviction)</span>
      <p class="mt-2"><b>Triggers:</b> NdPr sustainably &gt; $110/kg floor; Stage III milestones on schedule; new offtake from Apple/GM. <b>Risk:</b> ramp slips past 2028; China relaxes export rules collapsing NdPr. Multi-year hold.</p>
    </div>
    <div>
      <span class="pill pill-navy">Pair trade: long MP / short CNREG</span>
      <p class="mt-2"><b>Triggers:</b> Section 232 tariffs; escalating US–China decoupling. <b>Risk:</b> CNREG profits +124% YoY says China is winning today — short side may be early. Cleaner geopolitical expression.</p>
    </div>
    <div>
      <span class="pill pill-warn">Basket via REMX (theme exposure)</span>
      <p class="mt-2">REMX YTD ~25–42% — diversified critical-minerals. Trade-off: significant Chinese name weight inside; less direct US-domestic-supply exposure.</p>
    </div>
    <div>
      <span class="pill pill-bad">Avoid / wait</span>
      <p class="mt-2"><b>Re-enter triggers:</b> (i) Stage III magnet line first commercial output (~2028), (ii) trailing EBITDA sustainably positive, (iii) NdPr breaks below $80/kg without floor protection. Acknowledges 2026 valuation already prices in significant ramp.</p>
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
      <li>MP Materials Q1 2026 10-Q (mp-20260331) and Q1 2026 earnings release</li>
      <li>MP–DoD partnership press release (Jul 10, 2025); CNBC</li>
      <li>Lynas H1 FY26 results; Q3 FY26 trading update; StockAnalysis LYC.AX</li>
      <li>S&amp;P Global Market Intelligence — Lynas 2026 outlook (Dec 2025)</li>
      <li>Energy Fuels Phase 2 BFS (Jan 15, 2026); Q1 2026 results</li>
      <li>USA Rare Earth 8-K filings; magnet-line commissioning release</li>
      <li>China Northern Rare Earth FY25 results — Shanghai Metals Market</li>
      <li>Albemarle Q1 2026 earnings; SWOT (Investing.com)</li>
      <li>NdPr pricing: SMM, strategicmetalsinvest.com (May 2026)</li>
      <li>VanEck REMX ETF; Center on Global Energy Policy (Columbia SIPA)</li>
    </ul>
    <div class="font-semibold mt-4" style="color:var(--navy);">Data gaps and caveats</div>
    <ul class="dot mt-2">
      <li><b>MCP data sources</b> (CapIQ / FactSet / Daloopa) were NOT used — plugin connectors not configured. Cross-check before action.</li>
      <li><b>[E] flags</b> in companion .xlsx Inputs tab identify estimated figures with assumption documented in cell comments.</li>
      <li>Chinese major financials in CNY → USD at ~7.2 (May 2026 indicative).</li>
      <li>Forward consensus from public aggregators, not sell-side feeds.</li>
      <li>This is research / decision framing — <b>not investment advice</b>.</li>
    </ul>
  </div>
</section>

</main>

<footer class="bg-[var(--navy)] text-white py-6 mt-8">
  <div class="max-w-3xl mx-auto px-5 text-xs opacity-80 flex justify-between flex-wrap gap-2">
    <span>MP Materials competitive analysis · May 2026 · sourced public data</span>
    <span>Research only — not investment advice</span>
  </div>
</footer>

</body>
</html>
"""

OUT = HERE / "MP-Competitive-Analysis.html"
OUT.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT} ({len(HTML):,} bytes)")
