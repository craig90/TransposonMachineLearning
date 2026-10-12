# TransposonMachineLearning

The first thing is to build the maverickpolinton free dataset:
FINAL_TE_feature_extraction_dataset_without_maverickpolintona.csv as there are not enough
samples of this class for Random Forrest (and potentially others) to run.
Build this with csv_split.py

####
Using TE-Atas to see how RandomForest runs, but also to obtain preprocessed, 
feature extacted datasets to be used in Weka:

In order to obtain preprocessed and feature extracted dataset:

Install TE-Atlas python libaries in a python venv

1. Run TE-Atlas part 2 with full training csv:
FINAL_TE_feature_extraction_dataset_without_maverickpolintona.csv

This will take many hours, best to run overnight (the feature extraction is super slow).

2. Copy FINAL_TE_feature_extraction_dataset to folder for additional preprocessing.

Run remove_column_save_without_col_num.py script



For classification dataset:

1. Remove TE_ORDER from !FINAL_DROSCO_GREENLAND_STRONGYL_tester.csv with remove_csv_column.py

2. Run TE-Atlas part 3 with !FINAL_DROSCO_GREENLAND_STRONGYL_tester.csv with removed column TE_ORDER column

Part 3 of TE-Atlas has been modified to take an input dataset rather than output from Part 1 of the pipeline
since part 1 is not being run with for this ML setup

Thankfully the dataset is smaller so feature extraction runs in a reasonable amount of time.

3. For accuracy info, run the Classify/classify_compare script which is in the TE-Atlas repo


######
For Weka:

1. Training data set needs to have sequences and column nums removed, so we take the preprocessed
FINAL_TE_feature_extraction_dataset_without_maverickpolinton.csv and run it through 
make_weka_train_set.py to output a dataset that can go into weka.

2. Testing data set: we need to rejoin the preprocessed FINAL_tester_without_target.csv from the 
TE-Atlas pipeline back to !FINAL_DROSO_GREENLAND_STRONGYL_tester.csv to re-add the class names 
which get stripped in the TE_Atlas pipeline.  Then the sequence number and sequence content need to be dropped.
So do this by running make_weka_test_set.py