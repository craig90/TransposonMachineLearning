import pandas as pd

df_raw = pd.read_csv('PreprocessedDataSets/FINAL_TE_feature_extraction_dataset_without_maverickpolinton.csv')

df_new = df_raw.drop(columns="sequence_content")

df_new.to_csv("PreprocessedForWeka/TE_feature_extraction_dataset_for_weka.csv", index=False)