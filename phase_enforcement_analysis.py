import pandas as pd
import numpy as np

df = pd.read_csv("DACphase_nonopt_w1_2_nodes.csv")

target = df[(df["tech"] == "capture") & (df["stage"] == "approval")]

total_delay = target.groupby("project")["delay"].mean()
total_delay = total_delay.sort_values(ascending=True)

# pd.DataFrame(total_delay).to_csv("Newphase_nonopt_capture_delays_w11.csv")

com_time_by_tech = df[(df["tech"]=="capture") & (df["stage"]=="commissioning") & (df["abandoned"]==False)]
com_time_by_tech = com_time_by_tech.groupby("project_type")["finish_year"].mean()
com_time_by_tech = com_time_by_tech.sort_values(ascending=True)

pd.DataFrame(com_time_by_tech).to_csv("w12_avg_com_time_by_projType.csv")