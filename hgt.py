import os
import argparse
from types import ModuleType
import numpy as np
from collections import Counter
from math import sqrt
import random 
from word2vec import word2vec, cosdis


NUM_SWEETWORDS = 20 
NUM_USER = 10000 
NUM_ATTEMPT = 20 

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--generated", dest="generated", help="The generated text file")
    parser.add_argument(
        "--path-target",
        type=str,
        dest="path_target",
        help="The file containing the passwords that we want to honeywords from",
    )
    parser.add_argument(
        "--path-attack",
        type=str,
        dest="path_attack",
        help="The file containing the attack datasets",
    )
    parser.add_argument(
        "--hgt",
        type=int,
        dest="hgt",
        help="which htg to choose, used to calculate probability matrix",
    )

    return parser.parse_args()


args = parse_args()


# generate honeywords
def chaffing_by_model(path_generated, path_target):
    print("start to generate honeywords_model.")
    generated_file = open(path_generated, "r").readlines()
    generated_file = list(set(generated_file))
    targets = open(path_target, "r").readlines()
    targets = targets[:NUM_USER]
    dic = {}
    for target in targets:
        dic[target] = {}
        for i in range(len(generated_file)):
            vec_target = word2vec(target)
            generated = generated_file[i]
            score = cosdis(word2vec(generated), vec_target)
            dic[target][generated] = score

        # find the most num_words similar words to the real passwords in target as the honeywords
        dic[target] = list(
            dict(sorted(dic[target].items(), key=lambda x: x[1], reverse=True)).keys()
        )[:NUM_SWEETWORDS-1]
    # convert the dictionary to an array
    matrix = np.array([dic[i] for i in targets])
    # delete all \n in the matrix
    matrix = [[l[i].strip() for i in range(len(l))] for l in matrix]
    targets = [string.strip() for string in targets]
    combined_matrix = np.c_[targets, matrix]

    with open('honeywords_model.txt', 'w') as f:
        for row in combined_matrix:
            f.write(" ".join([str(a) for a in row] + list("\n")))
    print("honeywords_model generated.")
    return combined_matrix



def chafffing_by_tweak(path_target):
    print("start to generate honeywords_tweak.")
    real_passwords = open(path_target, "r").readlines()
    real_passwords = [l.strip() for l in real_passwords]
    real_passwords = real_passwords[:NUM_USER]
    symbols = ['!', '#', '$', '%', '&', '"', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
               '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', "'"]
    f = 0.03
    p = 0.3
    q = 0.05
    matrix = [[] * NUM_SWEETWORDS for _ in range(NUM_USER)]
    for n in range(NUM_USER):
        real_password = real_passwords[n]
        count = NUM_SWEETWORDS - 1
        while count > 0:
            temp = ''
            for i in range(len(real_password)):
                if real_password[i] >= "a" and real_password[i] <= "z":
                    if random.random() <= p:
                        temp += real_password[i].upper()
                    else:
                        temp += real_password[i]
                elif real_password[i] >= "A" and real_password[i] <= "Z":
                    if random.random() <= q:
                        temp += real_password[i].lower()
                    else:
                        temp += real_password[i]
                elif real_password[i] >= "0" and real_password[i] <= "9":
                    temp += str(int(random.random() * 10))
                elif real_password[i] in symbols:
                    temp += symbols[int(random.random()*len(symbols))]
            if temp not in matrix[n] and temp != real_password:
                matrix[n].append(temp)
                count -= 1
    combined_matrix = np.c_[real_passwords, matrix]
    # write the 2d matrix to a text file
    with open('honeywords_tweak.txt', 'w') as f:
        for row in combined_matrix :
            f.write(" ".join([str(a) for a in row] + list("\n")))
    print("honeywords_tweak generated.")
    return combined_matrix 

# change path 
def chaffing_by_fasttext():
    print("start to generate honeywords_fasttext.")
    model = fasttext.load_model("model_trained_on_rockyou_500_epochs.bin")
    real_passwords= open('rockyou_sorted_preprocessed.txt', "r").readlines()
    real_passwords = [l.strip() for l in real_passwords]
    honeywords=[]
    for real_password in real_passwords:
        honeywords.append(real_password)
        temp = model.get_nearest_neighbors(real_password,k=NUM_SWEETWORDS-1)
        for element in temp:
            honeywords.append(element[1])

    matrix = np.array(honeywords).reshape(-1, NUM_SWEETWORDS)
    with open('honeywords_fasttext.txt', 'w') as f:
        for row in matrix:
            f.write(" ".join([str(a) for a in row] + list("\n")))
    print("honeywords_fasttext generated.")
    return matrix

# calculate the probability matrix
def cal_probs(path_attack, hgt):
    probs = [[0 for x in range(NUM_SWEETWORDS)] for y in range(NUM_USER)] 
    if hgt == 0:
       matrix = chaffing_by_model(args.generated, args.path_target)
    elif hgt == 1:
        matrix = chafffing_by_tweak(args.path_target)
    else:
        matrix = chaffing_by_fasttext()

    attack= open(path_attack, "r").readlines()
    print("start to calculate probability matrix")
    for i in range(NUM_USER):
        for j in range(NUM_SWEETWORDS):
            honeyword = matrix[i][j]
            vec_honeyword = word2vec(honeyword)
            threshold = 0
            for attack_password in attack:
                score = cosdis(word2vec(attack_password), vec_honeyword)
                if score > threshold:
                    threshold = score
                probs[i][j] = threshold
    if hgt == 0:
        name = 'model'
    elif hgt == 1:
        name = 'tweak'
    else:
        name = 'fasttext'
    with open('probs_{}.txt'.format(name), 'w') as f:
        for row in probs:
            f.write(" ".join([str(a) for a in row] + list("\n")))
    print("prob matrix generated.")
    return probs


def attack():
    probs= cal_probs(args.path_attack, args.hgt)
    success_attempt_list = [0] * NUM_ATTEMPT # maximum sweetwords login attempts
    SUCCESS_COUNT = 0
    print('start to calculate attack success rate.')
    for attempt in range(NUM_ATTEMPT): 
        i = NUM_USER
        while i > 0 and len(probs) > 0:
            max_index = np.where(probs== np.amax(probs))
            # worst case scenario, if two words have the biggest prob, assume the attack guess correctly.
            listOfCordinates = list(zip(max_index[0], max_index[1]))
            for cord in listOfCordinates:
                if cord[1] == 0:
                    SUCCESS_COUNT += 1
                     # delete the user if attacker guess correctly
                    probs = np.delete(probs, cord[0], axis=0)
                    i -= 1
                    break
                else:
                    probs[cord[0]][cord[1]] = 0
                    i -= 1
        success_attempt_list[attempt] = round(SUCCESS_COUNT/NUM_USER, 6)
    return print("The number of users being attacked under each attempts is {}".format(success_attempt_list))

#execute program
if __name__ == '__main__':
    attack()
