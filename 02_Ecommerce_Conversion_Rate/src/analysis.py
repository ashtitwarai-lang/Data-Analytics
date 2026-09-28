import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data/ecommerce_sessions.csv", parse_dates=["date"])
df["conversion_rate_%"] = (df["purchases"] / df["visitors"] * 100).round(2)
df["cart_rate_%"] = (df["add_to_cart"] / df["visitors"] * 100).round(2)
df["checkout_rate_%"] = (df["checkouts"] / df["add_to_cart"].replace(0,1) * 100).round(2)
df["aov"] = (df["revenue"] / df["purchases"].replace(0,1)).round(2)

source = df.groupby("traffic_source").agg(
    visitors=("visitors","sum"),
    purchases=("purchases","sum"),
    revenue=("revenue","sum")
)
source["conversion_rate_%"] = (source["purchases"] / source["visitors"] * 100).round(2)
source["aov"] = (source["revenue"] / source["purchases"].replace(0,1)).round(2)
source = source.sort_values("conversion_rate_%", ascending=False)
source.to_csv(OUT / "traffic_source_summary.csv")

device = df.groupby("device").agg(
    visitors=("visitors","sum"),
    purchases=("purchases","sum"),
    revenue=("revenue","sum")
)
device["conversion_rate_%"] = (device["purchases"] / device["visitors"] * 100).round(2)
device.to_csv(OUT / "device_summary.csv")

plt.figure(figsize=(9,5))
source["conversion_rate_%"].sort_values().plot(kind="barh")
plt.title("Conversion Rate by Traffic Source")
plt.xlabel("Conversion Rate (%)")
plt.tight_layout()
plt.savefig(OUT / "conversion_by_source.png", dpi=180)
plt.close()

plt.figure(figsize=(8,5))
device["conversion_rate_%"].plot(kind="bar")
plt.title("Conversion Rate by Device")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "conversion_by_device.png", dpi=180)
plt.close()

print("E-COMMERCE CONVERSION RATE ANALYSIS")
print(source.round(2))
