from tkinter import *
from tkinter import messagebox

class CB:
    """helps managing checkbuttons without using too many code lines"""
    def __init__(self, frame, text, row, column):
        """constructor"""
        self.var = BooleanVar()
        self.button = Checkbutton(frame, text=text, variable=self.var, state="disabled")
        self.button.grid(row=row, column=column, sticky=W)

    def config(self, prop, new):
        """helps configure"""
        if prop == "state":
            self.button.config(state=new)

    def title(self):
        """returns the text of the button"""
        return self.button["text"]
