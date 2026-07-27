import pandas as pd
import numpy as np

df = pd.read_csv("Newphase_nonopt_w1_1_nodes.csv")

target = df[(df["tech"] == "capture") & (df["stage"] == "approval")]

total_delay = target.groupby("project")["delay"].mean()
total_delay = total_delay.sort_values(ascending=True)

pd.DataFrame(total_delay).to_csv("Newphase_nonopt_capture_delays_w11.csv")

