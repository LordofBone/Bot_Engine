from pathlib import Path

import nltk

model_path = Path(__file__).parent.parent / "models/nltk"
dataset_path = Path(__file__).parent.parent / "data/nltk"

nltk.data.path.append(dataset_path)
nltk.data.path.append(model_path)

vader_location = f"/models/nltk/sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt"
