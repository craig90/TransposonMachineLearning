"""
Usage:
python3 remove_csv_column.py input file

Removes the TE_Order column which needs to be removed for TE-Atlas classification
"""

import sys
import pandas as pd

input_file = sys.argv[1]

df = pd.read_csv(input_file)
print(f"File length of {input_file}: {len(df)}")
print(f"Column names: {df.columns}") 

df_new = df.drop(columns=["TE_Order"])
print(f"Column names after removal: {df_new.columns}")

result = input_file.split(".")
base = result[0]
out_file = f"{base}_without_target.csv"
print(out_file)

df_new.to_csv(out_file)

