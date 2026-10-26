"""
AI Time-Audit — demo analysis script
Run: python demo.py
Requires: pandas, matplotlib
IMPORTANT: included CSV values are illustrative; replace with measured data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
data = ROOT / "data" / "time_and_quality_data.csv"
df = pd.read_csv(data)

required = {"task", "manual_minutes", "ai_assisted_minutes",
            "manual_quality_1_to_5", "ai_quality_1_to_5"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
if (df["manual_minutes"] <= 0).any() or (df["ai_assisted_minutes"] < 0).any():
    raise ValueError("Times must be positive for manual work and non-negative for AI.")

df["minutes_saved"] = df["manual_minutes"] - df["ai_assisted_minutes"]
df["time_saved_percent"] = 100 * df["minutes_saved"] / df["manual_minutes"]
df["quality_difference"] = df["ai_quality_1_to_5"] - df["manual_quality_1_to_5"]

manual = df["manual_minutes"].sum()
ai = df["ai_assisted_minutes"].sum()
saved = manual - ai
print("AI TIME-AUDIT SUMMARY (check data status before interpreting)")
print(f"Tasks: {len(df)}")
print(f"Manual total: {manual:.0f} min")
print(f"AI-assisted total: {ai:.0f} min")
print(f"Difference: {saved:.0f} min ({saved/manual*100:.1f}%)")
print(f"Mean manual quality: {df['manual_quality_1_to_5'].mean():.2f}/5")
print(f"Mean AI quality: {df['ai_quality_1_to_5'].mean():.2f}/5")
print("\nPer-task results:")
print(df[["task", "manual_minutes", "ai_assisted_minutes",
          "minutes_saved", "time_saved_percent", "quality_difference"]].to_string(index=False))

ax = df.set_index("task")[["manual_minutes", "ai_assisted_minutes"]].plot(kind="bar", figsize=(10, 6))
ax.set_ylabel("Minutes")
ax.set_title("Manual vs AI-assisted time (demo data unless replaced)")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.show()
