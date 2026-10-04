import pandas as pd

df_raw = pd.read_csv('data/TE_feature_extraction_dataset.csv')

df_raw.to_csv("data/TE_feature_extraction_dataset_without_col_num.csv", index=False)