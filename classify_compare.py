"""
Usage python3 classify_compare.py TE-Atlas_results_file label_file

This script is use to combine the TE-Atlas results with the labelled file.
This is needed because TE-Atlas runs the classification on a file without labels.

This script also produces some classification metrics.

"""

import sys
import pandas as pd

classifcation_results_file, label_file = sys.argv[1], sys.argv[2]

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




