# run with google colab
import fasttext
import numpy as np

# define global variables
NUM_SWEETWORDS = 20
NUM_USER = 10000
NUM_ATTEMPT = 20

# train fasttext model
def train_model():
   # Skipgram model:
   epochs=500
   model = fasttext.train_unsupervised('rockyou_sorted_preprocessed.txt', minCount=1, minn=2, epoch=epochs, model='skipgram')
   print()
   #save model
   model.save_model("model_trained_on_rockyou_"+str(epochs)+"_epochs.bin")
   print("Model saved as model_trained_on_rockyou_"+str(epochs)+"_epochs.bin")

train_model()

model = fasttext.load_model("model_trained_on_rockyou_500_epochs.bin")
real_passwords= open('rockyou_sorted_preprocessed.txt', "r").readlines()
real_passwords = [l.strip() for l in real_passwords]
honeywords=[]
for real_password in real_passwords:
  honeywords.append(real_password)
  temp = model.get_nearest_neighbors(real_password,k=9)
  for element in temp:
    honeywords.append(element[1])

matrix = np.array(honeywords).reshape(-1, NUM_SWEETWORDS)
with open('honeywords_fasttext.txt', 'w') as f:
  for row in matrix:
    f.write(" ".join([str(a) for a in row] + list("\n")))
