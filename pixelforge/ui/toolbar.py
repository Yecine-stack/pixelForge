import tkinter as tk


class Toolbar:
    def __init__(self, parent, callbacks):
        self.frame = tk.Frame(parent)

        buttons = [
            ("Brush", callbacks["brush"]),
            ("Eraser", callbacks["eraser"]),
            ("Grayscale", callbacks["grayscale"]),
            ("Rotate", callbacks["rotate"]),
            ("Flip H", callbacks["flip_horizontal"]),
            ("Flip V", callbacks["flip_vertical"]),
            ("Resize", callbacks["resize"]),
            ("Undo", callbacks["undo"]),
            ("Redo", callbacks["redo"]),
        ]

        for text, command in buttons:
            button = tk.Button(
                self.frame,
                text=text,
                command=command
            )
            button.pack(side=tk.LEFT)

    def show(self):
        self.frame.pack()