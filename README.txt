# Project Nadir: Chronological RIA Intelligence Engine

Project Nadir is an institutional-grade data ingestion and predictive prioritization pipeline designed for B2B growth agencies. It targets independent Registered Investment Advisors (RIAs) by identifying **"Unrealized Capacity"**—firms that are actively expanding their advisor benches but suffering from stagnant asset velocity and a complete lack of digital marketing infrastructure.

By tracking three consecutive years of SEC Form ADV data (2024, 2025, and 2026) and combining it with real-time website text scraping, the engine bypasses surface-level vanity metrics to find stable, well-capitalized firms experiencing hidden operational friction.

---

## 🏗 System Architecture

The pipeline processes thousands of registered investment advisors through a three-phase distillation funnel:

1. [Phase 1: Ingest]       
   Source: SEC Form ADV Part 1A (2024, 2025, 2026 Timeline Data)
   Output: nadir_market_vault.json (Normalized Multi-Year Cache)

2. [Phase 2: Prioritize]   
   Source: nadir_market_vault.json
   Process: 20-Signal Vector Scoring Matrix & Goldilocks Filter (50 <= Score <= 65)
   Output: prospects_top100.csv (Ranked by Agency Propensity Index)

3. [Phase 3: Recon]        
   Source: prospects_top100.csv & nadir_market_vault.json
   Process: Live Web Scraping via Jina AI Reader API (r.jina.ai)
   Output: claude_briefing_[Firm_Name].txt (Unified AI Context Prompt)

---

## 🚦 The Strategic Filter: "Unrealized Capacity"

Project Nadir specifically isolates a high-conversion sales archetype. It filters out both hyper-growth "rocketships" (who don't believe they need help) and litigious or decaying "sinking ships" (who lack the capital or stability to buy). 

The scoring matrix tracks 20 longitudinal data points across 5 domains:
1. Human Capital: Multi-year hiring spikes, advisor attrition acceleration, and team structural velocity.
2. Leverage Shifts: Sudden spikes in AUM-per-advisor highlighting capacity bottlenecks.
3. Account Metrics: Shifts in account density and tracking the "Volume-Over-Value Trap."
4. AUM Trajectory: Identifying chronological stagnation, micro-declines, or boom-bust growth arcs.
5. Marketing & Compliance: Detecting 3-year digital voids and sudden regulatory disclosure infractions.

### The Propensity Index (PI) Formula
Once a firm qualifies for the stable Goldilocks Zone (Scores 20–65), it is ranked using a targeted agency alignment formula:

Propensity Index = OP1 (Operational Friction) + MK1 (Marketing Void) + LV3 (Advisor Share Improving) - Severe Crash Flag

* Tier 1 (PI = 3): Roster growing, zero marketing infrastructure, margin compression, assets stable. (Prime Target)
* Tier 2 (PI = 2): Two core friction signals present; stable asset environment.
* Tier 3 (PI <= 1): Weak signal alignment or asset freefall. (Programmatically Pruned)

---

## 💻 Script Registry & Execution

### Phase 1: Ingestion (nadir_phase1_ingest.py)
Queries the SEC data registry for all baseline-qualified independent RIAs (e.g., $100M to $5B AUM). It constructs a normalized multi-year chronological tree and saves the output locally.
* Input: SEC API / Form ADV Part 1A raw filings.
* Output: nadir_market_vault.json

### Phase 2: Prioritization (nadir_phase2_prioritize.py)
Processes the local JSON registry, runs the 20-signal diagnostic scoring vectors, prints a macro breakdown of the total addressable market tiers, and isolates the top 100 targets matching the Propensity Index criteria.
* Input: nadir_market_vault.json
* Output: prospects_top100.csv
* Execution Command: python nadir_phase2_prioritize.py

### Phase 3: Active AI Recon (nadir_phase3_recon.py)
An interactive terminal utility. Displays the highest-scoring prospects, prompts the user for a selection, and hooks into Jina AI's Reader API (r.jina.ai) to scrape the live home page of the target firm into clean Markdown text. It merges the financial data and web text into an unedited prompt engineered for Claude Pro.
* Input: prospects_top100.csv, nadir_market_vault.json
* Output: claude_briefing_[Firm_Name].txt
* Execution Command: python nadir_phase3_recon.py

---

## 🛠 Prerequisites & Installation

Project Nadir runs on Python 3.8+ and uses lightweight, high-performance libraries for data manipulation and web crawling.

1. Clone or navigate to your local directory.
2. Install the production-grade dependencies via terminal:
pip install pandas requests

---

## 🎯 Outreach Workflow

1. Generate Dossier: Run nadir_phase3_recon.py and select a target from your Top 100 queue.
2. Context Handover: Open the generated claude_briefing_[Firm_Name].txt file, copy its content, and paste it into a fresh Claude Pro conversation thread.
3. Analyze the Mismatch: Review Claude's "Corporate Biography," noting the variance between their internal hiring growth and their missing public video footprint (unmasking shell operations or bank subsidiaries instantly).
4. Record Video: Open Loom, hit record, and open with a high-context, peer-level financial observation directly tied to their 3-year arc.