"""
Generate ultra-modern AMOLED Dark/Light mode dashboard with future year forecasting.
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
  <title>⚡ Electricity Demand Intelligent Agent — Future Forecasting</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* AMOLED & Modern Aesthetics */
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
      --slider-bg: #e2e8f0;
      --glow: transparent;
    }}

    html.dark {{
      --bg: #000000;
      --card-bg: #08080a;
      --card-border: #18181c;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --accent-cyan: #00f0ff;
      --accent-emerald: #00ff9f;
      --accent-purple: #b026ff;
      --accent-amber: #ffb703;
      --slider-bg: #1f1f26;
      --glow: rgba(0, 240, 255, 0.15);
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    .amoled-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    html.dark .amoled-card:hover {{
      border-color: #2a2a32;
    }}

    .glow-cyan {{
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }}

    /* Custom range slider */
    input[type=range] {{
      -webkit-appearance: none;
      background: var(--slider-bg);
      border-radius: 9999px;
    }}

    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      height: 16px;
      width: 16px;
      border-radius: 50%;
      background: var(--accent-cyan);
      cursor: pointer;
      box-shadow: 0 0 8px var(--accent-cyan);
      transition: transform 0.1s ease;
    }}

    input[type=range]::-webkit-slider-thumb:hover {{
      transform: scale(1.2);
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(150, 150, 150, 0.25); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(150, 150, 150, 0.45); }}
  </style>
</head>
<body class="antialiased p-3 sm:p-5 lg:p-7 min-h-screen font-sans">
  <div class="max-w-[1440px] mx-auto space-y-6">

    <!-- Top Navigation / Header -->
    <header class="amoled-card rounded-2xl p-5 sm:p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-cyan-500 to-emerald-400 flex items-center justify-center text-black font-black text-xl shadow-md">
          ⚡
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl sm:text-2xl font-bold tracking-tight">Electricity Demand Agent</h1>
            <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Future Forecasting 2024–2050
            </span>
          </div>
          <p class="text-xs text-[var(--text-muted)] mt-0.5">
            Machine Learning Model strictly trained on 80% data & tested on 20% holdout (R²: 0.9979, MAE: 4.31 TWh)
          </p>
        </div>
      </div>

      <!-- Controls: Theme Toggle & Export -->
      <div class="flex items-center gap-3 self-stretch md:self-auto justify-end">
        <button onclick="toggleTheme()" id="theme-btn"
          class="px-3.5 py-2 rounded-xl border border-[var(--card-border)] bg-[var(--card-bg)] text-xs font-semibold hover:border-cyan-500/50 transition-all flex items-center gap-2 shadow-sm">
          <span id="theme-icon">🌙</span>
          <span id="theme-text">AMOLED</span>
        </button>

        <button onclick="exportCSV()"
          class="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 text-black font-semibold text-xs hover:opacity-95 active:scale-95 transition-all flex items-center gap-1.5 shadow-md">
          <span>📥</span> Export CSV
        </button>
      </div>
    </header>

    <!-- FUTURE YEAR SELECTOR BAR (HERO COMPONENT) -->
    <section class="amoled-card rounded-2xl p-5 shadow-sm border border-cyan-500/25 relative overflow-hidden">
      <div class="absolute -right-16 -top-16 w-48 h-48 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-lg">🔮</span>
            <h2 class="text-base font-bold tracking-tight">Target Forecast Year: <span id="display-target-year" class="text-cyan-400 text-xl font-extrabold">2030</span></h2>
          </div>
          <p class="text-xs text-[var(--text-muted)] mt-0.5">
            Select or type any year from 2024 to 2050 to forecast electricity consumption for selected countries.
          </p>
        </div>

        <!-- Quick Year Jump Pills -->
        <div class="flex flex-wrap items-center gap-1.5" id="year-pills">
          <button onclick="setYear(2024)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2024">2024 (Baseline)</button>
          <button onclick="setYear(2026)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2026">2026</button>
          <button onclick="setYear(2030)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-cyan-500 bg-cyan-500/15 text-cyan-400 font-bold transition-all" data-yr="2030">2030 (Agenda)</button>
          <button onclick="setYear(2035)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2035">2035</button>
          <button onclick="setYear(2040)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2040">2040</button>
          <button onclick="setYear(2050)" class="year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all" data-yr="2050">2050 (Net-Zero)</button>
        </div>
      </div>

      <!-- Year Slider Control -->
      <div class="mt-4 pt-4 border-t border-[var(--card-border)] flex flex-col sm:flex-row items-center gap-4">
        <span class="text-xs font-mono text-[var(--text-muted)]">2024</span>
        <input type="range" id="slider-target-year" min="2024" max="2050" value="2030" step="1"
          class="w-full h-2 rounded-lg cursor-pointer" oninput="onYearSliderChange(this.value)">
        <span class="text-xs font-mono text-[var(--text-muted)]">2050</span>

        <div class="flex items-center gap-1.5 self-end sm:self-auto shrink-0">
          <span class="text-xs text-[var(--text-muted)]">Exact:</span>
          <input type="number" id="input-target-year" min="2024" max="2050" value="2030"
            class="w-18 px-2 py-1 text-xs rounded-lg border border-[var(--card-border)] bg-[var(--card-bg)] text-cyan-400 font-bold font-mono focus:outline-none focus:ring-1 focus:ring-cyan-500 text-center"
            onchange="setYear(parseInt(this.value))">
        </div>
      </div>
    </section>

    <!-- Main Workspace Grid: Controls (4 cols) & Visuals/Table (8 cols) -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- LEFT SIDEBAR: Clusters, Factors, Filters -->
      <aside class="lg:col-span-4 space-y-5">

        <!-- Country Bunches / Clusters -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1.5">
              <span>🌍</span> Country Bunches
            </h3>
            <span id="selected-badge" class="text-[11px] px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 font-bold border border-cyan-500/20">
              7 selected
            </span>
          </div>
          <div class="grid grid-cols-2 gap-2" id="cluster-buttons">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- What-If Policy Sliders -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1.5">
              <span>⚙️</span> What-If Scenario Overrides
            </h3>
            <button onclick="resetSliders()" class="text-xs text-[var(--text-muted)] hover:text-cyan-400 transition-colors underline">
              Reset
            </button>
          </div>

          <!-- Slider 1: GDP Growth Adjustment -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[var(--text-muted)]">GDP Annual Growth Δ</span>
              <span id="val-gdp" class="font-mono font-bold text-cyan-400">+0.0%</span>
            </div>
            <input type="range" id="slider-gdp" min="-15" max="30" value="0" step="0.5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 2: Renewable Energy Expansion -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[var(--text-muted)]">Renewable Expansion Δ</span>
              <span id="val-re" class="font-mono font-bold text-emerald-400">+0%</span>
            </div>
            <input type="range" id="slider-re" min="0" max="150" value="0" step="5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 3: Primary Energy Demand Shift -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[var(--text-muted)]">Primary Energy Shift Δ</span>
              <span id="val-energy" class="font-mono font-bold text-amber-400">+0%</span>
            </div>
            <input type="range" id="slider-energy" min="-25" max="40" value="0" step="1"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 4: Population Growth Shift -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[var(--text-muted)]">Population Growth Δ</span>
              <span id="val-pop" class="font-mono font-bold text-purple-400">+0%</span>
            </div>
            <input type="range" id="slider-pop" min="-10" max="25" value="0" step="1"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>

          <!-- Slider 5: Electrification Rate Minimum -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs">
              <span class="font-medium text-[var(--text-muted)]">Target Electrification Access</span>
              <span id="val-elec" class="font-mono font-bold text-teal-400">Default</span>
            </div>
            <input type="range" id="slider-elec" min="0" max="100" value="0" step="5"
              class="w-full h-1.5" oninput="updateSimulation()">
          </div>
        </div>

        <!-- Individual Country Selector with Search -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">
              📋 Country Selector
            </h3>
            <div class="space-x-2 text-xs">
              <button onclick="selectAll(true)" class="text-cyan-400 hover:underline">Select All</button>
              <span class="text-[var(--text-muted)]">|</span>
              <button onclick="selectAll(false)" class="text-[var(--text-muted)] hover:underline">Clear</button>
            </div>
          </div>
          <input type="text" id="country-search" placeholder="Search 218 countries (e.g. India, USA, France)..."
            class="w-full px-3 py-2 text-xs rounded-xl border border-[var(--card-border)] bg-[var(--card-bg)] text-[var(--text)] focus:outline-none focus:border-cyan-500"
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
          <div class="amoled-card rounded-2xl p-5 relative overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-20 h-20 bg-cyan-500/10 rounded-full blur-xl pointer-events-none"></div>
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">Forecasted Demand (<span class="year-label font-bold text-cyan-400">2030</span>)</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-total-demand" class="text-3xl sm:text-4xl font-black tracking-tight text-cyan-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)]">TWh</span>
            </div>
            <p id="kpi-demand-delta" class="text-xs mt-1.5 font-semibold text-emerald-400 font-mono">+0.0% vs baseline</p>
          </div>

          <!-- KPI 2 -->
          <div class="amoled-card rounded-2xl p-5 relative overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-20 h-20 bg-purple-500/10 rounded-full blur-xl pointer-events-none"></div>
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">Avg Per-Capita Demand</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-per-capita" class="text-3xl sm:text-4xl font-black tracking-tight text-purple-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)]">kWh/person</span>
            </div>
            <p id="kpi-population" class="text-xs mt-1.5 text-[var(--text-muted)] font-mono">Projected for 0M people</p>
          </div>

          <!-- KPI 3 -->
          <div class="amoled-card rounded-2xl p-5 relative overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-20 h-20 bg-emerald-500/10 rounded-full blur-xl pointer-events-none"></div>
            <p class="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">Projected RE Capacity</p>
            <div class="flex items-baseline gap-2 mt-1.5">
              <span id="kpi-re-cap" class="text-3xl sm:text-4xl font-black tracking-tight text-emerald-400 font-mono">0</span>
              <span class="text-xs font-bold text-[var(--text-muted)]">GW</span>
            </div>
            <p id="kpi-country-count" class="text-xs mt-1.5 text-[var(--text-muted)] font-mono">Across 0 countries</p>
          </div>
        </div>

        <!-- Trajectory Timeline Visualizer (2024 to 2050) -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold flex items-center gap-2">
                <span>📈</span> Future Trajectory Pathway (2024 — 2050)
              </h3>
              <p class="text-xs text-[var(--text-muted)]">Combined projected electricity requirements (TWh) over time</p>
            </div>
            <div class="flex items-center gap-3 text-xs font-mono">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block"></span> Baseline Path</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span> Scenario Path</span>
            </div>
          </div>

          <!-- Responsive SVG Trajectory Chart -->
          <div class="w-full h-48 sm:h-56 pt-2" id="trajectory-chart-container">
            <!-- Injected by JS -->
          </div>
        </div>

        <!-- Comparative Country Breakdown Bars -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold flex items-center gap-2">
              <span>⚡</span> Country Forecast Rankings in <span class="year-label text-cyan-400">2030</span>
            </h3>
            <span class="text-xs text-[var(--text-muted)]">Electricity needed (TWh)</span>
          </div>
          <div id="chart-bars" class="space-y-3 max-h-72 overflow-y-auto pr-1">
            <!-- Dynamic country bars injected here -->
          </div>
        </div>

        <!-- Comprehensive Country Forecast Table -->
        <div class="amoled-card rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h3 class="text-sm font-bold flex items-center gap-2">
              <span>📊</span> Detailed Forecast Table (<span class="year-label text-cyan-400">2030</span>)
            </h3>
            <span class="text-xs text-[var(--text-muted)]" id="table-row-count">Showing 7 countries</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-[var(--card-border)] text-[var(--text-muted)] uppercase tracking-wider font-semibold">
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
    // Embedded Data Bundle
    const DATA = {json_str};

    let targetYear = 2030;
    let selectedCountryNames = new Set(DATA.groups.G7 || ["United States", "China", "India"]);
    let currentResults = [];

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
      updateSimulation(); // redraw SVG charts with theme colors
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

      // Update pill styling
      document.querySelectorAll(".year-pill").forEach(pill => {{
        const pyr = parseInt(pill.getAttribute("data-yr"));
        if (pyr === targetYear) {{
          pill.className = "year-pill px-3 py-1 rounded-lg text-xs font-bold border border-cyan-500 bg-cyan-500/15 text-cyan-400 transition-all";
        }} else {{
          pill.className = "year-pill px-3 py-1 rounded-lg text-xs font-semibold border border-[var(--card-border)] hover:border-cyan-500/50 transition-all";
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
      btn.className = `px-3 py-2 text-xs font-semibold rounded-xl border transition-all text-center ${{
        idx === 0
          ? "border-cyan-500 bg-cyan-500/15 text-cyan-400 font-bold"
          : "border-[var(--card-border)] hover:border-cyan-500/50 text-[var(--text)]"
      }}`;
      btn.innerText = gKey.replace("_", " ");
      btn.onclick = () => selectCluster(gKey, btn);
      clusterContainer.appendChild(btn);
    }});

    function selectCluster(gKey, activeBtn) {{
      document.querySelectorAll("#cluster-buttons button").forEach(b => {{
        b.className = "px-3 py-2 text-xs font-semibold rounded-xl border border-[var(--card-border)] hover:border-cyan-500/50 text-[var(--text)] text-center";
      }});
      if (activeBtn) {{
        activeBtn.className = "px-3 py-2 text-xs font-bold rounded-xl border border-cyan-500 bg-cyan-500/15 text-cyan-400 text-center";
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
          span.className = "font-medium text-[var(--text)]";
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

    // Future Simulation & Prediction Engine
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

        // Future Growth Dynamics (Compound extrapolation over dt years)
        const effectivePopCAGR = cagr.pop_cagr + (popShift / 100) * 0.01;
        const effectiveGDPCAGR = cagr.gdp_cagr + (gdpShift / 100) * 0.01;
        const effectivePECAGR = cagr.pe_cagr + (energyShift / 100) * 0.01;

        const pop = c.population * Math.pow(1 + effectivePopCAGR, dt);
        const gdp = c.gdp * Math.pow(1 + effectiveGDPCAGR, dt);
        const pe = c.primary_energy * Math.pow(1 + effectivePECAGR, dt);
        const reAdd = (cagr.re_add_mw_per_year * (1 + reExp / 100)) * dt;
        const reCap = c.re_capacity_mw + Math.max(0, reAdd);

        // ML Demand Response: primary energy elasticity (~0.94) + GDP elasticity (~0.08)
        let growthMultiplier = Math.pow(1 + effectivePECAGR, dt * 0.94) * Math.pow(1 + effectiveGDPCAGR, dt * 0.08);

        // Electrification boost if target access set
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

    // Render Future Trajectory Chart (2024 to 2050)
    function renderTrajectoryChart(selected) {{
      const container = document.getElementById("trajectory-chart-container");
      if (selected.length === 0) {{
        container.innerHTML = '<div class="h-full flex items-center justify-center text-xs text-[var(--text-muted)]">Select at least one country to view trajectory.</div>';
        return;
      }}

      const years = [2024, 2026, 2028, 2030, 2035, 2040, 2050];
      const gdpShift = parseFloat(document.getElementById("slider-gdp").value);
      const energyShift = parseFloat(document.getElementById("slider-energy").value);

      // Calculate baseline and scenario points
      const baselinePoints = [];
      const scenarioPoints = [];

      years.forEach(yr => {{
        const dt = yr - 2024;
        let baseSum = 0;
        let scenSum = 0;

        selected.forEach(c => {{
          const cagr = c.cagr || {{ pop_cagr: 0.008, gdp_cagr: 0.025, pe_cagr: 0.015 }};
          const bDem = c.baseline_demand_twh;

          // Baseline path
          const baseMult = Math.pow(1 + cagr.pe_cagr, dt * 0.94) * Math.pow(1 + cagr.gdp_cagr, dt * 0.08);
          baseSum += bDem * baseMult;

          // Scenario path
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

      // Build SVG
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
          <!-- Grid Lines -->
          ${{[0.25, 0.5, 0.75, 1.0].map(pct => {{
            const yv = minVal + pct * (maxVal - minVal);
            const ypos = getY(yv);
            return `
              <line x1="${{padL}}" y1="${{ypos}}" x2="${{w - padR}}" y2="${{ypos}}" stroke="currentColor" stroke-opacity="0.08" stroke-dasharray="4,4"/>
              <text x="${{padL - 8}}" y="${{ypos + 4}}" fill="currentColor" fill-opacity="0.4" font-size="10" font-family="monospace" text-anchor="end">${{Math.round(yv).toLocaleString()}}</text>
            `;
          }}).join("")}}

          <!-- Year Axis Labels -->
          ${{years.map(yr => `
            <text x="${{getX(yr)}}" y="${{h - 10}}" fill="currentColor" fill-opacity="0.5" font-size="10" font-family="monospace" text-anchor="middle">${{yr}}</text>
          `).join("")}}

          <!-- Baseline Curve -->
          <path d="${{baseD}}" fill="none" stroke="#00f0ff" stroke-width="2.5" stroke-dasharray="6,4" opacity="0.8"/>

          <!-- Scenario Curve -->
          <path d="${{scenD}}" fill="none" stroke="#00ff9f" stroke-width="3"/>

          <!-- Target Year Indicator Line -->
          <line x1="${{targetX}}" y1="${{padT}}" x2="${{targetX}}" y2="${{h - padB}}" stroke="#00f0ff" stroke-width="1.5" stroke-dasharray="2,2"/>
          <circle cx="${{targetX}}" cy="${{getY(scenarioPoints.find(p => p.year === targetYear)?.val || scenarioPoints[0].val)}}" r="5" fill="#00ff9f" stroke="#000000" stroke-width="2"/>
        </svg>
      `;
    }}

    function renderBars(items) {{
      const container = document.getElementById("chart-bars");
      container.innerHTML = "";
      if (items.length === 0) {{
        container.innerHTML = '<div class="text-xs text-[var(--text-muted)] py-4 text-center">No countries selected.</div>';
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
        note.className = "text-center text-xs text-[var(--text-muted)] pt-1";
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

    // Initialization
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

# Also copy to brain artifact directory
brain_dashboard = Path("/Users/vishaal/.gemini/antigravity/brain/45547b13-905e-46ad-835f-c9e939cfee67/dashboard.html")
with open(brain_dashboard, "w") as f:
    f.write(html_content)

print(f"Generated AMOLED dashboard at {output_path} ({len(html_content)} bytes)")
