# TransposonMachineLearning

This repo contains a number of python scripts which were used for preprocessing transposable element dataset(s) into the formats that are needed for different ML pipelines and models. The training data set is not included in the repo due to size but these scripts assume a csv format of Sequence_ID,sequence_content,TE_Order.  The smaller preprosessed test set is included under PreprocessedDataSets/FINAL_tester_without_target_full_set.csv. 

Some of the scripts prepare the dataset(s) for TE-Atlas: https://github.com/mirzaahmadi/TE-Atlas/tree/main.
The preprocessing performed in TE-Atlas was then used for other ML models.

Other scripts prepare the datasets for Weka: https://sourceforge.net/projects/weka/.

While other scripts prepare the datasets for GLARE: https://code.jgi.doe.gov/NHaas/glare.

There is also a custom LSTM for TE classification included in this repo.

## Te-Atlas instructions:

These instructions are based on the dataset I was provided with and the first step will be unecessary with a more balanced dataset:
The first thing is to create FINAL_TE_feature_extraction_dataset_without_maverickpolinton.csv as there are not enough
samples of maverick polinton in the dataset for Random Forrest (and potentially others) to run.
Build this with csv_split.py

##
Using TE-Atas to see how Random Forest runs, but also to obtain preprocessed, 
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

3. For accuracy info and other metrics, run classify_compare.py script


## For Weka:

1. Training data set needs to have sequences and column nums removed, so we take the preprocessed
FINAL_TE_feature_extraction_dataset_without_maverickpolinton.csv and run it through 
make_weka_train_set.py to output a dataset that can go into weka.

2. Testing data set: we need to rejoin the preprocessed FINAL_tester_without_target.csv from the 
TE-Atlas pipeline back to !FINAL_DROSO_GREENLAND_STRONGYL_tester.csv to re-add the class names 
which get stripped in the TE_Atlas pipeline.  Then the sequence number and sequence content need to be dropped.
So do this by running make_weka_test_set.py

3. The testing sets seem to not work as csvs, so load them into Weka as .csv and then save as .arff, then
reload the .arff file to use for test classification.

## General

There is a gaussian_noise.py script that can be used to augment datasets with certain transposon classes
with more sequeneces.


### For GLARE:

The test set !FINAL_DROSCO_GREENLAND_STRONGYL_tester.csv can be run through GLARE,
this is what to do to run it

1. Clone the GLARE repo and setup a venv with the correct dependencies.  The GLARE README 
talks about using Linux with an NVIDEA graphics card and using pixi, but it can be 
run without these on a Macbook.  Just make sure all the library versions match.

2. Run make_glare_fasta.py, which turns the csv into a fasta but also creates a csv with
labels for comparison afterwards

3. Run glare predict, view the settings in their README.. Set --threshold 0.
This is kind of slow, even with the ~600 sequence test set it took 15 minutes to run on an M4 Macbook.

4. Run glare_label_compare.py which takes the output from GLARE and combines it with the labels from
make_glare_fasta.py and creates a confusion matrix and other statistics.

## Reconstruct dataset for TE-Atlas using GLARE datasets.

1. Download Repbase and PanTEon.  Glare specifies the specific PanTEon version they
used but not Repbase.

2. Run create_glare_test_set.py -> This script uses GLARE's train/val/test split script 
to create a combined PanTEon Repbase test set for use with TE-Atlas

