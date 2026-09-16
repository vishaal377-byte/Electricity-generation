"""
Command-Line Interface and interactive agent for the Electricity Demand system.
"""

import argparse
import sys
from typing import List, Optional
from tabulate import tabulate

from .agent import ElectricityDemandAgent
from .config import COUNTRY_GROUPS


def format_number(val: float, precision: int = 2) -> str:
    return f"{val:,.{precision}f}"


def print_banner():
    banner = """
========================================================================
   ⚡ ELECTRICITY DEMAND INTELLIGENT AGENT (ML-TRAINED SYSTEM) ⚡
   Data Sources: Cleaned IRENA/IMF Transition Dataset & OWID History
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

        res = agent.calculate_country(
            args.country, factors_override=overrides if overrides else None
        )

        print(f"\n⚡ Electricity Demand Analysis for {res['country']} ({res['iso_code']})")
        print("-" * 65)
        print(f"• Baseline Historical Demand: {format_number(res['actual_demand_twh'])} TWh")
        print(f"• ML Model Predicted Demand:  {format_number(res['predicted_demand_twh'])} TWh")
        if res["delta_twh"] != 0:
            print(f"• Scenario Delta:             {res['delta_twh']:+,.2f} TWh ({res['delta_pct']:+.1f}%)")
        print(f"• Electricity Per Capita:     {format_number(res['per_capita_kwh'], 1)} kWh/person")
        print(f"• Installed RE Capacity:      {format_number(res['total_re_capacity_mw'], 1)} MW")
        print(f"• RE Generation Share:        {res['re_generation_share_pct']:.1f}%")
        print(f"• Capacity vs Gen Gap:        {res['capacity_generation_gap_pct']:.1f}%")
        print("-" * 65)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_bunch(agent: ElectricityDemandAgent, args):
    try:
        targets = args.group or args.countries
        if not targets:
            print("❌ Please specify either --group (e.g. G7, BRICS) or --countries (e.g. 'India,Japan')")
            return

        res = agent.calculate_bunch(targets)
        print(f"\n⚡ Batch Electricity Calculation: {res['group_name']} ({res['country_count']} countries)")
        print("=" * 80)

        headers = [
            "Country", "ISO3", "Pred Demand (TWh)", "Per Capita (kWh)",
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
        print(f"Total Electricity Needed for Group: {format_number(res['total_electricity_needed_twh'])} TWh")
        if res["not_found_countries"]:
            print(f"⚠️ Countries not found: {', '.join(res['not_found_countries'])}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)


def handle_scenario(agent: ElectricityDemandAgent, args):
    try:
        targets = args.group or args.countries
        if not targets:
            print("❌ Please specify either --group or --countries")
            return

        res = agent.simulate_scenario(
            targets,
            gdp_growth_pct=args.gdp_growth,
            pop_growth_pct=args.pop_growth,
            primary_energy_growth_pct=args.energy_growth,
            re_capacity_expansion_pct=args.re_expansion,
            target_electrification_pct=args.electrification_target,
        )

        print(f"\n⚡ Policy & Growth Scenario Simulation: {res['group_name']}")
        print("Parameters applied:")
        print(f"  • GDP Growth:               {args.gdp_growth:+.1f}%")
        print(f"  • Population Growth:        {args.pop_growth:+.1f}%")
        print(f"  • Primary Energy Growth:    {args.energy_growth:+.1f}%")
        print(f"  • Renewable Expansion:      {args.re_expansion:+.1f}%")
        if args.electrification_target:
            print(f"  • Electrification Target:   {args.electrification_target:.1f}%")
        print("=" * 85)

        headers = [
            "Country", "ISO3", "Baseline (TWh)", "Scenario (TWh)",
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
        res = agent.explain_country_factors(args.country)
        print(f"\n🔍 Factor Attribution & Sensitivity for {res['country']}")
        print(f"Predicted Electricity Demand: {format_number(res['predicted_demand_twh'])} TWh")
        print("=" * 75)

        headers = ["Factor", "Current Value", "+10% Shock Delta (TWh)", "Global Importance"]
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
    print("  1. calc <country>                 - Calculate electricity for a country")
    print("  2. bunch <group|country,country>  - Calculate electricity for a bunch of countries")
    print("  3. sim <group> <gdp%> <re%>       - Run scenario with GDP growth% and RE expansion%")
    print("  4. explain <country>              - View factor sensitivities")
    print("  5. groups                         - List supported country groups")
    print("  6. exit / quit                    - Exit agent\n")

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
                    print("Usage: calc <country>")
                    continue
                cname = " ".join(parts[1:])
                res = agent.calculate_country(cname)
                print(f"➡️ {res['country']}: {res['predicted_demand_twh']} TWh ({res['per_capita_kwh']} kWh/person)")
            elif cmd == "bunch":
                if len(parts) < 2:
                    print("Usage: bunch <group_name or comma_separated_countries>")
                    continue
                target = parts[1]
                res = agent.calculate_bunch(target)
                print(f"➡️ {res['group_name']}: Total {res['total_electricity_needed_twh']} TWh across {res['country_count']} countries.")
            elif cmd == "sim":
                if len(parts) < 4:
                    print("Usage: sim <group> <gdp_growth_pct> <re_expansion_pct>")
                    continue
                grp, gdp_g, re_g = parts[1], float(parts[2]), float(parts[3])
                res = agent.simulate_scenario(grp, gdp_growth_pct=gdp_g, re_capacity_expansion_pct=re_g)
                print(f"➡️ {res['group_name']} Scenario: {res['total_baseline_twh']} TWh -> {res['total_scenario_twh']} TWh ({res['total_delta_pct']:+.1f}%)")
            elif cmd == "explain":
                if len(parts) < 2:
                    print("Usage: explain <country>")
                    continue
                cname = " ".join(parts[1:])
                res = agent.explain_country_factors(cname)
                top_3 = list(res["factor_sensitivities"].items())[:3]
                print(f"➡️ Top drivers for {res['country']}:")
                for f, d in top_3:
                    print(f"   - {f}: impact {d['sensitivity_impact_twh']:+,.4f} TWh (Global Importance: {d['global_importance']:.4f})")
            else:
                print("Unknown command. Try: calc, bunch, sim, explain, groups, exit")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as err:
            print(f"⚠️ Error: {err}")


def main():
    parser = argparse.ArgumentParser(
        description="Electricity Demand Intelligent Agent (ML-Trained System)"
    )
    subparsers = parser.add_subparsers(dest="command")

    # calculate
    calc_parser = subparsers.add_parser("calculate", help="Calculate electricity for a single country")
    calc_parser.add_argument("--country", "-c", required=True, help="Country name or ISO3 code")
    calc_parser.add_argument("--gdp", type=float, help="Override GDP in USD")
    calc_parser.add_argument("--population", type=float, help="Override population")
    calc_parser.add_argument("--re-capacity", type=float, help="Override Total RE Capacity (MW)")
    calc_parser.add_argument("--electrification", type=float, help="Override electrification access %")

    # bunch
    bunch_parser = subparsers.add_parser("bunch", help="Calculate electricity for a group of countries")
    bunch_parser.add_argument("--group", "-g", help="Predefined group (G7, BRICS, EU_TOP, LATAM_TOP, etc.)")
    bunch_parser.add_argument("--countries", help="Comma-separated country names or ISO codes")

    # scenario
    scen_parser = subparsers.add_parser("scenario", help="Simulate what-if policy scenarios")
    scen_parser.add_argument("--group", "-g", help="Predefined group")
    scen_parser.add_argument("--countries", help="Comma-separated countries")
    scen_parser.add_argument("--gdp-growth", type=float, default=0.0, help="GDP growth %")
    scen_parser.add_argument("--pop-growth", type=float, default=0.0, help="Population growth %")
    scen_parser.add_argument("--energy-growth", type=float, default=0.0, help="Primary energy growth %")
    scen_parser.add_argument("--re-expansion", type=float, default=0.0, help="Renewable capacity expansion %")
    scen_parser.add_argument("--electrification-target", type=float, default=None, help="Target electrification access %")

    # explain
    explain_parser = subparsers.add_parser("explain", help="Explain factor influence for a country")
    explain_parser.add_argument("--country", "-c", required=True, help="Country name or ISO code")

    # groups
    subparsers.add_parser("list-groups", help="List predefined country groups")

    # interactive
    subparsers.add_parser("interactive", help="Start interactive agent REPL")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    agent = ElectricityDemandAgent()

    if args.command == "calculate":
        handle_calculate(agent, args)
    elif args.command == "bunch":
        handle_bunch(agent, args)
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
