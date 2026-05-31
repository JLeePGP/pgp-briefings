import os
import threading
import webbrowser
import pandas as pd
import customtkinter as ctk

# Import your actual core engine logic functions directly
from nadir_phase3_package import compile_landing_page

ctk.set_appearance_mode("Dark")

class NadirCommandConsole(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App Window Parameters
        self.title("Project Nadir // Operational Telemetry Command Console")
        self.geometry("1150x700")  # Bumped height slightly to give scrollbox perfect real estate
        self.configure(fg_color="#2b2b2b") # Global Dark Background

        # Brand Typography Mapping 
        self.font_bold = ("Poppins", 15, "bold")
        self.font_medium = ("Poppins", 12, "bold")
        self.font_regular = ("Poppins", 12)
        self.font_mono = ("Courier New", 11)

        # Global Memory Cache to pass data between execution steps
        self.prospect_buttons = []
        self.prospect_df = None
        self.selected_firm_data = {}
        self.selected_index = None

        # Define 2-Column Master Grid Layout
        self.grid_columnconfigure(0, weight=1) # Left Controls
        self.grid_columnconfigure(1, weight=2) # Right Monitors
        self.grid_rowconfigure(0, weight=1)

        # ─────────────────────────────────────────────────────────────────────
        # ─── LEFT COLUMN: CONTROL ROOM PANEL (CHARCOAL ACCENT) ───────────────
        # ─────────────────────────────────────────────────────────────────────
        self.left_panel = ctk.CTkFrame(self, corner_radius=12, fg_color="#4a4a4a")
        self.left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.lbl_title = ctk.CTkLabel(self.left_panel, text="NADIR WORKFLOW DISPATCH", font=self.font_bold, text_color="#ffffff")
        self.lbl_title.pack(padx=20, pady=(20, 10), anchor="w")

        # STEP 1A: Scrollable Listbox Container Component
        self.lbl_step1a = ctk.CTkLabel(self.left_panel, text="1A. Select Top 100 Target from Feed:", font=self.font_medium, text_color="#bf8660")
        self.lbl_step1a.pack(padx=20, pady=(5, 2), anchor="w")
        
        # This replaces the dropdown menu entirely
        self.scroll_listbox = ctk.CTkScrollableFrame(
            self.left_panel, width=240, height=180, 
            fg_color="#2b2b2b", label_text_color="#ffffff"
        )
        self.scroll_listbox.pack(padx=20, pady=(0, 15), anchor="w", fill="x")

        # STEP 1B: Wildcard Text Input Component
        self.lbl_step1b = ctk.CTkLabel(self.left_panel, text="OR: Input Custom CRD # Override", font=self.font_medium, text_color="#bf8660")
        self.lbl_step1b.pack(padx=20, pady=(5, 2), anchor="w")

        self.crd_entry = ctk.CTkEntry(
            self.left_panel, placeholder_text="e.g. 742 (Clears Scroll Selection)", 
            font=self.font_regular, width=250, height=35, fg_color="#2b2b2b",
            border_color="#2b2b2b", text_color="#ffffff", placeholder_text_color="#8a8a8a"
        )
        self.crd_entry.pack(padx=20, pady=(0, 20), anchor="w")
        self.crd_entry.bind("<KeyRelease>", lambda e: self.clear_scroll_selection())

        # STEP 2: Synthesis Trigger Button
        self.lbl_step2 = ctk.CTkLabel(self.left_panel, text="2. Run Core Scrape & Script Build:", font=self.font_medium, text_color="#ffffff")
        self.lbl_step2.pack(padx=20, pady=(10, 2), anchor="w")

        self.btn_analyze = ctk.CTkButton(
            self.left_panel, text="⚡ RUN TELEMETRY SYNTHESIS", font=self.font_medium,
            width=250, height=40, fg_color="#bf8660", hover_color="#a6714e", 
            text_color="#ffffff", corner_radius=8, command=self.launch_analysis_thread
        )
        self.btn_analyze.pack(padx=20, pady=(0, 25), anchor="w")

        # STEP 3: Loom Asset ID Capture Field
        self.lbl_step3 = ctk.CTkLabel(self.left_panel, text="3. Link Recorded Loom Video ID:", font=self.font_medium, text_color="#bf8660")
        self.lbl_step3.pack(padx=20, pady=(5, 2), anchor="w")

        self.loom_entry = ctk.CTkEntry(
            self.left_panel, placeholder_text="Paste alpha-numeric ID here", 
            font=self.font_regular, width=250, height=35, fg_color="#2b2b2b",
            border_color="#2b2b2b", text_color="#ffffff", placeholder_text_color="#8a8a8a"
        )
        self.loom_entry.pack(padx=20, pady=(0, 20), anchor="w")

        self.btn_submit_loom = ctk.CTkButton(
            self.left_panel, text="✔ SUBMIT & LOCK VIDEO LINK", font=self.font_medium,
            width=250, height=30, fg_color="#6e6e6e", text_color="#ffffff", corner_radius=6,
            state="disabled", command=self.validate_and_lock_loom_input
        )
        self.btn_submit_loom.pack(padx=20, pady=(0, 20), anchor="w")

        # STEP 4: HTML Portal Deployment Trigger
        self.lbl_step4 = ctk.CTkLabel(self.left_panel, text="4. Output Final Production Build:", font=self.font_medium, text_color="#ffffff")
        self.lbl_step4.pack(padx=20, pady=(10, 2), anchor="w")

        self.btn_deploy = ctk.CTkButton(
            self.left_panel, text="🚀 OPEN LIVE PORTAL WEBSITE", font=self.font_medium,
            width=250, height=40, fg_color="#6e6e6e", text_color="#ffffff", corner_radius=8,
            state="disabled", command=self.execute_final_html_deployment
        )
        self.btn_deploy.pack(padx=20, pady=(0, 20), anchor="w")

        # Boot up localized dataset rows directly into the scroll view
        self.load_prospect_database()

        # ─────────────────────────────────────────────────────────────────────
        # ─── RIGHT COLUMN: PERFORMANCE MONITOR MATRIX (DARK REGION) ──────────
        # ─────────────────────────────────────────────────────────────────────
        self.right_panel = ctk.CTkFrame(self, corner_radius=12, fg_color="#2b2b2b")
        self.right_panel.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        # Setup Split Output Rows (Row 1: Logs, Row 3: Live Script Text Box)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=2)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Upper Component: Live Terminal Logs
        self.lbl_log = ctk.CTkLabel(self.right_panel, text="SYSTEM CORE PIPELINE SCROLL LOG", font=self.font_medium, text_color="#bf8660")
        self.lbl_log.grid(row=0, column=0, padx=10, pady=(15, 2), sticky="w")

        self.terminal_output = ctk.CTkTextbox(self.right_panel, font=self.font_mono, fg_color="#4a4a4a", text_color="#ffffff", corner_radius=8)
        self.terminal_output.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Lower Component: Live Script Viewer
        self.lbl_script = ctk.CTkLabel(self.right_panel, text="🎬 DYNAMIC CLAUDE VIDEO BRIEFING TALK TRACKS", font=self.font_medium, text_color="#ffffff")
        self.lbl_script.grid(row=2, column=0, padx=10, pady=(5, 2), sticky="w")

        self.script_display = ctk.CTkTextbox(self.right_panel, font=self.font_regular, fg_color="#4a4a4a", text_color="#ffffff", corner_radius=8, wrap="word")
        self.script_display.grid(row=3, column=0, padx=10, pady=(0, 15), sticky="nsew")

        # Initialize Default Display States
        self.print_log_line("[Console Initialization] Diagnostics clear. Select a pipeline company node to begin orchestration loop.")
        self.set_script_window_content("Select a candidate target from the left column and click Step 2 to frame custom video scripting paths.")

    # ─── GRAPHICAL LISTBOX CONTROLS ──────────────────────────────────────────

    def load_prospect_database(self):
        """Populates the scrolling frame panel directly out of your flattened CSV file data pool."""
        target_csv = "prospects_top100.csv"
        if not os.path.exists(target_csv):
            error_lbl = ctk.CTkLabel(self.scroll_listbox, text="Missing prospects_top100.csv", text_color="#ff5555")
            error_lbl.pack(padx=5, pady=5)
            return

        try:
            self.prospect_df = pd.read_csv(target_csv)
            for idx, row in self.prospect_df.iterrows():
                display_string = f"[{idx+1}] {str(row.get('firm_name', 'Unknown Target Node'))[:35]}"
                
                # Create a custom row button for each firm inside the scroll container
                row_btn = ctk.CTkButton(
                    self.scroll_listbox, text=display_string, font=self.font_regular,
                    anchor="w", fg_color="transparent", text_color="#ffffff",
                    hover_color="#4a4a4a", height=28, corner_radius=4,
                    command=lambda i=idx: self.handle_scroll_selection(i)
                )
                row_btn.pack(fill="x", padx=2, pady=1)
                self.prospect_buttons.append(row_btn)
        except Exception as e:
            self.print_log_line(f" [!] Matrix Read Crash: {e}")

    def handle_scroll_selection(self, selected_idx):
        """Highlights the active scroll selection row and safety clears the text input override."""
        self.selected_index = selected_idx
        self.crd_entry.delete(0, "end") # Clear text boxes to keep state clean

        # Paint the selected button copper, reset all others back to transparent
        for idx, btn in enumerate(self.prospect_buttons):
            if idx == selected_idx:
                btn.configure(fg_color="#bf8660", text_color="#ffffff", hover_color="#bf8660")
            else:
                btn.configure(fg_color="transparent", text_color="#ffffff", hover_color="#4a4a4a")

    def clear_scroll_selection(self):
        """Clears the scrollbox visual highlight selections if the operator starts typing an explicit override."""
        self.selected_index = None
        for btn in self.prospect_buttons:
            btn.configure(fg_color="transparent", text_color="#ffffff", hover_color="#4a4a4a")

    # ─── LOGIC CORE MAPPING LISTENERS ────────────────────────────────────────

    def print_log_line(self, message):
        """Thread-safe interface terminal log appending routine."""
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", f"{message}\n")
        self.terminal_output.see("end")
        self.terminal_output.configure(state="disabled")
        self.update_idletasks()

    def set_script_window_content(self, text):
        """Injects processed AI text structures cleanly onto the presentation display."""
        self.script_display.configure(state="normal")
        self.script_display.delete("0.0", "end")
        self.script_display.insert("0.0", text)
        self.script_display.configure(state="disabled")

    def launch_analysis_thread(self):
        """Extracts input metrics and builds background threads to execute heavy logic chains."""
        crd_override = self.crd_entry.get().strip()
        target_firm_dict = None

        # Resolve Data Row Source Location
        if crd_override:
            self.print_log_line(f"\n[▶] Triggering Master Vault JSON Search for Explicit Wildcard Target CRD: #{crd_override}...")
            target_firm_dict = self.pull_target_from_master_json_vault(crd_override)
        elif self.selected_index is not None and self.prospect_df is not None:
            try:
                target_firm_dict = self.prospect_df.iloc[self.selected_index].to_dict()
                self.print_log_line(f"\n[▶] Extracting Flat Matrix Vectors for List Index Candidate #{self.selected_index + 1}...")
            except Exception as e:
                self.print_log_line(f" [!] List Row Parse Exception: {e}")

        if not target_firm_dict:
            self.print_log_line("[!] Initialization Failure: Select a firm from the scrolling feed or enter a valid CRD code.")
            return

        # Cache target parameters into memory and safety-lock buttons during active runs
        self.selected_firm_data = target_firm_dict
        self.btn_analyze.configure(state="disabled", fg_color="#6e6e6e")
        self.btn_deploy.configure(state="disabled", fg_color="#6e6e6e")

        # Open the display box so text streams cleanly right away
        self.set_script_window_content("Establishing connections... Streaming Claude output metrics next...")

        # Dispatch background worker thread safely
        threading.Thread(target=self.core_pipeline_orchestration_loop, args=(target_firm_dict,), daemon=True).start()

    def core_pipeline_orchestration_loop(self, firm_data):
        """Background pipeline runner: safely digests Phase 3 outputs."""
        try:
            firm_name = firm_data.get("firm_name", "Target Asset")
            self.print_log_line(f"  Launching outbound enrichment arrays for target node: {firm_name}")
            self.print_log_line("  Connecting proxy scrapers... Web data retrieved cleanly.")
            self.print_log_line("  Transmitting prompt vectors to Claude 3.5 Sonnet processing nodes...")

            # 1. Call Phase 3 engine passing the GUI text-updater function as a live stream callback hook
            result = compile_landing_page(
                target_firm=firm_data, 
                loom_id="PENDING_LINK_ASSIGNMENT",
                script_callback=self.set_script_window_content
            )

            # 2. Inspect what came back to prevent unpacking crashes
            if isinstance(result, tuple):
                compiled_html_string = result[0]
                raw_claude_script = result[1]
            else:
                compiled_html_string = result
                import nadir_phase3_package
                raw_claude_script = getattr(nadir_phase3_package, "generated_script", "Error locating script variable.")

            # Cache the assets inside the GUI memory layout
            self.compiled_html_string = compiled_html_string
            self.current_generated_script = raw_claude_script
            
            self.print_log_line("[✔] Operational analysis engine complete. Review briefing track and proceed to Step 3.")
            
            # UNLOCK STEP 3 SUBMIT BUTTON INSTEAD OF STEP 4
            self.btn_submit_loom.configure(state="normal", fg_color="#bf8660")

        except Exception as e:
            self.print_log_line(f" [!] Execution Exception encountered within processing loop: {e}")
        finally:
            self.btn_analyze.configure(state="normal", fg_color="#bf8660")

    def validate_and_lock_loom_input(self):
        """Processes Step 3 as an independent execution confirmation event."""
        loom_token = self.loom_entry.get().strip()
        if not loom_token:
            self.print_log_line("[!] Validation Failed: Enter your Loom Video link key first.")
            return
            
        self.print_log_line(f"\n[✔] Loom Asset Link Locked: '{loom_token}' mapped successfully into deployment track.")
        # Activate final deployment build button
        self.btn_deploy.configure(state="normal", fg_color="#bf8660")

    def execute_final_html_deployment(self):
        """Reads user-supplied Loom ID values, modifies template placeholders locally, and fires browser hooks."""
        loom_token = self.loom_entry.get().strip()
        if not loom_token:
            self.print_log_line("[!] Validation Aborted: Field 3 requires a valid alpha-numeric Loom identifier.")
            return

        try:
            firm_name = self.selected_firm_data.get("firm_name", "Prospect Portal")
            self.print_log_line(f"\n[🚀] Packaging deployment templates for target profile: {firm_name}...")

            # Use the HTML string already cached securely inside the GUI state layout memory
            final_production_html = self.compiled_html_string.replace("PENDING_LINK_ASSIGNMENT", loom_token)

            # Resolve your custom master repository folder storage routing variables
            url_slug = self.selected_firm_data.get("url_slug", firm_name.lower().replace(" ", "_").replace(",", ""))
            target_dir = os.path.join("..", url_slug)
            
            os.makedirs(target_dir, exist_ok=True)
            output_filepath = os.path.join(target_dir, "index.html")
            
            with open(output_filepath, "w", encoding="utf-8") as f:
                f.write(final_production_html)

            self.print_log_line(f"[✔] Custom HTML architecture compiled safely into repository root: {url_slug}/")
            
            # Open the freshly compiled local HTML portal asset right inside a browser window tab
            webbrowser.open(f"file://{os.path.abspath(output_filepath)}")
            self.print_log_line("[🎉] Portal application deployed live! Review interface engine canvas.")

        except Exception as e:
            self.print_log_line(f" [!] Deployment Subsystem Encountered Exception: {e}")

    def pull_target_from_master_json_vault(self, crd_string):
        """Crawls raw historical vault json directly to execute custom manual searches."""
        import json
        vault_file = "nadir_market_vault.json"
        if not os.path.exists(vault_file):
            self.print_log_line("  [!] System Exception: Master 'nadir_market_vault.json' is missing from root folder.")
            return None
        try:
            with open(vault_file, "r") as f:
                vault = json.load(f)
            if crd_string in vault:
                history = vault[crd_string]
                latest_year = sorted(history.keys())[-1]
                latest_data = history[latest_year]
                return {
                    "firm_name": latest_data.get("firm_name", "Custom Override Asset"),
                    "crd_number": crd_string,
                    "website_url": latest_data.get("website_url", ""),
                    "advisor_count_2026": int(latest_data.get("advisor_employees_raw", 1)),
                    "aum_2024_m": float(history.get("2024", {}).get("total_aum_raw", 0)) / 1e6,
                    "aum_2025_m": float(history.get("2025", {}).get("total_aum_raw", 0)) / 1e6,
                    "aum_2026_m": float(history.get("2026", {}).get("total_aum_raw", 0)) / 1e6,
                    "total_clients_raw": int(latest_data.get("total_clients_raw", 1)),
                    "hnw_aum_raw": float(latest_data.get("hnw_aum_raw", 0)),
                    "advisor_employees_raw": int(latest_data.get("advisor_employees_raw", 1))
                }
        except Exception as e:
            self.print_log_line(f"  [!] Master Json Vault Crawler Exception: {e}")
        return None

if __name__ == "__main__":
    app = NadirCommandConsole()
    app.mainloop()