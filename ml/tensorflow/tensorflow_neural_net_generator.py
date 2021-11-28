import logging

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses

from config.tensorflow_config import *

"""Code from https://www.tensorflow.org/tutorials/keras/text_classification """

logger = logging.getLogger("tensorflow-nnet-gen-logger")


def create_neural_net():
    model = tf.keras.Sequential([
        layers.Embedding(max_features + 1, embedding_dim),
        layers.Dropout(0.2),
        layers.GlobalAveragePooling1D(),
        layers.Dropout(0.2),
        layers.Dense(1)])

    model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
                  optimizer='adam',
                  metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

    logger.debug(model.summary())

    return model
