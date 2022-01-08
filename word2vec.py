import numpy as np
from collections import Counter
from math import sqrt

def word2vec(word):
    cw = Counter(word)
    sw = set(cw)
    lw = sqrt(sum(c * c for c in cw.values()))
    return cw, sw, lw

# compute cosine similarity
def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]