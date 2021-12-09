import logging
import threading
from time import sleep

from functions.chatbot_functions import BotInterface

logger = logging.getLogger("thought-generator-logger")


# todo: finish and implement this --currently unused--
class ThoughtGenerator(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.latest_thought = ""

    def run(self):
        while True:
            self.latest_thought = BotInterface.generate_sentence()
            logger.debug(f'Thought generated: {self.latest_thought}')
            sleep(5)


ThoughtGeneratorInterface = ThoughtGenerator()
ThoughtGeneratorInterface.start()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    ThoughtGeneratorInterface.join()
