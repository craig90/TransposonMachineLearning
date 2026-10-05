import pandas as pd

# read in and drop sequence content from both cvs
df_test_feature_extracted_without_target = pd.read_csv("PreprocessedDataSets/FINAL_tester_without_target.csv")
df_test_feature_extracted_without_target = df_test_feature_extracted_without_target.drop(columns="sequence_content")

df_test_with_target = pd.read_csv("data/!FINAL_DROSO_GREENLAND_STRONGYL_tester.csv")
df_test_with_target = df_test_with_target.drop(columns="sequence_content")

print(df_test_feature_extracted_without_target.head())
print(df_test_with_target.head())


# merge on Sequence_ID then drop it since
df_merged = pd.merge(df_test_feature_extracted_without_target, df_test_with_target, on="Sequence_ID")
df_merged = df_merged.drop(columns="Sequence_ID")


df_merged.rename(columns={"TE_Order":"Final_Class"}, inplace=True)
print(df_merged.head())


df_merged.to_csv("PreprocessedForWeka/TE_FINAL_tester_for_weka.csv", index=False)