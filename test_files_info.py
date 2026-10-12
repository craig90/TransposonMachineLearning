import pandas as pd

df_train_preprocessed = pd.read_csv("PreprocessedForWeka/TE_feature_extraction_dataset_for_weka.csv")

print("Training dataset counts:")
print(df_train_preprocessed["Final_Class"].value_counts())
print(df_train_preprocessed["Final_Class"].count)

df_tester_preprocessed = pd.read_csv("PreprocessedForWeka/TE_FINAL_tester_for_weka.csv")

print("\nTesting dataset counts:")
print(df_tester_preprocessed["Final_Class"].value_counts())
print(df_tester_preprocessed["Final_Class"].count)


print("\nFull testing dataset counts:")

df_tester_raw = pd.read_csv("data/!FINAL_DROSO_GREENLAND_STRONGYL_tester.csv")
print("First 100:")
print(df_tester_raw['TE_Order'].head(100).value_counts())
print("First 200:")
print(df_tester_raw['TE_Order'].head(200).value_counts())
print("First 225:")
print(df_tester_raw['TE_Order'].head(225).value_counts())
print("Everything:")
print(df_tester_raw["TE_Order"].value_counts())

print("\nFull Feature extracted dataset counts:")