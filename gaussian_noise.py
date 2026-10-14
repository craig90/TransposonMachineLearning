import numpy as np
import pandas as pd

def add_gaussian_noise(X, y, target_counts, sigma=0.01, random_state=42):
    
    rng = np.random.default_rng(random_state)

    synthetic_X = []
    synthetic_y = []

    for class_label, n_new in target_counts.items():
        class_samples = X.loc[y == class_label]

        if class_samples.empty:
            continue

        for _ in range(n_new):
            original = class_samples.iloc[rng.integers(len(class_samples))].to_numpy(dtype=float)
        
            noise = rng.normal(0, sigma, size=original.shape)
            synthetic_X.append(original+noise)
            synthetic_y.append(class_label)

    X_synthetic = pd.DataFrame(
        synthetic_X,
        columns=X.columns
    )

    y_synthetic = pd.Series(
        synthetic_y,
        name=y.name
    )

    return (pd.concat([X, X_synthetic], ignore_index=True),
            pd.concat([y.reset_index(drop=True),
                       y_synthetic.reset_index(drop=True)],
                       ignore_index=True)
    )



df = pd.read_csv("PreprocessedForWeka/TE_FINAL_tester_for_weka_full_set.csv")

print(df["Final_Class"].value_counts())

targets = df["Final_Class"].copy()
features = df.drop(columns=["Final_Class"]).copy()

target_counts = {
    "Penelope-like Element/PLE": 8,
    "DIRS": 4,
    "Non-LTR/LINE": 2
}

features_augmented, targets_augmented = add_gaussian_noise(features, targets, target_counts)

print(targets_augmented.value_counts())



augmented_df = pd.concat(
    [features_augmented.reset_index(drop=True),
    targets_augmented.reset_index(drop=True).rename("Final_Class")],
    axis=1
)

print(augmented_df["Final_Class"].value_counts())

augmented_df.to_csv("PreprocessedForWeka/TE_FINAL_tester_augmented.csv", index=False)

assert len(features_augmented) == len(targets_augmented)
assert features_augmented.columns.tolist() == features.columns.tolist()

print("Feature rows:", len(features_augmented))
print("Target rows:", len(targets_augmented))
print("Total rows:", len(augmented_df))