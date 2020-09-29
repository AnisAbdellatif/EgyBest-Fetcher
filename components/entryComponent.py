import tkinter as tk

class Entry():
    def __init__(self, master, entry):
        column = entry[0]
        labelText = entry[1]
        entryText = entry[2]
        tk.Label(master, text=labelText).grid(row=0, column=column)
        tk.Entry(master, textvariable=entryText).grid(row=1, column=column, padx=10, ipady=5)