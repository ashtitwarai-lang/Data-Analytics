import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data/inventory_data.csv")
df["stock_value"] = df["current_stock"] * df["unit_cost"]
df["days_of_stock"] = (df["current_stock"] / df["monthly_demand"].replace(0,1) * 30).round(1)

def classify(r):
    if r.current_stock <= r.reorder_level:
        return "REORDER"
    if r.current_stock > r.max_stock * 0.85:
        return "OVERSTOCK"
    return "NORMAL"

df["status"] = df.apply(classify, axis=1)

audit = df.groupby("category").agg(
    skus=("sku","count"),
    stock_units=("current_stock","sum"),
    stock_value=("stock_value","sum"),
    monthly_demand=("monthly_demand","sum")
)
audit["inventory_turnover_est"] = (
    audit["monthly_demand"] / audit["stock_units"].replace(0,1)
).round(2)
audit.to_csv(OUT / "category_audit.csv")

df[df["status"]=="REORDER"].sort_values("stock_value", ascending=False).to_csv(
    OUT / "reorder_list.csv", index=False
)

plt.figure(figsize=(9,5))
audit["stock_value"].sort_values().plot(kind="barh")
plt.title("Inventory Value by Category")
plt.xlabel("Inventory Value")
plt.tight_layout()
plt.savefig(OUT / "inventory_value_by_category.png", dpi=180)
plt.close()

plt.figure(figsize=(7,5))
df["status"].value_counts().plot(kind="bar")
plt.title("Inventory Status")
plt.ylabel("Number of SKUs")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "inventory_status.png", dpi=180)
plt.close()

print("INVENTORY STOCK LEVEL AUDIT")
print(audit.round(2))
print("\nSKUs requiring reorder:", (df["status"]=="REORDER").sum())
