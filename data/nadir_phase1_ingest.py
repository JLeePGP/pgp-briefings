"""
Project Nadir — Phase 1: Longitudinal Ingestion Engine
======================================================
Source: SEC Form ADV Part 1A bulk CSVs
https://www.sec.gov/help/foiadocsinvafoiahtm.html

DESCRIPTION:
    Ingests 3 consecutive years of SEC bulk data dumps, applies strict institutional
    baseline filters (ICP qualifiers + Strict Scale Windows), standardizes raw 
    operational metrics, and compiles a multi-year nested dictionary mapped by 
    unique Organization CRD#.

DEPENDENCIES:
    pip install pandas

USAGE:
    1. Place this script in the same directory as your 3 SEC CSV files.
    2. Ensure the filenames in the YEAR_FILES dictionary match your local files.
    3. Run: python nadir_phase1.py
"""

import pandas as pd
import os

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
# Map your specific years to your exact local CSV data file names
YEAR_FILES = {
    2024: "ia050324.csv",  
    2025: "ia050225.csv",  
    2026: "ia050126.csv"  
}

# Strict Target Scale Window to focus resources on the absolute best ICP fits
MIN_AUM = 150_000_000         # $150 Million Floor
MAX_AUM = 5_000_000_000       # $5 Billion Ceiling
MAX_EMPLOYEES = 200           # 200 Total Team Size Ceiling

# Form ADV Part 1A column definitions used to aggregate true metrics
CLIENT_COUNT_COLS = [
    "5D(a)(1)", "5D(b)(1)", "5D(c)(1)", "5D(d)(1)", "5D(e)(1)",
    "5D(f)(1)", "5D(g)(1)", "5D(h)(1)", "5D(i)(1)", "5D(j)(1)",
    "5D(k)(1)", "5D(l)(1)", "5D(m)(1)",
]

MARKETING_COLS = [
    "5L(1)(a)", "5L(1)(b)", "5L(1)(c)", "5L(1)(d)", "5L(1)(e)",
    "5L(2)", "5L(3)", "5L(4)"
]

DISC_COLS_TO_TRACK = [
    "11A(1)", "11A(2)", "11B(1)", "11B(2)", "11C(1)", "11C(2)", 
    "11C(3)", "11C(4)", "11C(5)", "11D(1)", "11D(2)", "11D(3)"
]
# ──────────────────────────────────────────────────────────────────────────────


def safe_float(val):
    try:
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0


def safe_int(val):
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return 0


def load_and_clean_base_csv(path):
    if not os.path.exists(path):
        print(f"  WARNING: File tracking error. '{path}' not found. Skipping year.")
        return None
        
    print(f"  Reading {path} into system memory...")
    df = pd.read_csv(path, dtype=str, encoding="latin-1", low_memory=False)
    initial_count = len(df)
    
    # ── MANDATORY HARD FILTERS (Institutional Baseline Fit) ─────────────────────
    # 1. EV = Y (Compensated via % of Assets Under Management)
    df = df[df["5E(1)"].str.strip().str.upper() == "Y"].copy()
    
    # 2. EZ = N (Does NOT accept sales commissions - ensures true independence)
    df = df[df["5E(5)"].str.strip().str.upper() == "N"].copy()
    
    # 3. FD = Y (Provides continuous and regular advisory management services)
    df = df[df["5F(1)"].str.strip().str.upper() == "Y"].copy()
    
    # ── SCALE WINDOW FILTERS (ICP Optimization) ──────────────────────────────────
    # 4. AUM Window Calculation ($150M to $5B)
    df["_disc"] = df["5F(2)(a)"].apply(safe_float)
    df["_ndisc"] = df["5F(2)(b)"].apply(safe_float)
    df["_total_aum"] = df["_disc"] + df["_ndisc"]
    df = df[(df["_total_aum"] >= MIN_AUM) & (df["_total_aum"] <= MAX_AUM)].copy()
    
    # 5. Team Size Headcount Cap (200 Employee Ceil via Item 5A)
    df["_emp_count"] = df["5A"].apply(safe_int)
    df = df[df["_emp_count"] <= MAX_EMPLOYEES].copy()
    
    print(f"  -> {len(df):,} of {initial_count:,} firms passed compliance and scale filters.")
    return df


def extract_all_raw_metrics(row, df_columns):
    """Normalizes and maps raw metrics out of the SEC row architecture."""
    disc_aum = safe_float(row.get("5F(2)(a)", 0))
    ndisc_aum = safe_float(row.get("5F(2)(b)", 0))
    total_reg_aum = safe_float(row.get("5F(2)(c)", 0))
    if total_reg_aum == 0:
        total_reg_aum = disc_aum + ndisc_aum  # Safety operational fallback

    total_clients = sum(safe_int(row.get(c, 0)) for c in CLIENT_COUNT_COLS if c in df_columns)
    has_disclosure_flag = any(str(row.get(c, "")).strip().upper() == "Y" for c in DISC_COLS_TO_TRACK if c in df_columns)

    return {
        "firm_name": str(row.get("Primary Business Name", "")).strip(),
        "address": str(row.get("Main Office Street Address 1", "")).strip(),
        "state": str(row.get("Main Office State", "")).strip().upper(),
        "website_url": str(row.get("Website Address", "")).strip(),
        "fiscal_year_end_month": str(row.get("3B", "")).strip(),
        "team_size_raw": safe_int(row.get("5A", 0)),
        "advisor_employees_raw": safe_int(row.get("5B(1)", 0)),
        
        "total_aum_raw": total_reg_aum,
        "disc_aum_raw": disc_aum,
        "disc_accounts_raw": safe_int(row.get("5F(2)(d)", 0)),
        "non_disc_aum_raw": ndisc_aum,
        "non_disc_accounts_raw": safe_int(row.get("5F(2)(e)", 0)),
        
        "total_clients_raw": total_clients,
        "hnw_client_count_raw": safe_int(row.get("5D(b)(1)", 0)),
        "hnw_aum_raw": safe_float(row.get("5D(b)(3)", 0)),
        "non_hnw_client_count_raw": safe_int(row.get("5D(a)(1)", 0)),
        "non_hnw_aum_raw": safe_float(row.get("5D(a)(3)", 0)),
        
        "has_marketing_infrastructure": any(str(row.get(c, "")).strip().upper() == "Y" for c in MARKETING_COLS if c in df_columns),
        "regulatory_disclosures_reported": "Yes" if has_disclosure_flag else "None Reported",
        "latest_adv_filing_date": str(row.get("Latest ADV Filing Date", "")).strip()
    }


def run_longitudinal_ingestion():
    print("=" * 70)
    print(" PROJECT NADIR — PHASE 1: LONGITUDINAL INGESTION ENGINE RUNNING")
    print("=" * 70)
    
    firms = {}
    
    for year, file_path in YEAR_FILES.items():
        print(f"\nProcessing Pipeline Block for Calendar Year: {year}...")
        df = load_and_clean_base_csv(file_path)
        if df is None:
            continue
            
        df_columns = df.columns
        
        for _, row in df.iterrows():
            crd = str(row.get("Organization CRD#", "")).strip()
            if not crd:
                continue
                
            if crd not in firms:
                firms[crd] = {}
                
            firms[crd][year] = extract_all_raw_metrics(row, df_columns)
            
    print(f"\n{'='*70}")
    print(f"[✔] PHASE 1 COMPLETE: {len(firms):,} unique qualified sweet-spot RIAs compiled.")
    print(f"{'='*70}\n")
    return firms


if __name__ == "__main__":
    # Execute the ingestion engine
    firms_database = run_longitudinal_ingestion()
    
    # Save the memory tree to a local JSON file for Phase 2 to use instantly
    import json
    print("  Saving qualified registry to 'nadir_market_vault.json'...")
    with open("nadir_market_vault.json", "w") as f:
        json.dump(firms_database, f)
    print("[✔] Phase 1 Vault Locked.\n")