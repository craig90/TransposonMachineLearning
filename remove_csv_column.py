import pandas as pd

df_raw = pd.read_csv('data/!FINAL_DROSO_GREENLAND_STRONGYL_tester.csv')
print(len(df_raw))

df_new = df_raw.drop(columns=["TE_Order"])
print(len(df_new))

df_new.to_csv('data/tester_without_target.csv')

