import logging
import pickle
import re
import string

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from config.nltk_config import *

"""Thanks to https://realpython.com/python-nltk-sentiment-analysis/ & 
https://stackoverflow.com/questions/29395248/show-label-probability-confidence-in-nltk """

logger = logging.getLogger("nltk-twitter-classifier-logger")


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|''(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


class TextClassifierTwitter:
    def __init__(self):
        self.classifier = None
        self.path = ""
        self.f = None
        self.labels = ["Positive", "Negative"]
        self.confidences = {self.labels[0]: 0.0, self.labels[1]: 0.0}

        self.load_model()

    def load_model(self):
        self.path = f'{model_path}/saved_classifier.pickle'

        logger.debug(f'Loading model: {self.path}')

        self.f = open(self.path, 'rb')
        self.classifier = pickle.load(self.f)
        self.f.close()

    def classify_words(self, words):
        custom_tokens = remove_noise(word_tokenize(words))

        self.classifier.classify(dict([token, True] for token in custom_tokens))  # Returns one label
        multi_label = self.classifier.prob_classify(
            dict([token, True] for token in custom_tokens))  # Returns a DictionaryProbDist object
        for label in self.labels:
            self.confidences[label] = multi_label.prob(label)
        logger.debug(f'Confidences: {self.confidences}')
        result = self.confidences[self.labels[0]] - self.confidences[self.labels[1]]
        logger.debug(f'Calculated compound score ({self.labels[0]} minus {self.labels[1]}: {result})')
        return result


TextClassifierInterface = TextClassifierTwitter()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    while True:
        text = input("Test text: ")
        print(TextClassifierInterface.classify_words(text))
