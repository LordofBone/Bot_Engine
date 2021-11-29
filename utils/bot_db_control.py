import argparse

from utils.pathutils import bot_installer

import_success = False

while not import_success:
    try:
        from bot_8 import BotLoop
        from bot_8_trainer import bot_trainer
        from database.delete_db import delete_db
        from database.setup_db import fresh_db_setup
        from Chatbot_8.ml.markovify.markovify_trainer import mk_trainer
        from Chatbot_8.ml.markovify.markovify_delete_models import mk_model_delete

        import_success = True
    except ModuleNotFoundError:
        bot_installer()
        print("Chatbot was not installed, have installed with PIP and retrying...")

from functions.chatbot_functions import BotInterface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run DB operations on the Bot')

    parser.add_argument('-o', '--db-operation', action="store", dest="db_op", type=str, default='TRAIN',
                        choices=['TRAIN', 'ERASE', 'FRESHDB'], help='DB operation to perform')

    args = parser.parse_args()

    db_op = args.db_op

    if db_op == "TRAIN":
        BotInterface.bot_training()
    elif db_op == "ERASE":
        BotInterface.bot_erase_db()
    elif db_op == "FRESHDB":
        BotInterface.bot_fresh_db()
