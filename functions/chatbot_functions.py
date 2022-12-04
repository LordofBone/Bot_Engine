import logging

import psycopg2

from config.bot_config import *

from Chatbot_8.run_container_stack import run_all
from Chatbot_8.bot_8 import BotLoop
from Chatbot_8.bot_8_trainer import bot_trainer
from Chatbot_8.database.delete_db import delete_db
from Chatbot_8.database.setup_db import fresh_db_setup
from Chatbot_8.ml.markovify.markovify_trainer import mk_trainer
from Chatbot_8.ml.markovify.markovify_delete_models import mk_model_delete

logger = logging.getLogger("nltk-chatbot-functions-logger")


def chatbot_online_check(method):
    """Will perform a check on whether the chatbot is online or not and set the bot_status to the appropriate
    setting. Will also allow attempts for handling disconnects and attempting reconnects. """

    def online_checker(*args, **kw):
        logger.debug(f'Chatbot status is {BotInterface.bot_status}.')
        if BotInterface.bot_status == "ONLINE":
            try:
                logger.debug(f'Attempting to access the bot with an input.')
                return method(*args, **kw)
            except TypeError:
                logger.debug(f'Chatbot non-responsive attempting a re-connect.')
                BotInterface.connect_to_bot()
                if BotInterface.bot_status == "OFFLINE":
                    logger.debug(f'Failed to re-connect to chatbot - setting bot status to {BotInterface.bot_status}.')
                    return BotInterface.default, None
                else:
                    logger.debug(f'Successfully re-connected to the chatbot.')
                    logger.debug(f'Attempting to access the bot with an input.')
                    return method(*args, **kw)
        elif BotInterface.bot_status == "OFFLINE":
            logger.debug(f'Chatbot marked as {BotInterface.bot_status} attempting a re-connect.')
            BotInterface.connect_to_bot()
            if BotInterface.bot_status == "OFFLINE":
                logger.debug(f'Failed to re-connect to chatbot - keeping bot status as {BotInterface.bot_status}.')
                return BotInterface.default, None
            else:
                logger.debug(f'Successfully re-connected to the chatbot.')
                logger.debug(f'Attempting to access the bot with an input.')
                return method(*args, **kw)

    return online_checker


class BotController:
    def __init__(self):
        self.ai_chat = None
        self.default = f'{ai_name} chatbot offline.'
        self.reply = self.default
        self.words = ""
        self.bot_status = "OFFLINE"
        self.fresh_db = True
        self.reply_list = []
        self.attempted_container_launch = False

        self.connect_to_bot()

    @chatbot_online_check
    def bot_talk(self, words):
        self.words = words

        logger.debug(f'Sending {self.words} to chatbot conversation.')
        self.reply, self.reply_list = self.ai_chat.conversation(self.words)

        return self.reply, self.reply_list

    # handling short term memory inserts on a higher level, to account for emotional responses
    @chatbot_online_check
    def short_term_memory_insert(self, words):
        self.ai_chat.short_term_memory_insert(words)

    @chatbot_online_check
    def generate_sentence(self):
        generated_sentence = self.ai_chat.sentence_gen()

        return generated_sentence

    def bot_training(self):
        bot_trainer(fresh_db=self.fresh_db)

    def bot_erase_db(self):
        delete_db()
        self.fresh_db = True

    def bot_fresh_db(self):
        fresh_db_setup()
        self.fresh_db = False

    def mk_model_delete(self):
        mk_model_delete()
        self.fresh_db = True

    def mk_model_train(self):
        mk_trainer()
        self.fresh_db = False

    def launch_portainer_container(self):
        run_all()
        self.attempted_container_launch = True

    def connect_to_bot(self):
        # Initialise chatbot with short term memory off, running inserts from a higher level to account for extra
        # reply choice processing
        if not self.ai_chat:
            try:
                logger.debug(
                    f'Previously instantiated class does not exist and chatbot status is: {self.bot_status}, '
                    f'attempting to get a reply.')
                self.ai_chat = BotLoop(enable_short_term_memory=False, include_possible_replies=True)
                logger.debug(f'Successfully connected to chatbot, setting chatbot status to ONLINE')
                self.bot_status = "ONLINE"
            except psycopg2.OperationalError as err:
                err = str(err)
                if "Connection refused" in err:
                    logger.debug(f'Error from chatbot: {err}, setting chatbot status to OFFLINE.')
                    self.bot_status = "OFFLINE"
                elif "does not exist" in err:
                    logger.debug(f'Error from chatbot: {err}, setting chatbot status to OFFLINE.')
                    self.bot_training()
                    self.ai_chat = BotLoop(enable_short_term_memory=False, include_possible_replies=True)
                    self.bot_status = "ONLINE"
        else:
            try:
                logger.debug(f'Previously instantiated class exists and chatbot status is: {self.bot_status}, '
                             f'attempting to get a reply.')
                self.ai_chat.establish_connection()
                self.reply, self.reply_list = self.ai_chat.conversation(self.words)
                logger.debug(f'Successfully connected to chatbot, setting chatbot status to ONLINE')
                self.bot_status = "ONLINE"
            except psycopg2.OperationalError as err:
                err = str(err)
                if "Connection refused" in err:
                    logger.debug(f'Error from chatbot: {err}, setting chatbot status to OFFLINE.')
                    self.bot_status = "OFFLINE"
                elif "does not exist" in err:
                    logger.debug(f'Error from chatbot: {err}, setting chatbot status to OFFLINE.')
                    self.bot_training()
                    self.reply, self.reply_list = self.ai_chat.conversation(self.words)
                    self.bot_status = "ONLINE"
            except TypeError as err:
                logger.debug(f'Chatbot interface class non-responsive: {err}, setting chatbot status to OFFLINE.')
                self.bot_status = "OFFLINE"


BotInterface = BotController()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    while True:
        words_in = input("You: ")
        print(f'Bot: {BotInterface.bot_talk(words_in)[0]}')
