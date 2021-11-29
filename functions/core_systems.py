from config.bot_config import *
from config.machine_interface_config import *
from functions.admin_controls import admin_control
from functions.chatbot_functions import BotInterface
from functions.emotion_controller import EmotionEngineInterface
from functions.gui_controller import GUIController
from functions.terminal_controller import TerminalController
from functions.voice_controller import VoiceControllerAccess


class CoreSystem:

    def __init__(self):
        self.bot_reply = f'{ai_name} chatbot offline.'
        self.bot_emotion = None
        self.admin_mode = False
        self.processing_reply = False

    def bot_talk_io(self, words):
        self.processing_reply = True

        if words == "admin mode access":
            self.admin_mode = not self.admin_mode
            if self.admin_mode:
                return f"{ai_name} IN ADMIN MODE"
            else:
                return f"{ai_name} IN NORMAL MODE"

        if self.admin_mode:
            self.bot_reply = admin_control(words)
            if self.bot_reply == "admin_exit":
                self.admin_mode = False
            return self.bot_reply

        self.bot_reply = EmotionEngineInterface.process_response(words)

        BotInterface.short_term_memory_insert(self.bot_reply)

        self.processing_reply = False

        return self.bot_reply

    def boot(self):
        if interface_mode == "GUI":
            gui_control = GUIController(self)
            gui_control.begin()
        elif interface_mode == "TERM":
            VoiceControllerAccess.play_online()
            term_control = TerminalController(self)
            term_control.talk_loop()
        elif interface_mode == "ROBOT":
            VoiceControllerAccess.play_online()
            term_control = TerminalController(self)
            term_control.talk_loop()


CoreInterface = CoreSystem()
