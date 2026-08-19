#!/usr/bin/env python3
"""Validate company_profile.json before a grant search run.

Exits non-zero with a readable message if the profile is malformed or
still has unfilled placeholders, so a bad edit fails loudly instead of
silently producing empty digests.
"""

import json
import pathlib
import sys

PROFILE = pathlib.Path(__file__).parent / "company_profile.json"

REQUIRED = [
    "company_name",
    "org_type",
    "mission_summary",
    "focus_areas",
    "home_base",
    "service_areas",
    "grant_types",
]


def main():
    try:
        profile = json.loads(PROFILE.read_text())
    except FileNotFoundError:
        sys.exit(f"error: {PROFILE} not found")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {PROFILE.name} is not valid JSON — {exc}")

    problems = []

    for key in REQUIRED:
        if key not in profile:
            problems.append(f"missing required field: {key}")

    for key in ("focus_areas", "service_areas", "grant_types"):
        value = profile.get(key)
        if key in profile and (not isinstance(value, list) or not value):
            problems.append(f"{key} must be a non-empty list")

    home_base = profile.get("home_base")
    if "home_base" in profile:
        if not isinstance(home_base, dict):
            problems.append("home_base must be an object")
        else:
            for key in ("country", "state_or_region", "city"):
                if not home_base.get(key):
                    problems.append(f"home_base.{key} is empty")

    # Catch placeholders left over from the template, at any nesting depth.
    def find_placeholders(node, path="profile"):
        if isinstance(node, str) and node.startswith("REPLACE_"):
            problems.append(f"unfilled placeholder at {path}: {node}")
        elif isinstance(node, dict):
            for key, value in node.items():
                find_placeholders(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                find_placeholders(value, f"{path}[{index}]")

    find_placeholders(profile)

    # These get pasted straight into web search queries.
    for index, area in enumerate(profile.get("service_areas", [])):
        if isinstance(area, str) and "_" in area:
            problems.append(
                f"service_areas[{index}] contains underscores ({area!r}); "
                "use natural text so web searches match"
            )

    if problems:
        sys.exit("profile invalid:\n  - " + "\n  - ".join(problems))

    print(f"profile OK: {profile['company_name']} ({profile['org_type']})")


if __name__ == "__main__":
    main()
