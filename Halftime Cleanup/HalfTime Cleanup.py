# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file simply iterates through a list of incidents in an excel file.
# At each iteration, it breaks up the string into an array.
# For each item in that array, we parse the time to see if any goals were
# scored before the 15 minute mark, and before the half time mark.

import os
import ast
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "input_HT_incidents_AllYears.xlsx")
output_file = os.path.join(script_dir, "output_HT_incidents_AllYears.xlsx")
df = pd.read_excel(input_file)

# Name of header column i'm looking for
EVENTS_COL = "Inc"

# function that converts item in incident report string into int. 
# example: "45+2' Goal_Home - Erwin Medina (Penalty)" ==> 45. 
# basically ignores stoppage time
def parse_time(event: str) -> int:
    try:
        time_part = event.split("'")[0]
        if "+" in time_part:
            base, _ = time_part.split("+")
            return int(base)  # ignore stoppage time
        return int(time_part)
    except:
        return None


def analyze_events(cell):
    # Checks if any info was missing, replaces it with defaults
    if pd.isna(cell):
        return None, False, False, 0, 0 
    
    # Convert the incident report string into a list.
    try:
        events = ast.literal_eval(cell)  
    except:
        return cell, False, False, 0, 0

    # This is what we initialize / start off with.
    h_15 = False
    a_15 = False
    ht_h_score = 0
    ht_a_score = 0

    # Iterate through each row in the dataset
    for e in events:

        # Note: Penalties were counted as "Goal_Home/Away - {Player} (Penalty)"
        # If there were goals:
        if "Goal_Home" in e or "Goal_Away" in e or "Own_Home" in e or "Own_Away" in e:
            minute = parse_time(e)
            if minute is None:
                continue

            # Goals before 15'
            if ("Goal_Home" in e or "Own_Home" in e) and minute <= 15:
                h_15 = True
            if ("Goal_Away" in e or "Own_Away" in e) and minute <= 15:
                a_15 = True

            # Half-time goals (<= 45)
            if minute <= 45:
                if "Goal_Home" in e or "Own_Home" in e:
                    ht_h_score += 1
                elif "Goal_Away" in e or "Own_Away" in e:
                    ht_a_score += 1

    return events, h_15, a_15, ht_h_score, ht_a_score

# Apply the analyze_events function to each row
df[["Incident", "H_15", "A_15", "HT_H_Score", "HT_A_Score"]] = df[EVENTS_COL].apply(
    lambda x: pd.Series(analyze_events(x))
)

# Save our results.
df.to_excel(output_file, index=False)