import argparse
import os
import sys

chatbot_dir = os.path.join(os.path.dirname(__file__), '../Chatbot_8')

sys.path.append(chatbot_dir)

import_success = False


from functions.chatbot_functions import BotInterface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run MK model operations on the Bot')

    parser.add_argument('-o', '--db-operation', action="store", dest="db_op", type=str, default='TRAIN',
                        choices=['TRAIN', 'ERASE'], help='MK model operation to perform')

    args = parser.parse_args()

    db_op = args.db_op

    if db_op == "TRAIN":
        BotInterface.mk_model_train()
    elif db_op == "ERASE":
        BotInterface.mk_model_delete()
