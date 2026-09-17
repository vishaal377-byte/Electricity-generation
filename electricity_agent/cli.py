"""
Command-Line Interface and interactive agent for the Electricity Demand system.
Supports future year forecasting (2024-2050) and scenario simulations.
"""

import argparse
import sys
from typing import List, Optional
from tabulate import tabulate

from .agent import ElectricityDemandAgent
from .config import COUNTRY_GROUPS, DEFAULT_BASE_YEAR


def format_number(val: float, precision: int = 2) -> str:
    return f"{val:,.{precision}f}"


def print_banner():
    banner = """
========================================================================
   ⚡ ELECTRICITY DEMAND INTELLIGENT AGENT (ML-TRAINED SYSTEM) ⚡
   Predicting Electricity Requirements & Future Projections (2024-2050)
========================================================================
"""
    print(banner)


def handle_calculate(agent: ElectricityDemandAgent, args):
    try:
        overrides = {}
        if args.gdp is not None:
            overrides["gdp"] = args.gdp
        if args.population is not None:
            overrides["population"] = args.population
        if args.re_capacity is not None:
            overrides["Total_RE_Capacity_MW_current"] = args.re_capacity
        if args.electrification is not None:
            overrides["electricity_access_pct"] = args.electrification

        target_year = args.year or DEFAULT_BASE_YEAR

        res = agent.calculate_country(
            args.country,
            target_year=target_year,
            factors_override=overrides if overrides else None,
        )

        print(f"\n⚡ Electricity Demand Forecast: {res['country']} ({res['iso_code']}) — Year {res['target_year']}")
        print("-" * 70)
        print(f"• Baseline Historical (2022/24): {format_number(res['actual_demand_historical_twh'])} TWh")
        print(f"• ML Model Forecast ({target_year}):       {format_number(res['predicted_demand_twh'])} TWh")
        if res["delta_twh"] != 0:
            print(f"• Scenario Delta:             {res['delta_twh']:+,.2f} TWh ({res['delta_pct']:+.1f}%)")
        print(f"• Electricity Per Capita:     {format_number(res['per_capita_kwh'], 1)} kWh/person")
        print(f"• Projected RE Capacity:      {format_number(res['total_re_capacity_mw'], 1)} MW")
        print(f"• Projected RE Gen Share:     {res['re_generation_share_pct']:.1f}%")
        print(f"• Capacity vs Gen Gap:        {res['capacity_generation_gap_pct']:.1f}%")
        print("-" * 70)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_bunch(agent: ElectricityDemandAgent, args):
    try:
        targets = args.group or args.countries
        if not targets:
            print("❌ Please specify either --group (e.g. G7, BRICS) or --countries (e.g. 'India,Japan')")
            return

        target_year = args.year or DEFAULT_BASE_YEAR
        res = agent.calculate_bunch(targets, target_year=target_year)

        print(f"\n⚡ Batch Electricity Forecast: {res['group_name']} ({res['country_count']} countries) — Year {res['target_year']}")
        print("=" * 80)

        headers = [
            "Country", "ISO3", f"Forecast {target_year} (TWh)", "Per Capita (kWh)",
            "RE Cap (MW)", "RE Gen Share (%)"
        ]
        table_rows = []
        for c in res["countries"]:
            table_rows.append([
                c["country"],
                c["iso_code"],
                format_number(c["predicted_demand_twh"]),
                format_number(c["per_capita_kwh"], 1),
                format_number(c["total_re_capacity_mw"], 1),
                f"{c['re_generation_share_pct']:.1f}%"
            ])

        print(tabulate(table_rows, headers=headers, tablefmt="rounded_grid"))
        print("-" * 80)
        print(f"Total Electricity Needed for Group ({target_year}): {format_number(res['total_electricity_needed_twh'])} TWh")
        if res["not_found_countries"]:
            print(f"⚠️ Countries not found: {', '.join(res['not_found_countries'])}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_trajectory(agent: ElectricityDemandAgent, args):
    try:
        targets = args.group or args.countries or args.country
        if not targets:
            print("❌ Please specify --country, --group, or --countries")
            return

        start_yr = args.start_year or 2024
        end_yr = args.end_year or 2035
        step = args.step or 1

        res = agent.forecast_trajectory(targets, start_year=start_yr, end_year=end_yr, step=step)
        print(f"\n⚡ Electricity Trajectory Forecast ({start_yr} - {end_yr})")
        print("=" * 70)

        headers = ["Year", "Total TWh"] + [c for c in res["countries"][:5]]
        table_rows = []
        for point in res["trajectory"]:
            row = [point["year"], format_number(point["total_twh"])]
            for c in res["countries"][:5]:
                val = point["country_demands"].get(c, 0.0)
                row.append(format_number(val))
            table_rows.append(row)

        print(tabulate(table_rows, headers=headers, tablefmt="rounded_grid"))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_scenario(agent: ElectricityDemandAgent, args):
    try:
        targets = args.group or args.countries
        if not targets:
            print("❌ Please specify either --group or --countries")
            return

        target_year = args.year or DEFAULT_BASE_YEAR

        res = agent.simulate_scenario(
            targets,
            target_year=target_year,
            gdp_growth_pct=args.gdp_growth,
            pop_growth_pct=args.pop_growth,
            primary_energy_growth_pct=args.energy_growth,
            re_capacity_expansion_pct=args.re_expansion,
            target_electrification_pct=args.electrification_target,
        )

        print(f"\n⚡ Policy & Growth Scenario Simulation: {res['group_name']} — Target Year {res['target_year']}")
        print("Parameters applied:")
        print(f"  • GDP Growth:               {args.gdp_growth:+.1f}%")
        print(f"  • Population Growth:        {args.pop_growth:+.1f}%")
        print(f"  • Primary Energy Growth:    {args.energy_growth:+.1f}%")
        print(f"  • Renewable Expansion:      {args.re_expansion:+.1f}%")
        if args.electrification_target:
            print(f"  • Electrification Target:   {args.electrification_target:.1f}%")
        print("=" * 85)

        headers = [
            "Country", "ISO3", f"Baseline {target_year} (TWh)", f"Scenario {target_year} (TWh)",
            "Delta (TWh)", "Change (%)", "Per Capita (kWh)"
        ]
        table_rows = []
        for c in res["countries"]:
            table_rows.append([
                c["country"],
                c["iso_code"],
                format_number(c["baseline_twh"]),
                format_number(c["scenario_twh"]),
                f"{c['delta_twh']:+,.2f}",
                f"{c['delta_pct']:+.1f}%",
                format_number(c["per_capita_kwh"], 1)
            ])

        print(tabulate(table_rows, headers=headers, tablefmt="rounded_grid"))
        print("-" * 85)
        print(f"Combined Baseline: {format_number(res['total_baseline_twh'])} TWh")
        print(f"Combined Scenario: {format_number(res['total_scenario_twh'])} TWh")
        print(f"Net Change:        {res['total_delta_twh']:+,.2f} TWh ({res['total_delta_pct']:+.2f}%)")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_explain(agent: ElectricityDemandAgent, args):
    try:
        target_year = args.year or DEFAULT_BASE_YEAR
        res = agent.explain_country_factors(args.country, target_year=target_year)
        print(f"\n🔍 Factor Attribution & Sensitivity for {res['country']} ({target_year})")
        print(f"Predicted Electricity Demand: {format_number(res['predicted_demand_twh'])} TWh")
        print("=" * 75)

        headers = ["Factor", "Current/Projected Value", "+10% Shock Delta (TWh)", "Global Importance"]
        table_rows = []
        for factor, data in res["factor_sensitivities"].items():
            table_rows.append([
                factor,
                format_number(data["current_value"]),
                f"{data['sensitivity_impact_twh']:+,.4f}",
                f"{data['global_importance']:.4f}"
            ])

        print(tabulate(table_rows, headers=headers, tablefmt="rounded_grid"))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def interactive_mode(agent: ElectricityDemandAgent):
    print_banner()
    print("Welcome to the Interactive Electricity Agent REPL.")
    print("Commands:")
    print("  1. calc <country> [year]           - Calculate electricity (e.g. 'calc India 2030')")
    print("  2. bunch <group> [year]            - Calculate for a bunch (e.g. 'bunch G7 2035')")
    print("  3. sim <group> <year> <gdp%> <re%> - Run scenario for future year")
    print("  4. traj <country|group> [end_year] - View year-by-year trajectory (e.g. 'traj BRICS 2040')")
    print("  5. explain <country> [year]        - View factor sensitivities")
    print("  6. groups                          - List supported country groups")
    print("  7. exit / quit                     - Exit agent\n")

    while True:
        try:
            line = input("⚡ agent> ").strip()
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].lower()

            if cmd in ["exit", "quit"]:
                print("Goodbye!")
                break
            elif cmd == "groups":
                for g, clist in COUNTRY_GROUPS.items():
                    print(f"  • {g:15s}: {', '.join(clist)}")
            elif cmd == "calc":
                if len(parts) < 2:
                    print("Usage: calc <country> [year]")
                    continue
                cname = parts[1]
                yr = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else DEFAULT_BASE_YEAR
                res = agent.calculate_country(cname, target_year=yr)
                print(f"➡️ {res['country']} ({yr}): {res['predicted_demand_twh']} TWh ({res['per_capita_kwh']} kWh/person)")
            elif cmd == "bunch":
                if len(parts) < 2:
                    print("Usage: bunch <group_name or countries> [year]")
                    continue
                target = parts[1]
                yr = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else DEFAULT_BASE_YEAR
                res = agent.calculate_bunch(target, target_year=yr)
                print(f"➡️ {res['group_name']} ({yr}): Total {res['total_electricity_needed_twh']} TWh across {res['country_count']} countries.")
            elif cmd == "traj":
                if len(parts) < 2:
                    print("Usage: traj <country|group> [end_year]")
                    continue
                target = parts[1]
                end_yr = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 2035
                res = agent.forecast_trajectory(target, start_year=2024, end_year=end_yr)
                print(f"➡️ Trajectory for {target} (2024 to {end_yr}):")
                for p in res["trajectory"][::2]:  # every 2 years
                    print(f"   {p['year']}: {p['total_twh']:,.1f} TWh")
            elif cmd == "sim":
                if len(parts) < 5:
                    print("Usage: sim <group> <year> <gdp_growth_pct> <re_expansion_pct>")
                    continue
                grp, yr, gdp_g, re_g = parts[1], int(parts[2]), float(parts[3]), float(parts[4])
                res = agent.simulate_scenario(grp, target_year=yr, gdp_growth_pct=gdp_g, re_capacity_expansion_pct=re_g)
                print(f"➡️ {res['group_name']} ({yr}) Scenario: {res['total_baseline_twh']} TWh -> {res['total_scenario_twh']} TWh ({res['total_delta_pct']:+.1f}%)")
            elif cmd == "explain":
                if len(parts) < 2:
                    print("Usage: explain <country> [year]")
                    continue
                cname = parts[1]
                yr = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else DEFAULT_BASE_YEAR
                res = agent.explain_country_factors(cname, target_year=yr)
                top_3 = list(res["factor_sensitivities"].items())[:3]
                print(f"➡️ Top drivers for {res['country']} in {yr}:")
                for f, d in top_3:
                    print(f"   - {f}: impact {d['sensitivity_impact_twh']:+,.4f} TWh (Importance: {d['global_importance']:.4f})")
            else:
                print("Unknown command. Try: calc, bunch, sim, traj, explain, groups, exit")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as err:
            print(f"⚠️ Error: {err}")


def main():
    parser = argparse.ArgumentParser(
        description="Electricity Demand Intelligent Agent (ML-Trained System with Future Forecasting)"
    )
    subparsers = parser.add_subparsers(dest="command")

    # calculate
    calc_parser = subparsers.add_parser("calculate", help="Calculate electricity for a single country")
    calc_parser.add_argument("--country", "-c", required=True, help="Country name or ISO3 code")
    calc_parser.add_argument("--year", "-y", type=int, default=DEFAULT_BASE_YEAR, help="Target year (2024-2050)")
    calc_parser.add_argument("--gdp", type=float, help="Override GDP in USD")
    calc_parser.add_argument("--population", type=float, help="Override population")
    calc_parser.add_argument("--re-capacity", type=float, help="Override Total RE Capacity (MW)")
    calc_parser.add_argument("--electrification", type=float, help="Override electrification access %")

    # bunch
    bunch_parser = subparsers.add_parser("bunch", help="Calculate electricity for a group of countries")
    bunch_parser.add_argument("--group", "-g", help="Predefined group (G7, BRICS, EU_TOP, LATAM_TOP, etc.)")
    bunch_parser.add_argument("--countries", help="Comma-separated country names or ISO codes")
    bunch_parser.add_argument("--year", "-y", type=int, default=DEFAULT_BASE_YEAR, help="Target year (2024-2050)")

    # trajectory
    traj_parser = subparsers.add_parser("trajectory", help="Forecast annual trajectory across multiple years")
    traj_parser.add_argument("--country", "-c", help="Country name")
    traj_parser.add_argument("--group", "-g", help="Predefined group")
    traj_parser.add_argument("--countries", help="Comma-separated countries")
    traj_parser.add_argument("--start-year", type=int, default=2024, help="Start year (default 2024)")
    traj_parser.add_argument("--end-year", type=int, default=2035, help="End year (default 2035)")
    traj_parser.add_argument("--step", type=int, default=1, help="Year step (default 1)")

    # scenario
    scen_parser = subparsers.add_parser("scenario", help="Simulate what-if policy scenarios")
    scen_parser.add_argument("--group", "-g", help="Predefined group")
    scen_parser.add_argument("--countries", help="Comma-separated countries")
    scen_parser.add_argument("--year", "-y", type=int, default=DEFAULT_BASE_YEAR, help="Target year (2024-2050)")
    scen_parser.add_argument("--gdp-growth", type=float, default=0.0, help="GDP growth %")
    scen_parser.add_argument("--pop-growth", type=float, default=0.0, help="Population growth %")
    scen_parser.add_argument("--energy-growth", type=float, default=0.0, help="Primary energy growth %")
    scen_parser.add_argument("--re-expansion", type=float, default=0.0, help="Renewable capacity expansion %")
    scen_parser.add_argument("--electrification-target", type=float, default=None, help="Target electrification %")

    # explain
    explain_parser = subparsers.add_parser("explain", help="Explain factor influence for a country")
    explain_parser.add_argument("--country", "-c", required=True, help="Country name or ISO code")
    explain_parser.add_argument("--year", "-y", type=int, default=DEFAULT_BASE_YEAR, help="Target year")

    # groups
    subparsers.add_parser("list-groups", help="List predefined country groups")

    # prompt (natural language)
    prompt_cmd = subparsers.add_parser("prompt", help="Ask a question or scenario in plain English")
    prompt_cmd.add_argument("query", nargs="+", help="Natural language prompt")

    # interactive
    subparsers.add_parser("interactive", help="Start interactive agent REPL")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    agent = ElectricityDemandAgent()

    if args.command == "prompt":
        user_query = " ".join(args.query)
        res = agent.answer_prompt(user_query)
        print(f"\n💬 Query: \"{user_query}\"")
        print("=" * 80)
        print(f"🤖 Agent Response:\n{res['answer']}\n")
        headers = ["Country", "ISO3", f"Demand {res['target_year']} (TWh)", "Delta (TWh)", "Per Capita (kWh)"]
        rows = [
            [c["country"], c["iso_code"], format_number(c["scenario_twh"]), f"{c['delta_twh']:+,.2f}", format_number(c["per_capita_kwh"], 1)]
            for c in res["country_breakdown"]
        ]
        print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))
        print("-" * 80)
        print(f"Total Forecasted: {format_number(res['total_demand_twh'])} TWh")

    elif args.command == "calculate":
        handle_calculate(agent, args)
    elif args.command == "bunch":
        handle_bunch(agent, args)
    elif args.command == "trajectory":
        handle_trajectory(agent, args)
    elif args.command == "scenario":
        handle_scenario(agent, args)
    elif args.command == "explain":
        handle_explain(agent, args)
    elif args.command == "list-groups":
        print("\nPre-configured Country Groups:")
        for g, clist in COUNTRY_GROUPS.items():
            print(f"• {g:15s}: {', '.join(clist)}")
    elif args.command == "interactive":
        interactive_mode(agent)


if __name__ == "__main__":
    main()
