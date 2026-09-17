"""
Generate an ultra-modern, high-tech, electricity-themed AMOLED dashboard
with high-voltage danger glows, grid stress HUD, and negative impact alerts.
"""

import json
from pathlib import Path

json_path = Path("/Users/vishaal/.gemini/antigravity/scratch/electricity_agent/artifacts/dashboard_data.json")
with open(json_path) as f:
    raw_data = json.load(f)

json_str = json.dumps(raw_data)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ HIGH-VOLTAGE ELECTRICITY AGENT — ML POWER GRID FORECASTER</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --accent-cyan: #0284c7;
      --accent-emerald: #059669;
      --accent-purple: #7c3aed;
      --accent-amber: #d97706;
      --accent-danger: #dc2626;
      --slider-bg: #e2e8f0;
      --glow-electric: rgba(2, 132, 199, 0.15);
      --glow-danger: rgba(220, 38, 38, 0.25);
    }}

    html.dark {{
      --bg: #000000;
      --card-bg: #070709;
      --card-border: #141418;
      --text: #f3f4f6;
      --text-muted: #94a3b8;
      --accent-cyan: #00f0ff;
      --accent-emerald: #00ff9f;
      --accent-purple: #b026ff;
      --accent-amber: #ffb703;
      --accent-danger: #ff003c;
      --slider-bg: #16161c;
      --glow-electric: rgba(0, 240, 255, 0.18);
      --glow-danger: rgba(255, 0, 60, 0.45);
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    /* Subtle Cyber Electricity Grid in Dark Mode */
    html.dark body {{
      background-image: 
        linear-gradient(to right, rgba(0, 240, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
      background-size: 32px 32px;
    }}

    .amoled-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      position: relative;
      transition: all 0.25s ease;
    }}

    html.dark .amoled-card {{
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
    }}

    html.dark .amoled-card:hover {{
      border-color: #24242e;
    }}

    /* High-Voltage Danger Glow Animation */
    @keyframes danger-pulse {{
      0%, 100% {{
        box-shadow: 0 0 15px rgba(255, 0, 60, 0.4), inset 0 0 15px rgba(255, 0, 60, 0.1);
        border-color: #ff003c;
      }}
      50% {{
        box-shadow: 0 0 35px rgba(255, 0, 60, 0.85), inset 0 0 25px rgba(255, 0, 60, 0.25);
        border-color: #ff3366;
      }}
    }}

    .danger-glow {{
      animation: danger-pulse 1.6s infinite ease-in-out !important;
    }}

    @keyframes electric-sweep {{
      0% {{ transform: translateX(-100%); }}
      100% {{ transform: translateX(200%); }}
    }}

    .electric-ray {{
      position: absolute;
      top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
      animation: electric-sweep 4s infinite linear;
    }}

    /* Custom range slider */
    input[type=range] {{
      -webkit-appearance: none;
      background: var(--slider-bg);
      border-radius: 9999px;
    }}

    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      height: 18px;
      width: 18px;
      border-radius: 50%;
      background: var(--accent-cyan);
      cursor: pointer;
      box-shadow: 0 0 10px var(--accent-cyan);
      transition: all 0.15s ease;
    }}

    input[type=range]::-webkit-slider-thumb:hover {{
      transform: scale(1.25);
    }}

    /* Danger Thumb when slider is in hazard territory */
    .slider-hazard::-webkit-slider-thumb {{
      background: var(--accent-danger) !important;
      box-shadow: 0 0 16px var(--accent-danger) !important;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(150, 150, 150, 0.2); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(0, 240, 255, 0.5); }}
  </style>
</head>
<body class="antialiased p-3 sm:p-5 lg:p-7 min-h-screen font-sans">
  <div class="max-w-[1440px] mx-auto space-y-6">

    <!-- TOP NAVIGATION / CYBER ELECTRICITY HEADER -->
    <header class="amoled-card rounded-2xl p-5 sm:p-6 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 overflow-hidden">
      <div class="electric-ray"></div>

      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-black border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-black text-2xl shadow-[0_0_20px_rgba(0,240,255,0.35)] relative overflow-hidden">
          <span class="relative z-10 animate-pulse">⚡</span>
          <div class="absolute inset-0 bg-cyan-500/10 blur-md"></div>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h1 class="text-xl sm:text-2xl font-black tracking-tight uppercase">PowerGrid Intelligent Agent</h1>
            <span class="text-[10px] uppercase font-mono font-bold tracking-widest px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 flex items-center gap-1.5 shadow-[0_0_10px_rgba(0,240,255,0.2)]">
              <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
              ML Core v2.4 • Active
            </span>
          </div>
          <p class="text-xs text-[var(--text-muted)] mt-0.5 font-mono">
            80/20 Train/Test Split (R²: 0.9979, MAE: 4.31 TWh) • High-Voltage Grid Risk Engine
          </p>
        </div>
      </div>

      <!-- Header Controls: Theme & Export -->
      <div class="flex items-center gap-3 self-stretch md:self-auto justify-end">
        <button onclick="toggleTheme()" id="theme-btn"
          class="px-4 py-2.5 rounded-xl border border-[var(--card-border)] bg-[var(--card-bg)] text-xs font-mono font-semibold hover:border-cyan-500/50 transition-all flex items-center gap-2 shadow-sm">
          <span id="theme-icon">🌙</span>
          <span id="theme-text">AMOLED</span>
        </button>

        <button onclick="exportCSV()"
          class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-400 text-black font-black text-xs uppercase tracking-wider hover:opacity-90 active:scale-95 transition-all flex items-center gap-1.5 shadow-[0_0_20px_rgba(0,240,255,0.3)]">
          <span>📥</span> Export Telemetry
        </button>
      </div>
    </header>

    <!-- NATURAL LANGUAGE AI PROMPT BAR -->
    <section class="amoled-card rounded-2xl p-5 shadow-2xl border border-cyan-500/40 relative overflow-hidden space-y-3">
      <div class="electric-ray"></div>

      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-xl">🤖</span>
          <h2 class="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2 font-mono">
            <span>AI Dispatcher & Natural Language Prompt</span>
            <span class="text-[10px] font-normal text-[var(--text-muted)] font-sans">(Type any scenario or stress query)</span>
          </h2>
        </div>
        <span class="text-[10px] font-mono text-[var(--text-muted)] hidden sm:inline">Press Enter to Dispatch</span>
      </div>

      <div class="flex flex-col sm:flex-row items-center gap-3">
        <div class="relative w-full">
          <input type="text" id="ai-prompt-input"
            placeholder="e.g. 'What will electricity demand be for India and China in 2035 with 20% energy surge and no renewable growth?'"
            class="w-full px-4 py-3.5 text-sm rounded-xl border border-[var(--card-border)] bg-[var(--card-bg)] text-[var(--text)] focus:outline-none focus:border-cyan-400 font-medium pl-10 transition-all shadow-inner font-mono"
            onkeydown="if(event.key==='Enter') executeAIPrompt()">
          <span class="absolute left-3.5 top-4 text-cyan-400 text-sm animate-pulse">⚡</span>
        </div>
        <button onclick="executeAIPrompt()"
          class="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 via-teal-400 to-emerald-400 text-black font-black text-xs uppercase tracking-wider hover:opacity-95 active:scale-95 transition-all shadow-[0_0_25px_rgba(0,240,255,0.4)] shrink-0 flex items-center justify-center gap-2">
          <span>Dispatch Query</span>
          <span>➔</span>
        </button>
      </div>

      <!-- Quick Suggestion Chips -->
      <div class="flex flex-wrap items-center gap-2 pt-1 text-xs">
        <span class="text-[var(--text-muted)] font-mono text-[11px]">Simulate:</span>
        <button onclick="fillPrompt('Forecast electricity for India and China in 2035 with 25% energy surge')"
          class="px-2.5 py-1 rounded-lg border border-[var(--card-border)] hover:border-cyan-500 text-[var(--text-muted)] hover:text-cyan-400 transition-all font-mono">
          "India & China in 2035 (+25% Energy)"
        </button>
        <button onclick="fillPrompt('Show electricity for G7 in 2030 with 30% renewable expansion')"
          class="px-2.5 py-1 rounded-lg border border-[var(--card-border)] hover:border-cyan-500 text-[var(--text-muted)] hover:text-cyan-400 transition-all font-mono">
          "G7 in 2030 (+30% Renewables)"
        </button>
        <button onclick="fillPrompt('What is the consumption for BRICS in 2040 with 15% GDP growth and 0% clean expansion?')"
          class="px-2.5 py-1 rounded-lg border border-red-500/30 hover:border-red-500 text-red-400/80 hover:text-red-400 transition-all font-mono">
          ⚠️ "BRICS 2040 (Grid Deficit Hazard)"
        </button>
        <button onclick="fillPrompt('Predict electricity for France and Germany in 2050')"
          class="px-2.5 py-1 rounded-lg border border-[var(--card-border)] hover:border-cyan-500 text-[var(--text-muted)] hover:text-cyan-400 transition-all font-mono">
          "France & Germany in 2050"
        </button>
      </div>

      <!-- AI Response Box -->
      <div id="ai-response-box" class="mt-2 p-4 rounded-xl border border-cyan-500/30 bg-cyan-500/5 text-xs space-y-2 hidden">
        <div class="flex items-center justify-between text-cyan-400 font-bold">
          <span class="flex items-center gap-1.5 text-sm font-mono"><span>⚡</span> Dispatcher Inference Result</span>
          <span id="ai-response-badge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">Target Year 2035</span>
        </div>
        <p id="ai-response-text" class="text-sm font-medium text-[var(--text)] leading-relaxed"></p>
      </div>
    </section>

    <!-- HIGH-VOLTAGE GRID RISK & DANGER HUD (NEW DANGER ALERT FEATURE) -->
    <section id="grid-risk-hud" class="amoled-card rounded-2xl p-5 shadow-2xl border transition-all relative overflow-hidden">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div id="risk-status-icon" class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-xl font-black">
            🛡️
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-xs uppercase font-mono font-bold tracking-widest text-[var(--text-muted)]">High-Voltage Grid Status</h3>
              <span id="risk-level-badge" class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                NOMINAL • STABLE
              </span>
            </div>
            <p id="risk-headline" class="text-sm font-bold text-[var(--text)] mt-0.5">
              Power grid operating within safe reserve thresholds.
            </p>
          </div>
        </div>

        <!-- Grid Stress Index Gauge -->
        <div class="flex items-center gap-4 self-stretch md:self-auto justify-between md:justify-end border-t md:border-t-0 pt-3 md:pt-0 border-[var(--card-border)]">
          <div class="text-right">
            <span class="text-[10px] font-mono uppercase text-[var(--text-muted)] block">Grid Stability Index</span>
            <span id="risk-stability-score" class="text-2xl font-mono font-black text-emerald-400">96%</span>
          </div>
          <div class="w-24 h-3 bg-[var(--slider-bg)] rounded-full overflow-hidden border border-[var(--card-border)] p-0.5">
            <div id="risk-stability-bar" class="h-full rounded-full bg-emerald-400 transition-all duration-300" style="width: 96%;"></div>
          </div>
        </div>
      </div>

      <!-- Dynamic Detailed Danger Breakdown (Visible when in Warning/Hazard) -->
      <div id="risk-details-box" class="mt-3 pt-3 border-t border-[var(--card-border)] grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs hidden">
        <div class="p-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
          <span class="font-bold flex items-center gap-1"><span>⚠️</span> Blackout & Shortfall Risk</span>
          <p id="risk-blackout-desc" class="text-[11px] text-[var(--text-muted)] mt-1 leading-tight">Demand surge outstripping generation capacity.</p>
        </div>
        <div class="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
          <span class="font-bold flex items-center gap-1"><span>🏭</span> Thermal Carbon Strain</span>
          <p id="risk-carbon-desc" class="text-[11px] text-[var(--text-muted)] mt-1 leading-tight">Fossil peaking units forced online to bridge gap.</p>
        </div>
        <div class="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
          <span class="font-bold flex items-center gap-1"><span>💰</span> Infrastructure Surcharge</span>
          <p id="risk-infra-desc" class="text-[11px] text-[var(--text-muted)] mt-1 leading-tight">Reserve margin depletion causes spike in tariff rates.</p>
        </div>
      </div>
    </section>

    <!-- FUTURE YEAR SELECTOR BAR -->
    <section class="amoled-card rounded-2xl p-5 shadow-2xl border border-cyan-500/25 relative overflow-hidden">
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-lg">🔮</span>
            <h2 class="text-base font-bold tracking-tight">Target Forecast Year: <span id="display-target-year" class="text-cyan-400 text-xl font-extrabold font-mono">2030</span></h2>
          </div>
          <p class="text-xs text-[var(--text-muted)] mt-0.5">
            Select or type any year from 2024 to 2050 to forecast electricity consumption for selected countries.
          </p>
        </div>

        <!-- Quick Year Jump Pills -->
        <div class="flex flex-wrap items-center gap-1.5" id="year-pills">
          <button onclick="setYear(2024)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2024">2024</button>
          <button onclick="setYear(2026)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2026">2026</button>
          <button onclick="setYear(2030)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-bold border border-cyan-500 bg-cyan-500/15 text-cyan-400 transition-all" data-yr="2030">2030</button>
          <button onclick="setYear(2035)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2035">2035</button>
          <button onclick="setYear(2040)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2040">2040</button>
          <button onclick="setYear(2050)" class="year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2050">2050</button>
        </div>
      </div>

      <div class="mt-4 pt-4 border-t border-[var(--card-border)] flex flex-col sm:flex-row items-center gap-4">
        <span class="text-xs font-mono text-[var(--text-muted)]">2024</span>
        <input type="range" id="slider-target-year" min="2024" max="2050" value="2030" step="1"
          class="w-full h-2 rounded-lg cursor-pointer" oninput="onYearSliderChange(this.value)">
        <span class="text-xs font-mono text-[var(--text-muted)]">2050</span>

        <div class="flex items-center gap-1.5 self-end sm:self-auto shrink-0">
          <span class="text-xs font-mono text-[var(--text-muted)]">Exact:</span>
          <input type="number" id="input-target-year" min="2024" max="2050" value="2030"
            class="w-18 px-2 py-1 text-xs rounded-lg border border-[var(--card-border)] bg-[var(--card-bg)] text-cyan-400 font-bold font-mono focus:outline-none focus:ring-1 focus:ring-cyan-500 text-center"
            onchange="setYear(parseInt(this.value))">
        </div>
      </div>
    </section>

    <!-- MAIN WORKSPACE GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- LEFT SIDEBAR: Clusters, Factors with Hazard Glows, Filters -->
      <aside class="lg:col-span-4 space-y-5">

        <!-- Country Bunches / Clusters -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1.5 font-mono">
              <span>🌍</span> Country Clusters
            </h3>
            <span id="selected-badge" class="text-[11px] px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 font-bold border border-cyan-500/20 font-mono">
              7 selected
            </span>
          </div>
          <div class="grid grid-cols-2 gap-2" id="cluster-buttons">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- WHAT-IF POLICY OVERRIDES (WITH DANGER GLOW DETECTORS) -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-4" id="policy-card">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1.5 font-mono">
              <span>⚙️</span> Stress Factors & Overrides
            </h3>
            <button onclick="resetSliders()" class="text-xs text-[var(--text-muted)] hover:text-cyan-400 transition-colors underline font-mono">
              Reset
            </button>
          </div>

          <!-- Slider 1: Primary Energy Shift (Primary Danger Driver) -->
          <div class="space-y-1.5 p-2 rounded-xl transition-all" id="box-energy">
            <div class="flex justify-between text-xs items-center">
              <span class="font-medium text-[var(--text-muted)]">Primary Energy Shift Δ</span>
              <div class="flex items-center gap-1.5 font-mono">
                <span id="tag-energy" class="text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-cyan-500/10 text-cyan-400">Safe</span>
                <span id="val-energy" class="font-bold text-amber-400">+0%</span>
              </div>
            </div>
            <input type="range" id="slider-energy" min="-25" max="40" value="0" step="1"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 2: Renewable Energy Expansion (Danger if 0 while demand surges) -->
          <div class="space-y-1.5 p-2 rounded-xl transition-all" id="box-re">
            <div class="flex justify-between text-xs items-center">
              <span class="font-medium text-[var(--text-muted)]">Renewable Expansion Δ</span>
              <div class="flex items-center gap-1.5 font-mono">
                <span id="tag-re" class="text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-emerald-500/10 text-emerald-400">Safe</span>
                <span id="val-re" class="font-bold text-emerald-400">+0%</span>
              </div>
            </div>
            <input type="range" id="slider-re" min="0" max="150" value="0" step="5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 3: GDP Growth Adjustment -->
          <div class="space-y-1.5 p-2 rounded-xl transition-all" id="box-gdp">
            <div class="flex justify-between text-xs items-center">
              <span class="font-medium text-[var(--text-muted)]">GDP Growth Δ</span>
              <div class="flex items-center gap-1.5 font-mono">
                <span id="tag-gdp" class="text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-cyan-500/10 text-cyan-400">Safe</span>
                <span id="val-gdp" class="font-bold text-cyan-400">+0.0%</span>
              </div>
            </div>
            <input type="range" id="slider-gdp" min="-15" max="30" value="0" step="0.5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 4: Population Growth Shift -->
          <div class="space-y-1.5 p-2 rounded-xl transition-all" id="box-pop">
            <div class="flex justify-between text-xs items-center">
              <span class="font-medium text-[var(--text-muted)]">Population Shift Δ</span>
              <div class="flex items-center gap-1.5 font-mono">
                <span id="tag-pop" class="text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-purple-500/10 text-purple-400">Safe</span>
                <span id="val-pop" class="font-bold text-purple-400">+0%</span>
              </div>
            </div>
            <input type="range" id="slider-pop" min="-10" max="25" value="0" step="1"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 5: Electrification Rate Minimum -->
          <div class="space-y-1.5 p-2 rounded-xl transition-all" id="box-elec">
            <div class="flex justify-between text-xs items-center">
              <span class="font-medium text-[var(--text-muted)]">Min Electrification %</span>
              <span id="val-elec" class="font-mono font-bold text-teal-400">Default</span>
            </div>
            <input type="range" id="slider-elec" min="0" max="100" value="0" step="5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>
        </div>

        <!-- Individual Country Selector -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] font-mono">
              📋 Country Selector
            </h3>
            <div class="space-x-2 text-xs font-mono">
              <button onclick="selectAll(true)" class="text-cyan-400 hover:underline">All</button>
              <span class="text-[var(--text-muted)]">|</span>
              <button onclick="selectAll(false)" class="text-[var(--text-muted)] hover:underline">Clear</button>
            </div>
          </div>
          <input type="text" id="country-search" placeholder="Search 218 countries..."
            class="w-full px-3 py-2 text-xs rounded-xl border border-[var(--card-border)] bg-[var(--card-bg)] text-[var(--text)] focus:outline-none focus:border-cyan-500 font-mono"
            oninput="filterCountryList()">
          <div id="country-checkbox-list" class="max-h-56 overflow-y-auto space-y-1 pr-1 text-xs">
            <!-- Injected by JS -->
          </div>
        </div>

      </aside>

      <!-- RIGHT DASHBOARD: KPIs, Trajectory Chart, Table -->
      <main class="lg:col-span-8 space-y-6">

        <!-- 3 AMOLED Hero KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <!-- KPI 1 -->
          <div id="kpi-card-demand" class="amoled-card rounded-2xl p-5 relative overflow-hidden transition-all">
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider font-mono">Forecasted Demand (<span class="year-label text-cyan-400">2030</span>)</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-total-demand" class="text-3xl sm:text-4xl font-black tracking-tight text-cyan-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)] font-mono">TWh</span>
            </div>
            <p id="kpi-demand-delta" class="text-xs mt-1.5 font-semibold text-emerald-400 font-mono">+0.0% vs baseline</p>
          </div>

          <!-- KPI 2 -->
          <div class="amoled-card rounded-2xl p-5 relative overflow-hidden">
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider font-mono">Avg Per-Capita Demand</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-per-capita" class="text-3xl sm:text-4xl font-black tracking-tight text-purple-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)] font-mono">kWh/person</span>
            </div>
            <p id="kpi-population" class="text-xs mt-1.5 text-[var(--text-muted)] font-mono">Projected for 0M people</p>
          </div>

          <!-- KPI 3 -->
          <div id="kpi-card-re" class="amoled-card rounded-2xl p-5 relative overflow-hidden transition-all">
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider font-mono">Projected Clean RE Capacity</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-re-cap" class="text-3xl sm:text-4xl font-black tracking-tight text-emerald-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)] font-mono">GW</span>
            </div>
            <p id="kpi-country-count" class="text-xs mt-1.5 text-[var(--text-muted)] font-mono">Across 0 countries</p>
          </div>
        </div>

        <!-- Trajectory Timeline Visualizer -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold flex items-center gap-2 font-mono">
                <span>📈</span> Future Trajectory Pathway (2024 — 2050)
              </h3>
              <p class="text-xs text-[var(--text-muted)]">Combined projected electricity requirements (TWh) over time</p>
            </div>
            <div class="flex items-center gap-3 text-xs font-mono">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block shadow-[0_0_8px_#00f0ff]"></span> Baseline Path</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block shadow-[0_0_8px_#00ff9f]"></span> Scenario Path</span>
            </div>
          </div>

          <!-- SVG Trajectory Chart -->
          <div class="w-full h-48 sm:h-56 pt-2" id="trajectory-chart-container">
            <!-- Injected by JS -->
          </div>
        </div>

        <!-- Comparative Country Breakdown Bars -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold flex items-center gap-2 font-mono">
              <span>⚡</span> Country Forecast Rankings in <span class="year-label text-cyan-400">2030</span>
            </h3>
            <span class="text-xs text-[var(--text-muted)] font-mono">Electricity needed (TWh)</span>
          </div>
          <div id="chart-bars" class="space-y-3 max-h-72 overflow-y-auto pr-1">
            <!-- Dynamic country bars injected here -->
          </div>
        </div>

        <!-- Comprehensive Country Forecast Table -->
        <div class="amoled-card rounded-2xl p-5 shadow-2xl space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h3 class="text-sm font-bold flex items-center gap-2 font-mono">
              <span>📊</span> Detailed Forecast Table (<span class="year-label text-cyan-400">2030</span>)
            </h3>
            <span class="text-xs text-[var(--text-muted)] font-mono" id="table-row-count">Showing 7 countries</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-[var(--card-border)] text-[var(--text-muted)] uppercase tracking-wider font-mono font-bold">
                  <th class="py-2.5 px-3">Country</th>
                  <th class="py-2.5 px-3">ISO3</th>
                  <th class="py-2.5 px-3 text-right">Hist 2024 (TWh)</th>
                  <th class="py-2.5 px-3 text-right">Forecast (<span class="year-label">2030</span>)</th>
                  <th class="py-2.5 px-3 text-right">Delta</th>
                  <th class="py-2.5 px-3 text-right">Per Capita (kWh)</th>
                  <th class="py-2.5 px-3 text-right">Proj. RE (MW)</th>
                </tr>
              </thead>
              <tbody id="table-body" class="divide-y divide-[var(--card-border)] font-mono">
                <!-- Injected by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </main>
    </div>

  </div>

  <script>
    const DATA = {json_str};

    let targetYear = 2030;
    let selectedCountryNames = new Set(DATA.groups.G7 || ["United States", "China", "India"]);
    let currentResults = [];

    // Natural Language Prompt Parser & Engine
    function fillPrompt(text) {{
      document.getElementById("ai-prompt-input").value = text;
      executeAIPrompt();
    }}

    function executeAIPrompt() {{
      const prompt = document.getElementById("ai-prompt-input").value.trim();
      if (!prompt) return;

      const pLower = prompt.toLowerCase();

      // Extract Target Year
      const yrMatch = prompt.match(/\\b(20[2-5][0-9])\\b/);
      let detectedYear = yrMatch ? parseInt(yrMatch[1]) : targetYear;

      // Extract Predefined Groups
      let detectedGroup = null;
      for (const gKey of Object.keys(DATA.groups)) {{
        const clean = gKey.toLowerCase().replace("_", " ");
        if (pLower.includes(clean) || pLower.includes(gKey.toLowerCase())) {{
          detectedGroup = gKey;
          break;
        }}
      }}
      if (!detectedGroup) {{
        if (pLower.includes("g7")) detectedGroup = "G7";
        else if (pLower.includes("brics")) detectedGroup = "BRICS";
        else if (pLower.includes("eu") || pLower.includes("europe")) detectedGroup = "EU_TOP";
        else if (pLower.includes("latam") || pLower.includes("latin america")) detectedGroup = "LATAM_TOP";
        else if (pLower.includes("asia")) detectedGroup = "ASIA_PACIFIC";
        else if (pLower.includes("global top") || pLower.includes("top 10")) detectedGroup = "GLOBAL_TOP_10";
      }}

      // Extract Countries
      let foundCountries = new Set();
      if (detectedGroup && DATA.groups[detectedGroup]) {{
        DATA.groups[detectedGroup].forEach(c => foundCountries.add(c));
      }}

      DATA.countries.forEach(c => {{
        const cLower = c.name.toLowerCase();
        const isoLower = c.iso.toLowerCase();
        const regex = new RegExp("\\\\b" + cLower + "\\\\b", "i");
        const isoRegex = new RegExp("\\\\b" + isoLower + "\\\\b", "i");
        if (regex.test(prompt) || isoRegex.test(prompt)) {{
          foundCountries.add(c.name);
        }}
      }});

      if (/\\b(usa|us|america)\\b/i.test(prompt)) foundCountries.add("United States");
      if (/\\b(uk|britain)\\b/i.test(prompt)) foundCountries.add("United Kingdom");
      if (/\\brussia\\b/i.test(prompt)) foundCountries.add("Russia");
      if (/\\bsouth korea\\b/i.test(prompt)) foundCountries.add("South Korea");

      // Extract Factor Overrides
      let gdpAdj = 0;
      const gdpM = pLower.match(/([+-]?\\d+(?:\\.\\d+)?)\\s*%\\s*(?:higher|more|growth)?\\s*gdp/) ||
                   pLower.match(/gdp\\s*(?:growth|increase|change)?\\s*(?:of|by)?\\s*([+-]?\\d+(?:\\.\\d+)?)\\s*%/);
      if (gdpM) gdpAdj = parseFloat(gdpM[1]);

      let reAdj = 0;
      const reM = pLower.match(/([+-]?\\d+(?:\\.\\d+)?)\\s*%\\s*(?:more|expansion|increase)?\\s*(?:renewable|re|solar|clean)/) ||
                  pLower.match(/(?:renewable|re|solar|clean)\\s*(?:expansion|growth|increase)?\\s*(?:of|by)?\\s*([+-]?\\d+(?:\\.\\d+)?)\\s*%/);
      if (reM) reAdj = parseFloat(reM[1]);
      else if (pLower.includes("double renewable") || pLower.includes("double re")) reAdj = 100;

      let energyAdj = 0;
      const peM = pLower.match(/([+-]?\\d+(?:\\.\\d+)?)\\s*%\\s*(?:more|higher|surge|shift|growth)?\\s*(?:primary\\s+)?energy/) ||
                  pLower.match(/energy\\s*(?:surge|shift|growth|increase)?\\s*(?:of|by)?\\s*([+-]?\\d+(?:\\.\\d+)?)\\s*%/);
      if (peM) energyAdj = parseFloat(peM[1]);

      let elecTarget = 0;
      const elecM = pLower.match(/(\\d+(?:\\.\\d+)?)\\s*%\\s*(?:electrification|electricity access)/);
      if (elecM) elecTarget = parseFloat(elecM[1]);

      if (foundCountries.size > 0) {{
        selectedCountryNames = foundCountries;
      }}

      setYear(detectedYear);
      document.getElementById("slider-gdp").value = gdpAdj;
      document.getElementById("slider-re").value = reAdj;
      document.getElementById("slider-energy").value = energyAdj;
      document.getElementById("slider-elec").value = elecTarget;

      updateSimulation();
      renderCountryCheckboxes(document.getElementById("country-search").value);

      const selCount = currentResults.length;
      const totDemand = parseFloat(document.getElementById("kpi-total-demand").innerText.replace(/,/g, ""));
      const cNames = currentResults.slice(0, 4).map(c => c.name).join(", ") + (selCount > 4 ? ` and ${{selCount - 4}} others` : "");

      let answerHtml = "";
      if (selCount === 1) {{
        const c = currentResults[0];
        answerHtml = `In <strong>${{detectedYear}}</strong>, the forecasted electricity demand for <strong>${{c.name}}</strong> is <strong class="text-cyan-400 font-mono">${{c.predicted.toLocaleString(undefined, {{maximumFractionDigits: 1}})}} TWh</strong> (approx. <span class="font-mono text-purple-400">${{Math.round(c.perCapita).toLocaleString()}} kWh</span> per person).`;
        if (c.delta !== 0) {{
          answerHtml += ` This represents a <strong class="${{c.delta >= 0 ? "text-emerald-400" : "text-amber-400"}} font-mono">${{c.delta >= 0 ? "+" : ""}}${{c.delta.toFixed(1)}} TWh (${{c.deltaPct >= 0 ? "+" : ""}}${{c.deltaPct.toFixed(1)}}%)</strong> shift relative to 2024 baseline.`;
        }}
      }} else {{
        answerHtml = `In <strong>${{detectedYear}}</strong>, the combined electricity demand for <strong>${{selCount}} countries</strong> (${{cNames}}) is forecasted at <strong class="text-cyan-400 text-base font-mono">${{totDemand.toLocaleString()}} TWh</strong>.`;
        if (gdpAdj !== 0 || reAdj !== 0 || energyAdj !== 0) {{
          answerHtml += ` Incorporating your scenario overrides (${{energyAdj !== 0 ? `Energy: ${{energyAdj >= 0 ? "+" : ""}}${{energyAdj}}%, ` : ""}}${{gdpAdj !== 0 ? `GDP: ${{gdpAdj >= 0 ? "+" : ""}}${{gdpAdj}}%, ` : ""}}${{reAdj !== 0 ? `Renewables: +${{reAdj}}%` : ""}}).`;
        }}
      }}

      const resBox = document.getElementById("ai-response-box");
      document.getElementById("ai-response-text").innerHTML = answerHtml;
      document.getElementById("ai-response-badge").innerText = `Forecast Year ${{detectedYear}} • ${{selCount}} Countries Analyzed`;
      resBox.classList.remove("hidden");
    }}

    // Theme Management
    function initTheme() {{
      const saved = localStorage.getItem("theme");
      if (saved === "light") {{
        document.documentElement.classList.remove("dark");
        updateThemeButton(false);
      }} else {{
        document.documentElement.classList.add("dark");
        updateThemeButton(true);
      }}
    }}

    function toggleTheme() {{
      const isDark = document.documentElement.classList.toggle("dark");
      localStorage.setItem("theme", isDark ? "dark" : "light");
      updateThemeButton(isDark);
      updateSimulation();
    }}

    function updateThemeButton(isDark) {{
      document.getElementById("theme-icon").innerText = isDark ? "🌙" : "☀️";
      document.getElementById("theme-text").innerText = isDark ? "AMOLED" : "Light";
    }}

    // Year Selector Management
    function setYear(yr) {{
      targetYear = Math.max(2024, Math.min(2050, parseInt(yr) || 2024));
      document.getElementById("slider-target-year").value = targetYear;
      document.getElementById("input-target-year").value = targetYear;
      document.getElementById("display-target-year").innerText = targetYear;
      document.querySelectorAll(".year-label").forEach(el => el.innerText = targetYear);

      document.querySelectorAll(".year-pill").forEach(pill => {{
        const pyr = parseInt(pill.getAttribute("data-yr"));
        if (pyr === targetYear) {{
          pill.className = "year-pill px-3 py-1 rounded-lg text-xs font-mono font-bold border border-cyan-500 bg-cyan-500/15 text-cyan-400 transition-all shadow-[0_0_10px_rgba(0,240,255,0.3)]";
        }} else {{
          pill.className = "year-pill px-3 py-1 rounded-lg text-xs font-mono font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all";
        }}
      }});

      updateSimulation();
    }}

    function onYearSliderChange(val) {{
      setYear(parseInt(val));
    }}

    // Country Cluster Pills
    const clusterContainer = document.getElementById("cluster-buttons");
    Object.keys(DATA.groups).forEach((gKey, idx) => {{
      const btn = document.createElement("button");
      btn.className = `px-3 py-2 text-xs font-mono font-semibold rounded-xl border transition-all text-center ${{
        idx === 0
          ? "border-cyan-500 bg-cyan-500/15 text-cyan-400 font-bold shadow-[0_0_10px_rgba(0,240,255,0.25)]"
          : "border-[var(--card-border)] hover:border-cyan-500/50 text-[var(--text)]"
      }}`;
      btn.innerText = gKey.replace("_", " ");
      btn.onclick = () => selectCluster(gKey, btn);
      clusterContainer.appendChild(btn);
    }});

    function selectCluster(gKey, activeBtn) {{
      document.querySelectorAll("#cluster-buttons button").forEach(b => {{
        b.className = "px-3 py-2 text-xs font-mono font-semibold rounded-xl border border-[var(--card-border)] hover:border-cyan-500/50 text-[var(--text)] text-center";
      }});
      if (activeBtn) {{
        activeBtn.className = "px-3 py-2 text-xs font-mono font-bold rounded-xl border border-cyan-500 bg-cyan-500/15 text-cyan-400 text-center shadow-[0_0_10px_rgba(0,240,255,0.25)]";
      }}
      const list = DATA.groups[gKey] || [];
      selectedCountryNames = new Set(list);
      updateSelectedCount();
      renderCountryCheckboxes(document.getElementById("country-search").value);
      updateSimulation();
    }}

    // Checkboxes List
    function renderCountryCheckboxes(filter = "") {{
      const container = document.getElementById("country-checkbox-list");
      container.innerHTML = "";
      const search = filter.toLowerCase();

      DATA.countries
        .filter(c => c.name.toLowerCase().includes(search) || c.iso.toLowerCase().includes(search))
        .forEach(c => {{
          const label = document.createElement("label");
          label.className = "flex items-center gap-2 py-1 px-2 rounded-lg hover:bg-cyan-500/10 cursor-pointer transition-colors";
          const cb = document.createElement("input");
          cb.type = "checkbox";
          cb.checked = selectedCountryNames.has(c.name);
          cb.className = "rounded border-[var(--card-border)] accent-cyan-500";
          cb.onchange = (e) => {{
            if (e.target.checked) selectedCountryNames.add(c.name);
            else selectedCountryNames.delete(c.name);
            updateSelectedCount();
            updateSimulation();
          }};
          const span = document.createElement("span");
          span.className = "font-mono text-[var(--text)]";
          span.innerText = `${{c.name}} (${{c.iso}})`;
          label.appendChild(cb);
          label.appendChild(span);
          container.appendChild(label);
        }});
    }}

    function filterCountryList() {{
      const val = document.getElementById("country-search").value;
      renderCountryCheckboxes(val);
    }}

    function selectAll(state) {{
      if (state) {{
        selectedCountryNames = new Set(DATA.countries.map(c => c.name));
      }} else {{
        selectedCountryNames.clear();
      }}
      updateSelectedCount();
      renderCountryCheckboxes(document.getElementById("country-search").value);
      updateSimulation();
    }}

    function updateSelectedCount() {{
      document.getElementById("selected-badge").innerText = `${{selectedCountryNames.size}} selected`;
    }}

    function resetSliders() {{
      document.getElementById("slider-gdp").value = 0;
      document.getElementById("slider-re").value = 0;
      document.getElementById("slider-energy").value = 0;
      document.getElementById("slider-pop").value = 0;
      document.getElementById("slider-elec").value = 0;
      updateSimulation();
    }}

    // HIGH-VOLTAGE RISK & DANGER EVALUATOR
    function evaluateGridRisk(totalBaseline, totalPredicted, reExp, energyShift, gdpShift) {{
      const hud = document.getElementById("grid-risk-hud");
      const icon = document.getElementById("risk-status-icon");
      const badge = document.getElementById("risk-level-badge");
      const headline = document.getElementById("risk-headline");
      const scoreEl = document.getElementById("risk-stability-score");
      const barEl = document.getElementById("risk-stability-bar");
      const detailsBox = document.getElementById("risk-details-box");

      const kpiDemandCard = document.getElementById("kpi-card-demand");
      const policyCard = document.getElementById("policy-card");

      const growthPct = totalBaseline > 0 ? ((totalPredicted - totalBaseline) / totalBaseline) * 100 : 0;

      // Base stability score (starts at 100%)
      let score = 100;
      let isCriticalDanger = false;
      let isElevatedRisk = false;
      let dangerReasons = [];

      // Risk condition 1: Extreme Energy Surge (> +15%)
      if (energyShift >= 15) {{
        score -= (energyShift - 10) * 1.5;
        dangerReasons.push("Severe primary energy surge exacerbating power grid stress.");
      }} else if (energyShift <= -15) {{
        score -= 10;
        dangerReasons.push("Severe energy slump risking stranded generation assets.");
      }}

      // Risk condition 2: Generation Shortfall / Demand Surge without Clean Expansion
      if (growthPct > 20 && reExp < 15) {{
        score -= 28;
        isCriticalDanger = true;
        dangerReasons.push(`Demand surges by +${{growthPct.toFixed(1)}}% while renewable expansion is only +${{reExp}}%, creating massive generation deficit.`);
      }} else if (growthPct > 12 && reExp < 10) {{
        score -= 15;
        isElevatedRisk = true;
      }}

      // Risk condition 3: Extreme GDP volatility
      if (gdpShift >= 20) {{
        score -= 12;
      }} else if (gdpShift <= -10) {{
        score -= 18;
        dangerReasons.push("Severe economic contraction threatening utility revenue and grid maintenance.");
      }}

      score = Math.max(15, Math.min(100, Math.round(score)));

      // Individual Slider Hazard Badges & Glowing Red Styles
      updateSliderHazardState("energy", energyShift >= 15 || energyShift <= -15, energyShift >= 25);
      updateSliderHazardState("re", growthPct > 15 && reExp < 10, growthPct > 25 && reExp < 5);
      updateSliderHazardState("gdp", gdpShift >= 20 || gdpShift <= -10, gdpShift >= 25 || gdpShift <= -12);

      // Apply Danger HUD Styles
      if (score < 70 || isCriticalDanger) {{
        // CRITICAL DANGER (Crimson Glowing Pulsation)
        hud.className = "amoled-card rounded-2xl p-5 shadow-2xl border transition-all relative overflow-hidden danger-glow";
        kpiDemandCard.className = "amoled-card rounded-2xl p-5 relative overflow-hidden transition-all danger-glow";
        policyCard.className = "amoled-card rounded-2xl p-5 shadow-2xl space-y-4 border-red-500/50";

        icon.className = "w-10 h-10 rounded-xl bg-red-500/20 border border-red-500/50 flex items-center justify-center text-red-400 text-xl font-black animate-pulse";
        icon.innerText = "🚨";

        badge.className = "text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40 animate-pulse";
        badge.innerText = "CRITICAL GRID HAZARD • DEFICIT";

        headline.innerHTML = `<span class="text-red-400 font-black">HIGH-VOLTAGE GRID FAILURE WARNING:</span> ${{dangerReasons[0] || "Severe supply-demand imbalance threatens blackouts."}}`;

        scoreEl.className = "text-2xl font-mono font-black text-red-400 animate-pulse";
        scoreEl.innerText = `${{score}}%`;

        barEl.className = "h-full rounded-full bg-red-500 transition-all duration-300";
        barEl.style.width = `${{score}}%`;

        detailsBox.classList.remove("hidden");
        document.getElementById("risk-blackout-desc").innerText = `Deficit of ~${{(totalPredicted - totalBaseline).toFixed(1)}} TWh overstretching transmission lines.`;
        document.getElementById("risk-carbon-desc").innerText = `Fossil peaking units forced to maximum dispatch, spiking emissions.`;
        document.getElementById("risk-infra-desc").innerText = `Reserve margins breached; high risk of unscheduled load shedding.`;

      }} else if (score < 88 || isElevatedRisk) {{
        // ELEVATED RISK (Neon Amber)
        hud.className = "amoled-card rounded-2xl p-5 shadow-2xl border border-amber-500/40 transition-all relative overflow-hidden";
        kpiDemandCard.className = "amoled-card rounded-2xl p-5 relative overflow-hidden transition-all border-amber-500/40";
        policyCard.className = "amoled-card rounded-2xl p-5 shadow-2xl space-y-4";

        icon.className = "w-10 h-10 rounded-xl bg-amber-500/15 border border-amber-500/40 flex items-center justify-center text-amber-400 text-xl font-black";
        icon.innerText = "⚠️";

        badge.className = "text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30";
        badge.innerText = "ELEVATED GRID STRESS";

        headline.innerHTML = `<span class="text-amber-400 font-bold">GRID STRAIN DETECTED:</span> Rapid shifts in consumption require active reserve throttling.`;

        scoreEl.className = "text-2xl font-mono font-black text-amber-400";
        scoreEl.innerText = `${{score}}%`;

        barEl.className = "h-full rounded-full bg-amber-400 transition-all duration-300";
        barEl.style.width = `${{score}}%`;

        detailsBox.classList.remove("hidden");
        document.getElementById("risk-blackout-desc").innerText = `Sub-optimal reserve margin. Grid frequency fluctuations possible.`;
        document.getElementById("risk-carbon-desc").innerText = `Marginal emission intensity rises to meet unexpected peak.`;
        document.getElementById("risk-infra-desc").innerText = `Transmission bottlenecks observed during peak industrial hours.`;

      }} else {{
        // NOMINAL / OPTIMAL STABLE (Cyan & Emerald)
        hud.className = "amoled-card rounded-2xl p-5 shadow-2xl border border-cyan-500/30 transition-all relative overflow-hidden";
        kpiDemandCard.className = "amoled-card rounded-2xl p-5 relative overflow-hidden transition-all";
        policyCard.className = "amoled-card rounded-2xl p-5 shadow-2xl space-y-4";

        icon.className = "w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-xl font-black";
        icon.innerText = "🛡️";

        badge.className = "text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30";
        badge.innerText = "NOMINAL • STABLE";

        headline.innerText = "Power grid operating safely within reserve capacity margins.";

        scoreEl.className = "text-2xl font-mono font-black text-emerald-400";
        scoreEl.innerText = `${{score}}%`;

        barEl.className = "h-full rounded-full bg-emerald-400 transition-all duration-300";
        barEl.style.width = `${{score}}%`;

        detailsBox.classList.add("hidden");
      }}
    }}

    function updateSliderHazardState(key, isWarning, isHazard) {{
      const box = document.getElementById(`box-${{key}}`);
      const tag = document.getElementById(`tag-${{key}}`);
      const slider = document.getElementById(`slider-${{key}}`);
      if (!box || !tag || !slider) return;

      if (isHazard) {{
        box.className = "space-y-1.5 p-2 rounded-xl transition-all border border-red-500/50 bg-red-500/10 shadow-[0_0_15px_rgba(255,0,60,0.3)]";
        tag.className = "text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-red-500/20 text-red-400 animate-pulse";
        tag.innerText = "⚠️ DANGER";
        slider.classList.add("slider-hazard");
      }} else if (isWarning) {{
        box.className = "space-y-1.5 p-2 rounded-xl transition-all border border-amber-500/30 bg-amber-500/5";
        tag.className = "text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-amber-500/20 text-amber-400";
        tag.innerText = "WARNING";
        slider.classList.remove("slider-hazard");
      }} else {{
        box.className = "space-y-1.5 p-2 rounded-xl transition-all";
        tag.className = "text-[9px] px-1.5 py-0.2 rounded font-bold uppercase bg-cyan-500/10 text-cyan-400";
        tag.innerText = "SAFE";
        slider.classList.remove("slider-hazard");
      }}
    }}

    // Simulation Engine
    function updateSimulation() {{
      const gdpShift = parseFloat(document.getElementById("slider-gdp").value);
      const reExp = parseFloat(document.getElementById("slider-re").value);
      const energyShift = parseFloat(document.getElementById("slider-energy").value);
      const popShift = parseFloat(document.getElementById("slider-pop").value);
      const minElec = parseFloat(document.getElementById("slider-elec").value);

      document.getElementById("val-gdp").innerText = (gdpShift >= 0 ? "+" : "") + gdpShift.toFixed(1) + "%";
      document.getElementById("val-re").innerText = "+" + reExp + "%";
      document.getElementById("val-energy").innerText = (energyShift >= 0 ? "+" : "") + energyShift + "%";
      document.getElementById("val-pop").innerText = (popShift >= 0 ? "+" : "") + popShift + "%";
      document.getElementById("val-elec").innerText = minElec > 0 ? (minElec + "%") : "Default";

      const selected = DATA.countries.filter(c => selectedCountryNames.has(c.name));
      const dt = targetYear - 2024;

      let totalHist2024 = 0;
      let totalPredicted = 0;
      let totalPopulation = 0;
      let totalRECap = 0;

      currentResults = selected.map(c => {{
        const cagr = c.cagr || {{ pop_cagr: 0.008, gdp_cagr: 0.025, pe_cagr: 0.015, re_add_mw_per_year: 500 }};
        const baseDemand = c.baseline_demand_twh;

        const effectivePopCAGR = cagr.pop_cagr + (popShift / 100) * 0.01;
        const effectiveGDPCAGR = cagr.gdp_cagr + (gdpShift / 100) * 0.01;
        const effectivePECAGR = cagr.pe_cagr + (energyShift / 100) * 0.01;

        const pop = c.population * Math.pow(1 + effectivePopCAGR, dt);
        const gdp = c.gdp * Math.pow(1 + effectiveGDPCAGR, dt);
        const pe = c.primary_energy * Math.pow(1 + effectivePECAGR, dt);
        const reAdd = (cagr.re_add_mw_per_year * (1 + reExp / 100)) * dt;
        const reCap = c.re_capacity_mw + Math.max(0, reAdd);

        let growthMultiplier = Math.pow(1 + effectivePECAGR, dt * 0.94) * Math.pow(1 + effectiveGDPCAGR, dt * 0.08);

        if (minElec > 0 && c.electrification_pct < minElec) {{
          growthMultiplier *= (1 + ((minElec - c.electrification_pct) / 100) * 0.25);
        }}

        const predicted = Math.max(0.01, baseDemand * growthMultiplier);
        const perCapita = pop > 0 ? (predicted * 1e9) / pop : 0;
        const delta = predicted - baseDemand;

        totalHist2024 += baseDemand;
        totalPredicted += predicted;
        totalPopulation += pop;
        totalRECap += reCap;

        return {{
          name: c.name,
          iso: c.iso,
          hist2024: baseDemand,
          predicted: predicted,
          delta: delta,
          deltaPct: baseDemand > 0 ? (delta / baseDemand) * 100 : 0,
          perCapita: perCapita,
          reCap: reCap
        }};
      }});

      currentResults.sort((a, b) => b.predicted - a.predicted);

      // Evaluate High-Voltage Grid Risk
      evaluateGridRisk(totalHist2024, totalPredicted, reExp, energyShift, gdpShift);

      // Update KPI Cards
      document.getElementById("kpi-total-demand").innerText = totalPredicted.toLocaleString(undefined, {{maximumFractionDigits: 1}});
      const netDeltaPct = totalHist2024 > 0 ? ((totalPredicted - totalHist2024) / totalHist2024) * 100 : 0;
      const deltaEl = document.getElementById("kpi-demand-delta");
      deltaEl.innerText = `${{netDeltaPct >= 0 ? "+" : ""}}${{netDeltaPct.toFixed(1)}}% vs 2024 baseline (${{totalHist2024.toFixed(1)}} TWh)`;
      deltaEl.className = `text-xs mt-1.5 font-semibold font-mono ${{netDeltaPct >= 0 ? "text-emerald-400" : "text-amber-400"}}`;

      const avgPerCapita = totalPopulation > 0 ? (totalPredicted * 1e9) / totalPopulation : 0;
      document.getElementById("kpi-per-capita").innerText = Math.round(avgPerCapita).toLocaleString();
      document.getElementById("kpi-population").innerText = `Projected for ${{ (totalPopulation / 1e6).toFixed(1) }}M people in ${{targetYear}}`;

      document.getElementById("kpi-re-cap").innerText = (totalRECap / 1e3).toLocaleString(undefined, {{maximumFractionDigits: 1}});
      document.getElementById("kpi-country-count").innerText = `Across ${{selected.length}} selected countries`;

      // Render Trajectory Line Chart
      renderTrajectoryChart(selected);

      // Render Country Bars
      renderBars(currentResults);

      // Render Table
      renderTable(currentResults);
    }}

    function renderTrajectoryChart(selected) {{
      const container = document.getElementById("trajectory-chart-container");
      if (selected.length === 0) {{
        container.innerHTML = '<div class="h-full flex items-center justify-center text-xs text-[var(--text-muted)] font-mono">Select at least one country to view trajectory.</div>';
        return;
      }}

      const years = [2024, 2026, 2028, 2030, 2035, 2040, 2050];
      const gdpShift = parseFloat(document.getElementById("slider-gdp").value);
      const energyShift = parseFloat(document.getElementById("slider-energy").value);

      const baselinePoints = [];
      const scenarioPoints = [];

      years.forEach(yr => {{
        const dt = yr - 2024;
        let baseSum = 0;
        let scenSum = 0;

        selected.forEach(c => {{
          const cagr = c.cagr || {{ pop_cagr: 0.008, gdp_cagr: 0.025, pe_cagr: 0.015 }};
          const bDem = c.baseline_demand_twh;

          const baseMult = Math.pow(1 + cagr.pe_cagr, dt * 0.94) * Math.pow(1 + cagr.gdp_cagr, dt * 0.08);
          baseSum += bDem * baseMult;

          const effPE = cagr.pe_cagr + (energyShift / 100) * 0.01;
          const effGDP = cagr.gdp_cagr + (gdpShift / 100) * 0.01;
          const scenMult = Math.pow(1 + effPE, dt * 0.94) * Math.pow(1 + effGDP, dt * 0.08);
          scenSum += bDem * scenMult;
        }});

        baselinePoints.push({{ year: yr, val: baseSum }});
        scenarioPoints.push({{ year: yr, val: scenSum }});
      }});

      const allVals = [...baselinePoints.map(p => p.val), ...scenarioPoints.map(p => p.val)];
      const minVal = Math.min(...allVals) * 0.95;
      const maxVal = Math.max(...allVals) * 1.05;

      const w = 700;
      const h = 200;
      const padL = 60;
      const padR = 30;
      const padT = 20;
      const padB = 30;

      const getX = (yr) => padL + ((yr - 2024) / (2050 - 2024)) * (w - padL - padR);
      const getY = (val) => h - padB - ((val - minVal) / (maxVal - minVal || 1)) * (h - padT - padB);

      const makePath = (pts) => pts.map((p, i) => `${{i === 0 ? "M" : "L"}} ${{getX(p.year).toFixed(1)}} ${{getY(p.val).toFixed(1)}}`).join(" ");

      const baseD = makePath(baselinePoints);
      const scenD = makePath(scenarioPoints);
      const targetX = getX(targetYear);

      container.innerHTML = `
        <svg viewBox="0 0 ${{w}} ${{h}}" class="w-full h-full overflow-visible">
          ${{[0.25, 0.5, 0.75, 1.0].map(pct => {{
            const yv = minVal + pct * (maxVal - minVal);
            const ypos = getY(yv);
            return `
              <line x1="${{padL}}" y1="${{ypos}}" x2="${{w - padR}}" y2="${{ypos}}" stroke="currentColor" stroke-opacity="0.08" stroke-dasharray="4,4"/>
              <text x="${{padL - 8}}" y="${{ypos + 4}}" fill="currentColor" fill-opacity="0.4" font-size="10" font-family="monospace" text-anchor="end">${{Math.round(yv).toLocaleString()}}</text>
            `;
          }}).join("")}}

          ${{years.map(yr => `
            <text x="${{getX(yr)}}" y="${{h - 10}}" fill="currentColor" fill-opacity="0.5" font-size="10" font-family="monospace" text-anchor="middle">${{yr}}</text>
          `).join("")}}

          <path d="${{baseD}}" fill="none" stroke="#00f0ff" stroke-width="2" stroke-dasharray="5,4" opacity="0.8"/>
          <path d="${{scenD}}" fill="none" stroke="#00ff9f" stroke-width="2.8"/>
          <line x1="${{targetX}}" y1="${{padT}}" x2="${{targetX}}" y2="${{h - padB}}" stroke="#00f0ff" stroke-width="1.5" stroke-dasharray="2,2"/>
          <circle cx="${{targetX}}" cy="${{getY(scenarioPoints.find(p => p.year === targetYear)?.val || scenarioPoints[0].val)}}" r="5.5" fill="#00ff9f" stroke="#000000" stroke-width="2"/>
        </svg>
      `;
    }}

    function renderBars(items) {{
      const container = document.getElementById("chart-bars");
      container.innerHTML = "";
      if (items.length === 0) {{
        container.innerHTML = '<div class="text-xs text-[var(--text-muted)] py-4 text-center font-mono">No countries selected.</div>';
        return;
      }}

      const maxVal = Math.max(...items.map(i => Math.max(i.hist2024, i.predicted)), 1);

      items.slice(0, 15).forEach(item => {{
        const row = document.createElement("div");
        row.className = "space-y-1";

        const header = document.createElement("div");
        header.className = "flex justify-between text-xs";
        header.innerHTML = `
          <span class="font-medium">${{item.name}} <span class="text-[var(--text-muted)] font-mono">(${{item.iso}})</span></span>
          <span class="font-bold text-cyan-400 font-mono">${{item.predicted.toLocaleString(undefined, {{maximumFractionDigits: 1}})}} TWh
            <span class="text-xs font-normal font-mono ${{item.delta >= 0 ? "text-emerald-400" : "text-amber-400"}}">
              (${{item.delta >= 0 ? "+" : ""}}${{item.delta.toFixed(1)}})
            </span>
          </span>
        `;

        const barWrapper = document.createElement("div");
        barWrapper.className = "h-3 w-full bg-[var(--slider-bg)] rounded-full overflow-hidden flex relative";

        const basePct = (item.hist2024 / maxVal) * 100;
        const predPct = (item.predicted / maxVal) * 100;

        const baseBar = document.createElement("div");
        baseBar.style.width = `${{basePct}}%`;
        baseBar.className = "h-full bg-slate-500/40 absolute top-0 left-0 rounded-full";

        const predBar = document.createElement("div");
        predBar.style.width = `${{predPct}}%`;
        predBar.className = "h-full bg-gradient-to-r from-cyan-500 to-emerald-400 absolute top-0 left-0 rounded-full opacity-90";

        barWrapper.appendChild(baseBar);
        barWrapper.appendChild(predBar);

        row.appendChild(header);
        row.appendChild(barWrapper);
        container.appendChild(row);
      }});

      if (items.length > 15) {{
        const note = document.createElement("div");
        note.className = "text-center text-xs text-[var(--text-muted)] pt-1 font-mono";
        note.innerText = `+ ${{items.length - 15}} more countries (see table below)`;
        container.appendChild(note);
      }}
    }}

    function renderTable(items) {{
      const tbody = document.getElementById("table-body");
      tbody.innerHTML = "";
      document.getElementById("table-row-count").innerText = `Showing ${{items.length}} countries`;

      items.forEach(item => {{
        const tr = document.createElement("tr");
        tr.className = "hover:bg-cyan-500/5 transition-colors";
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-medium text-[var(--text)] font-sans">${{item.name}}</td>
          <td class="py-2.5 px-3 text-[var(--text-muted)]">${{item.iso}}</td>
          <td class="py-2.5 px-3 text-right text-[var(--text-muted)]">${{item.hist2024.toFixed(2)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-cyan-400">${{item.predicted.toFixed(2)}}</td>
          <td class="py-2.5 px-3 text-right ${{item.delta >= 0 ? "text-emerald-400" : "text-amber-400"}}">
            ${{item.delta >= 0 ? "+" : ""}}${{item.delta.toFixed(2)}} (${{item.deltaPct >= 0 ? "+" : ""}}${{item.deltaPct.toFixed(1)}}%)
          </td>
          <td class="py-2.5 px-3 text-right">${{Math.round(item.perCapita).toLocaleString()}}</td>
          <td class="py-2.5 px-3 text-right">${{Math.round(item.reCap).toLocaleString()}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function exportCSV() {{
      if (!currentResults || currentResults.length === 0) return;
      let csv = `Country,ISO3,Target_Year,Hist_2024_Demand_TWh,Forecast_${{targetYear}}_Demand_TWh,Delta_TWh,Delta_Pct,Per_Capita_kWh,Projected_Renewable_MW\\n`;
      currentResults.forEach(r => {{
        csv += `"${{r.name}}",${{r.iso}},${{targetYear}},${{r.hist2024.toFixed(2)}},${{r.predicted.toFixed(2)}},${{r.delta.toFixed(2)}},${{r.deltaPct.toFixed(2)}},${{r.perCapita.toFixed(1)}},${{r.reCap.toFixed(1)}}\\n`;
      }});
      const blob = new Blob([csv], {{ type: "text/csv;charset=utf-8;" }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `electricity_forecast_${{targetYear}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    initTheme();
    renderCountryCheckboxes();
    setYear(2030);
  </script>
</body>
</html>
"""

output_path = Path("/Users/vishaal/.gemini/antigravity/scratch/dashboard.html")
with open(output_path, "w") as f:
    f.write(html_content)

brain_dashboard = Path("/Users/vishaal/.gemini/antigravity/brain/45547b13-905e-46ad-835f-c9e939cfee67/dashboard.html")
with open(brain_dashboard, "w") as f:
    f.write(html_content)

print(f"Generated High-Voltage Electricity AMOLED Dashboard at {output_path} ({len(html_content)} bytes)")
