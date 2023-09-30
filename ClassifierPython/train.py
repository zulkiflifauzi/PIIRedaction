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
import asyncio

async def train_data(fileName, sentence, labels):
    print("message: start training.")
    df = pd.read_csv(fileName)

    corpus = df[sentence].apply(nfx.remove_stopwords) 

    tfidf = TfidfVectorizer()

    Xfeatures = tfidf.fit_transform(corpus).toarray()

    y = df[labels]

    X_train,X_test,y_train,y_test = train_test_split(Xfeatures,y,test_size=0.3,random_state=42)

    binary_rel_clf = BinaryRelevance(classifier=MultinomialNB(alpha=1.0, class_prior=None,
                                            fit_prior=True),
                    require_dense=[True, True])

    binary_rel_clf.fit(X_train,y_train)

    br_prediction = binary_rel_clf.predict(X_test)

    print(br_prediction.toarray())

    model_pkl_file = fileName + ".pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(binary_rel_clf, file)

    print("training completed.")
