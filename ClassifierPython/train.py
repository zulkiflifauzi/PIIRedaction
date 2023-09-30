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

Xfeatures = tfidf.fit_transform(corpus).toarray()

y = df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']]

X_train,X_test,y_train,y_test = train_test_split(Xfeatures,y,test_size=0.3,random_state=42)

binary_rel_clf = BinaryRelevance(classifier=MultinomialNB(alpha=1.0, class_prior=None,
                                         fit_prior=True),
                require_dense=[True, True])

binary_rel_clf.fit(X_train,y_train)

br_prediction = binary_rel_clf.predict(X_test)

model_pkl_file = "tweet_model.pkl"  

with open(model_pkl_file, 'wb') as file:  
    pickle.dump(binary_rel_clf, file)

ex1 = "COCKSUCKER BEFORE YOU PISS AROUND ON MY WORK"

vec_example = tfidf.transform([ex1])

print(binary_rel_clf.predict(vec_example).toarray())
