
class IntegrationController:
    def __init__(self, core_access):
        self.core_access = core_access

    def input_get_response(self, text_in):
        self.core_access.bot_hello = self.core_access.bot_talk_io(text_in)
        response = {"text": self.core_access.bot_hello, "emotion": EmotionEngineInterface.get_emotion()}
        return response
