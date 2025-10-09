# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file was created to clean up the incidents reports. What that means
# is that it was meant to do the following:
# - Remove all instances of 'sub' or 'substitution'
# - Remove all unknowns labeled as 'Other - ...'
# - Remove all double parentheses (should only be single like: (...), not ((...))
# - Fix or adjust the white space.
# However, this file wasn't 'removing', simply going through each item and
# ignoring anything that fit the above criteria.

import pandas as pd
import ast
import re

# Load your Excel file
df = pd.read_excel("output_incidents_random.xlsx")
# df = pd.read_excel("output_incidents_2002-2003.xlsx")
# df = pd.read_excel("output_incidents_2003-2004.xlsx")
# df = pd.read_excel("output_incidents_2004-2005.xlsx")
# df = pd.read_excel("output_incidents_2005-2006.xlsx")
# df = pd.read_excel("output_incidents_2006-2007.xlsx")
# df = pd.read_excel("output_incidents_2007-2008.xlsx")
# df = pd.read_excel("output_incidents_2008-2009.xlsx")
# df = pd.read_excel("output_incidents_2009-2010.xlsx")
# df = pd.read_excel("output_incidents_2010-2011.xlsx")
# df = pd.read_excel("output_incidents_2011-2012.xlsx")
# df = pd.read_excel("output_incidents_2012-2013.xlsx")
# df = pd.read_excel("output_incidents_2013-2014.xlsx")
# df = pd.read_excel("output_incidents_2014-2015.xlsx")
# df = pd.read_excel("output_incidents_2015-2016.xlsx")
# df = pd.read_excel("output_incidents_2016-2017.xlsx")
# df = pd.read_excel("output_incidents_2017-2018.xlsx")
# df = pd.read_excel("output_incidents_2018-2019.xlsx")
# df = pd.read_excel("output_incidents_2019-2020.xlsx")
# df = pd.read_excel("output_incidents_2020-2021.xlsx")
# df = pd.read_excel("output_incidents_2021-2022.xlsx")
# df = pd.read_excel("output_incidents_2022-2023.xlsx")
# df = pd.read_excel("output_incidents_2023-2024.xlsx")
# df = pd.read_excel("output_incidents_2024-2025.xlsx")

def clean_events(cell):
    # Checks if anything in the row was left blank.
    if pd.isna(cell):
        return cell, None
    
    try:
        events = ast.literal_eval(cell)
        cleaned_events = []
        error_flag = None

        for e in events:
            # Normalize double parentheses into single parentheses
            e = re.sub(r"\(\(\s*(.*?)\s*\)\)", r"(\1)", e)

            # Skip unwanted substitutions/other events
            if any(skip in e for skip in ["Sub_Home", "Sub_Away", "Other_Home", "Other_Away", "Substitution"]):
                continue

            # Check for missing player name (e.g., ends with "- ")
            # This was designed to flag incident reports that didn't respond well to the scraping
            if e.strip().endswith("-"):
                error_flag = "Error"

            cleaned_events.append(e)

        return cleaned_events, error_flag

    except Exception:
        return cell, "Error"  # mark parsing failures as errors

# Apply the function to get both cleaned events and error flag
df[["Cleaned_Events", "Error"]] = df["events"].apply(
    lambda x: pd.Series(clean_events(x))
)

# Keep id, original, cleaned, error
cleaned_df = df[["id", "events", "Cleaned_Events", "Error"]]

# Save back to Excel
cleaned_df.to_excel("cleaned_file_random.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2002-2003.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2003-2004.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2004-2005.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2005-2006.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2006-2007.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2007-2008.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2008-2009.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2009-2010.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2010-2011.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2011-2012.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2012-2013.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2013-2014.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2014-2015.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2015-2016.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2016-2017.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2017-2018.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2018-2019.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2019-2020.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2020-2021.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2021-2022.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2022-2023.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2023-2024.xlsx", index=False)
# cleaned_df.to_excel("cleaned_file_2024-2025.xlsx", index=False)
