import pandas as pd
import ast
import re

incidents_df = pd.read_excel("full_data_v5.xlsx")
players_df = pd.read_excel("Player Information v3.xlsx")
players_df["Corrected Name"] = players_df["Corrected Name"].str.strip()

card_pattern = re.compile(r"(Yellow|Red)[_\w]*\s*-\s*(.+)")

players_found_list = []
federations_list = []

for cell in incidents_df["INC"]:
    if pd.isna(cell):
        players_found_list.append([])
        federations_list.append([])
        continue
    try:
        incidents = ast.literal_eval(cell) # String to List
    except Exception:
        players_found_list.append([])
        federations_list.append([])
        continue

    player_names = []

    for incident in incidents:
        match = card_pattern.search(incident)
        if match:
            player_name = match.group(2).strip()
            player_name = re.sub(r"\(.*?\)", "", player_name).strip()
            player_names.append(player_name)

    unique_players = list(set(player_names))

    federations = []
    for name in unique_players:
        match = players_df.loc[players_df["Corrected Name"] == name, "Federation"]
        if not match.empty:
            federations.append(match.values[0])
        else:
            federations.append("Unknown")

    players_found_list.append(unique_players)
    federations_list.append(federations)

incidents_df["Players Found"] = players_found_list
incidents_df["Federations"] = federations_list
output_path = "output_incidents_with_federations.xlsx"
incidents_df.to_excel(output_path, index=False)