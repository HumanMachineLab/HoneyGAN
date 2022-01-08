import os
from types import ModuleType
import numpy as np
from collections import Counter
from math import sqrt
import argparse
from statistics import mean
from word2vec import word2vec, cosdis

'''
python3 inner_similarity.py --path-sweetwords sweetwords/chaffing_by_tweak/rockyou_10000_20.txt
'''
NUM_SWEETWORDS = 20
NUM_USER = 10000
NUM_ATTEMPT = 20

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path-sweetwords",
        type=str,
        dest="path_sweetwords",
        help="The file containing the sweetwords datasets",
    )

    return parser.parse_args()


args = parse_args()

def inner_similarity(path_sweetwords):
    sweetwords= open(path_sweetwords, "r").readlines()
    sweetwords = [l.strip() for l in sweetwords]
    sweetwords_2d = [sweetwords[i].split() for i in range(len(sweetwords))]
    l_score = [] 
    for i in range(NUM_USER):
        score = 0
        for j in range(1, NUM_SWEETWORDS):
            score += cosdis(word2vec(sweetwords_2d[i][0]), word2vec(sweetwords_2d[i][j]))
        l_score.append(score/(NUM_SWEETWORDS-1))
    return print('The average similarity score of each honewords with its real password in the file is {}'.format(mean(l_score)))


inner_similarity(args.path_sweetwords)



