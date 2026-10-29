"""Field dictionaries for the SEC ABS Schedule AL **automobile** asset-data schema.

Each metric lists *candidate* XML local-tag names. The parser tries them in order
and uses the first one present on a given loan record. This keeps the pool
analytics correct even if a tag name varies slightly between schema versions or
asset classes — and makes adding CMBS/RMBS later a matter of adding more maps.
"""
from __future__ import annotations

# --- identifiers -------------------------------------------------------------
ASSET_NUMBER_FIELDS = ["assetNumber", "assetNumberId", "originalLoanNumber"]

# --- amounts / rates / terms (numeric) ---------------------------------------
# Current outstanding balance (prefer period-end, then beginning, then original).
BALANCE_FIELDS = [
    "reportingPeriodActualEndBalanceAmount",
    "reportingPeriodEndingActualBalanceAmount",
    "reportingPeriodBeginningLoanBalanceAmount",
    "nextReportingPeriodBeginningLoanBalanceAmount",
    "originalLoanAmount",
]
ORIGINAL_AMOUNT_FIELDS = ["originalLoanAmount"]
INTEREST_RATE_FIELDS = [
    "reportingPeriodInterestRatePercentage",
    "nextInterestRatePercentage",
    "originalInterestRatePercentage",
]
CREDIT_SCORE_FIELDS = ["obligorCreditScore"]
ORIGINAL_TERM_FIELDS = ["originalLoanTerm", "originalLoanTermNumber"]
REMAINING_TERM_FIELDS = ["remainingTermToMaturityNumber", "remainingTermNumber"]
PTI_FIELDS = ["paymentToIncomePercentage"]
LTV_FIELDS = ["originalLoanToValueRatio", "loanToValueRatio"]

# Loss / recovery (period figures on the tape).
CHARGEOFF_FIELDS = [
    "chargedoffPrincipalAmount",
    "chargedOffPrincipalAmount",
    "chargeoffPrincipalAmount",
    "reportingPeriodRealizedLossAmount",
]
RECOVERY_FIELDS = ["recoveredAmount", "recoveryPrincipalAmount"]

# --- categoricals ------------------------------------------------------------
STATE_FIELDS = ["obligorGeographicLocation", "geographicLocation", "obligorStateGeographicLocation"]
NEW_USED_FIELDS = ["vehicleNewUsedCode", "vehicleNewUsedIndicator"]
CREDIT_SCORE_TYPE_FIELDS = ["obligorCreditScoreType"]
RATE_TYPE_FIELDS = ["originalInterestRateTypeCode"]
DELINQUENCY_FIELDS = ["currentDelinquencyStatus", "delinquencyStatusText"]
ZERO_BALANCE_FIELDS = ["zeroBalanceCode"]
MANUFACTURER_FIELDS = ["vehicleManufacturerName"]
MODEL_YEAR_FIELDS = ["vehicleModelYear"]

# Balance-weighted averages to report (output label -> candidate source fields).
WA_METRICS = {
    "coupon_pct": INTEREST_RATE_FIELDS,
    "credit_score": CREDIT_SCORE_FIELDS,
    "original_term_months": ORIGINAL_TERM_FIELDS,
    "remaining_term_months": REMAINING_TERM_FIELDS,
    "payment_to_income_pct": PTI_FIELDS,
    "original_ltv_pct": LTV_FIELDS,
}

# Categorical distributions to report (output label -> candidate source fields).
CATEGORICAL = {
    "state": STATE_FIELDS,
    "new_used": NEW_USED_FIELDS,
    "delinquency_status": DELINQUENCY_FIELDS,
    "credit_score_type": CREDIT_SCORE_TYPE_FIELDS,
    "interest_rate_type": RATE_TYPE_FIELDS,
    "manufacturer": MANUFACTURER_FIELDS,
}

# --- banding (numeric -> ordered band label) ---------------------------------
# Each entry: (edges, labels) where len(labels) == len(edges) + 1 and a value v
# lands in labels[bisect_right(edges, v)].
FICO_BANDS = ([550, 600, 650, 700], ["<550", "550-599", "600-649", "650-699", "700+"])
TERM_BANDS = ([49, 61, 73], ["<=48", "49-60", "61-72", "73+"])
PTI_BANDS = ([10, 15, 20], ["<=10", "10-15", "15-20", "20+"])

# Dimensions usable in stratify / cross-tab: name -> ("numeric"|"categorical"|"special", spec).
#   numeric     -> (candidate fields, (edges, labels))
#   categorical -> candidate fields
#   special     -> handled in code (delinquency_bucket)
DIMENSIONS = {
    "fico_band": ("numeric", (CREDIT_SCORE_FIELDS, FICO_BANDS)),
    "orig_term_band": ("numeric", (ORIGINAL_TERM_FIELDS, TERM_BANDS)),
    "pti_band": ("numeric", (PTI_FIELDS, PTI_BANDS)),
    "state": ("categorical", STATE_FIELDS),
    "new_used": ("categorical", NEW_USED_FIELDS),
    "manufacturer": ("categorical", MANUFACTURER_FIELDS),
    "model_year": ("categorical", MODEL_YEAR_FIELDS),
    "credit_score_type": ("categorical", CREDIT_SCORE_TYPE_FIELDS),
    "delinquency_bucket": ("special", "delinquency_bucket"),
}

# Fixed display order for banded / bucketed dimensions (others order by balance).
ORDERED_LABELS = {
    "fico_band": FICO_BANDS[1],
    "orig_term_band": TERM_BANDS[1],
    "pti_band": PTI_BANDS[1],
    "delinquency_bucket": ["current", "1-30", "31-60", "61-90", "91+", "unknown"],
}

# zeroBalanceCode -> resolution state (SEC ABS-EE auto code set; tolerant of variants).
ZERO_BALANCE_STATES = {
    "1": "Prepaid", "01": "Prepaid",
    "2": "Repurchased", "02": "Repurchased",
    "3": "Charged-off", "03": "Charged-off",
    "4": "Charged-off", "04": "Charged-off",
}
