import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_file(filname):
    f = open(filname, 'r')
    text = [line.decode('utf-8').strip() for line in f.readlines()]
    text = ''.join(text)
    return nltk.sent_tokenize(text)


sent_tokens = read_file('serverless.txt')

def lematize(tokens):
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]

def normalize_tokens(text):
    return lematize(nltk.word_tokenize(text.lower().translate(dict((ord(p), None) for p in string.punctuation))))

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    # print(sent_tokens)
    TfidfVec = TfidfVectorizer(tokenizer=normalize_tokens, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response

def answer_query(message):

    user_response = message.lower()
    bot_reponnse = (response(user_response) + "\n")
    sent_tokens.remove(user_response)

    return bot_reponnse
