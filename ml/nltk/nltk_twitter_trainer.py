import logging
import os
import pickle

from utils.pathutils import delete_with_override

from nltk import NaiveBayesClassifier
from nltk import classify

from config.nltk_config import *
from ml.nltk.nltk_dataset_downloader import download_twitter_datasets
from ml.nltk.nltk_twitter_data_processor import process_data

logger = logging.getLogger("nltk-twitter-trainer-logger")


def delete_model():
    if os.path.exists(f'{model_path}/saved_model'):
        logger.debug(f'Model: {model_path}/saved_model exists, deleting.')
        delete_with_override(f'{model_path}/saved_model')

    else:
        logger.debug(f'Model: {model_path}/saved_model does not currently exist, no deletion required.')


# todo: folders will always exist as a part of the repo now; need to adjust to code to account for this
def export_model(model_to_save):
    try:
        f = open(f'{model_path}/saved_model/saved_classifier.pickle', 'wb')
    except FileNotFoundError:
        os.mkdir(f'{model_path}/saved_model/')
        f = open(f'{model_path}/saved_model/saved_classifier.pickle', 'wb')
    pickle.dump(model_to_save, f)
    f.close()


def trainer():
    download_twitter_datasets()

    delete_model()

    train_data, test_data = process_data()

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    export_model(classifier)


if __name__ == "__main__":
    trainer()
    # delete_model()
