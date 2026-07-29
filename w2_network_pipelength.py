import pandas as pd

df = pd.read_csv("pipelines_uncoordinated_fixedsinks.csv")

avg_length = (df["length_km"].sum())/61.0

df["multiplier"] = df["length_km"]/avg_length

df.to_csv("uncoordinated_multipliers.csv")
