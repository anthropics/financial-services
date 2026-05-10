---
skill: kyc-onboarding-rules
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# KYC and Onboarding Rules

## Overview

KAELUM operates KYC and onboarding requirements across three participant
types: Customers, Creators, and Merchants. All onboarding is governed
by K.A.T.E. via the Onboarding Concierge agent and the Compliance and
Regulatory agent. SENTINEL screens all participants at onboarding and
on an ongoing basis.

## Customer Onboarding

**Minimum Active Balance:** 400 KLM (£36 at floor price)
**Framing:** Starting balance, not a fee

**Required:**
- Name and email verification
- Account creation via kaelum.app
- Active Balance of 400 KLM purchased to activate account
- Agreement to KAELUM Customer terms

**KYC Level:** Standard consumer KYC
- Identity verification (name, date of birth, address)
- SENTINEL AML screening on account creation
- Ongoing transaction monitoring by SENTINEL

**Onboarding Flow:**
1. Customer registers at kaelum.app
2. Onboarding Concierge agent guides through verification
3. Identity verified by Compliance and Regulatory agent
4. Active Balance of 400 KLM purchased via TrueLayer or Stripe
3. Account activated
4. new_user_registered event fired to Paperclip, routed to
   Onboarding Concierge agent

## Creator Onboarding

**Minimum Active Balance:** 1,800 KLM (£162 at floor price)
**Framing:** Starting balance, not a fee

**Required:**
- All Customer requirements plus:
- Active public profile with content history (mandatory for verification)
- Social profile verification by K.A.T.E. Creator Acquisition agent
- Agreement to KAELUM Creator terms
- Active Balance of 1,800 KLM purchased to unlock Creator tools

**KYC Level:** Enhanced consumer KYC with commerce verification
- Identity verification (as Customer)
- Social profile authenticity check by K.A.T.E.
- Content history review confirming active creator status
- SENTINEL AML screening on account creation and on first redemption
- Business activity verification if Creator operates as a business entity

**Onboarding Flow:**
1. Creator applies via kaelum.app Creator onboarding
2. Creator Acquisition agent reviews social profile and content history
3. Compliance and Regulatory agent completes KYC
4. Active Balance of 1,800 KLM purchased
5. Creator Studio, Social Paylinks, Commerce Drops, and all Creator
   tools unlocked
6. new_user_registered event fired to Paperclip

**Creator Tools Unlocked on Onboarding:**
- Creator Studio
- Social Paylinks
- Commerce Drops
- Creator Advisor
- PCC (Personal Commerce Control)
- Discount Engine
- Bill Pay
- Agentic Banking Suite
- KVI Creator Dashboard
- KST Revenue Calculator
- Referral Hub
- Research Scout
- Social Commerce

## Merchant Onboarding

**Minimum Active Balance:** 3,690 KLM (£332.10 at floor price)
**Framing:** Starting balance, not a fee

**Required:**
- Business registration verification
- Director/owner identity verification
- Business bank account confirmation
- Agreement to KAELUM Merchant terms
- Active Balance of 3,690 KLM purchased to activate merchant account

**KYC Level:** Full business KYC and AML
- Business identity verification (Companies House or equivalent)
- Director/UBO identity verification
- Source of funds confirmation
- SENTINEL AML screening on account creation and on every redemption
- Ongoing transaction monitoring and periodic re-verification

**Onboarding Flow:**
1. Merchant applies via kaelum.app Merchant onboarding
2. Merchant Acquisition agent manages pipeline
3. Compliance and Regulatory agent completes business KYC
4. SENTINEL clears AML check
5. Active Balance of 3,690 KLM purchased
6. Merchant account activated
7. new_user_registered event fired to Paperclip

## Ongoing Compliance

All three participant types are subject to:

- Continuous SENTINEL transaction monitoring
- Periodic KYC refresh (frequency determined by risk profile)
- kyc_result_received event fired to Paperclip on every KYC update,
  routed to Compliance and Regulatory agent and Onboarding Concierge
- Immediate account restriction if SENTINEL flags suspicious activity

## KLM Redemption KYC

Before any Merchant or Creator redemption is processed:

- SENTINEL runs a full AML screen on the redemption request
- Compliance and Regulatory agent confirms KYC is current
- Finance agent approves redemption above threshold amounts
- Redemption processed at current KLM price at time of approval

## Commands

- `/kyc-onboarding-rules:onboarding-status` — Return KYC status for
  a given participant account
- `/kyc-onboarding-rules:redemption-clearance` — Run pre-redemption
  KYC and AML check for a given Merchant or Creator
- `/kyc-onboarding-rules:refresh-required` — Return list of participants
  due for KYC refresh
- `/kyc-onboarding-rules:sentinel-flags` — Return active SENTINEL flags
  across all participant accounts