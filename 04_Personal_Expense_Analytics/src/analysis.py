import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data/personal_expenses.csv", parse_dates=["date"])

category = df.groupby("category").agg(
    transactions=("amount","count"),
    total_spend=("amount","sum"),
    average_spend=("amount","mean")
).sort_values("total_spend", ascending=False)
category.to_csv(OUT / "category_summary.csv")

method = df.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
method.to_csv(OUT / "payment_method_summary.csv", header=["total_spend"])

need_want = df.groupby("need_or_want")["amount"].sum()
need_want.to_csv(OUT / "need_vs_want.csv", header=["total_spend"])

plt.figure(figsize=(9,5))
category["total_spend"].sort_values().plot(kind="barh")
plt.title("Monthly Spending by Category")
plt.xlabel("Spend")
plt.tight_layout()
plt.savefig(OUT / "spending_by_category.png", dpi=180)
plt.close()

plt.figure(figsize=(7,5))
need_want.plot(kind="pie", autopct="%1.1f%%")
plt.title("Needs vs Wants")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "needs_vs_wants.png", dpi=180)
plt.close()

print("PERSONAL EXPENSE ANALYTICS")
print(category.round(2))
print("\nTotal spending:", round(df["amount"].sum(), 2))
print("Average transaction:", round(df["amount"].mean(), 2))
