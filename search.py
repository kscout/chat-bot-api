import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer as ps
from nltk.stem.wordnet import WordNetLemmatizer as wnl

def process_text(message):

    #Create Stop words
    stop_words = (stopwords.words("english"))
    stop_words += ["search", "want", "like", "apps"]

    #Remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', message)

    # Convert to lowercase
    text = text.lower()

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    #Create tokens
    text = set(nltk.word_tokenize(text))

    # Stemming
    text = [ps.stem(word) for word in text if not word in
                                                        stop_words]
    # Lemmatization
    text = [wnl.lemmatize(word) for word in text if not word in
                                                        stop_words]

    return (text)


# def search_apps(message):


