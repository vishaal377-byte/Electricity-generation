"""
Natural language prompt parser for the Electricity Demand Agent.
Extracts countries, country groups, target years, and scenario factors from user prompts.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple
from .config import COUNTRY_GROUPS, DEFAULT_BASE_YEAR


class PromptParser:
    """Parses user prompts to extract query intent, target countries, years, and scenario factors."""

    def __init__(self, all_countries: List[str]):
        self.all_countries = all_countries
        self._country_lookup = {c.lower(): c for c in all_countries}

    def parse(self, prompt: str) -> Dict[str, Any]:
        """
        Parses free-form user prompt into structured parameters:
        - countries: list of identified country names
        - group: identified country group (e.g. 'G7', 'BRICS')
        - target_year: extracted target year (2024-2050, default 2024)
        - gdp_growth_pct: extracted GDP adjustment %
        - re_expansion_pct: extracted renewable expansion %
        - energy_growth_pct: extracted primary energy shift %
        - pop_growth_pct: extracted population shift %
        - electrification_target_pct: extracted electrification target %
        """
        text = prompt.strip()
        text_lower = text.lower()

        # 1. Extract Target Year (2020-2050)
        year_match = re.search(r"\b(20[2-5][0-9])\b", text)
        target_year = int(year_match.group(1)) if year_match else DEFAULT_BASE_YEAR

        # 2. Extract Predefined Groups
        matched_group = None
        for group_name in COUNTRY_GROUPS.keys():
            gn_clean = group_name.lower().replace("_", " ")
            if (
                re.search(rf"\b{re.escape(gn_clean)}\b", text_lower)
                or re.search(rf"\b{re.escape(group_name.lower())}\b", text_lower)
                or (group_name == "EU_TOP" and re.search(r"\beu\b|europe", text_lower))
                or (group_name == "LATAM_TOP" and re.search(r"latin america|latam", text_lower))
                or (group_name == "ASIA_PACIFIC" and re.search(r"asia|asia pacific", text_lower))
            ):
                matched_group = group_name
                break

        # 3. Extract Country Names
        detected_countries: Set[str] = set()

        # Check group members first if group is present
        if matched_group:
            for c in COUNTRY_GROUPS[matched_group]:
                detected_countries.add(c)

        # Check against full country list
        for c_lower, c_orig in self._country_lookup.items():
            # word boundary match to avoid partial false matches
            pattern = rf"\b{re.escape(c_lower)}\b"
            if re.search(pattern, text_lower):
                detected_countries.add(c_orig)

        # Common aliases
        aliases = {
            "usa": "United States",
            "us": "United States",
            "america": "United States",
            "uk": "United Kingdom",
            "britain": "United Kingdom",
            "uae": "United Arab Emirates",
            "russia": "Russia",
            "south korea": "South Korea",
            "korea": "South Korea",
        }
        for alias, c_orig in aliases.items():
            if re.search(rf"\b{alias}\b", text_lower):
                if c_orig in self._country_lookup.values():
                    detected_countries.add(c_orig)

        # Default to G7 or India if no countries/groups specified
        if not detected_countries and not matched_group:
            detected_countries.add("India")

        # 4. Extract Scenario Factors (e.g. "+15% GDP", "20% renewable", "double renewables")
        gdp_growth = 0.0
        gdp_match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%\s*(?:higher|more|growth)?\s*gdp", text_lower) or \
                    re.search(r"gdp\s*(?:growth|increase|change)?\s*(?:of|by)?\s*([+-]?\d+(?:\.\d+)?)\s*%", text_lower)
        if gdp_match:
            gdp_growth = float(gdp_match.group(1))

        re_expansion = 0.0
        re_match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%\s*(?:more|expansion|increase)?\s*(?:renewable|re|solar|clean)", text_lower) or \
                   re.search(r"(?:renewable|re|solar|clean)\s*(?:expansion|growth|increase)?\s*(?:of|by)?\s*([+-]?\d+(?:\.\d+)?)\s*%", text_lower)
        if re_match:
            re_expansion = float(re_match.group(1))
        elif "double renewable" in text_lower or "double re" in text_lower:
            re_expansion = 100.0

        energy_growth = 0.0
        pe_match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%\s*(?:primary\s+)?energy", text_lower) or \
                   re.search(r"energy\s*(?:growth|change)?\s*(?:of|by)?\s*([+-]?\d+(?:\.\d+)?)\s*%", text_lower)
        if pe_match:
            energy_growth = float(pe_match.group(1))

        pop_growth = 0.0
        pop_match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%\s*population", text_lower) or \
                    re.search(r"population\s*(?:growth|change)?\s*(?:of|by)?\s*([+-]?\d+(?:\.\d+)?)\s*%", text_lower)
        if pop_match:
            pop_growth = float(pop_match.group(1))

        elec_target = None
        elec_match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:electrification|electricity access)", text_lower)
        if elec_match:
            elec_target = float(elec_match.group(1))

        return {
            "raw_prompt": text,
            "target_year": target_year,
            "group": matched_group,
            "countries": sorted(list(detected_countries)),
            "gdp_growth_pct": gdp_growth,
            "re_expansion_pct": re_expansion,
            "energy_growth_pct": energy_growth,
            "pop_growth_pct": pop_growth,
            "electrification_target_pct": elec_target,
        }
