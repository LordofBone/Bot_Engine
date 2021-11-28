from config.nltk_config import *


def download_twitter_datasets():
    nltk.download('twitter_samples', download_dir=dataset_path)
    nltk.download('wordnet', download_dir=dataset_path)
    nltk.download('stopwords', download_dir=dataset_path)


if __name__ == "__main__":
    nltk.download(download_dir=dataset_path)
