import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import ttk

from PIL import Image

from config.gui_config import *
from config.bot_config import *
from functions.emotion_controller import EmotionEngineInterface
from functions.voice_controller import VoiceControllerAccess

"""thanks to code from: https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter"""

logger = logging.getLogger("gui-logger")


def load_image(im):
    frame_count = 0
    try:
        while 1:
            im.seek(im.tell() + 1)
            frame_count += 1
    except EOFError:
        pass

    return [PhotoImage(file=im.filename, format='gif -index %i' % i) for i in range(frame_count)], frame_count


# todo: make this into a superclass so someone can design their own GUI/Interface around the basic mechanics required
class GUIController:
    def __init__(self, core_access):

        self.root = Tk()

        self.root.title(ai_name)

        self.root.configure(bg=window_background_colour)

        self.root.wm_state(window_setting)

        self.core_access = core_access

        self.person_reply = tk.StringVar()

        self.face = "passive"
        self.first_boot = True

        self.ind = 0
        self.prev_ind = 0

        self.frame_style = ttk.Style()
        self.frame_style.configure('TLabelframe', background=window_background_colour)

        self.screen_chat_frame = ttk.LabelFrame(self.root)
        self.screen_chat_frame.pack(side="bottom", fill="both", expand="yes")

        self.text_entry = ttk.Entry(self.screen_chat_frame, textvariable=self.person_reply)
        self.text_entry.pack(side="left")

        self.send_button = ttk.Button(self.screen_chat_frame, text="Send", command=self.chat_threader)
        self.send_button.pack(side="right")

        self.root.bind('<Return>', lambda event: self.chat_threader())

        self.path = Path(__file__).parent / "../images"

        self.frames = None
        self.frame_count = None

        self.activate_im = Image.open(f'{self.path}/activate.gif')
        self.angry_im = Image.open(f'{self.path}/angry.gif')
        self.passive_im = Image.open(f'{self.path}/passive.gif')
        self.talking_im = Image.open(f'{self.path}/talking.gif')
        self.happy_im = Image.open(f'{self.path}/happy.gif')

        self.images = {
            'activate': [load_image(self.activate_im)],
            'angry': [load_image(self.angry_im)],
            'passive': [load_image(self.passive_im)],
            'talking': [load_image(self.talking_im)],
            'happy': [load_image(self.happy_im)]}

        self.label = Label(self.root)

    def chat_threader(self):
        threading.Thread(target=self.send_chat, daemon=True).start()

    def send_chat(self):
        if not self.core_access.processing_reply:
            self.screen_chat_frame.config(text="")
            input_temp = self.person_reply.get()
            self.text_entry.delete(0, END)
            bot_response = self.core_access.bot_talk_io(input_temp)
            self.screen_chat_frame.config(text=bot_response)

    def activation(self):
        VoiceControllerAccess.play_online()

        self.core_access.bot_talk_io("hello")

        intro_words = self.core_access.bot_reply

        self.screen_chat_frame.config(text=intro_words)

    def update(self, ind):
        if self.face == "activate":
            if self.first_boot:
                threading.Thread(target=self.activation, daemon=True).start()
                self.first_boot = False

        if not self.face == "talking":
            if VoiceControllerAccess.talking:
                if not self.face == "activate":
                    ind = 0
                    self.gif_changer("talking")
            else:
                if ind == self.frame_count:
                    ind = 0
                    self.gif_changer(EmotionEngineInterface.get_emotion())
        else:
            if not VoiceControllerAccess.talking:
                ind = 0
                self.gif_changer(EmotionEngineInterface.get_emotion())

        try:
            frame = self.frames[ind]
        except IndexError:
            ind = 0
            frame = self.frames[ind]

        ind += 1

        self.label.configure(image=frame)
        self.root.after(100, self.update, ind)

    def begin(self):
        self.label.pack()

        self.gif_changer('activate')

        self.root.after(0, self.update, 0)

        self.root.mainloop()

    def gif_changer(self, gif_name):
        self.face = gif_name
        self.frames = self.images[gif_name][0][0]
        self.frame_count = self.images[gif_name][0][1]
