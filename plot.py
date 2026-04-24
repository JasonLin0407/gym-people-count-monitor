import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time")

# 7 天資料
latest = df["time"].max()
df = df[df["time"] >= latest - pd.Timedelta(days=7)]

plt.figure(figsize=(12,5))
plt.plot(df["time"], df["current"])
plt.title("Gym Occupancy - Last 7 Days")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("plot.png")
