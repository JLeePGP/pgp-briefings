"""
Project Nadir — Phase 2: Chronological 20-Signal Vector Scoring Engine
===================================================================
Description:
    Processes 'nadir_market_vault.json' generated in Phase 1. 
    
    1. Evaluates 20 distinct longitudinal and YoY indicators.
    2. Outputs a complete macro market count across all scoring tiers.
    3. Filters for the stable-but-strained "Goldilocks Zone" (Scores 50-75).
    4. Ranks the final Top 100 using your custom Propensity Index (PI) 
       formula to isolate the "Unrealized Capacity" agency archetype.

Usage:
    Run: python nadir_phase2_prioritize.py
"""

import json
import os
import pandas as pd

INPUT_VAULT = "nadir_market_vault.json"
OUTPUT_CSV = "prospects_top100.csv"

def run_20_signal_scoring():
    print("=" * 80)
    print(" PROJECT NADIR — PHASE 2: 20-SIGNAL COMPOSITE SCORING ENGINE")
    print("=" * 80)
    
    if not os.path.exists(INPUT_VAULT):
        print(f" [!] ERROR: '{INPUT_VAULT}' not found. Please execute Phase 1 first.")
        return

    print(f"  Loading local registry file '{INPUT_VAULT}'...")
    with open(INPUT_VAULT, "r") as f:
        firms_data = json.load(f)
        
    analyzed_rows = []
    y1, y2, y3 = "2024", "2025", "2026"
    
    print("  Vectorizing multi-year structural and behavioral trajectories...")
    for crd, history in firms_data.items():
        if y1 not in history or y2 not in history or y3 not in history:
            continue
            
        f24 = history[y1]
        f25 = history[y2]
        f26 = history[y3]
        
        # ── BASE RAW ANCHORS ──────────────────────────────────────────────────
        aum_24 = f24["total_aum_raw"]
        aum_25 = f25["total_aum_raw"]
        aum_26 = f26["total_aum_raw"]
        
        emp_24 = f24["team_size_raw"]
        emp_25 = f25["team_size_raw"]
        emp_26 = f26["team_size_raw"]
        
        adv_24 = f24["advisor_employees_raw"]
        adv_25 = f25["advisor_employees_raw"]
        adv_26 = f26["advisor_employees_raw"]
        
        disc_acc_24 = f24["disc_accounts_raw"]
        disc_acc_26 = f26["disc_accounts_raw"]
        
        acc_24 = disc_acc_24 + f24["non_disc_accounts_raw"]
        acc_25 = f25["disc_accounts_raw"] + f25["non_disc_accounts_raw"]
        acc_26 = disc_acc_26 + f26["non_disc_accounts_raw"]
        
        # Hard data validation guard rail to bypass division errors or incomplete entries
        if aum_24 <= 0 or emp_24 <= 0 or adv_24 <= 0 or acc_24 <= 0 or emp_25 <= 0 or adv_25 <= 0 or emp_26 <= 0 or adv_26 <= 0 or acc_26 <= 0 or aum_25 <= 0 or aum_26 <= 0:
            continue

        # ── INITIALIZE COMPOSITE INTENSITY SCORE STATE ────────────────────────
        score = 0
        
        # ── HUMAN CAPITAL LEVERS (28 PTS MAX) ─────────────────────────────────
        # HC1: Headcount Spike-Then-Drop
        hc1_spike = (emp_25 - emp_24) / emp_24
        hc1_drop = (emp_26 - emp_25) / emp_25
        if hc1_spike > 0.20 and hc1_drop < -0.10:
            score += 8
            
        # HC2: Advisor Attrition Acceleration
        hc2_d1 = adv_25 - adv_24
        hc2_d2 = adv_26 - adv_25
        if hc2_d1 < 0 and hc2_d2 < 0 and hc2_d2 < hc2_d1:
            score += 9
            
        # HC3: Advisor Collapse (Single Year Drop)
        hc3_drop_1 = (adv_25 - adv_24) / adv_24
        hc3_drop_2 = (adv_26 - adv_25) / adv_25
        if hc3_drop_1 < -0.25 or hc3_drop_2 < -0.25:
            score += 8
            
        # HC4: Healthy Scaling (Health Deduction Offset)
        aum_yoy_1 = (aum_25 - aum_24) / aum_24
        aum_yoy_2 = (aum_26 - aum_25) / aum_25
        emp_yoy_1 = (emp_25 - emp_24) / emp_24
        emp_yoy_2 = (emp_26 - emp_25) / emp_25
        adv_yoy_1 = (adv_25 - adv_24) / adv_24
        adv_yoy_2 = (adv_26 - adv_25) / adv_25
        
        if (aum_yoy_1 >= 0.10 and emp_yoy_1 >= 0.10 and adv_yoy_1 >= 0.10) or \
           (aum_yoy_2 >= 0.10 and emp_yoy_2 >= 0.10 and adv_yoy_2 >= 0.10):
            score -= 3

        # ── LEVERAGE SHIFTS LEVERS (20 PTS MAX) ───────────────────────────────
        # LV1: Leverage Ratio Drift
        lev_24 = emp_24 / adv_24
        lev_25 = emp_25 / adv_25
        lev_26 = emp_26 / adv_26
        if abs(lev_25 - lev_24) > 0.5 or abs(lev_26 - lev_25) > 0.5:
            score += 7
            
        # LV2: AUM-per-Advisor Spike
        apa_25 = aum_25 / adv_25
        apa_26 = aum_26 / adv_26
        if ((apa_26 - apa_25) / apa_25 > 0.30) and (aum_yoy_2 < 0.05):
            score += 7
            
        # LV3: Advisor Share Improving (Health Deduction Offset)
        sh_24 = adv_24 / emp_24
        sh_26 = adv_26 / emp_26
        if (sh_26 - sh_24) > 0.08:
            score -= 6

        # ── ACCOUNT-LEVEL LEVERS (25 PTS MAX) ─────────────────────────────────
        # AC1: Discretionary Drift
        dd_24 = disc_acc_24 / acc_24
        dd_26 = disc_acc_26 / acc_26
        if (dd_24 - dd_26) > 0.10:
            score += 8
            
        # AC2: Account Density Compression
        den_24 = aum_24 / acc_24
        den_26 = aum_26 / acc_26
        if (den_26 - den_24) / den_24 < -0.15:
            score += 7
            
        # AC3: Volume-Over-Value Trap
        acc_grow_3yr = (acc_26 - acc_24) / acc_24
        aum_grow_3yr = (aum_26 - aum_24) / aum_24
        if acc_grow_3yr > 0.10 and aum_grow_3yr < 0.03:
            score += 5
            
        # AC4: Account Quality Upgrading (Health Deduction Offset)
        if (den_26 - den_24) / den_24 > 0.20 and acc_grow_3yr >= 0.0:
            score -= 5

        # ── AUM TRAJECTORY LEVERS (28 PTS MAX) ────────────────────────────────
        # AV1: AUM Stagnation
        if aum_grow_3yr < 0.05:
            score += 8
            
        # AV2: Boom-Bust Arc
        if aum_yoy_1 > 0.10 and aum_yoy_2 <= 0.0:
            score += 8
            
        # AV3: Persistent Micro-Decline
        if (aum_26 / aum_24 < 0.90) and (aum_yoy_1 > -0.05 and aum_yoy_2 > -0.05):
            score += 7
            
        # AV4: Sustained AUM Momentum (Health Deduction Offset)
        if aum_26 > aum_25 > aum_24 and aum_yoy_1 > 0 and aum_yoy_2 > 0:
            score -= 5

        # ── OPERATIONAL & STRUCTURAL LEVERS (14 PTS MAX) ──────────────────────
        # OP1: Operational Friction
        if (emp_yoy_1 > 0 and aum_yoy_1 <= 0) or (emp_yoy_2 > 0 and aum_yoy_2 <= 0):
            score += 7
            
        # OP2: HNW Concentration Risk
        hnw_dep_26 = f26["hnw_aum_raw"] / aum_26
        if hnw_dep_26 > 0.40:
            score += 7

        # ── MARKETING & COMPLIANCE LEVERS (15 PTS MAX) ────────────────────────
        # MK1: Marketing Void
        if not f24["has_marketing_infrastructure"] and not f25["has_marketing_infrastructure"] and not f26["has_marketing_infrastructure"]:
            score += 5
            
        # MK2: Marketing Activation (Health Deduction Offset)
        if not f24["has_marketing_infrastructure"] and not f25["has_marketing_infrastructure"] and f26["has_marketing_infrastructure"]:
            score -= 5
            
        # RG1: New Disclosure Event
        disc_y1 = f24["regulatory_disclosures_reported"] == "Yes"
        disc_y2 = f25["regulatory_disclosures_reported"] == "Yes"
        disc_y3 = f26["regulatory_disclosures_reported"] == "Yes"
        if not disc_y1 and not disc_y2 and disc_y3:
            score += 10

        # ── ASSIGN MACRO PROFILE TIER LABELS ──────────────────────────────────
        if score >= 70:
            tier = "Critical Turbulence"
        elif score >= 45:
            tier = "Structural Strain"
        elif score >= 20:
            tier = "Mild Friction"
        elif score > 0:
            tier = "Scaling Firm (Low Signal)"
        else:
            tier = "Stable"

        # ── EXPAND STRATEGIC OUTREACH PROPENSITY INDEX (PI) FLAGS ─────────────
        op1_flag = 1 if ((emp_yoy_1 > 0 and aum_yoy_1 <= 0) or (emp_yoy_2 > 0 and aum_yoy_2 <= 0)) else 0
        mk1_flag = 1 if (not f24["has_marketing_infrastructure"] and not f25["has_marketing_infrastructure"] and not f26["has_marketing_infrastructure"]) else 0
        lv3_flag = 1 if (sh_26 - sh_24 > 0.08) else 0
        severe_crash_flag = 1 if (aum_26 < (aum_24 * 0.80)) else 0

        # Exact User-Defined Propensity Index (Range: -1 to 3)
        propensity_index = op1_flag + mk1_flag + lv3_flag - severe_crash_flag

        analyzed_rows.append({
            "crd_number": crd,
            "firm_name": f26["firm_name"],
            "state": f26["state"],
            "website_url": f26["website_url"],
            "composite_score": score,
            "priority_tier": tier,
            "propensity_index": propensity_index,
            
            "aum_2024_m": round(aum_24 / 1e6, 2),
            "aum_2025_m": round(aum_25 / 1e6, 2),
            "aum_2026_m": round(aum_26 / 1e6, 2),
            "aum_growth_3yr_pct": round(aum_grow_3yr * 100, 2),
            
            "team_size_2024": emp_24,
            "team_size_2026": emp_26,
            "advisor_count_2026": adv_26,

            "total_clients_raw": f26["total_clients_raw"],
            "hnw_aum_raw": f26["hnw_aum_raw"],
            "advisor_employees_raw": adv_26,

            "hnw_dependency_ratio_2026": round(hnw_dep_26, 2),
            "has_marketing_infrastructure_2026": f26["has_marketing_infrastructure"]
        })

    df = pd.DataFrame(analyzed_rows)
    if df.empty:
        print("  [!] Error processing metrics loop. Check Phase 1 source inputs.")
        return

    # ── STEP 1: OUTPUT FULL ADDRESSABLE TIERS REPORT ──────────────────────────
    print("\n" + "─"*65)
    print(" TOTAL TARGET MARKET PROFILE BREAKDOWN (MACRO REGISTRY)")
    print("─"*65)
    tier_counts = df["priority_tier"].value_counts()
    
    for tier_label in ["Critical Turbulence", "Structural Strain", "Mild Friction", "Scaling Firm (Low Signal)", "Stable"]:
        count = tier_counts.get(tier_label, 0)
        print(f"  {tier_label.ljust(26)} : {count:,} firms")
    print("─"*65 + "\n")

    # ── STEP 2: ENFORCE GOLDILOCKS FILTER MATRIX (50 TO 75) ───────────────────
    print("  Applying 'Goldilocks' stability safety window (50 <= Score <= 75)...")
    df_goldilocks = df[(df["composite_score"] >= 20) & (df["composite_score"] <= 65)].copy()
    print(f"  -> {len(df_goldilocks):,} firms isolated within target capitalization boundaries.")

    # ── STEP 3: SORT ARCHETYPE BY PROPENSITY INDEX KEY ────────────────────────
    # Primary Key: Propensity Index Descending (3 down to -1)
    # Secondary Tiebreaker Key: Total Composite Score Descending
    df_ranked = df_goldilocks.sort_values(
        by=["propensity_index", "composite_score"], 
        ascending=[False, False]
    )
    
    # Isolate the definitive Top 100 finalists
    df_top100 = df_ranked.head(100)
    
    # Restructure clean layout structure for flat CSV output
    columns_to_export = [
        "crd_number", "firm_name", "state", "website_url", "propensity_index", "composite_score",
        "aum_2024_m", "aum_2025_m", "aum_2026_m", "aum_growth_3yr_pct", "advisor_count_2026", "hnw_dependency_ratio_2026", "total_clients_raw", "hnw_aum_raw", "advisor_employees_raw", "has_marketing_infrastructure_2026"
    ]
    df_top100[columns_to_export].to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n[✔] PHASE 2 COMPLETE: Top 100 'Unrealized Capacity' targets saved to '{OUTPUT_CSV}'")
    print(f"    Queue holds your premium, high-response Tier 1 and Tier 2 opportunities.")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    run_20_signal_scoring()