import tkinter as tk


class BrushSelector:
    def __init__(self, parent, callback):
        self.callback = callback

        self.entry = tk.Entry(parent)
        self.entry.insert(0, "5")

        self.button = tk.Button(
            parent,
            text="Brush Size",
            command=self.update_size
        )

    def update_size(self):
        size = int(self.entry.get())
        self.callback(size)

    def show(self):
        self.entry.pack(side=tk.LEFT)
        self.button.pack(side=tk.LEFT)