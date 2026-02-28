#!/usr/bin/env python3
"""
Update food preferences after a search session.
Appends/updates entries in references/preferences.md.

Usage:
    python3 update_prefs.py --cuisine "Japanese" --location "Shibuya" \\
        --chosen "Ichiran Ramen" --party-size 2 --budget "1500-2000"
"""

import argparse
import os
import re
from datetime import date

PREFS_PATH = os.path.expanduser(
    "~/.claude/skills/cfo/references/preferences.md"
)


def read_prefs():
    if os.path.exists(PREFS_PATH):
        with open(PREFS_PATH, "r") as f:
            return f.read()
    return ""


def write_prefs(content):
    with open(PREFS_PATH, "w") as f:
        f.write(content)


def update_cuisine(content, cuisine):
    today = date.today().isoformat()
    entry = f"- {cuisine} (ordered {today})"

    # Check if cuisine already exists
    pattern = re.compile(
        rf"^- {re.escape(cuisine)}.*$", re.MULTILINE | re.IGNORECASE
    )
    match = pattern.search(content)
    if match:
        # Update the existing entry with new date
        content = pattern.sub(
            f"- {cuisine} (high preference, last ordered {today})", content
        )
    else:
        # Add after "## Cuisine Preferences" section
        marker = "## Cuisine Preferences"
        if marker in content:
            idx = content.index(marker) + len(marker)
            # Find end of line
            newline_idx = content.index("\n", idx)
            content = content[: newline_idx + 1] + entry + "\n" + content[newline_idx + 1 :]
    return content


def update_location(content, location):
    # Check if location already listed
    if location.lower() not in content.lower():
        marker = "## Locations"
        if marker in content:
            idx = content.index(marker) + len(marker)
            newline_idx = content.index("\n", idx)
            content = (
                content[: newline_idx + 1]
                + f"- {location}\n"
                + content[newline_idx + 1 :]
            )
    return content


def update_order_history(content, restaurant, cuisine):
    today = date.today().isoformat()
    new_row = f"| {today} | {restaurant} | {cuisine} | - | Auto-logged |"

    # Add to order history table
    marker = "## Order History"
    if marker in content:
        # Find the last line of the table
        lines = content.split("\n")
        insert_idx = None
        in_history = False
        for i, line in enumerate(lines):
            if "## Order History" in line:
                in_history = True
            elif in_history and line.startswith("|"):
                insert_idx = i + 1
            elif in_history and not line.startswith("|") and line.strip():
                break

        if insert_idx:
            lines.insert(insert_idx, new_row)
            content = "\n".join(lines)
    return content


def update_favorites(content, restaurant, location, cuisine):
    entry = f"- {restaurant} ({location}) — {cuisine}"
    if restaurant.lower() not in content.lower():
        marker = "## Favorites"
        if marker in content:
            idx = content.index(marker) + len(marker)
            newline_idx = content.index("\n", idx)
            content = (
                content[: newline_idx + 1]
                + entry + "\n"
                + content[newline_idx + 1 :]
            )
    return content


def main():
    parser = argparse.ArgumentParser(description="Update food preferences")
    parser.add_argument("--cuisine", help="Cuisine searched for")
    parser.add_argument("--location", help="Delivery location")
    parser.add_argument("--chosen", help="Restaurant chosen (if any)")
    parser.add_argument("--party-size", type=int, help="Party size")
    parser.add_argument("--budget", help="Budget range")
    args = parser.parse_args()

    content = read_prefs()

    if args.cuisine:
        content = update_cuisine(content, args.cuisine)

    if args.location:
        content = update_location(content, args.location)

    if args.chosen and args.cuisine:
        content = update_order_history(content, args.chosen, args.cuisine)
        location = args.location or "unknown"
        content = update_favorites(content, args.chosen, location, args.cuisine)

    write_prefs(content)
    print(f"Preferences updated: cuisine={args.cuisine}, location={args.location}, chosen={args.chosen}")


if __name__ == "__main__":
    main()
