import pandas as pd

transposon_classes = [
    "LTR",
    "Non-LTR/LINE",
    "SINE",
    "TIR",
    "Helitron",
    "Crypton",
    "DIRS",
    "Maverick",
    "Penelope-like Element/PLE"
]


df_train_set = pd.read_csv(
    "LSTMDataSets/PREPROCESSED_TE_feature_extraction_dataset_without_maverickpolinton.csv"
)

df_test_set = pd.read_csv(
    "LSTMDataSets/FINAL_tester_with_targets.csv"
)

# df_train_data = pd.DataFrame(columns=['TE_Order', "Train_Mean_Length", "Train_Median_Length"])
# df_test_data = pd.DataFrame(columns=['TE_Order', "Test_Mean_Length", "Test_Median_Length"])
train_data = []
test_data = []

for te_class in transposon_classes:
    median_len = df_train_set.loc[df_train_set['TE_Order'] == te_class, "sequence_content"].str.len().median()
    mean_len = df_train_set.loc[df_train_set['TE_Order'] == te_class, "sequence_content"].str.len().mean()
    print(f"{te_class}: median length: {median_len} mean length: {mean_len}")
    train_data.append({"TE_Order": te_class, "Mean_Train_Length": mean_len, "Median_Train_Length": median_len})

for te_class in transposon_classes:
    median_len = df_test_set.loc[df_test_set['TE_Order'] == te_class, "sequence_content"].str.len().median()
    mean_len = df_test_set.loc[df_test_set['TE_Order'] == te_class, "sequence_content"].str.len().mean()
    print(f"{te_class}: median length: {median_len} mean length: {mean_len}")
    test_data.append({"TE_Order": te_class, "Mean_Test_Length": mean_len, "Median_Test_Length": median_len})

df_train_data = pd.DataFrame(train_data)
df_test_data = pd.DataFrame(test_data)

print(df_train_data)
print(df_test_data)

df_merged = pd.merge(df_train_data, df_test_data, on="TE_Order", how="inner")
print(df_merged)

