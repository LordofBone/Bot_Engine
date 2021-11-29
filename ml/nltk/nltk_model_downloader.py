from config.nltk_config import *


def download_vader():
    nltk.download('vader_lexicon', download_dir=f'{model_path_root}/vader')


# todo: append these paths into nltk path
def download_twitter_models():
    nltk.download('punkt', download_dir=model_path_punkt)
    nltk.download('averaged_perceptron_tagger', download_dir=model_path_avg_pt)


if __name__ == "__main__":
    nltk.download(download_dir=model_path_root)
