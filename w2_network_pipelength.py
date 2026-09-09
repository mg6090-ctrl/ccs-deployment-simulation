import pandas as pd

df = pd.read_csv("uncoordinated_sequential_pipelines.csv")

avg_length = (df["length_km"].sum())/49.0

df["multiplier"] = df["length_km"]/avg_length

df.to_csv("uncoordinated_multipliers.csv")

UNCOORD_PIPE_MULT = {
    "projT" + str(serial): ratio
    for serial, ratio in zip(df["source_id"], df["multiplier"])
}

PROJECTS 