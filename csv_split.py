import pandas as pd

df_raw = pd.read_csv('data/TE_feature_extraction_dataset.csv')

# print(df_raw.head())
# print(len(df_raw))

# df_new = df_raw.iloc[0:100]

# df_new.to_csv('data/TE_feature_extraction_dataset_first_100.csv')


## 3 per class
# small_df = df_raw.groupby("TE_Order").sample(n=3, random_state=42)
# print(len(small_df))
# small_df.to_csv('data/TE_feature_extraction_dataset_3_per_class.csv')


# print(f"Data set length {len(df_raw)}")


# # raw acounts
# class_counts = df_raw['TE_Order'].value_counts()
# print(class_counts)


# # 6 per class df
# df_filtered = df_raw[df_raw['TE_Order'] != "Maverick/Polinton"] 
# six_per_df = df_filtered.groupby("TE_Order").sample(n=6, random_state=42)

# print(len(six_per_df))

# six_per_df.to_csv('data/TE_feature_extraction_dataset_6_per_class.csv')


# 20 per class df
# df_filtered = df_raw[df_raw['TE_Order'] != "Maverick/Polinton"] 
# six_per_df = df_filtered[df_filtered["TE_Order"] == "Maverick"].sample(n=6, random_state=42)

# other_classes = (
#     df_filtered[df_filtered["TE_Order"] != "Maverick"]
#     .groupby("TE_Order")
#     .sample(n=20, random_state=42)
# )

# df_sampled = pd.concat([six_per_df, other_classes])

# print(len(df_sampled))

# df_sampled.to_csv('data/TE_feature_extraction_dataset_20_per_class.csv')


## 100 per class df
# df_filtered = df_raw[df_raw['TE_Order'] != "Maverick/Polinton"] 
# six_per_df = df_filtered[df_filtered["TE_Order"] == "Maverick"].sample(n=6, random_state=42)

# other_classes = (
#     df_filtered[df_filtered["TE_Order"] != "Maverick"]
#     .groupby("TE_Order")
#     .sample(n=100, random_state=42)
# )

# df_sampled = pd.concat([six_per_df, other_classes])

# print(len(df_sampled))

# df_sampled.to_csv('data/TE_feature_extraction_dataset_100_per_class.csv')


print(len(df_raw))
## full dataset without Maverick/Polinton
df_filtered = df_raw[df_raw['TE_Order'] != "Maverick/Polinton"] 
print(len(df_filtered))
df_filtered.to_csv('data/TE_feature_extraction_dataset_without_maverickpolinton.csv')
