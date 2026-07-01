"""Offline tests for the securitisation EDGAR connector.

No network: the streaming parser runs on a bundled synthetic loan tape, and the
search/filings logic runs against the real EDGAR JSON shapes via a fake client.
Run with:  python tests/test_connector.py   (from the connector/ directory)
"""
import csv
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # connector/ -> importable edgar_sf

from edgar_sf.regions.us import absee_parser, timeseries
from edgar_sf.regions.us.edgar import UsEdgar
from edgar_sf.core.models import FilingRef

FX = os.path.join(HERE, "sample_auto_absee.xml")
P1 = os.path.join(HERE, "sample_auto_absee_p1.xml")
P2 = os.path.join(HERE, "sample_auto_absee_p2.xml")
P_FLAT = os.path.join(HERE, "sample_auto_flat_absee.xml")
_ok = _fail = 0


def check(name, cond, got=None):
    global _ok, _fail
    if cond:
        _ok += 1; print(f"  PASS  {name}")
    else:
        _fail += 1; print(f"  FAIL  {name}  got={got!r}")


class FakeClient:
    def __init__(self, jmap, text=""):
        self.jmap = jmap; self.text = text
    def get_json(self, url):
        for k, v in self.jmap.items():
            if k in url:
                return v
        raise KeyError(url)
    def get_text(self, url):
        return self.text


def test_parser_summary():
    print("== streaming parser: pool summary ==")
    with open(FX, "rb") as s:
        r = absee_parser.parse_tape(s, mode="summary", sample=2)
    check("loans counted = 5", r["loans_in_tape"] == 5, r["loans_in_tape"])
    check("total current balance = 105000", r["total_current_balance"] == 105000.0, r["total_current_balance"])
    check("balance-weighted coupon = 6.8571", r["weighted_averages"]["coupon_pct"] == 6.8571)
    check("balance-weighted FICO = 605.7143", r["weighted_averages"]["credit_score"] == 605.7143)
    check("namespace stripped + nested fields flattened", "obligorCreditScore" in r["sample_loans"][0])
    top = r["distributions"]["state"][0]
    check("top state by balance = CA / 70000", top["value"] == "CA" and top["balance"] == 70000.0, top)


def test_filter_and_csv():
    print("== filter mode + CSV ==")
    out = os.path.join(tempfile.gettempdir(), "test_ca.csv")
    with open(FX, "rb") as s:
        r = absee_parser.parse_tape(s, mode="filter", filters={"obligorGeographicLocation": "CA"}, out_path=out)
    check("matched 2 of 5", r["loans_matched"] == 2 and r["loans_in_tape"] == 5)
    check("aggregates respect filter (bal 70000)", r["total_current_balance"] == 70000.0)
    check("CSV has 2 data rows", len(list(csv.DictReader(open(out)))) == 2)
    with open(FX, "rb") as s:
        r2 = absee_parser.parse_tape(s, mode="summary", filters={"obligorCreditScore": {"max": 600}})
    check("FICO<=600 numeric range -> 2 loans", r2["loans_matched"] == 2)


def test_search_and_filings():
    print("== EDGAR JSON parsing (fake client) ==")
    efts = {"hits": {"total": {"value": 2}, "hits": [
        {"_id": "0001694010-18-000036:absee_5710x092018.htm", "_source": {
            "ciks": ["0001694010"], "adsh": "0001694010-18-000036",
            "display_names": ["AmeriCredit Automobile Receivables Trust 2017-1  (CIK 0001694010)"],
            "form": "ABS-EE", "file_date": "2018-10-23", "sics": ["6189"]}}]}}
    us = UsEdgar(client=FakeClient({"efts.sec.gov": efts}))
    sr = us.search_deals("AmeriCredit", asset_class="auto", form_type="ABS-EE")
    check("issuer cleaned of (CIK ...)", sr["results"][0]["issuer"] == "AmeriCredit Automobile Receivables Trust 2017-1")
    check("document_url built correctly",
          sr["results"][0]["document_url"].endswith("/1694010/000169401018000036/absee_5710x092018.htm"))

    sub = {"cik": "0001694010", "name": "AmeriCredit Automobile Receivables Trust 2017-1", "sic": "6189",
           "filings": {"recent": {
               "accessionNumber": ["0001193125-17-053869", "0001-18-0002", "0001694010-18-000036"],
               "form": ["424B5", "10-D", "ABS-EE"], "filingDate": ["2017-02-08", "2018-10-25", "2018-10-23"],
               "reportDate": ["", "2018-09-30", "2018-09-30"],
               "primaryDocument": ["d424b5.htm", "s10d.htm", "absee.htm"],
               "primaryDocDescription": ["424B5", "10-D", "ABS-EE"], "size": [1, 2, 3]}}}
    us2 = UsEdgar(client=FakeClient({"submissions": sub}))
    check("all filings = 3", len(us2.get_deal_filings("1694010").filings) == 3)
    check("ABS-EE filter -> 1", len(us2.get_deal_filings("1694010", form_type="ABS-EE").filings) == 1)


def test_url_construction():
    print("== URL construction ==")
    f = FilingRef(cik="0001694010", accession="0001193125-17-053869", form="424B5", primary_document="d.htm")
    check("strips CIK zeros + accession dashes",
          f.document_url == "https://www.sec.gov/Archives/edgar/data/1694010/000119312517053869/d.htm", f.document_url)


def test_step1_enrichment():
    print("== step 1: loss + delinquency buckets ==")
    with open(P1, "rb") as s:
        r = absee_parser.parse_tape(s, mode="summary")
    db = r["delinquency_buckets"]
    check("current bucket balance = 35000", db["current"]["balance"] == 35000.0, db.get("current"))
    check("61-90 bucket balance = 40000", db["61-90"]["balance"] == 40000.0, db.get("61-90"))
    check("dq 60+ pct = 38.1", r["dq_60plus_pct"] == 38.1, r["dq_60plus_pct"])
    check("P1 net loss in period = 0", r["net_loss_in_period"] == 0.0, r["net_loss_in_period"])
    with open(P2, "rb") as s:
        r2 = absee_parser.parse_tape(s, mode="summary")
    check("P2 net loss in period = 30000", r2["net_loss_in_period"] == 30000.0, r2["net_loss_in_period"])


def test_stratify_one_dim():
    print("== step 2: stratify by fico_band ==")
    with open(P1, "rb") as s:
        r = absee_parser.parse_tape(s, mode="summary", stratify_by=["fico_band"])
    rows = r["stratification"]["rows"]
    by = {row["bucket"]: row for row in rows}
    check("bands = <550/600-649/700+", set(by) == {"<550", "600-649", "700+"}, set(by))
    check("<550 balance = 40000", by["<550"]["current_balance"] == 40000.0, by["<550"])
    check("<550 pct_of_pool = 38.1", by["<550"]["pct_of_pool"] == 38.1, by["<550"]["pct_of_pool"])
    check("600-649 balance = 50000", by["600-649"]["current_balance"] == 50000.0)
    check("rows ordered low band first", rows[0]["bucket"] == "<550", rows[0]["bucket"])


def test_stratify_cross_tab():
    print("== step 2: cross-tab fico_band x state ==")
    with open(P1, "rb") as s:
        r = absee_parser.parse_tape(s, mode="summary", stratify_by=["fico_band", "state"])
    st = r["stratification"]
    check("two dimensions", st["dimensions"] == ["fico_band", "state"], st["dimensions"])
    m = {row["bucket"]: row["cells"] for row in st["matrix"]}
    check("<550 x CA balance = 40000", m["<550"]["CA"]["current_balance"] == 40000.0, m["<550"]["CA"])
    check("<550 x TX is empty", m["<550"]["TX"] is None, m["<550"]["TX"])
    check("600-649 x CA balance = 30000", m["600-649"]["CA"]["current_balance"] == 30000.0)


def _opener():
    paths = {"p1": P1, "p2": P2}
    return lambda key: open(paths[key], "rb")


def test_timeseries_static_pool_loss():
    print("== step 3: static-pool loss curve ==")
    r = timeseries.static_pool_loss(_opener(), [("P1", "p1"), ("P2", "p2")])
    check("original pool = 105000", r["original_pool_balance"] == 105000.0, r["original_pool_balance"])
    row2 = r["rows"][1]
    check("P2 cumulative net loss = 30000", row2["cumulative_net_loss"] == 30000.0, row2)
    check("P2 cum loss pct = 28.5714", row2["cumulative_net_loss_pct"] == 28.5714, row2["cumulative_net_loss_pct"])
    check("P2 pool factor = 54.7619", row2["pool_factor_pct"] == 54.7619, row2["pool_factor_pct"])


def test_timeseries_roll_rate():
    print("== step 3: roll-rate matrix ==")
    r = timeseries.roll_rate(_opener(), [("P1", "p1"), ("P2", "p2")])
    rows = {row["from_state"]: row["to"] for row in r["rows"]}
    check("Current -> 31-60 = 57.14", rows["Current"]["31-60"] == 57.14, rows["Current"])
    check("Current -> Prepaid = 14.29", rows["Current"]["Prepaid"] == 14.29, rows["Current"])
    check("61-90 -> Charged-off = 100", rows["61-90"]["Charged-off"] == 100.0, rows["61-90"])
    check("1-30 -> Current = 100", rows["1-30"]["Current"] == 100.0, rows["1-30"])


def test_timeseries_prepayment():
    print("== step 3: prepayment ==")
    r = timeseries.prepayment(_opener(), [("P1", "p1"), ("P2", "p2")])
    row2 = r["rows"][1]
    check("P2 voluntary payoff loans = 1", row2["voluntary_payoff_loans"] == 1, row2)
    check("P2 voluntary payoff balance = 5000", row2["voluntary_payoff_balance"] == 5000.0, row2)
    check("P2 pool paydown = 45.2381", row2["pool_paydown_pct"] == 45.2381, row2["pool_paydown_pct"])


def test_flat_auto_layout():
    print("== flat auto layout (no <asset> wrapper) regression ==")
    with open(P_FLAT, "rb") as s:
        r = absee_parser.parse_tape(s, mode="summary", stratify_by=["fico_band"])
    check("flat layout: 5 loans parsed (not 0)", r["loans_in_tape"] == 5, r["loans_in_tape"])
    check("flat layout: total balance 105000", r["total_current_balance"] == 105000.0, r["total_current_balance"])
    check("flat layout: WA coupon 6.8571", r["weighted_averages"]["coupon_pct"] == 6.8571, r["weighted_averages"].get("coupon_pct"))
    check("flat layout: top state CA 70000", r["distributions"]["state"][0]["balance"] == 70000.0, r["distributions"]["state"][0])
    check("flat layout: stratify 550-599 = 40000",
          next(x["current_balance"] for x in r["stratification"]["rows"] if x["bucket"] == "550-599") == 40000.0)


if __name__ == "__main__":
    test_parser_summary(); test_filter_and_csv(); test_search_and_filings(); test_url_construction()
    test_step1_enrichment(); test_stratify_one_dim(); test_stratify_cross_tab()
    test_timeseries_static_pool_loss(); test_timeseries_roll_rate(); test_timeseries_prepayment()
    test_flat_auto_layout()
    print(f"\nRESULT: {_ok} passed, {_fail} failed")
    sys.exit(1 if _fail else 0)

