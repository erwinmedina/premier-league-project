# ----------------------------------------------------------------------- #
# Summary:
# ----------------------------------------------------------------------- #
# This file was created to normalize all player names [or majority]. Foreign
# players have accents, or special characters not found in the english 
# language. By replacing them with their english counterpart, i'm able
# to connect this player info dataset with the master dataset.

import pandas as pd
import unicodedata

# Mapping special characters into english.
mapping = {
    "ø": "o", "Ø": "O",
    "æ": "ae", "Æ": "Ae",
    "å": "a", "Å": "A",
    "œ": "oe", "Œ": "Oe"
}

# Strips and handles special characters
def remove_accents(text):
    
    # Only looks at strings.
    if isinstance(text, str):  

        # Step 1: normalize and remove combining accents
        normalized = ''.join(
            c for c in unicodedata.normalize('NFKD', text)
            if not unicodedata.combining(c)
        )
        
        # Step 2: replace special characters
        return ''.join(mapping.get(c, c) for c in normalized)
    
    return text

# Input and output file names
input_file = "Player Information.xlsx"
output_file = "Revised_PlayerInformation.xlsx"
df = pd.read_excel(input_file)

# Apply transformation
df["Corrected Name"] = df["Corrected Name"].apply(remove_accents)

# Saves our file! :D
df.to_excel(output_file, index=False)
print(f"Finished! Cleaned file is complete!")
