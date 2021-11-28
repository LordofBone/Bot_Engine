from ml.nltk.nltk_model_downloader import download_vader
from ml.nltk.nltk_twitter_trainer import trainer as nltk_trainer
from ml.tensorflow.tensorflow_dataset_trainer import trainer as tf_trainer

"""Downloads datasets/NLTK VADER model and trains the NLTK/Tensorflow text sentiment analysis models """

if __name__ == "__main__":
    download_vader()
    nltk_trainer()
    tf_trainer()
