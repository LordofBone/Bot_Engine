from utils.sentiment_training_suite import train_all
from utils.bot_db_control import BotInterface

if __name__ == "__main__":
    train_all()
    BotInterface.bot_training()

