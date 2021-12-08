import logging

from config.emotion_config import *
from functions.chatbot_functions import BotInterface
from functions.voice_controller import VoiceControllerAccess

if emotion_engine == "nltk-vader":
    from ml.nltk.nltk_vader_classifier import TextClassifierInterface
if emotion_engine == "nltk-twitter":
    from ml.nltk.nltk_twitter_classifier import TextClassifierInterface
elif emotion_engine == "tensorflow":
    from ml.tensorflow.tensorflow_classifier import TextClassifierInterface
else:
    raise Exception(f'Unknown emotion engine: {emotion_engine}. Options are: {engines}')

from collections import deque

logger = logging.getLogger("emotion-engine-logger")


class EmotionEngine:

    def __init__(self):
        self.process_emotions = process_emotions
        self.current_emotion = "passive"

        self.avg_compound_emotion = initial_emotion_average
        self.compound_emotion_recent = deque(maxlen=max_emotion_short_memory)

        logger.debug(f'Loading emotion engine: {emotion_engine}')

    def process_response(self, words):
        reply, replies = BotInterface.bot_talk(words)

        if self.process_emotions:
            score = TextClassifierInterface.classify_words(words)

            self.log_emotion(score)

            logger.debug(f'Classifier model: "{emotion_engine}" response score: "{score}" for sentence: "{words}"')

            if replies:
                emotional_reply = self.replies_to_emotion(replies)
                if emotional_reply:
                    reply = emotional_reply
        # todo: move this to the chatbot_functions module?
        VoiceControllerAccess.tts(reply)

        return reply

    def get_emotion(self):
        if self.avg_compound_emotion < negative_emotion_threshold:
            self.current_emotion = "angry"
            VoiceControllerAccess.angry_pitch()
        elif negative_emotion_threshold < self.avg_compound_emotion < positive_emotion_threshold:
            self.current_emotion = "passive"
            VoiceControllerAccess.default_pitch()
        elif self.avg_compound_emotion > positive_emotion_threshold:
            self.current_emotion = "happy"
            VoiceControllerAccess.happy_pitch()

        return self.current_emotion

    def average(self):
        return sum(list(self.compound_emotion_recent)) / len(list(self.compound_emotion_recent))

    def log_emotion(self, score_to_log):
        logger.debug(f'Compound score: {score_to_log}')
        self.compound_emotion_recent.append(score_to_log)

        logger.debug(f'Recent emotion scores: {self.compound_emotion_recent} max: {max_emotion_short_memory}')

        self.avg_compound_emotion = self.average()
        logger.debug(f'Average emotion score: {self.avg_compound_emotion}')

    def replies_to_emotion(self, in_replies):
        emotional_reply_dict = {}
        logger.debug(f'Replies to analyse: {in_replies}')

        for reply in in_replies:
            score = TextClassifierInterface.classify_words(reply)

            update = {reply: score}
            emotional_reply_dict.update(update)

        logger.debug(f'Dict of possible responses: {emotional_reply_dict}')

        if emotional_reply_dict:
            logger.debug(
                f'Emotional replies exist, getting best match for average compound: {self.avg_compound_emotion}')
            best, best_val = min(emotional_reply_dict.items(), key=lambda x: abs(self.avg_compound_emotion - x[1]))
            logger.debug(f'Closes value: {best_val} found for reply: {best}')
        else:
            best = None

        logger.debug(f'Best response from dict: {best}')

        return best


EmotionEngineInterface = EmotionEngine()
