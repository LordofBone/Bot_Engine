import logging
from pathlib import Path

import espeakng
from playsound import playsound

from config.voice_config import *

logger = logging.getLogger("voice-controller-logger")


def talking_start_finish(method):
    """ Using just the tts in-build 'is_talking' method will of course only work for tts, for playing wav files this
    has been added in so that the system knows when words are being spoken """

    def talk_time(*args, **kw):
        while VoiceControllerAccess.talking:
            pass
        VoiceControllerAccess.talking = True
        logger.debug(f'Set talking variable to: {VoiceControllerAccess.talking}')
        method(*args, **kw)
        VoiceControllerAccess.talking = False
        logger.debug(f'Set talking variable to: {VoiceControllerAccess.talking}')

    return talk_time


class VoiceController:
    def __init__(self):
        self.engine = espeakng.Speaker()

        self.engine.pitch = default_voice_pitch
        self.engine.wpm = default_voice_wpm
        self.engine.wordgap = default_voice_gap

        self.audio_on = audio_on
        self.talking = False

        self.path = Path(__file__).parent / "../audio"

        self.online = f'{self.path}/online.wav'
        self.training = f'{self.path}/training.wav'

    def default_pitch(self):
        self.engine.pitch = default_voice_pitch
        self.engine.wpm = default_voice_wpm
        self.engine.wordgap = default_voice_gap

    def angry_pitch(self):
        self.engine.pitch = angry_voice_pitch
        self.engine.wpm = angry_voice_wpm
        self.engine.wordgap = angry_voice_gap

    def happy_pitch(self):
        self.engine.pitch = happy_voice_pitch
        self.engine.wpm = happy_voice_wpm
        self.engine.wordgap = happy_voice_gap

    @talking_start_finish
    def play_online(self):
        if self.audio_on:
            playsound(self.online)

    @talking_start_finish
    def play_training(self):
        if self.audio_on:
            playsound(self.training)

    @talking_start_finish
    def tts(self, words):
        if self.audio_on:
            self.engine.say(words)
            # needs this or it will just continue on out of the function and change the classes 'talking' variable to
            # 'False' too soon. For some reason not required when using 'playsound' for wavs.
            while self.engine.is_talking():
                pass


VoiceControllerAccess = VoiceController()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    VoiceControllerAccess.play_training()
