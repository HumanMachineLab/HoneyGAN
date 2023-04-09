# HoneyGAN
This repository is created for the review process of paper ["HoneyGAN: Creating Indistinguishable Honeywords with Improved Generative Adversarial Networks." ](https://link.springer.com/chapter/10.1007/978-3-031-29504-1_11#citeas) 

HoneyGAN is a honeyword generation technique (HGT) based on [GNPassGAN](https://github.com/fangyiyu/GNPassGAN). 

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
## Citation
If you find our work is relevant to your research, please cite:
```
@InProceedings{10.1007/978-3-031-29504-1_11,
author="Yu, Fangyi and Vargas Martin, Miguel",
title="HoneyGAN: Creating Indistinguishable Honeywords with Improved Generative Adversarial Networks",
booktitle="Security and Trust Management",
year="2023",
publisher="Springer International Publishing",
pages="189--198",
abstract="Honeywords are fictitious passwords inserted into databases in order to identify password breaches. Producing honeywords that are difficult to distinguish from actual passwords automatically is a sophisticated task. We propose a honeyword generation technique (HGT) called HoneyGAN and an evaluation metric based on representation learning for measuring the indistinguishability of fake passwords, together with a novel attack model for evaluating the efficiency of HGTs. We compare HoneyGAN to state-of-the-art HGTs proposed in the literature using both evaluation metrics and a human study. Our findings indicate that HoneyGAN creates genuine-looking honeywords, leading to a low success rate for knowledgeable attackers in identifying them. We also demonstrate that our attack model is more capable of finding real passwords among sets of honeywords compared to previous works.",
isbn="978-3-031-29504-1"
}
```
