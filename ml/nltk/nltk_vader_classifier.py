import logging

from nltk.sentiment import SentimentIntensityAnalyzer

from config.nltk_config import *
from ml.nltk.nltk_model_downloader import download_vader

"""Thanks to https://realpython.com/python-nltk-sentiment-analysis/ """

logger = logging.getLogger("nltk-vader-classifier-logger")


class TextClassifierVader:
    def __init__(self):
        self.classifier = None
        self.path = ""

        self.load_model()

    def load_model(self):
        self.path = f"../..{vader_location}"

        logger.debug(f'Loading model: {self.path}')

        # hacky way of determining whether this is being run or imported from above folder, as the file locator in
        # nltk 'SentimentIntensityAnalyzer' doesn't like PATH variables for the model location it seems
        for i in range(3):
            try:
                logger.debug(f'Trying to setup a classifier with model: {self.path}')
                self.classifier = SentimentIntensityAnalyzer(lexicon_file=self.path)
            except LookupError:
                if i == 0:
                    logger.debug(f'Classifier init failed, may need VADER model; downloading.')
                    download_vader()
                else:
                    logger.debug(f'Classifier init failed again, this may be being imported from above; changing path.')
                    self.path = vader_location

    def classify_words(self, words):
        result = self.classifier.polarity_scores(words)
        logger.debug(f'Confidences: {result}')
        logger.debug(f'Calculated compound score: {result["compound"]})')

        return result['compound']


TextClassifierInterface = TextClassifierVader()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    while True:
        text = input("Test text: ")

        print(TextClassifierInterface.classify_words(text))
