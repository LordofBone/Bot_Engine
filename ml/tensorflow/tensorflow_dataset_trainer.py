import logging

from utils.pathutils import delete_with_override

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses

from config.tensorflow_config import *
from ml.tensorflow.tensorflow_dataset_downloader import downloader
from ml.tensorflow.tensorflow_dataset_processor import get_datasets, vectorize_layer
from ml.tensorflow.tensorflow_history_plots import plot_history
from ml.tensorflow.tensorflow_neural_net_generator import create_neural_net

"""Code from https://www.tensorflow.org/tutorials/keras/text_classification """

logger = logging.getLogger("tensorflow-dataset-trainer-logger")


def train_model(model, train_ds, val_ds):
    model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
                  optimizer='adam',
                  metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs)

    return history


def evaluate_model(model, test_ds):
    loss, accuracy = model.evaluate(test_ds)

    logger.debug("Loss: ", loss)
    logger.debug("Accuracy: ", accuracy)


def export_trained_model(model, raw_test_ds):
    export_model_out = tf.keras.Sequential([
        vectorize_layer,
        model,
        layers.Activation('sigmoid')
    ])

    export_model_out.compile(
        loss=losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
    )

    # Test it with `raw_test_ds`, which yields raw strings
    loss, accuracy = export_model_out.evaluate(raw_test_ds)
    logger.debug(accuracy)

    return export_model_out

# todo: folders will always exist as a part of the repo now; need to adjust to code to account for this
def delete_model():
    if os.path.exists(f'{models_path}/saved_model'):
        logger.debug(f'Model: {models_path}/saved_model exists, deleting.')
        delete_with_override(f'{models_path}/saved_model')
    else:
        logger.debug(f'Model: {models_path}/saved_model does not currently exist, no deletion required.')


def export_model(model_to_save):
    model_to_save.save(f'{models_path}/saved_model')


def trainer(show_plots=False):
    downloader()
    model = create_neural_net()
    train_ds, val_ds, test_ds, raw_test_ds = get_datasets()
    history = train_model(model, train_ds, val_ds)
    evaluate_model(model, test_ds)
    if show_plots:
        plot_history(history)
    model_final = export_trained_model(model, raw_test_ds)
    delete_model()
    export_model(model_final)


if __name__ == "__main__":
    trainer(show_plots=False)
