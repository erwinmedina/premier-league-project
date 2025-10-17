import pandas as pd
import ast

confederations = ["AFC", "CAF", "CONMEBOL", "CONCACAF", "OFC", "UEFA"]
df = pd.read_excel("Output_Incidents_Federations.xlsx")

def count_federations(fed_list_str):
    if isinstance(fed_list_str, str):
        try:
            fed_list = ast.literal_eval(fed_list_str)
        except:
            fed_list = []
    elif isinstance(fed_list_str, list):
        fed_list = fed_list_str
    else:
        fed_list = []

    counts = {fed: fed_list.count(fed) for fed in confederations}
    return pd.Series(counts)

federation_counts = df["Federations"].apply(count_federations)

df = pd.concat([df, federation_counts], axis=1)
output_path = "incidents_with_federation_counts.xlsx"
df.to_excel(output_path, index=False)