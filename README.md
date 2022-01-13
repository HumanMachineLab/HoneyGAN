# HoneyGAN
This repository is created for the review process of paper "HoneyGAN: Creating Indistinguishable Honeywords with Improved Generative Adversarial Networks."  

HoneyGAN is a honeyword generation technique (HGT) based on GNPassGAN. 

The datasets in the real passwords folder are taken from [BitBucket](https://bitbucket.org/srecgrp/honeygen-generating-honeywords-using-representation-learning/src/master/password_lists_processed_50000_records/).

### Install dependencies

```bash
python3 -m venv .venv 
source .venv/bin/activate  
pip3 install -r requirements.txt
```

### Train the fasttext model
```bash
python3 fasttext.py
```

### Generate honeywords using either HGTs in the paper (0 is GNPassGAN, 1 is tweaking, 2 is fasttext) and get attack success rate.
```bash
# change target and attack file path
python3 hgt.py --generated GNpassGAN_generated.txt \
               --path-target real_passwords/rockyou_sorted_preprocessed.txt \
               --path-attack real_passwords/dubsmash-com_sorted_preprocessed.txt  \
               --hgt 0
```

### Calculate inner text similarity
```bash
# change the path of the tested file
python3 inner_similarity.py --path-sweetwords sweetwords/chaffing_by_tweak/rockyou_10000_20.txt
```
