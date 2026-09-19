import pandas as pd
import random

ALLOWED_CHARS = "ACGT"

def remove_problematic_rows(df_raw):
    """
    Removes rows where over 1% of nucleotides are ambiguous
    """
    
    problematic_entries = 0
    rows_to_remove = []

    for row in df_raw.itertuples():
        
        total_nucleotides = len(row.sequence_content)
        ambigious_nucleotides = sum(char not in ALLOWED_CHARS for char in row.sequence_content)

        ## remove entries where more than 1% of nucleotides have a problem
        if ambigious_nucleotides / total_nucleotides > .01:
            problematic_entries += 1
            rows_to_remove.append(row.Index)
        
    return (df_raw.drop(index=rows_to_remove))


def fix_ambigious_nucleotides(df_partial):
    """
    Replaces ambigious nucleotides with random nucleotide
    """

    for row in df_partial.itertuples():
        
        sequence_str = row.sequence_content
        sequence_list = []

        for char in sequence_str:
            if (char in ALLOWED_CHARS):
                sequence_list.append(char)
            else:
                random_nuc = random.choice(ALLOWED_CHARS)
                sequence_list.append(random_nuc)

        new_seq_str = "".join(sequence_list)
        df_partial.at[row.Index, "sequence_content"] = new_seq_str

    return (df_partial)




df_raw = pd.read_csv('TE_feature_extraction_dataset.csv')

print(df_raw.head())
print(len(df_raw))

df_partial = remove_problematic_rows(df_raw)
df_processed = fix_ambigious_nucleotides(df_partial)

print(len(df_processed))

# df_processed.to_csv('TE_feature_extraction_dataset_pre-processed.csv')


