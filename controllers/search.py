import re
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer as wnl
import requests
from config import errors

CUSTOMIZED_STOP_WORDS: List[str] = ["search", "want", "like", "apps","deploy"]


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
        response = requests.get("https://api.kscout.io/nsearch?query=" + (",".join(list_of_keywords)), verify=False)
        if response.status_code != 200:
            status = {}
            status["error connecting to kscout"] = "kscout api not reachable"
            raise Exception(status)
        return response.text

    except ConnectionRefusedError:
        status = {}
        status["error connecting to kscout"] = "Connection Refused"
        raise Exception(status)
    except Exception as e:
        status = {}
        status["error connecting to kscout"] = str(e)
        raise Exception(status)
