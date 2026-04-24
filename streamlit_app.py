import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🏋️ Gym Occupancy Dashboard")

# ======================
# 讀資料
# ======================
df = pd.read_csv("data.csv")
df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time")

# ======================
# 過去 7 天
# ======================
latest = df["time"].max()
df_7d = df[df["time"] >= latest - pd.Timedelta(days=7)]

st.header("📈 Last 7 Days")

fig, ax = plt.subplots(figsize=(12, 5), dpi = 300)
ax.plot(df_7d["time"], df_7d["current"], marker = 'o')
labfs = 12; tfs = 16
ax.set_xlabel("Time", fontsize = labfs)
ax.set_ylabel("People", fontsize = labfs)
ax.set_title("Occupancy (Last 7 Days)", fontsize = tfs)
plt.xticks(rotation=45)

st.pyplot(fig)

# ======================
# 每天 × 每小時平均
# ======================
st.header("📊 Weekly Pattern")

df["day"] = df["time"].dt.day_name()
df["hour"] = df["time"].dt.hour

pivot = df.pivot_table(
    values="current",
    index="day",
    columns="hour",
    aggfunc="mean"
)

# 排序星期
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex(order)

fig2, ax2 = plt.subplots(figsize=(12, 5), dpi = 300)
sns.heatmap(pivot, cmap="YlOrRd", ax=ax2, annot=True)

ax2.set_title("Average Occupancy by Day & Hour")
ax2.set_ylabel('')

st.pyplot(fig2)
