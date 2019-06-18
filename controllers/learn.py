import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


# Read the given text blob line by line
def read_file(filname):
    f = open(filname, 'r')
    text = [line.strip() for line in f.readlines()]
    text = ''.join(text)
    return nltk.sent_tokenize(text)


# Dummy text file until the resources endpoint is up.
sent_tokens = read_file('controllers/serverless.txt')


# Group variants of the same word.
def lematize(tokens):
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]


# remove punctuations from the tokens
def normalize_tokens(text):
    return lematize(nltk.word_tokenize(text.lower().translate(dict((ord(p), None) for p in string.punctuation))))


# calculate response based on cosine similarity
def response(user_response):
    bot_response = ''
    sent_tokens.append(user_response)
    tfidf_vector = TfidfVectorizer(tokenizer=normalize_tokens, stop_words='english')

    # transform tokens to value
    tfidf = tfidf_vector.fit_transform(sent_tokens)

    # similarity value between given and stored data
    cosine_value = cosine_similarity(tfidf[-1], tfidf)
    idx = cosine_value.argsort()[0][-2]
    flat = cosine_value.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        bot_response = bot_response + "I am sorry! I don't understand you"
        return bot_response
    else:
        bot_response = bot_response + sent_tokens[idx]
        return bot_response


# function to send response as json string
def answer_query(message):
    user_response = message.lower()
    bot_response = (response(user_response) + "\n")
    sent_tokens.remove(user_response)
    bot_response = {"text": bot_response}

    return json.dumps(bot_response)
