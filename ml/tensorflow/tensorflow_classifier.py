import logging

import tensorflow as tf

from config.tensorflow_config import *

"""Code from https://www.tensorflow.org/tutorials/keras/text_classification """

logger = logging.getLogger("tensorflow-classifier-logger")

# Values for converting the 0.0 to 1.0 range this classifier returns into the -0.0 to 1.0 range that the system is
# designed to deal with.
old_max = 1.0
old_min = 0.0
new_min = -1.0
new_max = 1.0


# thanks to https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def number_convert(old_value):
    old_range = (old_max - old_min)
    if old_range == 0:
        new_value = new_min
    else:
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min

    return new_value


class TextClassifier:

    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        self.model = tf.keras.models.load_model(f'{models_path}/saved_model')

        logger.debug(self.model.summary())

    def classify_words(self, words):
        to_classify = [words]

        compound_score = number_convert(self.model.predict(to_classify))

        return compound_score


TextClassifierInterface = TextClassifier()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    while True:
        text = input("Test text: ")
        print(TextClassifierInterface.classify_words(text)[0][0])
