#!/usr/bin/env python3

# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file just counts all yellows and red cards in an incident report

import pandas as pd
import ast
from collections import Counter
import sys
import os

def parse_incidents(cell):
    if isinstance(cell, list):
        return cell
    if isinstance(cell, str):
        try:
            return ast.literal_eval(cell)
        except Exception:
            return []
    return []


def count_cards(events):

    # initialize counts
    counts = {
        "H_Yellow_Card": 0,
        "A_Yellow_Card": 0,
        "H_Red_Card": 0,
        "A_Red_Card": 0,
    }

    yellow_tracker = {"home": Counter(), "away": Counter()}

    for event in events:
        event_lower = event.lower()

        # direct reds
        if any(tag in event_lower for tag in ["red_home", "red_card_home"]):
            counts["H_Red_Card"] += 1
        elif any(tag in event_lower for tag in ["red_away", "red_card_away"]):
            counts["A_Red_Card"] += 1

        # yellows
        elif "yellow_home" in event_lower or "yellow_away" in event_lower:
            parts = event.split(" - ")
            if len(parts) > 1:
                player = parts[1].strip()
                if "yellow_home" in event_lower:
                    yellow_tracker["home"][player] += 1
                else:
                    yellow_tracker["away"][player] += 1

    # count second yellows; add to red totals
    for player, count in yellow_tracker["home"].items():
        counts["H_Yellow_Card"] += count
        if count >= 2:
            counts["H_Red_Card"] += 1

    for player, count in yellow_tracker["away"].items():
        counts["A_Yellow_Card"] += count
        if count >= 2:
            counts["A_Red_Card"] += 1

    return counts


def process_excel(infile, outfile):
    df = pd.read_excel(infile, dtype=str)

    results = []
    for _, row in df.iterrows():
        events = parse_incidents(row["INC"])
        counts = count_cards(events)
        results.append(counts)

    # merge the results into the dataframe
    counts_df = pd.DataFrame(results)
    df = pd.concat([df, counts_df], axis=1)

    df.to_excel(outfile, index=False)
    print(f"Output file is ready to roll, see: {outfile}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 '/Users/erwinmedina/code/finalproject/Incidents Cleanup/Incidents - YellowRed Cleanup - All/CardCounter.py' full_data_v4.xlsm full_data_v4_revisedCards.xlsx")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    process_excel(infile, outfile)
