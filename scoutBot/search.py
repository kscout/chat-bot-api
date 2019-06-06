import re
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer as wnl
import requests
from scoutBot import errors

CUSTOMIZED_STOP_WORDS: List[str] = ["search", "want", "like", "apps"]


# Process text to send to app-api
def process_text(message: str) -> str:
    # Create Stop words
    stop_words = (stopwords.words("english"))
    stop_words += CUSTOMIZED_STOP_WORDS

    # Remove punctuation
    text = re.sub("[^a-zA-Z]", ' ', message)

    # Convert to lowercase
    text = text.lower()

    # remove digits, characters
    text = re.sub('(\\d|\\W)+', " ", text)

    # Create tokens
    text = list(set(nltk.word_tokenize(text)))
    text = [wnl().lemmatize(word) for word in text if not word in stop_words]
    return (text)


# Search apps using app-api endpoint
def search_apps(message : str) -> str:
    list_of_keywords = (process_text(message))
    try:
        response = requests.get("http://api.kscout.io/apps?query=" + (",".join(list_of_keywords)), verify=False)
        return response.text

    except ConnectionRefusedError:
        return errors.CONNECTION_ERR
    except:
        return errors.NO_SUCH_APP_ERR
