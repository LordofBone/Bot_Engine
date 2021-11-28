import os
from pathlib import Path

max_features = 10000
sequence_length = 250

epochs = 10
batch_size = 32
seed = 42

url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
dataset_path = Path(__file__).parent.parent / f"data/tensorflow/"
models_path = Path(__file__).parent.parent / f"models/tensorflow/"
train_path = os.path.join(dataset_path, 'aclImdb/train')
test_path = os.path.join(dataset_path, 'aclImdb/test')

embedding_dim = 16
