from pathlib import Path

import nltk

model_path_root = Path(__file__).parent.parent / "models/nltk"
model_path_avg_pt = Path(__file__).parent.parent / "models/nltk/averaged_perceptron_tagger"
model_path_punkt = Path(__file__).parent.parent / "models/nltk/punkt"
model_path_saved = Path(__file__).parent.parent / "models/nltk/saved_model"

dataset_path_root = Path(__file__).parent.parent / "data/nltk"
dataset_path_stopwords = Path(__file__).parent.parent / "data/nltk/stopwords"
dataset_path_twitter_samples = Path(__file__).parent.parent / "data/nltk/twitter_samples"
dataset_path_wordnet = Path(__file__).parent.parent / "data/nltk/wordnet"

models_paths = [model_path_root, model_path_avg_pt, model_path_punkt, model_path_saved]
dataset_paths = [dataset_path_root, dataset_path_stopwords, dataset_path_twitter_samples, dataset_path_wordnet]

for path in models_paths:
    nltk.data.path.append(path)

for path in dataset_paths:
    nltk.data.path.append(path)

vader_location = f"/models/nltk/sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt"
