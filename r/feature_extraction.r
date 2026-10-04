# feature extraction script for transposon dataset
# script to be run after dataset has been preprocessed
# to remove ambiguous nucleotides

library(arrow)
library(ftrCOOL)

test_var1 <- 2
test_var2 <- 7

total <- test_var1 + test_var2

print(total)

# seems to be running from base directory so "../" not needed... bizarre
df <- read_parquet("data/preprocessed.parquet")

print(total)

# kNUComposition_DNA
# MMI_DNA
# Zcurve144bit_DNA - could be a different one -
# there are a bunch of zcurve functions