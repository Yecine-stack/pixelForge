import tkinter as tk
from tkinter import colorchooser


class ColorPicker:
    def __init__(self, parent, callback):
        self.callback = callback

        self.button = tk.Button(
            parent,
            text="Color",
            command=self.choose_color
        )

    def choose_color(self):
        color = colorchooser.askcolor()[1]

        if color:
            self.callback(color)

    def show(self):
        self.button.pack(side=tk.LEFT)