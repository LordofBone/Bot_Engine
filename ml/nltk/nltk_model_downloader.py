from config.nltk_config import *


def download_vader():
    nltk.download('vader_lexicon', download_dir=f'{model_path}/vader')


def download_twitter_models():
    nltk.download('punkt', download_dir=f'{model_path}/punkt')
    nltk.download('averaged_perceptron_tagger', download_dir=f'{model_path}/averaged_perceptron_tagger')


if __name__ == "__main__":
    nltk.download(download_dir=model_path)
