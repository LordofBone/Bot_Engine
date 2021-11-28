class TerminalController:
    def __init__(self, core_access):
        self.core_access = core_access

    def talk_loop(self):
        self.core_access.bot_hello = self.core_access.bot_talk_io("hello")
        print(self.core_access.bot_hello)
        while True:
            reply = input("You: ")
            print(self.core_access.bot_talk_io(reply))
