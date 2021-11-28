import logging

import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

from config.tensorflow_config import *

"""Code from https://www.tensorflow.org/tutorials/keras/text_classification """

logger = logging.getLogger("tensorflow-dataset-processor-logger")


def get_datasets():
    raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
        f'{dataset_path}/aclImdb/train',
        batch_size=batch_size,
        validation_split=0.2,
        subset='training',
        seed=seed)

    for text_batch, label_batch in raw_train_ds.take(1):
        for i in range(3):
            logger.debug("Review", text_batch.numpy()[i])
            logger.debug("Label", label_batch.numpy()[i])

    logger.debug("Label 0 corresponds to", raw_train_ds.class_names[0])
    logger.debug("Label 1 corresponds to", raw_train_ds.class_names[1])

    raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
        f'{dataset_path}/aclImdb/train',
        batch_size=batch_size,
        validation_split=0.2,
        subset='validation',
        seed=seed)

    raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
        f'{dataset_path}/aclImdb/test',
        batch_size=batch_size)

    # Make a text-only dataset (without labels), then call adapt
    train_text = raw_train_ds.map(lambda x, y: x)
    vectorize_layer.adapt(train_text)

    # retrieve a batch (of 32 reviews and labels) from the dataset
    text_batch, label_batch = next(iter(raw_train_ds))
    first_review, first_label = text_batch[0], label_batch[0]
    logger.debug("Review", first_review)
    logger.debug("Label", raw_train_ds.class_names[first_label])
    logger.debug("Vectorized review", vectorize_text(first_review, first_label))

    logger.debug("1287 ---> ", vectorize_layer.get_vocabulary()[1287])
    logger.debug(" 313 ---> ", vectorize_layer.get_vocabulary()[313])
    logger.debug('Vocabulary size: {}'.format(len(vectorize_layer.get_vocabulary())))

    train_ds = raw_train_ds.map(vectorize_text)
    val_ds = raw_val_ds.map(vectorize_text)
    test_ds = raw_test_ds.map(vectorize_text)

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, test_ds, raw_test_ds


# When loading a saved model was getting 'RuntimeError: Unable to restore a layer of class TextVectorization.' error,
# had to change the vectorize_layer config below; thanks to
# https://stackoverflow.com/questions/65050132/unable-to-restore-a-layer-of-class-textvectorization-text-classification
vectorize_layer = TextVectorization(
    standardize="lower_and_strip_punctuation",
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)


def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label


if __name__ == "__main__":
    get_datasets()
