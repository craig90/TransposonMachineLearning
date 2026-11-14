import sys
import pandas as pd

"""
This script recombines the preprocessed target less test set from TE-Atlas
with the unpreporcessed set to re-attach the labels
"""

preprocessed_file, label_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]

df_preprocessed = pd.read_csv(preprocessed_file)
df_labels = pd.read_csv(label_file)
print(df_preprocessed.head())

df_labels = df_labels.drop(columns="sequence_content")
print(df_labels.head())

df_merged = df_preprocessed.merge(df_labels, on="Sequence_ID", how="left")

print(df_merged.head())
print(len(df_merged))
df_merged.to_csv(out_file, columns=["Sequence_ID", "sequence_content", "TE_Order"])
