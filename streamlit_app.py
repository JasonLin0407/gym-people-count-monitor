import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🏋️ NTU Gym Attendance Dashboard")

# ======================
# 讀資料
# ======================
df = pd.read_csv("data.csv")
df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time")
df["date"] = df["time"].dt.date
df["hour"] = df["time"].dt.hour
df["day"] = df["time"].dt.day_name()

# ======================
# 1️⃣ TODAY vs HISTORICAL HOURLY
# ======================
st.header("📈 Today's Attendance")

latest_date = df["date"].max()

df_today = df[df["date"] == latest_date]
df_hist = df[df["date"] != latest_date]

# historical hourly average
hourly_avg = df_hist.groupby("hour")["current"].mean()

fig, ax = plt.subplots(figsize=(12, 5), dpi=300)

# ---- Today line ----
ax.plot(
    df_today["time"],
    df_today["current"],
    marker="o", color="darkorange",
    label="Today", linewidth = 3
)

# ---- Historical hourly pattern (mapped to today's timeline) ----
hist_times = pd.to_datetime(str(latest_date)) + pd.to_timedelta(hourly_avg.index, unit="h")

ax.plot(
    hist_times,
    hourly_avg.values,
    label="Historical Avg (Hourly)",
    color="silver", linewidth = 3
)

ax.set_xlabel("Time", fontsize=12)
ax.set_ylabel("People", fontsize=12)
ax.set_title("Today vs Historical Pattern", fontsize=16)

plt.xticks(rotation=45)
ax.legend()

st.pyplot(fig)

# ======================
# 2️⃣ WEEKLY HEATMAP
# ======================
st.header("📊 Historical Attendance Heatmap")

df["day"] = df["time"].dt.day_name()
df["hour"] = df["time"].dt.hour

pivot = df.pivot_table(
    values="current",
    index="day",
    columns="hour",
    aggfunc="mean"
)

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex(order)

fig2, ax2 = plt.subplots(figsize=(12, 5), dpi=300)

sns.heatmap(pivot, cmap="YlOrRd", ax=ax2, annot=True)

ax2.set_title("Average Occupancy by Day & Hour")
ax2.set_ylabel("")

st.pyplot(fig2)
