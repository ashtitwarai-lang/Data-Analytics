import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data/social_media_data.csv", parse_dates=["date"])
df["engagements"] = df["likes"] + df["comments"] + df["shares"]
df["engagement_rate_%"] = (df["engagements"] / df["reach"] * 100).round(2)
df["reach_rate_%"] = (df["reach"] / df["impressions"] * 100).round(2)

summary = df.groupby("platform").agg(
    posts=("platform","size"),
    impressions=("impressions","sum"),
    reach=("reach","sum"),
    engagements=("engagements","sum"),
    avg_engagement_rate=("engagement_rate_%","mean")
).sort_values("reach", ascending=False)
summary.to_csv(OUT / "platform_summary.csv")

plt.figure(figsize=(9,5))
summary["reach"].sort_values().plot(kind="barh")
plt.title("Total Reach by Platform")
plt.xlabel("Reach")
plt.tight_layout()
plt.savefig(OUT / "reach_by_platform.png", dpi=180)
plt.close()

content = df.groupby("content_type")["engagement_rate_%"].mean().sort_values()
plt.figure(figsize=(9,5))
content.plot(kind="bar")
plt.title("Average Engagement Rate by Content Type")
plt.ylabel("Engagement Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "engagement_by_content.png", dpi=180)
plt.close()

print("SOCIAL MEDIA REACH ANALYSIS")
print(summary.round(2))
