"""Offline tests for CMBS analytics — fixture mirrors the real flat schema/units."""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from edgar_sf.regions.us import cmbs_parser

FX = os.path.join(HERE, "sample_cmbs_absee.xml")
_ok = _fail = 0
def check(name, cond, got=None):
    global _ok, _fail
    if cond: _ok += 1; print(f"  PASS  {name}")
    else: _fail += 1; print(f"  FAIL  {name}  got={got!r}")

def run():
    with open(FX, "rb") as s:
        r = cmbs_parser.parse_cmbs_tape(s, mode="summary", stratify_by=["property_type"])
    wa = r["weighted_averages"]
    check("4 loans parsed from flat schema (no <asset> wrapper)", r["loans_in_tape"] == 4, r["loans_in_tape"])
    check("total balance 200M", r["total_current_balance"] == 200000000.0, r["total_current_balance"])
    check("pool debt yield 7.45%", r["pool_debt_yield_pct"] == 7.45, r["pool_debt_yield_pct"])
    check("WA coupon 4.175% (fraction->percent)", wa["coupon_pct"] == 4.175, wa.get("coupon_pct"))
    check("WA DSCR 1.75x (ratio, unscaled)", wa["dscr_ncf_x"] == 1.75, wa.get("dscr_ncf_x"))
    check("WA occupancy 93.05% (fraction->percent)", wa["occupancy_pct"] == 93.05, wa.get("occupancy_pct"))
    check("WA LTV 66.5% (computed balance/valuation)", wa["ltv_pct"] == 66.5, wa.get("ltv_pct"))
    pt = r["distributions"]["property_type"][0]
    check("top property type Office 150M/75%", pt["value"] == "Office" and pt["balance"] == 150000000.0 and pt["balance_pct"] == 75.0, pt)
    mp = {m["maturity_year"]: m["balance"] for m in r["maturity_profile"]}
    check("maturity wall 2027=80M,2028=20M,2031=100M", mp == {"2027": 80000000.0, "2028": 20000000.0, "2031": 100000000.0}, mp)
    top = r["largest_loans"][0]
    check("largest loan Tower D 100M, LTV 80%", top["property"] == "Tower D" and top["balance"] == 100000000.0 and top["ltv_pct"] == 80.0, top)
    office = next(x for x in r["stratification"]["rows"] if x["bucket"] == "Office")
    check("stratify Office: DSCR 1.83, LTV 70.0, debt yield 7.33",
          office["wa_dscr_ncf_x"] == 1.83 and office["wa_ltv_pct"] == 70.0 and office["debt_yield_pct"] == 7.33, office)
    with open(FX, "rb") as s:
        r2 = cmbs_parser.parse_cmbs_tape(s, mode="summary", stratify_by=["dscr_band"])
    bands = {x["bucket"]: x["current_balance"] for x in r2["stratification"]["rows"]}
    check("dscr_band 1.25-1.5x=30M,1.5-2.0x=70M,2.0x+=100M",
          bands == {"1.25-1.5x": 30000000.0, "1.5-2.0x": 70000000.0, "2.0x+": 100000000.0}, bands)
    with open(FX, "rb") as s:
        r3 = cmbs_parser.parse_cmbs_tape(s, mode="filter", filters={"propertyState": "NY"}, out_path=os.path.join(tempfile.gettempdir(), "cmbs_ny.csv"))
    check("filter NY -> 2 loans / 150M", r3["loans_matched"] == 2 and r3["total_current_balance"] == 150000000.0, (r3["loans_matched"], r3["total_current_balance"]))

if __name__ == "__main__":
    run(); print(f"\nRESULT: {_ok} passed, {_fail} failed"); sys.exit(1 if _fail else 0)
