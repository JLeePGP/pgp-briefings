# 🛰️ Project Nadir — Phase 3 Telemetry Engine

Project Nadir is an automated, high-propensity data recon and production pipeline built exclusively for **Precision Growth Partners**. It bridges raw linear regulatory filing updates with real-time web scrapers to construct bespoke strategic landing pages for target RIAs.

---

## 📐 Architectural Pipeline

1. **Target Selection:** ingests the prioritized `prospects_top100.csv` target list.
2. **Real-Time Recon:** Leverages a Jina AI layer to parse target web copy and brand signatures.
3. **Institutional Guardrails:** Scans text arrays for bank shell/asset-based lending flags and automatically halts the container deployment if detected.
4. **Dossier Generation:** Compiles a hard 3-year performance history matrix (`2024` → `2025` → `2026`) formatted as an unvarnished briefing file for LLM synthesis.
5. **Dynamic Compilation:** Renders custom Tailwind CSS dark-mode briefings embedded with diagnostic telemetry components.
6. **Git-Ops Sync:** Composes side-by-side local folder assets and pushes to this repository, triggering an instant serverless build edge-merge via Netlify.

---

## ⚡ Execution Matrix

To scale the outbound engine across your target queue, fire up your local terminal and run:

```bash
python nadir_phase3_package.py# pgp-briefings
Hyper-targeted outbound recon pipeline for Precision Growth Partners. Extracts live web infrastructure and 3-year SEC ADV linear historical data streams to programmatically compile, merge, and deploy secure custom-branded advisor benchmarking environments directly to the telemetry subdomain.
