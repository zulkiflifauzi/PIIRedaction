import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.metrics import accuracy_score,hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from skmultilearn.problem_transform import LabelPowerset
import neattext as nt
import neattext.functions as nfx
import pickle


df = pd.read_csv("train2.csv")

corpus = df['comment_text'].apply(nfx.remove_stopwords) 

tfidf = TfidfVectorizer()

tfidf.fit_transform(corpus).toarray()

# load saved model
with open('tweet_model.pkl' , 'rb') as f:
    lr = pickle.load(f)
# check prediction

ex1 = "Son of a bitch"

vec_example = tfidf.transform([ex1])

print(lr.predict(vec_example).toarray()) 