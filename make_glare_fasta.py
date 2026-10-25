""" usage python3 make_glare_fasta.py input.csv outputfilename [max_seqs]"""

import sys

import pandas as pd

ORDER_TO_GLARE = {
    "LTR": "LTR",
    "Non-LTR/LINE": "LINE",
    "SINE": "SINE",
    "TIR": "TIR",
    "Helitron": "HELITRON",
    "Crypton": "CRYPTON",
    "DIRS": "DIRS",
    "Maverick": "MAVERICK",
    "Maverick/Polinton": "MAVERICK",
    "Penelope-like Element/PLE": "PLE",
}

csv_path, fasta = sys.argv[1], sys.argv[2]
max_seqs = int(sys.argv[3]) if len(sys.argv) > 3 else None

df = pd.read_csv(csv_path)

# I'm going to remove the Simple_Repeat because it's not in my training set
df = df[df["TE_Order"] != "Simple_Repeat"]

# random subset for a smaller test run, fixed seed so it's the same each time
if max_seqs is not None and max_seqs < len(df):
    df = df.sample(n=max_seqs, random_state=42)

# can't have spaces or # in sequence id in glare fasta file
df["glare_id"] = df["Sequence_ID"].astype(str).str.replace(r"[\s#]+", "_", regex=True)
assert df["glare_id"].is_unique, "Repeat IDs"

with open(f"{fasta}.fasta", "w") as f:
    for sid, seq in zip(df["glare_id"], df["sequence_content"]):
        f.write(f">{sid}\n{str(seq).upper()}\n")

df["glare_order"] = df["TE_Order"].map(ORDER_TO_GLARE)
unmapped = df.loc[df["glare_order"].isna(), "TE_Order"].unique()

if(len(unmapped)):
    print("Count not convert the following TE_Orders to Glare orders", list(unmapped))

df[["glare_id", "Sequence_ID", "TE_Order", "glare_order"]].to_csv(f"{fasta}_labels.csv", index=False)
