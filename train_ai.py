from utils.sentiment_training_suite import train_all
import os
import sys

chatbot_dir = os.path.join(os.path.dirname(__file__), 'Chatbot_8')

sys.path.append(chatbot_dir)

from functions.core_systems import CoreInterface

from utils.bot_db_control import BotInterface

if __name__ == "__main__":
    train_all()
    BotInterface.bot_training()

