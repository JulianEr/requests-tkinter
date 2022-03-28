import tkinter as tk
import tkinter.scrolledtext as tks
from tkinter import ttk

class TextWidget(tk.Toplevel):

    def __init__(self, master, text):
        super().__init__(master)

        self.geometry('600x400')
        self.title('Request')

        self.create_content(text)

    def create_content(self, text):
        scrolled_text = tks.ScrolledText(self, width=550, height=400, wrap='word')
        scrolled_text.insert(1.0, text)
        scrolled_text.pack(side=tk.LEFT)