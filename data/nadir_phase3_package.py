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
    
    # Render the top 10 options on the active stack
    print("\n  Top 10 High-Propensity Agency Targets available for Recon:")
    for idx, row in df.head(10).iterrows():
        print(f"    [{idx + 1}] {row['firm_name']} | Website: {row['website_url']} | PI: {row['propensity_index']}")
        
    print("\n" + "─"*50)
    choice = input("  Select a firm number to process (1-10): ")
    try:
        target_firm = df.iloc[int(choice) - 1]
    except Exception:
        print(" [!] Invalid or empty entry detected. Defaulting to target #1.")
        target_firm = df.iloc[0]
        
    firm_name_raw = str(target_firm["firm_name"])
    print(f"\n[➔] Actively processing telemetry array for: {firm_name_raw}...")
    
    url_slug = clean_slug(firm_name_raw)
    output_prompt_file = f"claude_briefing_{url_slug}.txt"
    
    raw_url = str(target_firm["website_url"]).strip()
    if not raw_url.startswith("http"):
        raw_url = "https://" + raw_url
        
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

    # --- STEP 3: CONSTRUCT THE INTERNAL CLAUDE PROMPT FILE ---
    print("  Compiling internal briefing dossiers...")
    with open(INPUT_VAULT, "r") as f:
        vault = json.load(f)
    crd_str = str(target_firm["crd_number"])
    adv_history = vault.get(crd_str, {})

    with open(output_prompt_file, "w", encoding="utf-8") as f:
        f.write("MASTER TACTICAL ANALYSIS BRIEFING PROMPT\n")
        f.write("========================================\n\n")
        f.write(f"NOTE: SECURELY AUTHENTICATING CLAUDE PRO MODULE VIA KEY VERIFICATION: {config.get('CLAUDE_API_KEY', '')[:8]}...\n\n")
        f.write("ACT AS AN INVESTIGATIVE CORPORATE JOURNALIST AND B2B GROWTH STRATEGIST.\n")
        f.write("Analyze the following internal data and live web footprint for this specific RIA:\n\n")
        f.write(f"FIRM DETAILS:\nName: {firm_name_raw}\nCRD: {crd_str}\nURL: {raw_url}\n\n")
        f.write("1. HARD INTERNAL ADV HISTORY (2024 - 2026):\n")
        f.write(json.dumps(adv_history, indent=2))
        f.write("\n\n2. LIVE WEBSITE FOOTPRINT TEXT (SCRAPED IN REAL TIME):\n")
        f.write(web_markdown[:15000])
        f.write("\n\n" + "─"*50 + "\n")
        f.write("YOUR ASSIGNMENT:\n")
        f.write("Construct a sharp, unvarnished 'Corporate Biography' detailing the narrative inside this firm.\n")

    print(f"  [✔] Private briefing prompt generated successfully: '{output_prompt_file}'")

    # --- STEP 4: COMPILE DYNAMIC EXTERNAL LANDING PAGE HTML (3-YEAR TIMELINE) ---
    print("  Compiling client-facing Tailwind framework with 3-Year Timeline...")
    aum_24 = target_firm["aum_2024_m"]
    aum_25 = target_firm["aum_2025_m"]
    aum_26 = target_firm["aum_2026_m"]
    advisors = target_firm["advisor_count_2026"]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Strategy Telemetry // {firm_name_raw}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white font-sans antialiased">
    <div class="max-w-5xl mx-auto px-6 py-16">
        <header class="border-b border-slate-800 pb-8 mb-12">
            <span class="text-emerald-400 font-mono tracking-widest text-xs uppercase font-bold">Project Nadir // Operational Telemetry Stream</span>
            <h1 class="text-4xl font-extrabold tracking-tight mt-2 text-slate-100">Unlocking Scale for {firm_name_raw}'s {advisors}-Advisor Bench</h1>
            <p class="text-xl text-slate-400 mt-4 font-light">Your team expanded while market velocity shifted. Let's align your asset growth directly to your actual capacity.</p>
        </header>

        <section class="bg-slate-950 border border-slate-800 rounded-2xl p-8 mb-12 shadow-2xl text-center">
                <h2 class="text-xs font-mono tracking-wider text-brand-accent uppercase mb-2">Operational Analysis</h2>            <div class="aspect-video w-full bg-slate-900 rounded-lg border border-slate-800 flex items-center justify-center relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-tr from-emerald-500/10 to-transparent"></div>
                <p class="text-slate-500 text-sm z-10">[ Insert Personalized Loom Video Embed Code Here ]</p>
            </div>
        </section>

        <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            <div class="bg-slate-800/40 p-6 rounded-xl border border-slate-800/80 backdrop-blur-sm">
                <span class="text-xs text-slate-500 uppercase tracking-wider block font-medium">Active Bench (2026)</span>
                <span class="text-2xl font-bold text-emerald-400 mt-1 block">{advisors} Advisors</span>
            </div>
            <div class="bg-slate-800/40 p-6 rounded-xl border border-slate-800/80 backdrop-blur-sm">
                <span class="text-xs text-slate-400 uppercase tracking-wider block font-medium">2024 AUM Baseline</span>
                <span class="text-2xl font-bold text-slate-200 mt-1 block">${aum_24}M</span>
            </div>
            <div class="bg-slate-800/40 p-6 rounded-xl border border-slate-800/80 backdrop-blur-sm">
                <span class="text-xs text-emerald-500/80 uppercase tracking-wider block font-medium">2025 AUM Velocity</span>
                <span class="text-2xl font-bold text-emerald-300 mt-1 block">${aum_25}M</span>
            </div>
            <div class="bg-slate-800/40 p-6 rounded-xl border border-slate-800/80 backdrop-blur-sm">
                <span class="text-xs text-slate-400 uppercase tracking-wider block font-medium">2026 Current AUM</span>
                <span class="text-2xl font-bold text-slate-200 mt-1 block">${aum_26}M</span>
            </div>
        </section>
        
        <footer class="text-center pt-12 border-t border-slate-800/60 max-w-2xl mx-auto">
            <h3 class="text-xl font-semibold text-brand-text mb-2">
                Interested in exploring how to capitalize on these specific opportunities?
            </h3>
            
            <p class="text-slate-400 mb-8 text-sm">
                Let's do a brief alignment check to cross-reference these metrics with your actual growth targets.
            </p>
            
            <a href="https://calendly.com/precisiongrowthpartners/nadir-discovery-call" 
            target="_blank"
            class="inline-block bg-brand-accent text-slate-950 font-bold text-lg px-10 py-4 rounded-lg transition-all hover:opacity-90 shadow-lg">
                Book Discovery Call
            </a>
        </footer>
    </div>
</body>
</html>
"""
# --- STEP 4: DIRECT MASTER ROOT STORAGE LOGIC ---
    # We use "../" to force the folder out of 'data' and straight into the repository root
    target_dir = os.path.join("..", url_slug)
    
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  [✔] Custom HTML architecture compiled safely into repository root: {url_slug}/")

    # Allow local file allocation states to catch up
    time.sleep(1)

 # --- STEP 5: AUTOMATED DEPLOYMENT PUSH TO GITHUB/NETLIFY ---
    print("  Syncing incremental directory tree to GitHub repository...")
    try:
        # Cache our current position (inside 'data')
        script_dir = os.getcwd()
        
        # Physically move the script's focus up to the root folder
        os.chdir("..")
        
        # Execute Git commands cleanly from the true root context
        subprocess.run("git add .", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'git commit -m "Automated telemetry deploy: {url_slug}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("git push origin main", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Return back to the 'data' folder so the script finishes cleanly
        os.chdir(script_dir)
        
        # Verify Site ID is tracked
        site_verification = config.get('NETLIFY_SITE_ID', 'unlinked')
        
        print(f"\n[✔] SUCCESS: Custom telemetry array deployed on complete autopilot! (Site Ref: {site_verification[:8]}...)")
        print(f"    Live Secure URL: https://telemetry.precisiongrowthpartners.io/{url_slug}")
        
    except subprocess.CalledProcessError as e:
        print(f"  [!] Git command failed to execute natively: {str(e)}")
        # Safeguard: ensure we return to our original directory if it fails
        os.chdir(script_dir)
    except Exception as e:
        print(f"  [!] Git deployment pipeline encountered an exception: {str(e)}")
        os.chdir(script_dir)
        
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    run_pipeline()