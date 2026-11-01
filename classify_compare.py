"""
Usage python3 classify_compare.py TE-Atlas_results_file label_file

This script is use to combine the TE-Atlas results with the labelled file.
This is needed because TE-Atlas runs the classification on a file without labels.

This script also produces some classification metrics.

"""

import sys
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.metrics import ConfusionMatrixDisplay, f1_score

classifcation_results_file, label_file = sys.argv[1], sys.argv[2]
plot_png = sys.argv[3] if len(sys.argv) > 3 else "confusion_matrix.png"

df_classified = pd.read_csv(classifcation_results_file)
df_labels = pd.read_csv(label_file)

df_test_raw_indexed = df_labels.set_index("Sequence_ID")

correct_classifications = 0
incorrect_classifications = 0

total_classifications = len(df_classified)

for row in df_classified.itertuples():
    matching_row = df_test_raw_indexed.loc[row.Sequence_ID]

    if matching_row["TE_Order"] == row.Predicted_Class:
        correct_classifications += 1
    else:
        incorrect_classifications += 1

    print(f"Predicted class: {row.Predicted_Class} Actual class: {matching_row['TE_Order']}")

print(f"Correct classifications: {correct_classifications}")
print(f"Incorrect classifications: {incorrect_classifications}")

accuracy = correct_classifications/total_classifications

print(f"Accuracy: {accuracy}")

df_merged = df_labels.merge(df_classified, on="Sequence_ID", how="inner")

print(df_merged.columns)

f1 = f1_score(df_merged["TE_Order"], df_merged["Predicted_Class"], average="weighted", zero_division=0)
print("F1 score: ", f1)

y_true = df_merged["TE_Order"]
y_pred = df_merged["Predicted_Class"].fillna("UNKNOWN")
labels = sorted(set(y_true) | set(y_pred))

fig, ax = plt.subplots(figsize=(10, 8))
disp = ConfusionMatrixDisplay.from_predictions(
    y_true, y_pred, labels=labels, normalize="true",
    cmap="Blues", values_format=".0%", xticks_rotation=45, ax=ax,
)
disp.ax_.set_title(f"TE-Atlas Random Forest accuracy: {accuracy:.1%} F1: {f1:.1%}")

# anchor the end of each rotated label to its tick so long labels don't spill under the next column
plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")

# gridlines between cells
ax.set_xticks([x + 0.5 for x in range(len(labels) - 1)], minor=True)
ax.set_yticks([y + 0.5 for y in range(len(labels) - 1)], minor=True)
ax.grid(which="minor", color="lightgray", linewidth=1)
plt.tight_layout()
plt.savefig(plot_png, dpi=200)



