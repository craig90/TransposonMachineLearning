import sys
import pandas as pd


predictions_csv, labels_csv = sys.argv[1], sys.argv[2]

df_predictions = pd.read_csv(predictions_csv)
df_labels = pd.read_csv(labels_csv)

df_merged = df_labels.merge(df_predictions, left_on="glare_id", right_on="id", how="left")

df_merged["correct"] = df_merged["glare_order"] == df_merged["pred_order"]

print("Accuracy:", df_merged["correct"].mean())

print(pd.crosstab(df_merged["glare_order"], df_merged["pred_order"]))