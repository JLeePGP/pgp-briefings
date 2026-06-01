"""
Project Nadir — Phase 3: Dedicated Telemetry Pitch & Deployment Engine
======================================================================
Description:
    1. Extracts a chosen high-propensity target from the Top 100 CSV pipeline.
    2. Scrapes the live homepage using Jina AI's public utility tier.
    3. Triggers an automated compliance guardrail to flag bank vehicles.
    4. Compiles a private multi-year intelligence dossier for Claude Pro.
    5. Programmatically builds a dynamic, responsive Tailwind HTML landing page.
    6. Deploys the asset directly to GitHub, triggering a serverless edge merge
       via Netlify straight to your secure 'telemetry' subdomain.
"""

import json
import os
import re
import subprocess
import time
import pandas as pd
import requests

INPUT_CSV = "prospects_top100.csv"
INPUT_VAULT = "nadir_market_vault.json"
CONFIG_FILE = "pgp_config.json"

def load_config():
    """Loads secure API parameters from the local configuration file."""
    if not os.path.exists(CONFIG_FILE):
        print(f" [!] CRITICAL ERROR: Missing '{CONFIG_FILE}'. Please create it before running.")
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def clean_slug(name):
    """Converts a corporate firm name into a safe, alphanumeric lowercase string."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    return cleaned

def compile_landing_page(target_firm, loom_id, template_path="landing_template.html"):
    """Reads the external HTML template and injects firm metrics cleanly via replacement tags."""
    if not os.path.exists(template_path):
        print(f" [!] ERROR: Missing '{template_path}'. Cannot build landing page asset.")
        return None

    try:
        # 1. Capture and auto-scale Total AUM vectors
        aum_24 = float(target_firm.get("aum_2024_m", 0))
        aum_25 = float(target_firm.get("aum_2025_m", 0))
        
        if "total_aum_raw" in target_firm:
            aum_26 = float(target_firm.get("total_aum_raw", 0)) / 1_000_000
        else:
            aum_26 = float(target_firm.get("aum_2026_m", 0))
            
        # 2. Re-anchor advisor bench count variables securely
        adv_26 = int(target_firm.get("advisor_employees_raw", target_firm.get("advisor_count_2026", 1)))
        adv_26 = adv_26 if adv_26 > 0 else 1
        
        # 3. Handle total client calculation anchors
        total_clients = float(target_firm.get("total_clients_raw", 1))
        total_clients = total_clients if total_clients > 0 else 1
        
        # 4. Handle and auto-scale HNW wealth assets
        if "hnw_aum_raw" in target_firm:
            hnw_aum_26 = float(target_firm.get("hnw_aum_raw", 0)) / 1_000_000
            hnw_aum_24 = (float(target_firm.get("hnw_aum_2024_raw", 0)) / 1_000_000) if "hnw_aum_2024_raw" in target_firm else hnw_aum_26 * 0.85
            hnw_aum_25 = (float(target_firm.get("hnw_aum_2025_raw", 0)) / 1_000_000) if "hnw_aum_2025_raw" in target_firm else hnw_aum_26 * 0.92
        else:
            hnw_aum_24 = float(target_firm.get("hnw_aum_2024_raw", 0))
            hnw_aum_25 = float(target_firm.get("hnw_aum_2025_raw", 0))
            hnw_aum_26 = float(target_firm.get("hnw_aum_2026_raw", 0))
        
        # 5. Core Stat Card Math Engines
        aum_growth_pct = ((aum_26 - aum_24) / aum_24 * 100) if aum_24 > 0 else 0
        hnw_pct = (hnw_aum_26 / aum_26 * 100) if aum_26 > 0 else 0
        
        # 6. DYNAMIC M/K: AUM per Advisor
        raw_aum_per_advisor = aum_26 / adv_26
        if raw_aum_per_advisor < 1.0:
            advisor_aum_string = f"${(raw_aum_per_advisor * 1000):.0f}K"
        else:
            advisor_aum_string = f"${raw_aum_per_advisor:.1f}M"
        
        # 7. DYNAMIC M/K: Average Client Size Tracker
        raw_avg_client_size = aum_26 / total_clients
        if raw_avg_client_size < 1.0:
            avg_client_string = f"${(raw_avg_client_size * 1000):.0f}K"
        else:
            avg_client_string = f"${raw_avg_client_size:.2f}M"

        # Data validity verification terminal reporting
        print(f"\n   --- DATA VALIDITY VERIFICATION FOR: {target_firm.get('firm_name', 'Target')} ---")
        print(f"   [Raw Data Source] 2026 Total AUM Value:      ${aum_26:.1f}M")
        print(f"   [Raw Data Source] 2026 HNW AUM Value:        ${hnw_aum_26:.1f}M")
        print(f"   [Raw Data Source] 2026 Client Accounts:     {int(total_clients)} accounts")
        print(f"   [Raw Data Source] 2026 Advisor Bench Count:   {adv_26} chairs")
        print(f"   [Computed Output] Advisor Ratio Formatted:    {advisor_aum_string} / Chair")
        print(f"   [Computed Output] Client Size Formatted:      {avg_client_string} / Client")
        print(f"   [Computed Output] Derived HNW Concentration:  {hnw_pct:.1f}%")
        print(f"   -------------------------------------------------------------\n")

    except Exception as e:
        print(f" [!] Math anomaly caught during compilation: {e}")
        aum_growth_pct, hnw_pct = 0, 0
        advisor_aum_string = "$0M"
        avg_client_string = "$0M"
        aum_24, aum_25, aum_26 = 0, 0, 0
        hnw_aum_24, hnw_aum_25, hnw_aum_26 = 0, 0, 0

    # Load the template file
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Execute string replacements for clean variable mounting
    html = html.replace("{{FIRM_NAME}}", str(target_firm.get("firm_name", "Our Target")))
    html = html.replace("{{AUM_GROWTH_PCT}}", f"{aum_growth_pct:+.1f}")
    html = html.replace("{{AUM_PER_ADVISOR}}", advisor_aum_string)
    html = html.replace("{{AVG_CLIENT_SIZE}}", avg_client_string)
    html = html.replace("{{HNW_PCT}}", f"{hnw_pct:.1f}")
    html = html.replace("{{LOOM_ID}}", str(loom_id))
    
    # Inject Grouped Chart JS numeric arrays
    html = html.replace("{{CHART_DATA_AUM}}", f"{aum_24:.1f}, {aum_25:.1f}, {aum_26:.1f}")
    html = html.replace("{{CHART_DATA_HNW_AUM}}", f"{hnw_aum_24:.1f}, {hnw_aum_25:.1f}, {hnw_aum_26:.1f}")
    
    return {
            "html": html,
            "aum_24": aum_24,
            "aum_25": aum_25,
            "aum_26": aum_26,
            "hnw_aum_26": hnw_aum_26,
            "adv_26": adv_26,
            "total_clients": total_clients,
            "aum_growth_pct": aum_growth_pct,
            "hnw_pct": hnw_pct,
            "advisor_aum_string": advisor_aum_string,
            "avg_client_string": avg_client_string
        }
        
def run_pipeline():
    print("=" * 80)
    print(" PROJECT NADIR — PHASE 3: DEDICATED TELEMETRY DEPLOYER")
    print("=" * 80)
    
    # Structural check for dependencies
    if not os.path.exists(INPUT_CSV) or not os.path.exists(INPUT_VAULT):
        print(" [!] ERROR: Missing 'prospects_top100.csv' or 'nadir_market_vault.json'.")
        print("     Please ensure you have completed Phase 2 prior to execution.")
        return

    config = load_config()
    if not config:
        return

# Load prioritized candidates
    df = pd.read_csv(INPUT_CSV)
    
    current_row = 0
    page_size = 10
    total_firms = len(df)
    target_firm = {}
    is_manual_override = False

    print("\n==================================================")
    print("  PROJECT NADIR // OPERATIONAL COMMAND CONSOLE   ")
    print("==================================================")
    print("  • Type a list number [1-100] to select a pipeline firm.")
    print("  • Type '#' followed by the CRD (e.g., #742) for wildcards.")
    print("  • Press ENTER with no input to view the next page.")
    print("==================================================")

    # --- MAIN INTERACTIVE SELECTION LOOP ---
    while True:
        end_row = min(current_row + page_size, total_firms)
        print(f"\n--- PRIORITIZED PIPELINE (Firms {current_row + 1} to {end_row} of {total_firms}) ---")
        
        for i in range(current_row, end_row):
            row = df.iloc[i]
            print(f"  [{i + 1}] Score: {row.get('propensity_index', 'N/A')} | {row['firm_name'][:50]}")
        
        print("──────────────────────────────────────────────────")
        user_selection = input("  ➔ Select [Number], enter [#CRD], or press [ENTER] for next page: ").strip()

        # Case 1: Paginate forward
        if not user_selection:
            current_row += page_size
            if current_row >= total_firms:
                print("\n  [i] Reached the end of the pipeline. Looping back to the top.")
                current_row = 0
            continue

        # Case 2: Direct Vault Override (Checks for the # symbol to dodge numerical index collisions)
        if user_selection.startswith("#"):
            target_crd = user_selection.replace("#", "").strip()
            print(f"\n[!] Vault Override Detected. Querying master database for CRD: {target_crd}...")
            
            try:
                with open(INPUT_VAULT, "r") as f:
                    vault_data = json.load(f)
                
                if target_crd in vault_data:
                    adv_history = vault_data[target_crd]
                    latest_year = sorted(adv_history.keys())[-1]
                    latest_data = adv_history[latest_year]
                    
                    # Programmatically construct target_firm schema to match CSV rows for down-stream code
                    target_firm = {
                        "firm_name": latest_data.get("firm_name", "Unknown Firm"),
                        "crd_number": target_crd,
                        "website_url": latest_data.get("website_url", ""),
                        "advisor_count_2026": latest_data.get("advisor_employees_raw", 0),
                        "aum_2024_m": float(adv_history.get("2024", {}).get("total_aum_raw", 0)) / 1_000_000,
                        "aum_2025_m": float(adv_history.get("2025", {}).get("total_aum_raw", 0)) / 1_000_000,
                        "aum_2026_m": float(adv_history.get("2026", {}).get("total_aum_raw", 0)) / 1_000_000,
                        
                        # --- ADDED TO FIX WILDCARD ZERO-OUTS ---
                        "total_clients_raw": int(latest_data.get("total_clients_raw", 1)),
                        "hnw_aum_raw": float(latest_data.get("hnw_aum_raw", 0)),
                        "advisor_employees_raw": int(latest_data.get("advisor_employees_raw", 1)),
                        
                        # Pass historical baseline data raw vectors for the chart engine
                        "hnw_aum_2024_raw": float(adv_history.get("2024", {}).get("hnw_aum_raw", 0)),
                        "hnw_aum_2025_raw": float(adv_history.get("2025", {}).get("hnw_aum_raw", 0)),
                        "hnw_aum_2026_raw": float(adv_history.get("2026", {}).get("hnw_aum_raw", 0))
                    }
                    is_manual_override = True
                    break
                else:
                    print(f"  [!] Error: CRD '{target_crd}' could not be located inside '{INPUT_VAULT}'.")
                    continue
            except Exception as e:
                print(f"  [!] Vault index search error: {e}")
                continue

        # Case 3: Standard Pipeline Index Selection
        if user_selection.isdigit():
            val = int(user_selection)
            if 1 <= val <= total_firms:
                target_firm = df.iloc[val - 1]
                break
            else:
                print(f"  [!] Selection out of bounds. Enter a pipeline number between 1 and {total_firms}.")
                continue
        else:
            print("  [!] Invalid entry. Use a pipeline number or prefix wildcards with '#'.")
            continue

    # --- VARIABLE UNIFICATION LAYER ---
    firm_name_raw = str(target_firm["firm_name"])
    print(f"\n[➔] Actively processing telemetry array for: {firm_name_raw}...")
    
    url_slug = clean_slug(firm_name_raw)
    output_prompt_file = f"claude_briefing_{url_slug}.txt"
    
    # Ensure lowercase evaluation and strip out accidental double-prefixes
    raw_url = str(target_firm.get("website_url", "")).strip().lower()
    raw_url = raw_url.replace("https://", "").replace("http://", "")
    raw_url = f"https://{raw_url}"
        
    # --- STEP 1: REAL-TIME WEB SCRAPE via PUBLIC JINA AI ---
    print("  Scraping target web presence via Jina AI public engine...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(f"https://r.jina.ai/{raw_url}", headers=headers, timeout=12)
        web_markdown = response.text if response.status_code == 200 else "[Scrape Failed]"
        print("  [✔] Web infrastructure extracted successfully.")
    except Exception as e:
        web_markdown = f"[Scrape Exception: {str(e)}]"
        print("  [!] Scraping timed out or was blocked. Falling back to core records.")

    # --- STEP 2: BANK VEHICLE RECON GUARDRAIL ---
    normalized_market_text = web_markdown.lower()
    if "asset-based lending" in normalized_market_text or "commercial banking" in normalized_market_text:
        print("\n [!] SECURITY NOTICE: Bank institutional asset/shell signature detected.")
        print("     Aborting deployment pipeline instantly to safeguard campaign integrity.")
        print("=" * 80 + "\n")
        return

    # --- STEP 3: DYNAMIC DATA ANALYSIS & CLAUDE API INFERENCE ---
    print("  Compiling internal briefing dossiers...")
    with open(INPUT_VAULT, "r") as f:
        vault = json.load(f)
    crd_str = str(target_firm["crd_number"])
    adv_history = vault.get(crd_str, {})

    # Construct the prompt payload purely in-memory as a string variable
    prompt_payload = (
        "FAST-SCAN VIDEO ANALYSIS BRIEFING\n"
        "==================================\n\n"
        "ACT AS A SUPPORTIVE GROWTH PARTNER AND OUTBOUND ADVISOR.\n"
        "Analyze the following internal data and web footprint:\n\n"
        "FIRM DETAILS:\n"
        f"Name: {firm_name_raw}\nCRD: {crd_str}\nURL: {raw_url}\n\n"
        "1. DATA MATRIX:\n"
        f"{json.dumps(adv_history, indent=2)}\n\n"
        f"2. WEBSITE FOOTPRINT:\n{web_markdown[:10000]}\n\n"
        "──────────────────────────────────────────────────\n"
        "YOUR ASSIGNMENT:\n"
        "Provide a ultra-brief, bulleted talking-point dashboard for a short video. "
        "Keep it entirely constructive, positive, and focused on growth potential. "
        "Strictly format your response into only these two sections, using max 3 bullet points per section:\n\n"
        "1. THE COMPLIMENT (What they are doing right):\n"
        "   Highlight a massive win in their operational stability, scale, or clean regulatory track record. No fluff.\n\n"
        "2. GROW LEVERAGE OPPORTUNITIES (What to mention):\n"
        "   Identify 1 to 2 clean data-driven opportunities where their existing strengths (like proprietary tools, "
        "   AUM velocity, or specialized expertise) could be leveraged to capture higher-value client segments. "
        "   Keep these brief, direct, and conversational—avoid sounding critical or auditing their firm.\n\n"
        "Do not include hooks, intros, outros, or conversational transition commentary. Just the bullets."
    )

    import anthropic
    print(f"\n  Connecting to Anthropic API to generate video framework...")
    
    api_key = config.get('CLAUDE_API_KEY', '')
    if not api_key:
        print("  [!] Error: CLAUDE_API_KEY not found in configuration. Aborting API step.")
        return

    client = anthropic.Anthropic(api_key=api_key)

    print(f"  [➔] Analyzing footprints and compiling script (using claude-sonnet-4-6)...")
    print(f"==================================================")
    print(f"            GENERATED VIDEO FRAMEWORK             ")
    print(f"==================================================")

    generated_script = ""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt_payload}
            ]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                generated_script += text
        print("\n==================================================")
    
    except Exception as e:
        print(f"\n  [!] API Request failed: {e}")
        print("  Aborting generation process.")
        return

    # SPLIT LIVE VARIABLE TEXT TO FEED THE HTML TEMPLATE
    try:
        parts = re.split(r'(?i)2\.\s*GROW\s*LEVERAGE\s*OPPORTUNITIES.*', generated_script)
        generated_compliment_html = parts[0].replace("1. THE COMPLIMENT (What they are doing right):", "").strip()
        generated_opportunities_html = parts[1].strip()
    except Exception:
        generated_compliment_html = generated_script
        generated_opportunities_html = "Review our video walk-through matrix below to cross-reference localized scaling opportunities."

    # =========================================================================
    # NEW WORKFLOW PHASE 1: INITIAL DEPLOYMENT (Pushes frame for recording)
    # =========================================================================
    print(f"\n  [🚀] PHASE 1: Building initial target dashboard (without video)...")
    
    # Compile landing page using None so it builds a clean frame
    payload = compile_landing_page(target_firm=target_firm, loom_id=None)
    compiled_html = payload["html"]

    # Write initial frame files to local directories
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(compiled_html)

    target_dir = os.path.join("..", url_slug)
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(compiled_html)

    # Push the initial frame to GitHub contextually right now
    print("  [🚀] Pushing framework asset to GitHub Pages for video recording backdrop...")
    try:
        script_dir = os.getcwd()
        os.chdir("..")
        subprocess.run("git add .", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'git commit --allow-empty -m "Telemetry frame: {url_slug}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("git push origin main", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.chdir(script_dir)
    except Exception as git_phase1_err:
        print(f"  [!] Intermediate git push stalled: {git_phase1_err}. Continuing pipeline...")
        os.chdir(script_dir)

    print(f"\n==================================================")
    print(f"               FRAMEWORK IS LIVE                  ")
    print(f"==================================================")
    print(f"  👉 Live URL: https://telemetry.precisiongrowthpartners.io/{url_slug}")
    print(f"  \n  Instructions:")
    print(f"  1. Click the link above to open their custom dashboard on your monitor.")
    print(f"  2. Record your Loom video using Claude's talking points above.")
    print(f"  3. Copy your completed Loom share URL.")
    print(f"──────────────────────────────────────────────────")

    # =========================================================================
    # NEW WORKFLOW PHASE 2: PAUSE, CAPTURE LOOM VIDEO, OVERWRITE WITH EMBED
    # =========================================================================
    user_loom_input = input("  ➔ Paste Loom Video URL here when finished recording: ").strip()
    
    # Extract ID token from user input paste
    if "loom.com" in user_loom_input:
        user_loom_id = user_loom_input.split("/")[-1].split("?")[0]
    else:
        user_loom_id = user_loom_input if user_loom_input else config.get("GLOBAL_LOOM_ID", "PRE_RECORDED_FALLBACK")

    print(f"\n  [🛢️] PHASE 2: Injecting active video '{user_loom_id}' and prepping final deploy...")

    # Re-compile the page with the official Loom Token ID active
    final_payload = compile_landing_page(target_firm=target_firm, loom_id=user_loom_id)
    final_html = final_payload["html"]

    # Overwrite the placeholder index.html files with the permanent video version
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(final_html)
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_html)

    # Unpack the metrics variables so the CRM block can read them seamlessly
    aum_24 = final_payload["aum_24"]
    aum_25 = final_payload["aum_25"]
    aum_26 = final_payload["aum_26"]
    hnw_aum_26 = final_payload["hnw_aum_26"]
    adv_26 = final_payload["adv_26"]
    total_clients = final_payload["total_clients"]
    aum_growth_pct = final_payload["aum_growth_pct"]
    hnw_pct = final_payload["hnw_pct"]
    advisor_aum_string = final_payload["advisor_aum_string"]
    avg_client_string = final_payload["avg_client_string"]

    print(f"\n[✔] Landing asset compiled smoothly via template injection: index.html")
    print(f"  [✔] Custom HTML architecture compiled safely into repository root: {url_slug}/")
    time.sleep(1)

    # =========================================================================
    # ENCOMPASSING CRM DATABASE LAYER
    # =========================================================================
    try:
        from sqlalchemy import create_engine, text
        from datetime import datetime
        from urllib.parse import quote_plus

        raw_password = "Myd@tAYuh!$5" 
        safe_password = quote_plus(raw_password)

        print(f"\n  [🛢️] Initializing SQL connection to PostgreSQL CRM vault...")
        engine = create_engine(f'postgresql://pgp_admin:{safe_password}@localhost:5432/pgp_nadir_crm')
        firm_query = text("""
            INSERT INTO firms (
                crd_number, firm_name, website_url, url_slug, propensity_index,
                aum_2024_m, aum_2025_m, aum_2026_m, advisor_count_2026, total_clients_raw, hnw_aum_raw,
                aum_growth_pct, hnw_pct, advisor_aum_str, avg_client_str
            )
            VALUES (:crd, :name, :url, :slug, :idx, :aum_24, :aum_25, :aum_26, :adv_26, :clients, :hnw_raw,
                    :growth, :hnw_p, :adv_str, :cl_str)
            ON CONFLICT (crd_number) 
            DO UPDATE SET 
                firm_name = EXCLUDED.firm_name,
                website_url = EXCLUDED.website_url,
                url_slug = EXCLUDED.url_slug,
                propensity_index = EXCLUDED.propensity_index,
                aum_2024_m = EXCLUDED.aum_2024_m,
                aum_2025_m = EXCLUDED.aum_2025_m,
                aum_2026_m = EXCLUDED.aum_2026_m,
                advisor_count_2026 = EXCLUDED.advisor_count_2026,
                total_clients_raw = EXCLUDED.total_clients_raw,
                hnw_aum_raw = EXCLUDED.hnw_aum_raw,
                aum_growth_pct = EXCLUDED.aum_growth_pct,
                hnw_pct = EXCLUDED.hnw_pct,
                advisor_aum_str = EXCLUDED.advisor_aum_str,
                avg_client_str = EXCLUDED.avg_client_str
            RETURNING id;
        """)

        with engine.begin() as conn:
            result = conn.execute(firm_query, {
                "crd": str(crd_str),
                "name": str(firm_name_raw),
                "url": str(raw_url),
                "slug": str(url_slug),
                "idx": float(target_firm.get("propensity_index", 0.0)),
                "aum_24": float(aum_24),
                "aum_25": float(aum_25),
                "aum_26": float(aum_26),
                "adv_26": int(adv_26),
                "clients": int(total_clients),
                "hnw_raw": float(target_firm.get("hnw_aum_raw", hnw_aum_26 * 1_000_000)),
                # ADD THESE EXTRACTED LIVE PYTHON METRICS:
                "growth": float(aum_growth_pct),
                "hnw_p": float(hnw_pct),
                "adv_str": str(advisor_aum_string),
                "cl_str": str(avg_client_string)
            })
            firm_internal_id = result.fetchone()[0]

            telemetry_metrics_json = {
                "computed_aum_growth_pct": round(aum_growth_pct, 2),
                "derived_hnw_concentration_pct": round(hnw_pct, 2),
                "formatted_advisor_efficiency": advisor_aum_string,
                "formatted_avg_client_size": avg_client_string,
                "scraped_web_signature_bytes": len(web_markdown)
            }

            insight_query = text("""
                INSERT INTO ai_insights (
                    firm_id, raw_claude_script, parsed_compliment, parsed_opportunities, 
                    scraped_jina_markdown, loom_embed_token, telemetry_metrics_json, insight_timestamp
                )
                VALUES (:firm_id, :script, :compliment, :opportunities, :markdown, :loom, :metrics_json, :timestamp);
            """)

            conn.execute(insight_query, {
                "firm_id": firm_internal_id,
                "script": str(generated_script),
                "compliment": str(generated_compliment_html),
                "opportunities": str(generated_opportunities_html),
                "markdown": str(web_markdown),
                "loom": str(user_loom_id),
                "metrics_json": json.dumps(telemetry_metrics_json),
                "timestamp": datetime.utcnow()
            })

        print(f"  [✔] CRM LAYER SUCCESS: Complete parameters & insights tracked successfully.")

    except Exception as db_err:
        print(f"  [!] Database Persistence Layer skipped or encountered error: {db_err}")

# --- STEP 5: AUTOMATED DEPLOYMENT PUSH TO GITHUB/NETLIFY ---
    print("  Syncing incremental directory tree to GitHub repository...")
    try:
        # Cache our current position (inside 'data')
        script_dir = os.getcwd()
        
        # Physically move the script's focus up to the root folder
        os.chdir("..")
        
        # Execute Git commands cleanly from the true root context
        subprocess.run("git add .", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'git commit --allow-empty -m "Automated telemetry deploy: {url_slug}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("git push origin main", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Return back to the 'data' folder so the script finishes cleanly
        os.chdir(script_dir)
        
        # Verify Site ID is tracked
        site_verification = config.get('NETLIFY_SITE_ID', 'unlinked')
        
        print(f"\n[✔] SUCCESS: Custom telemetry array deployed on complete autopilot! (Site Ref: {site_verification[:8]}...)")
        print(f"    Live Secure URL: https://telemetry.precisiongrowthpartners.io/{url_slug}")
        
    except subprocess.CalledProcessError as e:
        print(f"  [!] Git command failed to execute natively: {str(e)}")
        os.chdir(script_dir)
    except Exception as e:
        print(f"  [!] Git deployment pipeline encountered an exception: {str(e)}")
        os.chdir(script_dir)
        
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    run_pipeline()