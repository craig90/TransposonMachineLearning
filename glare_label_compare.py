""" usage python3 glare_label_compare.py predictions.csv labels.csv [confusion_matrix.png]"""

import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay


predictions_csv, labels_csv = sys.argv[1], sys.argv[2]
plot_png = sys.argv[3] if len(sys.argv) > 3 else "confusion_matrix.png"

df_predictions = pd.read_csv(predictions_csv)
df_labels = pd.read_csv(labels_csv)

df_merged = df_labels.merge(df_predictions, left_on="glare_id", right_on="id", how="left")

df_merged["correct"] = df_merged["glare_order"] == df_merged["pred_order"]

print("Accuracy:", df_merged["correct"].mean())

classified_count = len(df_merged) - (df_merged["pred_order"] == "UNKNOWN").sum()
correctly_classified = df_merged["correct"].sum() / classified_count

print("Accuracy among non-unknown:", correctly_classified)

# print(pd.crosstab(df_merged["glare_order"], df_merged["pred_order"]))

# confusion matrix
y_true = df_merged["glare_order"]
y_pred = df_merged["pred_order"].fillna("UNKNOWN")
labels = sorted(set(y_true) | set(y_pred))

fig, ax = plt.subplots(figsize=(10, 8))
disp = ConfusionMatrixDisplay.from_predictions(
    y_true, y_pred, labels=labels, normalize="true",
    cmap="Blues", values_format=".0%", xticks_rotation=45, ax=ax,
)
disp.ax_.set_title(f"GLARE accuracy {df_merged['correct'].mean():.1%}")

# gridlines between cells
ax.set_xticks([x + 0.5 for x in range(len(labels) - 1)], minor=True)
ax.set_yticks([y + 0.5 for y in range(len(labels) - 1)], minor=True)
ax.grid(which="minor", color="lightgray", linewidth=1)
plt.tight_layout()
plt.savefig(plot_png, dpi=200)
