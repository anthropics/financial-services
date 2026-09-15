"""Field dictionaries for the SEC ABS Schedule AL commercial mortgage (CMBS) schema.

Validated against a real conduit filing (Benchmark 2018-B3, ex102.xml), which
revealed schema facts worth recording:
  * Loans are NOT wrapped in <asset>; they sit flat under <assets>, each starting
    with <assetTypeNumber> (the cmbs_parser record iterator splits on that).
  * A loan may own MULTIPLE <property> blocks (portfolio loans); we use the loan's
    first/primary property for type & state concentration.
  * Percentages are stored as DECIMAL FRACTIONS (rate ".0428" = 4.28%, occupancy
    ".92" = 92%); DSCR is a true ratio (e.g. "1.89"). The parser scales accordingly.
  * There is NO loan-to-value field - LTV is computed as balance / valuation.
  * One real tag has irregular casing: ...NetCashFlowpercentage (lowercase p).
"""
from __future__ import annotations

# The first field of each loan record - used to split the flat <assets> stream.
RECORD_START_FIELD = "assetTypeNumber"

# --- identifiers / descriptors ----------------------------------------------
ASSET_NUMBER_FIELDS = ["assetNumber", "assetNumberId", "loanId"]
PROPERTY_NAME_FIELDS = ["propertyName", "propertyNameText"]

# --- balances ($) ------------------------------------------------------------
BALANCE_FIELDS = [
    "reportPeriodEndActualBalanceAmount",
    "reportPeriodEndScheduledLoanBalanceAmount",
    "reportPeriodBeginningScheduleLoanBalanceAmount",
    "scheduledPrincipalBalanceSecuritizationAmount",
    "originalLoanAmount",
]
ORIGINAL_AMOUNT_FIELDS = ["originalLoanAmount", "scheduledPrincipalBalanceSecuritizationAmount"]

# --- income / coverage -------------------------------------------------------
NOI_FIELDS = ["mostRecentNetOperatingIncomeAmount", "netOperatingIncomeSecuritizationAmount"]
NCF_FIELDS = ["mostRecentNetCashFlowAmount", "netCashFlowFlowSecuritizationAmount"]
# NOTE: real tag uses lowercase 'p' in "...NetCashFlowpercentage" - keep it first.
DSCR_NCF_FIELDS = [
    "mostRecentDebtServiceCoverageNetCashFlowpercentage",
    "mostRecentDebtServiceCoverageNetCashFlowPercentage",
    "securitizationDebtServiceCoverageNetCashFlowPercentage",
]
DSCR_NOI_FIELDS = [
    "mostRecentDebtServiceCoverageNetOperatingIncomePercentage",
    "securitizationDebtServiceCoverageNetOperatingIncomePercentage",
]

# --- valuation / occupancy (percentages are FRACTIONS) ----------------------
VALUATION_FIELDS = ["mostRecentValuationAmount", "valuationSecuritizationAmount"]
OCCUPANCY_FIELDS = [
    "mostRecentPhysicalOccupancyPercentage",
    "physicalOccupancySecuritizationPercentage",
    "occupancyPercentage",
]

# --- rate / term / maturity (rate is a FRACTION) ----------------------------
INTEREST_RATE_FIELDS = [
    "reportPeriodInterestRatePercentage",
    "interestRateSecuritizationPercentage",
    "originalInterestRatePercentage",
]
REMAINING_TERM_FIELDS = ["remainingTermNumber", "remainingTermToMaturityNumber"]
MATURITY_DATE_FIELDS = ["maturityDate", "loanMaturityDate", "scheduledMaturityDate"]

# --- property / status categoricals -----------------------------------------
PROPERTY_TYPE_FIELDS = ["propertyTypeCode", "propertyType"]
PROPERTY_STATE_FIELDS = ["propertyState", "propertyStateCode"]
WATCHLIST_FIELDS = ["servicerWatchlistCode", "servicingWatchListCode"]

# Standard CMBS / CREFC property-type codes -> readable names (pass through unknowns).
PROPERTY_TYPE_NAMES = {
    "MF": "Multifamily", "RT": "Retail", "OF": "Office", "IN": "Industrial",
    "WH": "Warehouse", "LO": "Lodging", "HC": "Health Care", "MU": "Mixed Use",
    "SS": "Self Storage", "MH": "Manufactured Housing", "CH": "Cooperative Housing",
    "SE": "Securities", "ZZ": "Missing", "98": "Other", "OT": "Other",
}

# Categorical distributions to report (label -> candidate source fields).
CATEGORICAL = {
    "property_type": PROPERTY_TYPE_FIELDS,
    "property_state": PROPERTY_STATE_FIELDS,
    "watchlist": WATCHLIST_FIELDS,
}

# --- banding (numeric -> ordered band label); occupancy/LTV are in PERCENT ----
DSCR_BANDS = ([1.0, 1.25, 1.5, 2.0], ["<1.0x", "1.0-1.25x", "1.25-1.5x", "1.5-2.0x", "2.0x+"])
LTV_BANDS = ([50, 60, 70, 80], ["<=50%", "50-60%", "60-70%", "70-80%", "80%+"])
OCCUPANCY_BANDS = ([80, 90, 95], ["<80%", "80-90%", "90-95%", "95%+"])

DIMENSION_NAMES = [
    "property_type", "property_state", "watchlist",
    "dscr_band", "ltv_band", "occupancy_band", "maturity_year",
]

ORDERED_LABELS = {
    "dscr_band": DSCR_BANDS[1],
    "ltv_band": LTV_BANDS[1],
    "occupancy_band": OCCUPANCY_BANDS[1],
}
