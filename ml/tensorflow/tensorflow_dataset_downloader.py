import logging
import shutil

import tensorflow as tf

from config.tensorflow_config import *

"""Code from https://www.tensorflow.org/tutorials/keras/text_classification """

logger = logging.getLogger("tensorflow-dataset-downloader-logger")


def download_aclimdb():
    tf.keras.utils.get_file(f"{dataset_path}/aclImdb_v1", url, untar=True, cache_dir=dataset_path, cache_subdir='')


def remove_folders():
    remove_dir = os.path.join(train_path, 'unsup')
    shutil.rmtree(remove_dir)


def view_one():
    os.listdir(train_path)

    sample_file = os.path.join(train_path, 'pos/1181_9.txt')
    with open(sample_file) as f:
        logger.debug(f.read())


def downloader():
    download_aclimdb()
    view_one()
    remove_folders()


if __name__ == "__main__":
    downloader()
