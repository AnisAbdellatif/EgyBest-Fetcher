import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import pyperclip

class DialogBox():
    def __init__(self, master, title, msg, copiable=None, otherBtns=[]):
        msg = tk.StringVar(value=msg)
        box = tk.Toplevel(master)
        box.title(title)

        text = ScrolledText(box, height=13, width=60)
        text.pack()
        text.insert(tk.END, msg.get())
        text.config(state=tk.DISABLED)

        FrameButtons = tk.Frame(box, pady=20)
        FrameButtons.pack()
        column=0
        for button in otherBtns:
            tk.Button(FrameButtons, text=button["title"], command=button["command"]).grid(
                row=0, column=column, padx=3)
            column+=1

        if not (copiable is None):
            tk.Button(FrameButtons, text="Copy",
                      command=lambda: pyperclip.copy(copiable)).grid(row=0, column=column, padx=3)
            column += 1
        
        tk.Button(FrameButtons, text="Dismiss",
                  command=box.destroy).grid(row=0, column=column+1, padx=3)
