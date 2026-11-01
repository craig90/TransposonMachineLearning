"""
../GLARE/.venv/bin/python create_glare_test_set.py PANTEON_FASTA REPBASE_DIR OUT_DIR

PanTEon is stored as a fasta file PANTEON_FASTA
while Repbase is stored in a dir as REPBASE_DIR

Recreates GLARE's test set by calling GLARE's own loading/splitting code with
the settings from
configs/combined_repbase_panteon_repeatmasker_custom_no_clade_rc_augment_best_hpo_final.yaml
and writes them out as CSV.

Also creates CSVs with proper column names for TE-Atlas pipeline

GLARE paper test-set sizes: PanTEon 23,043, Repbase 11,778.

"""

import sys
from pathlib import Path

import pandas as pd
import yaml

# translates the Order labels back from GLARE to what TE-Atlas wants
GLARE_TO_TE_ATLAS = {
    "LTR": "LTR",
    "LINE": "Non-LTR/LINE",
    "SINE": "SINE",
    "TIR": "TIR",
    "HELITRON": "Helitron",
    "CRYPTON": "Crypton",
    "DIRS": "DIRS",
    "MAVERICK": "Maverick",
    # "Maverick/Polinton": "MAVERICK",
    "PLE": "Penelope-like Element/PLE",
}

# GLARE repo is expected next to this parent's folder - edit if it different spot
GLARE_DIR = Path(__file__).resolve().parent.parent / "GLARE"

sys.path.insert(0, str(GLARE_DIR))

from glare.constants import get_label_space
from glare.data import build_combined_repbase_panteon_records

CONFIG = GLARE_DIR / "configs/combined_repbase_panteon_repeatmasker_custom_no_clade_rc_augment_best_hpo_final.yaml"

panteon_fasta, repbase_dir, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

with open(CONFIG) as fh:
    config = yaml.safe_load(fh)

# update the config for the local non GLARE setup since the directories are different
data_config = dict(config["data"])
data_config["repbase_dir"] = repbase_dir
data_config["fasta_path"] = panteon_fasta
data_config["panteon_fasta_path"] = panteon_fasta
data_config["toml_mapping"] = str(GLARE_DIR / "data/repbase-to-repeatmasker-custom.toml")
data_config["panteon_label_mapping"] = str(GLARE_DIR / "data/panteon-to-repeatmasker-custom.toml")

label_space = get_label_space(data_config["label_space"])

# this calls the GLARE function to create the records
train_recs, val_recs, test_sets, _diagnostics = build_combined_repbase_panteon_records(
    data_config=data_config,
    val_fraction=config["training"]["val_fraction"],
    seed=config["training"]["seed"],
    superfamily2idx=label_space["superfamily2idx"],
    label_subset_labels=None,
    log=False,
)

print(f"train: {len(train_recs)}  val: {len(val_recs)}  (paper: 282,046 / 31,339)")

# test_sets contains dicts for both panteon and repbase
all_tests = []
for test_name, records in test_sets.items():
    df = pd.DataFrame(records)
    # PanTEon records use "id", Repbase records use "name"
    if "id" not in df.columns:
        df["id"] = df["name"]
    df.insert(0, "test_set", test_name)
    front = ["test_set", "id", "order", "superfamily", "species"]
    df = df[front + [c for c in df.columns if c not in front and c != "sequence"] + ["sequence"]]

    out_path = out_dir / f"{test_name}.csv"
    df.to_csv(out_path, index=False)
    print(f"{test_name}: {len(df)} records -> {out_path}")
    all_tests.append(df)

combined = pd.concat(all_tests, ignore_index=True)
combined.to_csv(out_dir / "glare_test_set_combined.csv", index=False)
print(f"combined: {len(combined)} records -> {out_dir / 'glare_test_set_combined.csv'}")

# create csvs for TE-Atlas
# remove the orders that are not in TE-Atlas
combined = combined[~combined["order"].isin(["SATELLITE", "STRUCTURAL_RNA"])]

df_for_TE_atlas = pd.DataFrame()
df_for_TE_atlas["Sequence_ID"] = combined["id"]
df_for_TE_atlas["sequence_content"] = combined["sequence"]
df_for_TE_atlas["TE_Order"] = combined["order"].map(GLARE_TO_TE_ATLAS)

assert df_for_TE_atlas["TE_Order"].notna().all(), combined.loc[df_for_TE_atlas["TE_Order"].isna(), "order"].unique()

df_for_TE_atlas.to_csv(out_dir / "glare_test_set_combined_for_TE_atlas.csv", index=False)
df_1000 = df_for_TE_atlas.sample(n=1000, random_state=42)

df_1000.to_csv(out_dir / "glare_test_set_combined_for_TE_atlas_1000_seq.csv", index=False)

print(f"created te-atlas csv with: {len(df_for_TE_atlas)} records -> {out_dir / 'glare_test_set_combined_for_TE_atlas.csv'}")
print(f"created te-atlas 1000 record csv with: {len(df_1000)} records -> {out_dir / 'glare_test_set_combined_for_TE_atlas_1000_seq.csv'}")